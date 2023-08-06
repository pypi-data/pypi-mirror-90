! This file is part of QLKNN-fortran
! You should have received the QLKNN-fortran LICENSE in the root of the project
!> Module testing our quicksort implementation
module test_regression
#include "../src/core/preprocessor.inc"
  use qlknn_types
  implicit none

  real(qlknn_dp), dimension(2), parameter :: max_err_hyper = (/ 1e-12, 1e-12 /)
contains
  subroutine regression_hyper_multi(casenum, input, err, derr, verbosityin)
    use qlknn_evaluate_nets
    use qlknn_disk_io
    implicit none
    integer, intent(in) :: casenum
    real(qlknn_dp), dimension(:,:), intent(in):: input
    real(qlknn_dp), dimension(:,:), intent(out), allocatable :: err
    real(qlknn_dp), dimension(:,:,:), intent(out), allocatable :: derr
    integer(lli), intent(in), optional :: verbosityin
    integer :: n_rho, n_in, n_out, n_in_outp, n_out_outp, n_rho_outp, inp, i_outp
    type (qlknn_options) :: opts
    type (qlknn_normpars) :: qlknn_norms
    integer(lli) :: verbosity
    real(qlknn_dp), dimension(:), allocatable :: this_err, this_derr
    real(qlknn_dp), dimension(:,:), allocatable :: qlknn_out, qlknn_reference_out
    real(qlknn_dp), dimension(:,:,:), allocatable :: dqlknn_out_dinput, dqlknn_reference_out_dinput
    character(len=4096) :: nn_path = '', input_path = '', output_path = ''

    namelist /sizes/ n_rho, n_in
    namelist /test/ input
    namelist /outp_sizes/ n_rho, n_in, n_out
    namelist /outp/ qlknn_out
    namelist /outp_jacobian/ dqlknn_out_dinput

    if(present(verbosityin)) then
       verbosity=verbosityin
    else
       verbosity = 0
    endif

    input_path = 'tests/test.nml'
    nn_path = 'data/qlknn-hyper-namelists'


    call default_qlknn_hyper_options(opts)

    select case (casenum)
    case(1)
      output_path = 'tests/output_regression_case1.nml'
    case(2)
      output_path = 'tests/output_regression_case2.nml'
    case default
      ERRORSTOP(.true., 'Given case number not implemented')
    endselect

    ! Read regression outputs
    open(10,file=output_path,action='READ')
    read(10,nml=outp_sizes)
    n_rho_outp = n_rho
    n_in_outp = n_in
    n_out_outp = n_out
    allocate(qlknn_out(n_rho, n_out))
    allocate(dqlknn_out_dinput(n_out, n_rho, n_in))
    close(10)
    open(10,file=output_path,action='READ')
    read(10,nml=outp)
    read(10,nml=outp_jacobian)
    close(10)

    ! Variables for Victor rule
    ALLOCATE(qlknn_norms%A1(n_rho))
    qlknn_norms%A1 = 2.
    qlknn_norms%R0 = 3.
    qlknn_norms%a = 1.

    allocate(dqlknn_reference_out_dinput(size(dqlknn_out_dinput, 1), size(dqlknn_out_dinput, 2), size(dqlknn_out_dinput, 3)))
    allocate(qlknn_reference_out(size(qlknn_out, 1), size(qlknn_out, 2)))
    dqlknn_reference_out_dinput = dqlknn_out_dinput
    qlknn_reference_out = qlknn_out

    select case (casenum)
    case(1)
      opts%merge_modes = .false.
      opts%force_evaluate_all = .true.
    case(2)
      opts%merge_modes = .false.
      opts%force_evaluate_all = .true.
      opts%apply_victor_rule = .true.
    endselect

    call evaluate_QLKNN_10D(input, nets, qlknn_out, verbosity, opts, qlknn_norms, dqlknn_out_dinput)

    ERRORSTOP(size(qlknn_out, 1) /= n_rho_outp, 'Expected n_rho of network evaluation to be the same as output')
    ERRORSTOP(size(qlknn_out, 2) /= n_out_outp, 'Expected n_out of network evaluation to be the same as output')
    ERRORSTOP(size(dqlknn_out_dinput, 1) /= n_out_outp, 'Expected n_rho of network jacobian evaluation to be the same as output')
    ERRORSTOP(size(dqlknn_out_dinput, 2) /= n_rho_outp, 'Expected n_rho of network jacobian evaluation to be the same as output')
    ERRORSTOP(size(dqlknn_out_dinput, 3) /= n_in_outp, 'Expected n_rho of network jacobian evaluation to be the same as output')

    allocate(err(size(qlknn_out, 1), size(qlknn_out, 2)))
    allocate(derr(size(dqlknn_out_dinput, 1), size(dqlknn_out_dinput, 2), &
         size(dqlknn_out_dinput, 3)))
    allocate(this_err(size(qlknn_out, 1)))
    allocate(this_derr(size(qlknn_out, 1)))
    call calc_error(qlknn_reference_out, qlknn_out, err)
    call calc_derror(dqlknn_reference_out_dinput, dqlknn_out_dinput, derr)

    do i_outp = 1, n_out
      this_err(:) = err(:, i_outp)
      if (verbosity >= 1) then
        write(*, '(A, I3, A)') 'err(:, ', i_outp, ')'
        write(*, *) this_err(:)
      endif
      do inp = 1, n_in
        this_derr(:) = derr(i_outp, :, inp)
        if (verbosity >= 2) then
          write(*, '(A, I3, A, I3, A)') 'derr(', i_outp, ', :, ', inp, ')'
          write(*, *) this_derr(:)
        endif
      enddo
    enddo

  end subroutine regression_hyper_multi

  subroutine calc_error(reference, new, error)
    real(qlknn_dp), dimension(:,:), intent(in) :: reference
    real(qlknn_dp), dimension(:,:), intent(in) :: new
    real(qlknn_dp), dimension(:,:), intent(out) :: error

    error = reference - new

  end subroutine calc_error

  subroutine calc_derror(reference, new, error)
    real(qlknn_dp), dimension(:,:,:), intent(in) :: reference
    real(qlknn_dp), dimension(:,:,:), intent(in) :: new
    real(qlknn_dp), dimension(:,:,:), intent(out) :: error

    integer :: ii

    do ii = 1, size(reference, 3)
      call calc_error(reference(:, :, ii), new(:, :, ii), error(:, :, ii))
    enddo

  end subroutine calc_derror

  subroutine passed_test(perr, err, max_err, err_okay, verbosityin)
    use qlknn_primitives, only: is_not_close
    real(qlknn_dp), dimension(:,:), intent(in) :: perr
    real(qlknn_dp), dimension(:,:,:), intent(in) :: err
    real(qlknn_dp), intent(in) :: max_err
    logical, dimension(:,:,:), allocatable, intent(out) :: err_okay
    integer(lli), intent(in), optional :: verbosityin

    logical, dimension(:,:), allocatable :: perr_okay
    real(qlknn_dp), dimension(:), allocatable :: this_err
    real(qlknn_dp), dimension(:), allocatable :: this_perr
    logical, dimension(:), allocatable :: this_err_okay
    integer(lli) :: inp, outp, verbosity

    logical, dimension(:), allocatable :: is_nonzero

    if(present(verbosityin)) then
       verbosity=verbosityin
    else
       verbosity = 0
    end if
    if (verbosity >= 1) then
      write(*,"(A,E9.2)")"Checking against error ", max_err
    endif

    allocate(err_okay(size(err, 1), size(err, 2), size(err, 3)))
    allocate(perr_okay(size(perr, 1), size(perr, 2)))
    allocate(this_err(size(err, 2)))
    allocate(this_err_okay(size(err, 2)))
    allocate(this_perr(size(err, 2)))
    allocate(is_nonzero(size(err, 2)))

    err_okay = abs(err) < max_err
    perr_okay = abs(perr) < max_err
    do inp = 1, size(err, 3)
      err_okay(:, :, inp) = err_okay(:, :, inp) .and. transpose(perr_okay)
    enddo
    deallocate(perr_okay)

    if (verbosity >= 1) then
      do inp = 1, size(err, 3)
        do outp = 1, size(err, 1)
          this_err = err(outp, :, inp)
          this_err_okay = err_okay(outp, :, inp)
          this_perr = perr(outp, :)
          call is_not_close(this_err, 0._qlknn_dp, is_nonzero)
          if (.not. any(is_nonzero) .and. verbosity <= 4) then
            ! Skip zero errors
            cycle
          endif

          ! Debug for profile error
          if (inp == 1) then
            if (verbosity >= 2) then
              write(*,*)
              write(*,'(A, I3, A, I3)') 'outp=', outp
            endif
            if (verbosity >= 3) then
              write(*,'(A, I3, A, I3, A, *(E9.2, 1X))')'abs(perr(', outp, ', :)) = ', abs(this_perr)
            endif
            if (verbosity >= 2) then
              write(*,'(A, I3, A, I3, A, *(E9.2, 1X))')'abs(perr(', outp, ', :)) = ', maxval(abs(this_perr))
              write(*, '(A, *(L1, 1X))')'err_okay(outp, :, inp) ', err_okay(outp, :, inp)
            endif
            if (verbosity >= 1 .and. .not. all(this_err_okay)) then
              write(*,'(A, I3, A, I3, A, E9.2)')'Failed! max(abs(err(', outp, ', :, ', inp, '))) = ', maxval(abs(this_err))
            endif
          endif

          ! Debug for Jacobian profile error
          if (verbosity >= 2) then
            write(*,*)
            write(*,'(A, I3, A, I3)')'inp=', inp, ', outp=', outp
          endif
          if (verbosity >= 3) then
            write(*,'(A, I3, A, I3, A, *(E9.2, 1X))')'abs(err(', outp, ', :, ', inp, ')) = ', abs(this_err)
          endif
          if (verbosity >= 2) then
            write(*,'(A, I3, A, I3, A, *(E9.2, 1X))')'max(abs(err(', outp, ', :, ', inp, '))) = ', maxval(abs(this_err))
            write(*, '(A, *(L1, 1X))')'err_okay(outp, :, inp) ', err_okay(outp, :, inp)
          endif
          if (verbosity >= 1 .and. .not. all(this_err_okay)) then
            write(*,'(A, I3, A, I3, A, E9.2)')'Failed! max(abs(err(', outp, ', :, ', inp, '))) = ', maxval(abs(this_err))
          endif
        enddo
      enddo
    endif
  end subroutine passed_test
end module test_regression
