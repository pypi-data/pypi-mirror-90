! This file is part of QLKNN-fortran
! You should have received the QLKNN-fortran LICENSE in the root of the project
program qlknn_hornnet
  !! Calculate fluxes as predicted by QLKNN-HornNet in standalone.
  !! Uses the [[evaluate_hornnet_constants]] and [[hornnet_flux_from_constants]]
  !! functions to predict \( q_{e, ETG}, q_{e, ITG}, q_{e, TEM}, q_{i, ITG}, q_{i, TEM}, \Gamma_{e, ITG}, \Gamma_{e, TEM} \)
  !! or a combination thereof, depending on the given flags. Run with `--help` flag
  !! for more information
  !!
  !! By default:
  !!
  !! - Do not evaluate Jacobians
  !! - Run with `verbosity=1`
  !! - Do not apply victor rule
  !! - Evaluate all fluxes and needed networks
  !! - Clip input and output
  !! - Do not merge modes together
  !!
  !! For more information see [[qlknn_options]] and [[default_qlknn_hornnet_options]]
#include "core/preprocessor.inc"
  use qlknn_evaluate_nets
  use qlknn_disk_io
  use cla
  use kinds
#ifdef MPI
  use mpi
#endif
  implicit none
  integer(lli) :: n_trails, trial, verbosity, n_rho, n_in, n_out, n_outputs, n_primitive_out, n_total_inputs
  type (qlknn_options) :: opts
  type (qlknn_normpars) :: qlknn_norms
  real(qlknn_dp), dimension(:,:), allocatable :: input
  real(qlknn_dp) :: start, finish
  real(qlknn_dp), dimension(:,:), allocatable :: qlknn_out
  real(qlknn_dp), dimension(:,:), allocatable :: hornnet_constants
  real(qlknn_dp), dimension(:,:,:), allocatable :: dqlknn_out_dinput
  real(qlknn_dp), dimension(:,:,:), allocatable :: dhornnet_constants_dinput
  real(qlknn_dp), dimension(:,:,:), allocatable :: dflux_dhornnet_constants, dflux_dinput

  character(len=4096) :: nn_path = '', input_path = '', output_path = ''
  character(len=13) :: cmd_name = 'qlknn_hornnet'
  character(len=STRLEN) :: key, arg
  logical :: calculate_jacobian, dump_to_disk, no_clip

#if defined(LLI) && defined(__INTEL_COMPILER)
    integer(lli) my_world_rank
#else
    integer(li) my_world_rank
#endif
#ifdef MPI
#if defined(LLI) && defined(__INTEL_COMPILER)
    integer(lli) mpi_ierr, world_size
#else
    integer(li) mpi_ierr, world_size
#endif
#endif

  namelist /sizes/ n_rho, n_in
  namelist /test/ input
  namelist /outp_sizes/ n_rho, n_in, n_out
  namelist /outp/ qlknn_out
  namelist /outp_jacobian/ dqlknn_out_dinput

  ! Command line argument parsing
  call cla_init


  call cla_register('-n', '--nn-path', 'Path to NN namelist folder', cla_char, 'data/qlknn-hornnet-namelists')
  call cla_register('-i', '--input', 'Path to input namelist file', cla_char, 'tests/test.nml')
  call cla_register('-o', '--output', 'Path to output namelist file', cla_char, 'tests/output.nml')
  call cla_register('-d', '--dump-to-disk', 'Dump output to disk', cla_flag, 'f')
  call cla_register('-j', '--jacobian', 'Calculate Jacobian', cla_flag, 'f')
  call cla_register('-m', '--merge-modes', 'Merge modes (ITG/TEM/ETG) together', cla_flag, 'f')
  call cla_register('-t', '--trails', 'Run the network calculation the specified amount of times', cla_int, '1')
  call cla_register('-v', '--verbosity', 'Set verbosity', cla_int, '1')
  call cla_register('-a', '--force-evaluate-all', 'Force to calculate all networks irrespective of settings', cla_flag, 'f')
  call cla_register('-p', '--no-clip', 'Do not clip inputs nor outputs', cla_flag, 'f')

  ! Look for help-like arguments
  call cla_get_command_argument(1, arg)
  key = trim(arg)
  if (cla_str_eq(trim(key),'-h')      .or. &
      cla_str_eq(trim(key),'-?')      .or. &
      cla_str_eq(trim(key),'/?')      .or. &
      cla_str_eq(trim(key),'-H')      .or. &
      cla_str_eq(trim(key),'help')    .or. &
      cla_str_eq(trim(key),'-help')   .or. &
      cla_str_eq(trim(key),'--help')  .or. &
      cla_str_eq(trim(key),'--usage')      &
      ) then
     call cla_help(cmd_name)
     stop
  endif

  !call cla_validate(cmd_name)

  call cla_get('--nn-path', nn_path)
  call cla_get('--input', input_path)
  call cla_get('--output', output_path)
  calculate_jacobian = cla_key_present('--jacobian')
  dump_to_disk = cla_key_present('--dump-to-disk')
  call cla_get('--trails', n_trails)
  call cla_get('--verbosity', verbosity)
  no_clip = cla_key_present('--no-clip')

  call default_qlknn_hornnet_options(opts)

  opts%force_evaluate_all = cla_key_present('--force-evaluate-all')
  opts%merge_modes = cla_key_present('--merge-modes')
  if (no_clip) then
    opts%constrain_inputs = .false.
    opts%constrain_outputs = .false.
  endif

  ! Read input namelist
  open(10,file=input_path,action='READ')
  read(10,nml=sizes)
  allocate(input(n_in, n_rho))
  read(10,nml=test)
  close(10)

  n_outputs = 4
  n_primitive_out = 7
  n_total_inputs = int(size(input, 1), li)

  if (opts%merge_modes) then
    n_out = 4
  else
    n_out = 7
  end if
  allocate(qlknn_out(n_rho, n_out))
  allocate(dqlknn_out_dinput(n_out, n_rho, n_in))

  allocate(hornnet_constants(n_rho, 15))
  allocate(dhornnet_constants_dinput(15, n_rho, n_in))
  allocate(dflux_dhornnet_constants(n_out, n_rho, 15))
  allocate(dflux_dinput(n_out, n_rho, n_in))

  ! Variables for Victor rule
  allocate(qlknn_norms%a1(n_rho))
  qlknn_norms%A1 = 2.
  qlknn_norms%R0 = 3.
  qlknn_norms%a = 1.


  call load_hornnet_nets_from_disk(nn_path, verbosity)

#ifdef MPI
    call MPI_INIT(mpi_ierr)
    call MPI_COMM_SIZE(MPI_COMM_WORLD, world_size, mpi_ierr)
    call MPI_COMM_RANK(MPI_COMM_WORLD, my_world_rank, mpi_ierr)
    if (verbosity >= 1) then
      if (my_world_rank == 0) then
        print *, 'World size is         ', world_size
      end if
      print *, 'Hello world from rank ', my_world_rank
    endif
#else
    my_world_rank = 0
#endif

  call cpu_time(start)
  do trial = 1,n_trails
    if (.not. calculate_jacobian) then
      call evaluate_hornnet_constants(input, blocks, hornnet_constants, verbosity, opts, qlknn_norms)
      call hornnet_flux_from_constants(input, blocks, hornnet_constants, qlknn_out, verbosity, opts, qlknn_norms)
    else
      call evaluate_hornnet_constants(input, blocks, hornnet_constants, verbosity, opts, qlknn_norms, dhornnet_constants_dinput)
      call hornnet_flux_from_constants(input, blocks, hornnet_constants, qlknn_out, verbosity, opts, qlknn_norms, dflux_dhornnet_constants, dflux_dinput)

      call hornnet_multiply_jacobians(dhornnet_constants_dinput, dflux_dhornnet_constants, dflux_dinput, dqlknn_out_dinput, verbosity)
    endif
  end do
  call cpu_time(finish)
  if (my_world_rank == 0) then
    print '("Trials = ",i9)',n_trails
    print '("Time   = ",f9.3," milliseconds.")',1e3*(finish-start)/n_trails
  endif

  if (dump_to_disk) then
    open(10,file=output_path,action='WRITE')
    write(10,nml=outp_sizes)
    write(10,nml=outp)
    if (calculate_jacobian) then
      write(10,nml=outp_jacobian)
    endif
    close(10)
  endif

#ifdef MPI
  call MPI_FINALIZE(mpi_ierr)
#endif

end program qlknn_hornnet
