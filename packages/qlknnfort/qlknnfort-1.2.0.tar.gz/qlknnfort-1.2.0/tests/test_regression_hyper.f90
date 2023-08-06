! This file is part of QLKNN-fortran
! You should have received the QLKNN-fortran LICENSE in the root of the project
module test_regression_hyper
#include "../src/core/preprocessor.inc"
  use fruit
  use fruit_util
  use qlknn_types

contains
  subroutine test_regression_hyper_case_one
    call regression_hyper_multi_fruit(1)
  end subroutine test_regression_hyper_case_one

  subroutine test_regression_hyper_case_two
    call regression_hyper_multi_fruit(2)
  end subroutine test_regression_hyper_case_two

  subroutine regression_hyper_multi_fruit(casenum)
    use fruit
    use fruit_util
    use qlknn_evaluate_nets
    use qlknn_disk_io
    use test_regression

    implicit none

    integer, intent(in) :: casenum
    integer(lli) :: verbosity, n_in, n_rho=24
    integer :: inp, i_outp
    real(qlknn_dp), dimension(:,:), allocatable :: input
    !real(qlknn_dp) :: start, finish
    real(qlknn_dp), dimension(:), allocatable :: err
    real(qlknn_dp), dimension(:), allocatable :: derr
    real(qlknn_dp) :: max_err
    logical, dimension(:), allocatable :: this_err_okay
    character(len=4096) :: nn_path, input_path
    character(len=512) :: ci_msg
    real(qlknn_dp), dimension(:,:), allocatable :: err_out
    real(qlknn_dp), dimension(:,:,:), allocatable :: derr_out
    logical, dimension(:,:,:), allocatable :: err_okay

    namelist /sizes/ n_rho, n_in
    namelist /test/ input

    input_path = 'tests/test.nml'
    nn_path = 'data/qlknn-hyper-namelists'
    verbosity = 0

    if (.not. allocated(nets%nets)) then
      call load_qlknn_hyper_nets_from_disk(nn_path, verbosity - 1)
    endif


    ! Read input namelist
    open(10,file=input_path,action='READ')
    read(10,nml=sizes)
    allocate(input(n_in, n_rho))
    read(10,nml=test)
    close(10)

    allocate(this_err_okay(n_rho))
    allocate(err(n_rho))
    allocate(derr(n_rho))

    max_err = max_err_hyper(casenum)
    call regression_hyper_multi(casenum, input, err_out, derr_out, verbosity)
    call passed_test(err_out, derr_out, max_err, err_okay, verbosity)

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
    call all_networktype_deallocate(nets)
  end subroutine regression_hyper_multi_fruit
end module test_regression_hyper
