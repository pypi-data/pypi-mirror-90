! This file is part of QLKNN-fortran
! You should have received the QLKNN-fortran LICENSE in the root of the project
module qlknn_python
    use qlknn_evaluate_nets
    use qlknn_disk_io

    implicit none
contains
    subroutine evaluate_QLKNN_10D_direct(qlknn_path, input, qlknn_out, verbosityin, optsin, qlknn_normsin)
        real(qlknn_dp), dimension(:,:), intent(in) :: input
        character(len=2048), intent(in) :: qlknn_path
        integer(lli), optional, intent(in) :: verbosityin
        type (qlknn_options), optional, intent(in) :: optsin
        type(qlknn_normpars), optional, intent(in) :: qlknn_normsin

        real(qlknn_dp), dimension(:,:), intent(out) :: qlknn_out

        logical, save :: nets_loaded=.false.

        if (.NOT. nets_loaded) then
            call load_qlknn_hyper_nets_from_disk(trim(qlknn_path), verbosityin)
            nets_loaded=.true.
        end if
        CALL evaluate_QLKNN_10D(input, nets, qlknn_out, verbosityin, optsin, qlknn_normsin)
    end subroutine evaluate_QLKNN_10D_direct

    subroutine finalize()
        call all_networktype_deallocate(nets)
    end subroutine

    !subroutine evaluate_QLKNN_fusion_direct(qlknn_path, input, qlknn_out, verbosityin, optsin, qlknn_normsin)
    !    real(qlknn_dp), dimension(:,:), intent(in) :: input
    !    character(len=2048), intent(in) :: qlknn_path
    !    integer(lli), optional, intent(in) :: verbosityin
    !    type (qlknn_options), optional, intent(in) :: optsin
    !    type(qlknn_normpars), optional, intent(in) :: qlknn_normsin

    !    real(qlknn_dp), dimension(:,:), intent(out) :: qlknn_out

    !    real(qlknn_dp), dimension(:,:), allocatable :: fusion_constants
    !    logical, save :: nets_loaded=.false.

    !    print *, 'entering function'

    !    if (.NOT. nets_loaded) then
    !        call load_fusion_nets_from_disk(trim(qlknn_path), verbosityin)
    !        nets_loaded=.true.
    !    end if
    !    print *, 'allocating constants'
    !    allocate(fusion_constants(size(input, 2), 15))
    !    print *, 'eval constants'
    !    call evaluate_fusion_constants(input, blocks, fusion_constants, verbosityin, optsin, qlknn_normsin)
    !    print *, 'eval flux'
    !    call fusion_flux_from_constants(input, blocks, fusion_constants, qlknn_out, verbosityin, optsin, qlknn_normsin)
    !end subroutine evaluate_QLKNN_fusion_direct

    subroutine abort(msg)
        character(len=2048), intent(in) :: msg
        write(stderr, *) trim(msg)
      end subroutine abort

end module qlknn_python
