! This file is part of QLKNN-fortran
! You should have received the QLKNN-fortran LICENSE in the root of the project
program qlknn_fullflux
#include "core/preprocessor.inc"
  use qlknn_evaluate_nets
  use qlknn_disk_io
  use cla
  use kinds
#ifdef MPI
  use mpi
#endif
  implicit none
  integer(lli) :: n_trails, trial, verbosity, n_rho, n_in, n_out
  type (qlknn_options) :: opts
  type (qlknn_normpars) :: qlknn_norms
  real(qlknn_dp), dimension(:,:), allocatable :: input
  real(qlknn_dp) :: start, finish
  real(qlknn_dp), dimension(:,:), allocatable :: qlknn_out
  real(qlknn_dp), dimension(:,:,:), allocatable :: dqlknn_out_dinput
  character(len=4096) :: nn_path = '', input_path = '', output_path = ''
  character(len=14) :: cmd_name = 'qlknn_fullflux'
  character(len=STRLEN) :: key, arg
  logical :: calculate_jacobian, dump_to_disk

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


  call cla_register('-n', '--nn-path', 'Path to NN namelist folder', cla_char, 'data/qlknn-fullflux-namelists')
  call cla_register('-i', '--input', 'Path to input namelist file', cla_char, 'tests/test.nml')
  call cla_register('-o', '--output', 'Path to output namelist file', cla_char, 'tests/output.nml')
  call cla_register('-d', '--dump-to-disk', 'Dump output to disk', cla_flag, 'f')
  call cla_register('-j', '--jacobian', 'Calculate Jacobian', cla_flag, 'f')
  call cla_register('-t', '--trails', 'Run the network calculation the specified amount of times', cla_int, '1')
  call cla_register('-v', '--verbosity', 'Set verbosity', cla_int, '1')
  call cla_register('-a', '--force-evaluate-all', 'Force to calculate all networks irrespective of settings', cla_flag, 'f')

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

  call default_qlknn_fullflux_options(opts)

  opts%force_evaluate_all = cla_key_present('--force-evaluate-all')

  ! Read input namelist
  open(10,file=input_path,action='READ')
  read(10,nml=sizes)
  allocate(input(n_in, n_rho))
  read(10,nml=test)
  close(10)

  n_out = 3
  allocate(qlknn_out(n_rho, n_out))
  allocate(dqlknn_out_dinput(n_out, n_rho, 3))

  ! Variables for Victor rule
  ALLOCATE(qlknn_norms%A1(n_rho))
  qlknn_norms%A1 = 2.
  qlknn_norms%R0 = 3.
  qlknn_norms%a = 1.


  call load_fullflux_nets_from_disk(nn_path, verbosity)

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
      call evaluate_fullflux_net(input, nets, qlknn_out, verbosity, opts)
    else
      call evaluate_fullflux_net(input, nets, qlknn_out, verbosity, opts, dqlknn_out_dinput)
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
  call all_networktype_deallocate(nets)

end program qlknn_fullflux
