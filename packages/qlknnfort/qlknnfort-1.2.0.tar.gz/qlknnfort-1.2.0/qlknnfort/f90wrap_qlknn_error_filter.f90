! Module qlknn_error_filter defined in file /builds/qualikiz-group/QLKNN-fortran/src/core/qlknn_error_filter.f90

subroutine f90wrap_determine_validity_with_eb(abs_limits, rel_limits, net_out, net_eb, validity, verbosity, mask, n0, &
    n1, n2, n3, n4, n5, n6, n7, n8)
    use qlknn_error_filter, only: determine_validity_with_eb
    implicit none
    
    real(8), intent(in), dimension(n0) :: abs_limits
    real(8), intent(in), dimension(n1) :: rel_limits
    real(8), intent(in), dimension(n2,n3) :: net_out
    real(8), intent(in), dimension(n4,n5) :: net_eb
    logical, intent(inout), dimension(n6,n7) :: validity
    integer(8), intent(in) :: verbosity
    logical, optional, intent(in), dimension(n8) :: mask
    integer :: n0
    !f2py intent(hide), depend(abs_limits) :: n0 = shape(abs_limits,0)
    integer :: n1
    !f2py intent(hide), depend(rel_limits) :: n1 = shape(rel_limits,0)
    integer :: n2
    !f2py intent(hide), depend(net_out) :: n2 = shape(net_out,0)
    integer :: n3
    !f2py intent(hide), depend(net_out) :: n3 = shape(net_out,1)
    integer :: n4
    !f2py intent(hide), depend(net_eb) :: n4 = shape(net_eb,0)
    integer :: n5
    !f2py intent(hide), depend(net_eb) :: n5 = shape(net_eb,1)
    integer :: n6
    !f2py intent(hide), depend(validity) :: n6 = shape(validity,0)
    integer :: n7
    !f2py intent(hide), depend(validity) :: n7 = shape(validity,1)
    integer :: n8
    !f2py intent(hide), depend(mask) :: n8 = shape(mask,0)
    call determine_validity_with_eb(abs_limits=abs_limits, rel_limits=rel_limits, net_out=net_out, net_eb=net_eb, &
        validity=validity, verbosity=verbosity, mask=mask)
end subroutine f90wrap_determine_validity_with_eb

subroutine f90wrap_determine_validity_multiplied_networks(leading_map, validity, verbosity, n0, n1, n2, n3)
    use qlknn_error_filter, only: determine_validity_multiplied_networks
    implicit none
    
    integer(8), intent(in), dimension(n0,n1) :: leading_map
    logical, intent(inout), dimension(n2,n3) :: validity
    integer(8), intent(in) :: verbosity
    integer :: n0
    !f2py intent(hide), depend(leading_map) :: n0 = shape(leading_map,0)
    integer :: n1
    !f2py intent(hide), depend(leading_map) :: n1 = shape(leading_map,1)
    integer :: n2
    !f2py intent(hide), depend(validity) :: n2 = shape(validity,0)
    integer :: n3
    !f2py intent(hide), depend(validity) :: n3 = shape(validity,1)
    call determine_validity_multiplied_networks(leading_map=leading_map, validity=validity, verbosity=verbosity)
end subroutine f90wrap_determine_validity_multiplied_networks

subroutine f90wrap_determine_validity_merged_modes(merge_map, validity, merged_validity, verbosity, n0, n1, n2, n3, n4, &
    n5)
    use qlknn_error_filter, only: determine_validity_merged_modes
    implicit none
    
    integer(8), intent(in), dimension(n0,n1) :: merge_map
    logical, intent(in), dimension(n2,n3) :: validity
    logical, intent(inout), dimension(n4,n5) :: merged_validity
    integer(8), intent(in) :: verbosity
    integer :: n0
    !f2py intent(hide), depend(merge_map) :: n0 = shape(merge_map,0)
    integer :: n1
    !f2py intent(hide), depend(merge_map) :: n1 = shape(merge_map,1)
    integer :: n2
    !f2py intent(hide), depend(validity) :: n2 = shape(validity,0)
    integer :: n3
    !f2py intent(hide), depend(validity) :: n3 = shape(validity,1)
    integer :: n4
    !f2py intent(hide), depend(merged_validity) :: n4 = shape(merged_validity,0)
    integer :: n5
    !f2py intent(hide), depend(merged_validity) :: n5 = shape(merged_validity,1)
    call determine_validity_merged_modes(merge_map=merge_map, validity=validity, merged_validity=merged_validity, &
        verbosity=verbosity)
end subroutine f90wrap_determine_validity_merged_modes

! End of module qlknn_error_filter defined in file /builds/qualikiz-group/QLKNN-fortran/src/core/qlknn_error_filter.f90

