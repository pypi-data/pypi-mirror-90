! This file is part of QLKNN-fortran
! You should have received the QLKNN-fortran LICENSE in the root of the project
! It is an "all in one" file containing FRUIT tests that can be extended to CLI later
module test_imas
#include "../src/core/preprocessor.inc"
  implicit none
contains
  subroutine test_imas_case_one
    call imas_multi_fruit(1)
  end subroutine test_imas_case_one

  subroutine imas_multi_fruit(casenum)
    !! Multifunctional function to collect imas cases. All file IO should happen here,
    !! while the actual tests should be in a separate test routine to improve
    !! re-usability and test isolation
    use fruit
    use fruit_util
    use qlknn_evaluate_nets
    use qlknn_disk_io
    use test_regression, only: calc_error, calc_derror, passed_test

    implicit none

    integer, intent(in) :: casenum
    integer(lli) :: verbosity, n_in, i_outp, n_rho
    integer :: inp, outp
    real(qlknn_dp), dimension(:,:), allocatable :: input
    real(qlknn_dp), dimension(:), allocatable :: err
    real(qlknn_dp), dimension(:), allocatable :: derr
    real(qlknn_dp) :: max_err
    logical, dimension(:), allocatable :: this_err_okay
    character(len=4096) :: nn_path, input_path
    real(qlknn_dp) :: stepsize
    character(len=512) :: ci_msg
    real(qlknn_dp), dimension(:,:), allocatable :: err_out
    real(qlknn_dp), dimension(:,:,:), allocatable :: derr_out
    logical, dimension(:,:,:), allocatable :: err_okay

    ! Set constants for this test suite
    namelist /sizes/ n_rho, n_in
    namelist /test/ input

    input_path = 'tests/test.nml'
    nn_path = 'data/qlknn-hyper-namelists'

    verbosity = 0

    ! Load QLKNN settings from library
    if (.not. allocated(blocks%input_blocks)) then
      call load_qlknn_hyper_nets_from_disk(nn_path, verbosity)
    endif


    ! Read input namelist
    ! Automatically determines n_in and n_rho
    open(10,file=input_path,action='READ')
    read(10,nml=sizes)
    allocate(input(n_in, n_rho))
    read(10,nml=test)
    close(10)

    ! Allocate containers for temporary error data
    allocate(this_err_okay(n_rho))
    allocate(err(n_rho))
    allocate(derr(n_rho))

    ! Call internal "generalizable" test subroutine and calculate errors
    max_err = 1e-7
    call imas_hyper_multi(casenum, input, err_out, derr_out, verbosityin=verbosity)
    call passed_test(err_out, derr_out, max_err, err_okay, verbosity)

    ! Use FRUIT to assert if tests have passed
    do i_outp = 1, size(err_out, 2)
      err(:) = err_out(:, i_outp)
      if (verbosity >= 1) then
        write(*, '(A, I3, A)') 'max abs err(:, ', i_outp, ')'
        write(*, *) maxval(abs(err))
      endif
      do inp = 1, size(derr_out, 3)
        derr(:) = derr_out(i_outp, :, inp)
        if (verbosity >= 2) then
          write(*, '(A, I3, A, I3, A)') 'max abs derr(', i_outp, ', :, ', inp, ')'
          write(*, *) maxval(abs(derr))
        endif
        this_err_okay = err_okay(i_outp, :, inp)
        write(ci_msg, *) 'max abs err = ', maxval(abs(err))
        call assert_true(all(this_err_okay), trim(ci_msg))
      enddo
    enddo

    ! De-allocate SAVEed network structures
    call all_networktype_deallocate(nets)
  end subroutine imas_multi_fruit

  subroutine imas_hyper_multi(casenum, input, err_out, derr_out, verbosityin)
    !! Multifunctional test routine not dependenend on FRUIT
    use qlknn_evaluate_nets
    use qlknn_disk_io
    use test_regression, only: calc_error, calc_derror, passed_test

    implicit none
    integer, intent(in) :: casenum
    real(qlknn_dp), dimension(:,:), intent(in):: input
    real(qlknn_dp), dimension(:,:), intent(out), allocatable :: err_out
    real(qlknn_dp), dimension(:,:,:), intent(out), allocatable :: derr_out
    integer(lli), intent(in), optional :: verbosityin
    integer :: n_rho, n_in, n_out, n_in_outp, n_out_outp, n_rho_outp, inp, i_outp
    type (qlknn_options) :: opts
    type (qlknn_normpars) :: qlknn_norms
    integer(lli) :: verbosity
    real(qlknn_dp), dimension(:), allocatable :: this_err, this_derr
    real(qlknn_dp), dimension(:,:), allocatable :: qlknn_out, qlknn_imas_out
    real(qlknn_dp), dimension(:,:,:), allocatable :: dqlknn_out_dinput, dqlknn_imas_out_dinput

    if(present(verbosityin)) then
       verbosity = verbosityin
    else
       verbosity = 0
    end if

    n_in = size(input, 1)
    n_rho = size(input, 2)

    call default_qlknn_hyper_options(opts)

    ! Set default options
    opts%constrain_inputs = .false.
    opts%constrain_outputs = .false.
    opts%force_evaluate_all = .true.
    opts%apply_victor_rule = .true.

    ! Variables for Victor rule
    ALLOCATE(qlknn_norms%A1(n_rho))
    qlknn_norms%A1 = 2.
    qlknn_norms%R0 = 3.
    qlknn_norms%a = 1.


    ! Set specific options, and allocated arrays that change shape between tests
    ! Each test should have at least:
    ! n_out: The amount of outputs of the outermost function
    ! n_in: The amount of inputs of the innermost function
    ! n_rho: The amount of radial points
    ! This defines the following quantities:
    ! dqlknn_out_dinput: The Jacobian of the outermost function with respect
    !    to the innermost input (n_out, n_rho, n_in)
    ! qlknn_out: The output of the outermost function
    select case (casenum)
    case(1)
      ! Test full IO conversion with Victor rule enabled
      opts%merge_modes = .false.
      n_out = 20
      allocate(qlknn_out(n_rho, n_out))
      allocate(dqlknn_out_dinput(n_out, n_rho, n_in))

      allocate(qlknn_imas_out(n_rho, n_out))
      allocate(dqlknn_imas_out_dinput(n_out, n_rho, n_in))
    case default
      ERRORSTOP(.true., 'Given case number not implemented')
    endselect

    ! TODO: Test IMAS implementation here. For now, call the same function twice to test CI
    call evaluate_QLKNN_10D(input, nets, qlknn_out, verbosity, opts, qlknn_norms, dqlknn_out_dinput)
    call evaluate_QLKNN_10D(input, nets, qlknn_imas_out, verbosity, opts, qlknn_norms, dqlknn_imas_out_dinput)

    ! Allocate arrays to contain "test has passed T/F" data
    allocate(err_out(size(qlknn_out, 1), size(qlknn_out, 2)))
    allocate(derr_out(size(dqlknn_out_dinput, 1), size(dqlknn_out_dinput, 2), &
         size(dqlknn_out_dinput, 3)))
    allocate(this_err(size(qlknn_out, 1)))
    allocate(this_derr(size(qlknn_out, 1)))

    ! Calculate absolute errors
    call calc_error(qlknn_imas_out, qlknn_out, err_out)
    call calc_derror(dqlknn_imas_out_dinput, dqlknn_out_dinput, derr_out)

    ! Set errors of output array
    do i_outp = 1, n_out
      this_err(:) = err_out(:, i_outp)
      if (verbosity >= 1) then
        write(*, '(A, I3, A)') 'err(:, ', i_outp, ')'
        write(*, *) this_err(:)
      endif
      do inp = 1, n_in
        this_derr(:) = derr_out(i_outp, :, inp)
        if (verbosity >= 2) then
          write(*, '(A, I3, A, I3, A)') 'derr(', i_outp, ', :, ', inp, ')'
          write(*, *) this_derr(:)
        endif
      enddo
    enddo
  end subroutine imas_hyper_multi
end module test_imas
