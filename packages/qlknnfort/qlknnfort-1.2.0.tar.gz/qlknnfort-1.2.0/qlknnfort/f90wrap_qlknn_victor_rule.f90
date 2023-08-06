! Module qlknn_victor_rule defined in file /builds/qualikiz-group/QLKNN-fortran/src/core/qlknn_victor_rule.f90

subroutine f90wrap_get_f_victorthesis(input, nets, f_victorthesis, dthesis_dinput, n0, n1, n2, n3, n4)
    use qlknn_types, only: net_collection
    use qlknn_victor_rule, only: get_f_victorthesis
    implicit none
    
    type net_collection_ptr_type
        type(net_collection), pointer :: p => NULL()
    end type net_collection_ptr_type
    real(8), intent(in), dimension(n0,n1) :: input
    type(net_collection_ptr_type) :: nets_ptr
    integer, intent(in), dimension(2) :: nets
    real(8), intent(inout), dimension(n2) :: f_victorthesis
    real(8), optional, dimension(n3,n4) :: dthesis_dinput
    integer :: n0
    !f2py intent(hide), depend(input) :: n0 = shape(input,0)
    integer :: n1
    !f2py intent(hide), depend(input) :: n1 = shape(input,1)
    integer :: n2
    !f2py intent(hide), depend(f_victorthesis) :: n2 = shape(f_victorthesis,0)
    integer :: n3
    !f2py intent(hide), depend(dthesis_dinput) :: n3 = shape(dthesis_dinput,0)
    integer :: n4
    !f2py intent(hide), depend(dthesis_dinput) :: n4 = shape(dthesis_dinput,1)
    nets_ptr = transfer(nets, nets_ptr)
    call get_f_victorthesis(input=input, nets=nets_ptr%p, f_victorthesis=f_victorthesis, dthesis_dinput=dthesis_dinput)
end subroutine f90wrap_get_f_victorthesis

subroutine f90wrap_get_f_vic(input, nets, qlknn_norms, f_vic, verbosity, df_vic_dinput, n0, n1, n2, n3, n4)
    use qlknn_victor_rule, only: get_f_vic
    use qlknn_types, only: net_collection, qlknn_normpars
    implicit none
    
    type net_collection_ptr_type
        type(net_collection), pointer :: p => NULL()
    end type net_collection_ptr_type
    type qlknn_normpars_ptr_type
        type(qlknn_normpars), pointer :: p => NULL()
    end type qlknn_normpars_ptr_type
    real(8), intent(in), dimension(n0,n1) :: input
    type(net_collection_ptr_type) :: nets_ptr
    integer, intent(in), dimension(2) :: nets
    type(qlknn_normpars_ptr_type) :: qlknn_norms_ptr
    integer, intent(in), dimension(2) :: qlknn_norms
    real(8), intent(inout), dimension(n2) :: f_vic
    integer(8), optional, intent(in) :: verbosity
    real(8), optional, intent(inout), dimension(n3,n4) :: df_vic_dinput
    integer :: n0
    !f2py intent(hide), depend(input) :: n0 = shape(input,0)
    integer :: n1
    !f2py intent(hide), depend(input) :: n1 = shape(input,1)
    integer :: n2
    !f2py intent(hide), depend(f_vic) :: n2 = shape(f_vic,0)
    integer :: n3
    !f2py intent(hide), depend(df_vic_dinput) :: n3 = shape(df_vic_dinput,0)
    integer :: n4
    !f2py intent(hide), depend(df_vic_dinput) :: n4 = shape(df_vic_dinput,1)
    nets_ptr = transfer(nets, nets_ptr)
    qlknn_norms_ptr = transfer(qlknn_norms, qlknn_norms_ptr)
    call get_f_vic(input=input, nets=nets_ptr%p, qlknn_norms=qlknn_norms_ptr%p, f_vic=f_vic, verbosity=verbosity, &
        df_vic_dinput=df_vic_dinput)
end subroutine f90wrap_get_f_vic

subroutine f90wrap_scale_with_victor(leading_map, input, nets, qlknn_norms, net_result, verbosity, dnet_out_dinput, n0, &
    n1, n2, n3, n4, n5, n6, n7, n8)
    use qlknn_victor_rule, only: scale_with_victor
    use qlknn_types, only: net_collection, qlknn_normpars
    implicit none
    
    type net_collection_ptr_type
        type(net_collection), pointer :: p => NULL()
    end type net_collection_ptr_type
    type qlknn_normpars_ptr_type
        type(qlknn_normpars), pointer :: p => NULL()
    end type qlknn_normpars_ptr_type
    integer(8), intent(in), dimension(n0,n1) :: leading_map
    real(8), intent(in), dimension(n2,n3) :: input
    type(net_collection_ptr_type) :: nets_ptr
    integer, intent(in), dimension(2) :: nets
    type(qlknn_normpars_ptr_type) :: qlknn_norms_ptr
    integer, intent(in), dimension(2) :: qlknn_norms
    real(8), intent(inout), dimension(n4,n5) :: net_result
    integer(8), optional, intent(in) :: verbosity
    real(8), optional, intent(inout), dimension(n6,n7,n8) :: dnet_out_dinput
    integer :: n0
    !f2py intent(hide), depend(leading_map) :: n0 = shape(leading_map,0)
    integer :: n1
    !f2py intent(hide), depend(leading_map) :: n1 = shape(leading_map,1)
    integer :: n2
    !f2py intent(hide), depend(input) :: n2 = shape(input,0)
    integer :: n3
    !f2py intent(hide), depend(input) :: n3 = shape(input,1)
    integer :: n4
    !f2py intent(hide), depend(net_result) :: n4 = shape(net_result,0)
    integer :: n5
    !f2py intent(hide), depend(net_result) :: n5 = shape(net_result,1)
    integer :: n6
    !f2py intent(hide), depend(dnet_out_dinput) :: n6 = shape(dnet_out_dinput,0)
    integer :: n7
    !f2py intent(hide), depend(dnet_out_dinput) :: n7 = shape(dnet_out_dinput,1)
    integer :: n8
    !f2py intent(hide), depend(dnet_out_dinput) :: n8 = shape(dnet_out_dinput,2)
    nets_ptr = transfer(nets, nets_ptr)
    qlknn_norms_ptr = transfer(qlknn_norms, qlknn_norms_ptr)
    call scale_with_victor(leading_map=leading_map, input=input, nets=nets_ptr%p, qlknn_norms=qlknn_norms_ptr%p, &
        net_result=net_result, verbosity=verbosity, dnet_out_dinput=dnet_out_dinput)
end subroutine f90wrap_scale_with_victor

subroutine f90wrap_qlknn_victor_rule__get__c_1(f90wrap_c_1)
    use qlknn_victor_rule, only: qlknn_victor_rule_c_1 => c_1
    implicit none
    real(8), intent(out) :: f90wrap_c_1
    
    f90wrap_c_1 = qlknn_victor_rule_c_1
end subroutine f90wrap_qlknn_victor_rule__get__c_1

subroutine f90wrap_qlknn_victor_rule__get__c_2(f90wrap_c_2)
    use qlknn_victor_rule, only: qlknn_victor_rule_c_2 => c_2
    implicit none
    real(8), intent(out) :: f90wrap_c_2
    
    f90wrap_c_2 = qlknn_victor_rule_c_2
end subroutine f90wrap_qlknn_victor_rule__get__c_2

subroutine f90wrap_qlknn_victor_rule__get__c_3(f90wrap_c_3)
    use qlknn_victor_rule, only: qlknn_victor_rule_c_3 => c_3
    implicit none
    real(8), intent(out) :: f90wrap_c_3
    
    f90wrap_c_3 = qlknn_victor_rule_c_3
end subroutine f90wrap_qlknn_victor_rule__get__c_3

subroutine f90wrap_qlknn_victor_rule__get__c_4(f90wrap_c_4)
    use qlknn_victor_rule, only: qlknn_victor_rule_c_4 => c_4
    implicit none
    real(8), intent(out) :: f90wrap_c_4
    
    f90wrap_c_4 = qlknn_victor_rule_c_4
end subroutine f90wrap_qlknn_victor_rule__get__c_4

subroutine f90wrap_qlknn_victor_rule__get__gamma0_lower_bound(f90wrap_gamma0_lower_bound)
    use qlknn_victor_rule, only: qlknn_victor_rule_gamma0_lower_bound => gamma0_lower_bound
    implicit none
    real(8), intent(out) :: f90wrap_gamma0_lower_bound
    
    f90wrap_gamma0_lower_bound = qlknn_victor_rule_gamma0_lower_bound
end subroutine f90wrap_qlknn_victor_rule__get__gamma0_lower_bound

subroutine f90wrap_qlknn_victor_rule__get__victor_Te_norm(f90wrap_victor_Te_norm)
    use qlknn_victor_rule, only: qlknn_victor_rule_victor_Te_norm => victor_Te_norm
    implicit none
    real(8), intent(out) :: f90wrap_victor_Te_norm
    
    f90wrap_victor_Te_norm = qlknn_victor_rule_victor_Te_norm
end subroutine f90wrap_qlknn_victor_rule__get__victor_Te_norm

! End of module qlknn_victor_rule defined in file /builds/qualikiz-group/QLKNN-fortran/src/core/qlknn_victor_rule.f90

