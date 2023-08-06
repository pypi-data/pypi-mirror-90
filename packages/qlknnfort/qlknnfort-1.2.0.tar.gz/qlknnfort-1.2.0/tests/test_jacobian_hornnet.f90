! This file is part of QLKNN-fortran
! You should have received the QLKNN-fortran LICENSE in the root of the project
module test_jacobian_hornnet
#include "../src/core/preprocessor.inc"
  use fruit
  use fruit_util
  use qlknn_types
  use test_jacobian, only: calc_error

contains
  subroutine test_jacobian_hornnet_case_one
    call jacobian_hornnet_multi_fruit(1)
  end subroutine test_jacobian_hornnet_case_one

  subroutine test_jacobian_hornnet_case_two
    call jacobian_hornnet_multi_fruit(2)
  end subroutine test_jacobian_hornnet_case_two

  subroutine test_jacobian_hornnet_case_three
    call jacobian_hornnet_multi_fruit(3)
  end subroutine test_jacobian_hornnet_case_three

  subroutine test_jacobian_hornnet_case_four
    call jacobian_hornnet_multi_fruit(4)
  end subroutine test_jacobian_hornnet_case_four

  subroutine test_jacobian_hornnet_case_five
    call jacobian_hornnet_multi_fruit(5)
  end subroutine test_jacobian_hornnet_case_five

  subroutine test_jacobian_hornnet_case_six
    call jacobian_hornnet_multi_fruit(6)
  end subroutine test_jacobian_hornnet_case_six

  subroutine jacobian_hornnet_multi_fruit(casenum)
    use fruit
    use fruit_util
    use qlknn_evaluate_nets
    use qlknn_disk_io
    use test_jacobian

    implicit none

    integer, intent(in) :: casenum
    integer(lli) :: verbosity, n_in, n_rho=24
    integer :: inp, outp
    real(qlknn_dp), dimension(:,:), allocatable :: input
    !real(qlknn_dp) :: start, finish
    real(qlknn_dp), dimension(:), allocatable :: err
    real(qlknn_dp) :: max_err
    logical, dimension(:), allocatable :: this_err_okay
    character(len=4096) :: nn_path, input_path
    real(qlknn_dp) :: stepsize
    character(len=512) :: ci_msg
    real(qlknn_dp), dimension(:,:,:), allocatable :: err_out
    logical, dimension(:,:,:), allocatable :: err_okay

    namelist /sizes/ n_rho, n_in
    namelist /test/ input

    input_path = 'tests/test.nml'
    nn_path = 'data/qlknn-hornnet-namelists'
    verbosity = 0

    if (.not. allocated(blocks%input_blocks)) then
      call load_hornnet_nets_from_disk(nn_path, verbosity - 1)
    endif


    ! Read input namelist
    open(10,file=input_path,action='READ')
    read(10,nml=sizes)
    allocate(input(n_in, n_rho))
    read(10,nml=test)
    close(10)

    allocate(this_err_okay(n_rho))
    allocate(err(n_rho))

    stepsize = stepsize_hornnet
    max_err = max_err_hornnet(casenum)
    call jacobian_hornnet_multi(casenum, input, stepsize, err_out, verbosity)
    call passed_test(err_out, max_err, err_okay)

    do inp = 1, size(err_out, 3)
      do outp = 1, size(err_out, 1)
        !write(ci_msg, '(*(E7.2, A2))') (err(ii), ",", ii=1,n_rho)
        err = err_out(outp, :, inp)
        this_err_okay = err_okay(outp, :, inp)
        write(ci_msg, *) 'max abs err = ', maxval(abs(err))
        call assert_true(all(this_err_okay), trim(ci_msg))
      enddo
    enddo
  end subroutine jacobian_hornnet_multi_fruit
end module test_jacobian_hornnet
