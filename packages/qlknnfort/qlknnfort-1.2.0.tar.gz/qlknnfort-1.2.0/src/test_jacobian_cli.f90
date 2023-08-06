! This file is part of QLKNN-fortran
! You should have received the QLKNN-fortran LICENSE in the root of the project
program qlknn_hyper
#include "core/preprocessor.inc"
  use cla
  use kinds
  use qlknn_types
  use qlknn_disk_io
  use test_jacobian

  use ieee_arithmetic
  implicit none
  integer(lli) :: verbosity, n_rho, n_in, n_out
  real(qlknn_dp), dimension(:,:), allocatable :: input
  real(qlknn_dp), dimension(:,:,:), allocatable :: dqlknn_out_dinput
  character(len=4096) :: nn_path = '', input_path = '', output_path = ''
  character(len=23) :: cmd_name = 'qlknn_jacobian_test_cli'
  character(len=STRLEN) :: key, arg
  logical :: dump_to_disk

  logical, dimension(:,:,:), allocatable :: err_okay
  real(qlknn_dp) :: max_err

  real(qlknn_dp) :: stepsize
  real(qlknn_dp), dimension(:,:,:), allocatable :: err_out
  integer(lli) :: net
  character(len=4096) :: nettype = ''
  integer :: casenum

  namelist /sizes/ n_rho, n_in
  namelist /test/ input
  namelist /outp_sizes/ n_rho, n_in, n_out
  namelist /outp/ err_out
  namelist /outp_jacobian/ dqlknn_out_dinput

  ! Command line argument parsing
  call cla_init


  call cla_register('-n', '--nn-path', 'Path to NN namelist folder', cla_char, '')
  call cla_register('-i', '--input', 'Path to input namelist file', cla_char, 'tests/test.nml')
  call cla_register('-o', '--output', 'Path to output namelist file', cla_char, 'tests/output.nml')
  call cla_register('-t', '--nettype', 'Type of the NN to run', cla_char, 'hyper')
  call cla_register('-c', '--casenum', 'Number of the testcase to run', cla_int, '1')
  call cla_register('-s', '--stepsize', 'Size of the step to be taken for Jacobian test', cla_float, 'NaN')
  call cla_register('-e', '--maxerr', 'Maximum error that constitutes a failed test"', cla_float, 'NaN')
  call cla_register('-d', '--dump-to-disk', 'Dump output to disk', cla_flag, 'f')
  call cla_register('-v', '--verbosity', 'Set verbosity', cla_int, '1')

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
  call cla_get('--nettype', nettype)
  call cla_get('--casenum', casenum)
  call cla_get('--stepsize', stepsize)
  call cla_get('--maxerr', max_err)
  call cla_get('--verbosity', verbosity)

  ! Read input namelist
  if (verbosity >= 1) then
    write(*,*) "Reading input path ", trim(input_path)
  endif
  open(10,file=input_path,action='READ')
  read(10,nml=sizes)
  allocate(input(n_in, n_rho))
  read(10,nml=test)
  close(10)
  if (verbosity >= 1) then
    write(*,"(A,I3,A,I3,A)") "Input is (n_in, rho)=(",n_in, ",", n_rho, ")"
  endif
  dump_to_disk = .true.

  if (trim(nettype) == "hyper") then
    if (nn_path == '') then
      nn_path = 'data/qlknn-hyper-namelists'
    endif
    if (.not. allocated(nets%nets)) then
      call load_qlknn_hyper_nets_from_disk(nn_path, verbosity - 1)
    endif
  elseif (trim(nettype) == "hornnet") then
    if (nn_path == '') then
      nn_path = 'data/qlknn-hornnet-namelists'
    endif
    if (.not. allocated(blocks%input_blocks)) then
      call load_hornnet_nets_from_disk(nn_path, verbosity - 1)
    endif
  else
    ERRORSTOP(.true., "Given --nettype not defined yet")
  endif

  if (ieee_is_nan(stepsize)) then
    ! The user didn't give it on the command line, grab defaults
    if (trim(nettype) == "hyper") then
      stepsize = stepsize_hyper
    elseif (trim(nettype) == "hornnet") then
      stepsize = stepsize_hornnet
    endif
  endif
  if (verbosity >= 0) then
    write(*,"(A,A,A,I2,A,E9.2)") "Running nettype '", trim(nettype), "', casenum=", casenum, " and stepsize h=", stepsize
  endif

  net = 4
  if (trim(nettype) == "hyper") then
    call jacobian_hyper_multi(casenum, input, stepsize, net, err_out, verbosity - 1)
  elseif (trim(nettype) == "hornnet") then
    call jacobian_hornnet_multi(casenum, input, stepsize, err_out, verbosity - 1)
  endif

  n_out = size(err_out, 1)
  n_rho = size(err_out, 2)
  n_in = size(err_out, 3)

  if (ieee_is_nan(max_err)) then
    ! The user didn't give it on the command line, grab defaults
    if (trim(nettype) == "hyper") then
      max_err = max_err_hyper(casenum)
    elseif (trim(nettype) == "hornnet") then
      max_err = max_err_hornnet(casenum)
    endif
  endif
  call passed_test(err_out, max_err, err_okay, verbosity)
  if (verbosity >= 0) then
    write(*,"(A,E9.2)") "Maximum error was ", maxval(abs(err_out))
  endif

  if (dump_to_disk) then
    if (verbosity >= 1) then
      write(*,"(A,A)") "Writing to ", trim(output_path)
    endif
    open(10,file=output_path,action='WRITE')
    write(10,nml=outp_sizes)
    write(10,nml=outp)
    close(10)
  endif

  if (trim(nettype) == "hyper") then
    call all_networktype_deallocate(nets)
  elseif (trim(nettype) == "hornnet") then
  endif

end program qlknn_hyper
