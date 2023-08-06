! Module qlknn_evaluate_nets defined in file /builds/qualikiz-group/QLKNN-fortran/src/core/qlknn_evaluate_nets.f90

subroutine f90wrap_evaluate_qlknn_10d(input, nets, qlknn_out, verbosityin, optsin, qlknn_normsin, dqlknn_out_dinput, n0, &
    n1, n2, n3, n4, n5, n6)
    use qlknn_types, only: net_collection, qlknn_options, qlknn_normpars
    use qlknn_evaluate_nets, only: evaluate_qlknn_10d
    implicit none
    
    type net_collection_ptr_type
        type(net_collection), pointer :: p => NULL()
    end type net_collection_ptr_type
    type qlknn_options_ptr_type
        type(qlknn_options), pointer :: p => NULL()
    end type qlknn_options_ptr_type
    type qlknn_normpars_ptr_type
        type(qlknn_normpars), pointer :: p => NULL()
    end type qlknn_normpars_ptr_type
    real(8), intent(in), dimension(n0,n1) :: input
    type(net_collection_ptr_type) :: nets_ptr
    integer, intent(in), dimension(2) :: nets
    real(8), intent(inout), dimension(n2,n3) :: qlknn_out
    integer(8), optional, intent(in) :: verbosityin
    type(qlknn_options_ptr_type) :: optsin_ptr
    integer, optional, intent(in), dimension(2) :: optsin
    type(qlknn_normpars_ptr_type) :: qlknn_normsin_ptr
    integer, optional, intent(in), dimension(2) :: qlknn_normsin
    real(8), optional, intent(inout), dimension(n4,n5,n6) :: dqlknn_out_dinput
    integer :: n0
    !f2py intent(hide), depend(input) :: n0 = shape(input,0)
    integer :: n1
    !f2py intent(hide), depend(input) :: n1 = shape(input,1)
    integer :: n2
    !f2py intent(hide), depend(qlknn_out) :: n2 = shape(qlknn_out,0)
    integer :: n3
    !f2py intent(hide), depend(qlknn_out) :: n3 = shape(qlknn_out,1)
    integer :: n4
    !f2py intent(hide), depend(dqlknn_out_dinput) :: n4 = shape(dqlknn_out_dinput,0)
    integer :: n5
    !f2py intent(hide), depend(dqlknn_out_dinput) :: n5 = shape(dqlknn_out_dinput,1)
    integer :: n6
    !f2py intent(hide), depend(dqlknn_out_dinput) :: n6 = shape(dqlknn_out_dinput,2)
    nets_ptr = transfer(nets, nets_ptr)
    if (present(optsin)) then
        optsin_ptr = transfer(optsin, optsin_ptr)
    else
        optsin_ptr%p => null()
    end if
    if (present(qlknn_normsin)) then
        qlknn_normsin_ptr = transfer(qlknn_normsin, qlknn_normsin_ptr)
    else
        qlknn_normsin_ptr%p => null()
    end if
    call evaluate_qlknn_10d(input=input, nets=nets_ptr%p, qlknn_out=qlknn_out, verbosityin=verbosityin, optsin=optsin_ptr%p, &
        qlknn_normsin=qlknn_normsin_ptr%p, dqlknn_out_dinput=dqlknn_out_dinput)
end subroutine f90wrap_evaluate_qlknn_10d

subroutine f90wrap_evaluate_fullflux_net(input, nets, qlknn_out, verbosityin, optsin, dqlknn_out_dinput, n0, n1, n2, n3, &
    n4, n5, n6)
    use qlknn_types, only: net_collection, qlknn_options
    use qlknn_evaluate_nets, only: evaluate_fullflux_net
    implicit none
    
    type net_collection_ptr_type
        type(net_collection), pointer :: p => NULL()
    end type net_collection_ptr_type
    type qlknn_options_ptr_type
        type(qlknn_options), pointer :: p => NULL()
    end type qlknn_options_ptr_type
    real(8), intent(in), dimension(n0,n1) :: input
    type(net_collection_ptr_type) :: nets_ptr
    integer, intent(in), dimension(2) :: nets
    real(8), intent(inout), dimension(n2,n3) :: qlknn_out
    integer(8), optional, intent(in) :: verbosityin
    type(qlknn_options_ptr_type) :: optsin_ptr
    integer, optional, intent(in), dimension(2) :: optsin
    real(8), optional, intent(inout), dimension(n4,n5,n6) :: dqlknn_out_dinput
    integer :: n0
    !f2py intent(hide), depend(input) :: n0 = shape(input,0)
    integer :: n1
    !f2py intent(hide), depend(input) :: n1 = shape(input,1)
    integer :: n2
    !f2py intent(hide), depend(qlknn_out) :: n2 = shape(qlknn_out,0)
    integer :: n3
    !f2py intent(hide), depend(qlknn_out) :: n3 = shape(qlknn_out,1)
    integer :: n4
    !f2py intent(hide), depend(dqlknn_out_dinput) :: n4 = shape(dqlknn_out_dinput,0)
    integer :: n5
    !f2py intent(hide), depend(dqlknn_out_dinput) :: n5 = shape(dqlknn_out_dinput,1)
    integer :: n6
    !f2py intent(hide), depend(dqlknn_out_dinput) :: n6 = shape(dqlknn_out_dinput,2)
    nets_ptr = transfer(nets, nets_ptr)
    if (present(optsin)) then
        optsin_ptr = transfer(optsin, optsin_ptr)
    else
        optsin_ptr%p => null()
    end if
    call evaluate_fullflux_net(input=input, nets=nets_ptr%p, qlknn_out=qlknn_out, verbosityin=verbosityin, &
        optsin=optsin_ptr%p, dqlknn_out_dinput=dqlknn_out_dinput)
end subroutine f90wrap_evaluate_fullflux_net

subroutine f90wrap_evaluate_jetexp_net(input, nets, n_members, qlknn_out, qlknn_eb, verbosityin, optsin, &
    dqlknn_out_dinput, qlknn_validity, n0, n1, n2, n3, n4, n5, n6, n7, n8, n9, n10)
    use qlknn_types, only: net_collection, qlknn_options
    use qlknn_evaluate_nets, only: evaluate_jetexp_net
    implicit none
    
    type net_collection_ptr_type
        type(net_collection), pointer :: p => NULL()
    end type net_collection_ptr_type
    type qlknn_options_ptr_type
        type(qlknn_options), pointer :: p => NULL()
    end type qlknn_options_ptr_type
    real(8), intent(in), dimension(n0,n1) :: input
    type(net_collection_ptr_type) :: nets_ptr
    integer, intent(in), dimension(2) :: nets
    integer(8), intent(in) :: n_members
    real(8), intent(inout), dimension(n2,n3) :: qlknn_out
    real(8), intent(inout), dimension(n4,n5) :: qlknn_eb
    integer(8), optional, intent(in) :: verbosityin
    type(qlknn_options_ptr_type) :: optsin_ptr
    integer, optional, intent(in), dimension(2) :: optsin
    real(8), optional, intent(inout), dimension(n6,n7,n8) :: dqlknn_out_dinput
    logical, optional, intent(inout), dimension(n9,n10) :: qlknn_validity
    integer :: n0
    !f2py intent(hide), depend(input) :: n0 = shape(input,0)
    integer :: n1
    !f2py intent(hide), depend(input) :: n1 = shape(input,1)
    integer :: n2
    !f2py intent(hide), depend(qlknn_out) :: n2 = shape(qlknn_out,0)
    integer :: n3
    !f2py intent(hide), depend(qlknn_out) :: n3 = shape(qlknn_out,1)
    integer :: n4
    !f2py intent(hide), depend(qlknn_eb) :: n4 = shape(qlknn_eb,0)
    integer :: n5
    !f2py intent(hide), depend(qlknn_eb) :: n5 = shape(qlknn_eb,1)
    integer :: n6
    !f2py intent(hide), depend(dqlknn_out_dinput) :: n6 = shape(dqlknn_out_dinput,0)
    integer :: n7
    !f2py intent(hide), depend(dqlknn_out_dinput) :: n7 = shape(dqlknn_out_dinput,1)
    integer :: n8
    !f2py intent(hide), depend(dqlknn_out_dinput) :: n8 = shape(dqlknn_out_dinput,2)
    integer :: n9
    !f2py intent(hide), depend(qlknn_validity) :: n9 = shape(qlknn_validity,0)
    integer :: n10
    !f2py intent(hide), depend(qlknn_validity) :: n10 = shape(qlknn_validity,1)
    nets_ptr = transfer(nets, nets_ptr)
    if (present(optsin)) then
        optsin_ptr = transfer(optsin, optsin_ptr)
    else
        optsin_ptr%p => null()
    end if
    call evaluate_jetexp_net(input=input, nets=nets_ptr%p, n_members=n_members, qlknn_out=qlknn_out, qlknn_eb=qlknn_eb, &
        verbosityin=verbosityin, optsin=optsin_ptr%p, dqlknn_out_dinput=dqlknn_out_dinput, qlknn_validity=qlknn_validity)
end subroutine f90wrap_evaluate_jetexp_net

subroutine f90wrap_hornnet_flux_from_constants(input, blocks, hornnet_constants, flux_out, verbosityin, optsin, &
    qlknn_normsin, dflux_dhornnet_constants, dflux_dinput, n0, n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11)
    use qlknn_types, only: block_collection, qlknn_options, qlknn_normpars
    use qlknn_evaluate_nets, only: hornnet_flux_from_constants
    implicit none
    
    type block_collection_ptr_type
        type(block_collection), pointer :: p => NULL()
    end type block_collection_ptr_type
    type qlknn_options_ptr_type
        type(qlknn_options), pointer :: p => NULL()
    end type qlknn_options_ptr_type
    type qlknn_normpars_ptr_type
        type(qlknn_normpars), pointer :: p => NULL()
    end type qlknn_normpars_ptr_type
    real(8), intent(in), dimension(n0,n1) :: input
    type(block_collection_ptr_type) :: blocks_ptr
    integer, intent(in), dimension(2) :: blocks
    real(8), intent(in), dimension(n2,n3) :: hornnet_constants
    real(8), intent(inout), dimension(n4,n5) :: flux_out
    integer(8), optional, intent(in) :: verbosityin
    type(qlknn_options_ptr_type) :: optsin_ptr
    integer, optional, intent(in), dimension(2) :: optsin
    type(qlknn_normpars_ptr_type) :: qlknn_normsin_ptr
    integer, optional, intent(in), dimension(2) :: qlknn_normsin
    real(8), optional, intent(inout), dimension(n6,n7,n8) :: dflux_dhornnet_constants
    real(8), optional, intent(inout), dimension(n9,n10,n11) :: dflux_dinput
    integer :: n0
    !f2py intent(hide), depend(input) :: n0 = shape(input,0)
    integer :: n1
    !f2py intent(hide), depend(input) :: n1 = shape(input,1)
    integer :: n2
    !f2py intent(hide), depend(hornnet_constants) :: n2 = shape(hornnet_constants,0)
    integer :: n3
    !f2py intent(hide), depend(hornnet_constants) :: n3 = shape(hornnet_constants,1)
    integer :: n4
    !f2py intent(hide), depend(flux_out) :: n4 = shape(flux_out,0)
    integer :: n5
    !f2py intent(hide), depend(flux_out) :: n5 = shape(flux_out,1)
    integer :: n6
    !f2py intent(hide), depend(dflux_dhornnet_constants) :: n6 = shape(dflux_dhornnet_constants,0)
    integer :: n7
    !f2py intent(hide), depend(dflux_dhornnet_constants) :: n7 = shape(dflux_dhornnet_constants,1)
    integer :: n8
    !f2py intent(hide), depend(dflux_dhornnet_constants) :: n8 = shape(dflux_dhornnet_constants,2)
    integer :: n9
    !f2py intent(hide), depend(dflux_dinput) :: n9 = shape(dflux_dinput,0)
    integer :: n10
    !f2py intent(hide), depend(dflux_dinput) :: n10 = shape(dflux_dinput,1)
    integer :: n11
    !f2py intent(hide), depend(dflux_dinput) :: n11 = shape(dflux_dinput,2)
    blocks_ptr = transfer(blocks, blocks_ptr)
    if (present(optsin)) then
        optsin_ptr = transfer(optsin, optsin_ptr)
    else
        optsin_ptr%p => null()
    end if
    if (present(qlknn_normsin)) then
        qlknn_normsin_ptr = transfer(qlknn_normsin, qlknn_normsin_ptr)
    else
        qlknn_normsin_ptr%p => null()
    end if
    call hornnet_flux_from_constants(input=input, blocks=blocks_ptr%p, hornnet_constants=hornnet_constants, &
        flux_out=flux_out, verbosityin=verbosityin, optsin=optsin_ptr%p, qlknn_normsin=qlknn_normsin_ptr%p, &
        dflux_dhornnet_constants=dflux_dhornnet_constants, dflux_dinput=dflux_dinput)
end subroutine f90wrap_hornnet_flux_from_constants

subroutine f90wrap_hornnet_multiply_jacobians(dhornnet_constants_dinput, dflux_dhornnet_constants, dflux_dinput, &
    dqlknn_out_dinput, verbosityin, n0, n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11)
    use qlknn_evaluate_nets, only: hornnet_multiply_jacobians
    implicit none
    
    real(8), intent(in), dimension(n0,n1,n2) :: dhornnet_constants_dinput
    real(8), intent(in), dimension(n3,n4,n5) :: dflux_dhornnet_constants
    real(8), intent(in), dimension(n6,n7,n8) :: dflux_dinput
    real(8), intent(inout), dimension(n9,n10,n11) :: dqlknn_out_dinput
    integer(8), intent(in), optional :: verbosityin
    integer :: n0
    !f2py intent(hide), depend(dhornnet_constants_dinput) :: n0 = shape(dhornnet_constants_dinput,0)
    integer :: n1
    !f2py intent(hide), depend(dhornnet_constants_dinput) :: n1 = shape(dhornnet_constants_dinput,1)
    integer :: n2
    !f2py intent(hide), depend(dhornnet_constants_dinput) :: n2 = shape(dhornnet_constants_dinput,2)
    integer :: n3
    !f2py intent(hide), depend(dflux_dhornnet_constants) :: n3 = shape(dflux_dhornnet_constants,0)
    integer :: n4
    !f2py intent(hide), depend(dflux_dhornnet_constants) :: n4 = shape(dflux_dhornnet_constants,1)
    integer :: n5
    !f2py intent(hide), depend(dflux_dhornnet_constants) :: n5 = shape(dflux_dhornnet_constants,2)
    integer :: n6
    !f2py intent(hide), depend(dflux_dinput) :: n6 = shape(dflux_dinput,0)
    integer :: n7
    !f2py intent(hide), depend(dflux_dinput) :: n7 = shape(dflux_dinput,1)
    integer :: n8
    !f2py intent(hide), depend(dflux_dinput) :: n8 = shape(dflux_dinput,2)
    integer :: n9
    !f2py intent(hide), depend(dqlknn_out_dinput) :: n9 = shape(dqlknn_out_dinput,0)
    integer :: n10
    !f2py intent(hide), depend(dqlknn_out_dinput) :: n10 = shape(dqlknn_out_dinput,1)
    integer :: n11
    !f2py intent(hide), depend(dqlknn_out_dinput) :: n11 = shape(dqlknn_out_dinput,2)
    call hornnet_multiply_jacobians(dhornnet_constants_dinput=dhornnet_constants_dinput, &
        dflux_dhornnet_constants=dflux_dhornnet_constants, dflux_dinput=dflux_dinput, dqlknn_out_dinput=dqlknn_out_dinput, &
        verbosityin=verbosityin)
end subroutine f90wrap_hornnet_multiply_jacobians

subroutine f90wrap_hornnet_multiplier(heaviside_function_times, clip_by_value, hornnet_constants, sepflux_out, outp, &
    pow_idx, block_idx, slope_idx, f, g, h, drelu_dhornnet_constants, drelu_dinput, dclip_by_value_dhornnet_constants, &
    dclip_by_value_dinput, df_dhornnet_constants, df_dinput, dg_dhornnet_constants, dg_dinput, dh_dhornnet_constants, &
    n0, n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11, n12, n13, n14, n15, n16, n17, n18, n19, n20, n21, n22, n23, n24, &
    n25, n26, n27, n28, n29, n30, n31, n32, n33, n34, n35, n36, n37, n38, n39, n40)
    use qlknn_evaluate_nets, only: hornnet_multiplier
    implicit none
    
    real(8), intent(in), dimension(n0,n1) :: heaviside_function_times
    real(8), intent(in), dimension(n2,n3) :: clip_by_value
    real(8), intent(in), dimension(n4,n5) :: hornnet_constants
    real(8), intent(inout), dimension(n6,n7) :: sepflux_out
    integer(8), intent(in) :: outp
    integer(8), intent(in) :: pow_idx
    integer(8), intent(in) :: block_idx
    integer(8), intent(in) :: slope_idx
    real(8), intent(inout), dimension(n8,n9) :: f
    real(8), intent(inout), dimension(n10,n11) :: g
    real(8), intent(inout), dimension(n12,n13) :: h
    real(8), intent(in), optional, dimension(n14,n15,n16) :: drelu_dhornnet_constants
    real(8), intent(in), optional, dimension(n17,n18,n19) :: drelu_dinput
    real(8), intent(in), optional, dimension(n20,n21,n22) :: dclip_by_value_dhornnet_constants
    real(8), intent(in), optional, dimension(n23,n24,n25) :: dclip_by_value_dinput
    real(8), intent(inout), optional, dimension(n26,n27,n28) :: df_dhornnet_constants
    real(8), intent(inout), optional, dimension(n29,n30,n31) :: df_dinput
    real(8), intent(inout), optional, dimension(n32,n33,n34) :: dg_dhornnet_constants
    real(8), intent(inout), optional, dimension(n35,n36,n37) :: dg_dinput
    real(8), intent(inout), optional, dimension(n38,n39,n40) :: dh_dhornnet_constants
    integer :: n0
    !f2py intent(hide), depend(heaviside_function_times) :: n0 = shape(heaviside_function_times,0)
    integer :: n1
    !f2py intent(hide), depend(heaviside_function_times) :: n1 = shape(heaviside_function_times,1)
    integer :: n2
    !f2py intent(hide), depend(clip_by_value) :: n2 = shape(clip_by_value,0)
    integer :: n3
    !f2py intent(hide), depend(clip_by_value) :: n3 = shape(clip_by_value,1)
    integer :: n4
    !f2py intent(hide), depend(hornnet_constants) :: n4 = shape(hornnet_constants,0)
    integer :: n5
    !f2py intent(hide), depend(hornnet_constants) :: n5 = shape(hornnet_constants,1)
    integer :: n6
    !f2py intent(hide), depend(sepflux_out) :: n6 = shape(sepflux_out,0)
    integer :: n7
    !f2py intent(hide), depend(sepflux_out) :: n7 = shape(sepflux_out,1)
    integer :: n8
    !f2py intent(hide), depend(f) :: n8 = shape(f,0)
    integer :: n9
    !f2py intent(hide), depend(f) :: n9 = shape(f,1)
    integer :: n10
    !f2py intent(hide), depend(g) :: n10 = shape(g,0)
    integer :: n11
    !f2py intent(hide), depend(g) :: n11 = shape(g,1)
    integer :: n12
    !f2py intent(hide), depend(h) :: n12 = shape(h,0)
    integer :: n13
    !f2py intent(hide), depend(h) :: n13 = shape(h,1)
    integer :: n14
    !f2py intent(hide), depend(drelu_dhornnet_constants) :: n14 = shape(drelu_dhornnet_constants,0)
    integer :: n15
    !f2py intent(hide), depend(drelu_dhornnet_constants) :: n15 = shape(drelu_dhornnet_constants,1)
    integer :: n16
    !f2py intent(hide), depend(drelu_dhornnet_constants) :: n16 = shape(drelu_dhornnet_constants,2)
    integer :: n17
    !f2py intent(hide), depend(drelu_dinput) :: n17 = shape(drelu_dinput,0)
    integer :: n18
    !f2py intent(hide), depend(drelu_dinput) :: n18 = shape(drelu_dinput,1)
    integer :: n19
    !f2py intent(hide), depend(drelu_dinput) :: n19 = shape(drelu_dinput,2)
    integer :: n20
    !f2py intent(hide), depend(dclip_by_value_dhornnet_constants) :: n20 = shape(dclip_by_value_dhornnet_constants,0)
    integer :: n21
    !f2py intent(hide), depend(dclip_by_value_dhornnet_constants) :: n21 = shape(dclip_by_value_dhornnet_constants,1)
    integer :: n22
    !f2py intent(hide), depend(dclip_by_value_dhornnet_constants) :: n22 = shape(dclip_by_value_dhornnet_constants,2)
    integer :: n23
    !f2py intent(hide), depend(dclip_by_value_dinput) :: n23 = shape(dclip_by_value_dinput,0)
    integer :: n24
    !f2py intent(hide), depend(dclip_by_value_dinput) :: n24 = shape(dclip_by_value_dinput,1)
    integer :: n25
    !f2py intent(hide), depend(dclip_by_value_dinput) :: n25 = shape(dclip_by_value_dinput,2)
    integer :: n26
    !f2py intent(hide), depend(df_dhornnet_constants) :: n26 = shape(df_dhornnet_constants,0)
    integer :: n27
    !f2py intent(hide), depend(df_dhornnet_constants) :: n27 = shape(df_dhornnet_constants,1)
    integer :: n28
    !f2py intent(hide), depend(df_dhornnet_constants) :: n28 = shape(df_dhornnet_constants,2)
    integer :: n29
    !f2py intent(hide), depend(df_dinput) :: n29 = shape(df_dinput,0)
    integer :: n30
    !f2py intent(hide), depend(df_dinput) :: n30 = shape(df_dinput,1)
    integer :: n31
    !f2py intent(hide), depend(df_dinput) :: n31 = shape(df_dinput,2)
    integer :: n32
    !f2py intent(hide), depend(dg_dhornnet_constants) :: n32 = shape(dg_dhornnet_constants,0)
    integer :: n33
    !f2py intent(hide), depend(dg_dhornnet_constants) :: n33 = shape(dg_dhornnet_constants,1)
    integer :: n34
    !f2py intent(hide), depend(dg_dhornnet_constants) :: n34 = shape(dg_dhornnet_constants,2)
    integer :: n35
    !f2py intent(hide), depend(dg_dinput) :: n35 = shape(dg_dinput,0)
    integer :: n36
    !f2py intent(hide), depend(dg_dinput) :: n36 = shape(dg_dinput,1)
    integer :: n37
    !f2py intent(hide), depend(dg_dinput) :: n37 = shape(dg_dinput,2)
    integer :: n38
    !f2py intent(hide), depend(dh_dhornnet_constants) :: n38 = shape(dh_dhornnet_constants,0)
    integer :: n39
    !f2py intent(hide), depend(dh_dhornnet_constants) :: n39 = shape(dh_dhornnet_constants,1)
    integer :: n40
    !f2py intent(hide), depend(dh_dhornnet_constants) :: n40 = shape(dh_dhornnet_constants,2)
    call hornnet_multiplier(heaviside_function_times=heaviside_function_times, clip_by_value=clip_by_value, &
        hornnet_constants=hornnet_constants, sepflux_out=sepflux_out, outp=outp, pow_idx=pow_idx, block_idx=block_idx, &
        slope_idx=slope_idx, f=f, g=g, h=h, drelu_dhornnet_constants=drelu_dhornnet_constants, drelu_dinput=drelu_dinput, &
        dclip_by_value_dhornnet_constants=dclip_by_value_dhornnet_constants, dclip_by_value_dinput=dclip_by_value_dinput, &
        df_dhornnet_constants=df_dhornnet_constants, df_dinput=df_dinput, dg_dhornnet_constants=dg_dhornnet_constants, &
        dg_dinput=dg_dinput, dh_dhornnet_constants=dh_dhornnet_constants)
end subroutine f90wrap_hornnet_multiplier

subroutine f90wrap_evaluate_hornnet_constants(input, blocks, qlknn_out, verbosityin, optsin, qlknn_normsin, &
    dqlknn_out_dinput, n0, n1, n2, n3, n4, n5, n6)
    use qlknn_types, only: block_collection, qlknn_options, qlknn_normpars
    use qlknn_evaluate_nets, only: evaluate_hornnet_constants
    implicit none
    
    type block_collection_ptr_type
        type(block_collection), pointer :: p => NULL()
    end type block_collection_ptr_type
    type qlknn_options_ptr_type
        type(qlknn_options), pointer :: p => NULL()
    end type qlknn_options_ptr_type
    type qlknn_normpars_ptr_type
        type(qlknn_normpars), pointer :: p => NULL()
    end type qlknn_normpars_ptr_type
    real(8), intent(in), dimension(n0,n1) :: input
    type(block_collection_ptr_type) :: blocks_ptr
    integer, intent(in), dimension(2) :: blocks
    real(8), intent(inout), dimension(n2,n3) :: qlknn_out
    integer(8), optional, intent(in) :: verbosityin
    type(qlknn_options_ptr_type) :: optsin_ptr
    integer, optional, intent(in), dimension(2) :: optsin
    type(qlknn_normpars_ptr_type) :: qlknn_normsin_ptr
    integer, optional, intent(in), dimension(2) :: qlknn_normsin
    real(8), optional, intent(inout), dimension(n4,n5,n6) :: dqlknn_out_dinput
    integer :: n0
    !f2py intent(hide), depend(input) :: n0 = shape(input,0)
    integer :: n1
    !f2py intent(hide), depend(input) :: n1 = shape(input,1)
    integer :: n2
    !f2py intent(hide), depend(qlknn_out) :: n2 = shape(qlknn_out,0)
    integer :: n3
    !f2py intent(hide), depend(qlknn_out) :: n3 = shape(qlknn_out,1)
    integer :: n4
    !f2py intent(hide), depend(dqlknn_out_dinput) :: n4 = shape(dqlknn_out_dinput,0)
    integer :: n5
    !f2py intent(hide), depend(dqlknn_out_dinput) :: n5 = shape(dqlknn_out_dinput,1)
    integer :: n6
    !f2py intent(hide), depend(dqlknn_out_dinput) :: n6 = shape(dqlknn_out_dinput,2)
    blocks_ptr = transfer(blocks, blocks_ptr)
    if (present(optsin)) then
        optsin_ptr = transfer(optsin, optsin_ptr)
    else
        optsin_ptr%p => null()
    end if
    if (present(qlknn_normsin)) then
        qlknn_normsin_ptr = transfer(qlknn_normsin, qlknn_normsin_ptr)
    else
        qlknn_normsin_ptr%p => null()
    end if
    call evaluate_hornnet_constants(input=input, blocks=blocks_ptr%p, qlknn_out=qlknn_out, verbosityin=verbosityin, &
        optsin=optsin_ptr%p, qlknn_normsin=qlknn_normsin_ptr%p, dqlknn_out_dinput=dqlknn_out_dinput)
end subroutine f90wrap_evaluate_hornnet_constants

subroutine f90wrap_evaluate_multinet(net_input, nets, net_evaluate, net_result, verbosityin, dnet_out_dnet_in, n0, n1, &
    n2, n3, n4, n5, n6, n7)
    use qlknn_types, only: net_collection
    use qlknn_evaluate_nets, only: evaluate_multinet
    implicit none
    
    type net_collection_ptr_type
        type(net_collection), pointer :: p => NULL()
    end type net_collection_ptr_type
    real(8), intent(in), dimension(n0,n1) :: net_input
    type(net_collection_ptr_type) :: nets_ptr
    integer, intent(in), dimension(2) :: nets
    logical, intent(in), dimension(n2) :: net_evaluate
    real(8), intent(inout), dimension(n3,n4) :: net_result
    integer(8), intent(in), optional :: verbosityin
    real(8), optional, intent(inout), dimension(n5,n6,n7) :: dnet_out_dnet_in
    integer :: n0
    !f2py intent(hide), depend(net_input) :: n0 = shape(net_input,0)
    integer :: n1
    !f2py intent(hide), depend(net_input) :: n1 = shape(net_input,1)
    integer :: n2
    !f2py intent(hide), depend(net_evaluate) :: n2 = shape(net_evaluate,0)
    integer :: n3
    !f2py intent(hide), depend(net_result) :: n3 = shape(net_result,0)
    integer :: n4
    !f2py intent(hide), depend(net_result) :: n4 = shape(net_result,1)
    integer :: n5
    !f2py intent(hide), depend(dnet_out_dnet_in) :: n5 = shape(dnet_out_dnet_in,0)
    integer :: n6
    !f2py intent(hide), depend(dnet_out_dnet_in) :: n6 = shape(dnet_out_dnet_in,1)
    integer :: n7
    !f2py intent(hide), depend(dnet_out_dnet_in) :: n7 = shape(dnet_out_dnet_in,2)
    nets_ptr = transfer(nets, nets_ptr)
    call evaluate_multinet(net_input=net_input, nets=nets_ptr%p, net_evaluate=net_evaluate, net_result=net_result, &
        verbosityin=verbosityin, dnet_out_dnet_in=dnet_out_dnet_in)
end subroutine f90wrap_evaluate_multinet

! End of module qlknn_evaluate_nets defined in file /builds/qualikiz-group/QLKNN-fortran/src/core/qlknn_evaluate_nets.f90

