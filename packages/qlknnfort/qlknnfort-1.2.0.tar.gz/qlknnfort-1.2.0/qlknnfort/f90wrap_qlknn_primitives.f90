! Module qlknn_primitives defined in file /builds/qualikiz-group/QLKNN-fortran/src/core/qlknn_primitives.f90

subroutine f90wrap_evaluate_network(input, net, output_1d, verbosityin, dnet_out1d_dinput, n0, n1, n2, n3, n4)
    use qlknn_types, only: networktype
    use qlknn_primitives, only: evaluate_network
    implicit none
    
    type networktype_ptr_type
        type(networktype), pointer :: p => NULL()
    end type networktype_ptr_type
    real(8), intent(in), dimension(n0,n1) :: input
    type(networktype_ptr_type) :: net_ptr
    integer, intent(in), dimension(2) :: net
    real(8), intent(inout), dimension(n2) :: output_1d
    integer(8), optional, intent(in) :: verbosityin
    real(8), optional, intent(inout), dimension(n3,n4) :: dnet_out1d_dinput
    integer :: n0
    !f2py intent(hide), depend(input) :: n0 = shape(input,0)
    integer :: n1
    !f2py intent(hide), depend(input) :: n1 = shape(input,1)
    integer :: n2
    !f2py intent(hide), depend(output_1d) :: n2 = shape(output_1d,0)
    integer :: n3
    !f2py intent(hide), depend(dnet_out1d_dinput) :: n3 = shape(dnet_out1d_dinput,0)
    integer :: n4
    !f2py intent(hide), depend(dnet_out1d_dinput) :: n4 = shape(dnet_out1d_dinput,1)
    net_ptr = transfer(net, net_ptr)
    call evaluate_network(input=input, net=net_ptr%p, output_1d=output_1d, verbosityin=verbosityin, &
        dnet_out1d_dinput=dnet_out1d_dinput)
end subroutine f90wrap_evaluate_network

subroutine f90wrap_evaluate_layer(input, weights, biases, activation_func, output, verbosityin, doutput_dinput, n0, n1, &
    n2, n3, n4, n5, n6, n7, n8, n9)
    use qlknn_primitives, only: evaluate_layer
    implicit none
    
    real(8), intent(in), dimension(n0,n1) :: input
    real(8), intent(in), dimension(n2,n3) :: weights
    real(8), intent(in), dimension(n4) :: biases
    character(4), intent(in) :: activation_func
    real(8), intent(inout), dimension(n5,n6) :: output
    integer(8), optional, intent(in) :: verbosityin
    real(8), optional, intent(inout), dimension(n7,n8,n9) :: doutput_dinput
    integer :: n0
    !f2py intent(hide), depend(input) :: n0 = shape(input,0)
    integer :: n1
    !f2py intent(hide), depend(input) :: n1 = shape(input,1)
    integer :: n2
    !f2py intent(hide), depend(weights) :: n2 = shape(weights,0)
    integer :: n3
    !f2py intent(hide), depend(weights) :: n3 = shape(weights,1)
    integer :: n4
    !f2py intent(hide), depend(biases) :: n4 = shape(biases,0)
    integer :: n5
    !f2py intent(hide), depend(output) :: n5 = shape(output,0)
    integer :: n6
    !f2py intent(hide), depend(output) :: n6 = shape(output,1)
    integer :: n7
    !f2py intent(hide), depend(doutput_dinput) :: n7 = shape(doutput_dinput,0)
    integer :: n8
    !f2py intent(hide), depend(doutput_dinput) :: n8 = shape(doutput_dinput,1)
    integer :: n9
    !f2py intent(hide), depend(doutput_dinput) :: n9 = shape(doutput_dinput,2)
    call evaluate_layer(input=input, weights=weights, biases=biases, activation_func=activation_func, output=output, &
        verbosityin=verbosityin, doutput_dinput=doutput_dinput)
end subroutine f90wrap_evaluate_layer

subroutine f90wrap_impose_output_constraints(output, opts, verbosity, dnet_out_dinput, output_eb, n0, n1, n2, n3, n4, &
    n5, n6)
    use qlknn_types, only: qlknn_options
    use qlknn_primitives, only: impose_output_constraints
    implicit none
    
    type qlknn_options_ptr_type
        type(qlknn_options), pointer :: p => NULL()
    end type qlknn_options_ptr_type
    real(8), intent(inout), dimension(n0,n1) :: output
    type(qlknn_options_ptr_type) :: opts_ptr
    integer, intent(in), dimension(2) :: opts
    integer(8), intent(in) :: verbosity
    real(8), optional, intent(inout), dimension(n2,n3,n4) :: dnet_out_dinput
    real(8), optional, intent(inout), dimension(n5,n6) :: output_eb
    integer :: n0
    !f2py intent(hide), depend(output) :: n0 = shape(output,0)
    integer :: n1
    !f2py intent(hide), depend(output) :: n1 = shape(output,1)
    integer :: n2
    !f2py intent(hide), depend(dnet_out_dinput) :: n2 = shape(dnet_out_dinput,0)
    integer :: n3
    !f2py intent(hide), depend(dnet_out_dinput) :: n3 = shape(dnet_out_dinput,1)
    integer :: n4
    !f2py intent(hide), depend(dnet_out_dinput) :: n4 = shape(dnet_out_dinput,2)
    integer :: n5
    !f2py intent(hide), depend(output_eb) :: n5 = shape(output_eb,0)
    integer :: n6
    !f2py intent(hide), depend(output_eb) :: n6 = shape(output_eb,1)
    opts_ptr = transfer(opts, opts_ptr)
    call impose_output_constraints(output=output, opts=opts_ptr%p, verbosity=verbosity, dnet_out_dinput=dnet_out_dinput, &
        output_eb=output_eb)
end subroutine f90wrap_impose_output_constraints

subroutine f90wrap_apply_stability_clipping(leading_map, net_result, verbosity, n0, n1, n2, n3)
    use qlknn_primitives, only: apply_stability_clipping
    implicit none
    
    integer(8), intent(in), dimension(n0,n1) :: leading_map
    real(8), intent(inout), dimension(n2,n3) :: net_result
    integer(8), intent(in) :: verbosity
    integer :: n0
    !f2py intent(hide), depend(leading_map) :: n0 = shape(leading_map,0)
    integer :: n1
    !f2py intent(hide), depend(leading_map) :: n1 = shape(leading_map,1)
    integer :: n2
    !f2py intent(hide), depend(net_result) :: n2 = shape(net_result,0)
    integer :: n3
    !f2py intent(hide), depend(net_result) :: n3 = shape(net_result,1)
    call apply_stability_clipping(leading_map=leading_map, net_result=net_result, verbosity=verbosity)
end subroutine f90wrap_apply_stability_clipping

subroutine f90wrap_impose_leading_flux_constraints(leading_map, net_result, verbosity, dnet_out_dnet_in, net_eb, n0, n1, &
    n2, n3, n4, n5, n6, n7, n8)
    use qlknn_primitives, only: impose_leading_flux_constraints
    implicit none
    
    integer(8), intent(in), dimension(n0,n1) :: leading_map
    real(8), intent(inout), dimension(n2,n3) :: net_result
    integer(8), intent(in) :: verbosity
    real(8), optional, intent(inout), dimension(n4,n5,n6) :: dnet_out_dnet_in
    real(8), optional, intent(inout), dimension(n7,n8) :: net_eb
    integer :: n0
    !f2py intent(hide), depend(leading_map) :: n0 = shape(leading_map,0)
    integer :: n1
    !f2py intent(hide), depend(leading_map) :: n1 = shape(leading_map,1)
    integer :: n2
    !f2py intent(hide), depend(net_result) :: n2 = shape(net_result,0)
    integer :: n3
    !f2py intent(hide), depend(net_result) :: n3 = shape(net_result,1)
    integer :: n4
    !f2py intent(hide), depend(dnet_out_dnet_in) :: n4 = shape(dnet_out_dnet_in,0)
    integer :: n5
    !f2py intent(hide), depend(dnet_out_dnet_in) :: n5 = shape(dnet_out_dnet_in,1)
    integer :: n6
    !f2py intent(hide), depend(dnet_out_dnet_in) :: n6 = shape(dnet_out_dnet_in,2)
    integer :: n7
    !f2py intent(hide), depend(net_eb) :: n7 = shape(net_eb,0)
    integer :: n8
    !f2py intent(hide), depend(net_eb) :: n8 = shape(net_eb,1)
    call impose_leading_flux_constraints(leading_map=leading_map, net_result=net_result, verbosity=verbosity, &
        dnet_out_dnet_in=dnet_out_dnet_in, net_eb=net_eb)
end subroutine f90wrap_impose_leading_flux_constraints

subroutine f90wrap_multiply_div_networks(leading_map, net_result, verbosity, dqlknn_out_dinput, net_eb, n0, n1, n2, n3, &
    n4, n5, n6, n7, n8)
    use qlknn_primitives, only: multiply_div_networks
    implicit none
    
    integer(8), intent(in), dimension(n0,n1) :: leading_map
    real(8), intent(inout), dimension(n2,n3) :: net_result
    integer(8), intent(in) :: verbosity
    real(8), optional, intent(inout), dimension(n4,n5,n6) :: dqlknn_out_dinput
    real(8), optional, intent(inout), dimension(n7,n8) :: net_eb
    integer :: n0
    !f2py intent(hide), depend(leading_map) :: n0 = shape(leading_map,0)
    integer :: n1
    !f2py intent(hide), depend(leading_map) :: n1 = shape(leading_map,1)
    integer :: n2
    !f2py intent(hide), depend(net_result) :: n2 = shape(net_result,0)
    integer :: n3
    !f2py intent(hide), depend(net_result) :: n3 = shape(net_result,1)
    integer :: n4
    !f2py intent(hide), depend(dqlknn_out_dinput) :: n4 = shape(dqlknn_out_dinput,0)
    integer :: n5
    !f2py intent(hide), depend(dqlknn_out_dinput) :: n5 = shape(dqlknn_out_dinput,1)
    integer :: n6
    !f2py intent(hide), depend(dqlknn_out_dinput) :: n6 = shape(dqlknn_out_dinput,2)
    integer :: n7
    !f2py intent(hide), depend(net_eb) :: n7 = shape(net_eb,0)
    integer :: n8
    !f2py intent(hide), depend(net_eb) :: n8 = shape(net_eb,1)
    call multiply_div_networks(leading_map=leading_map, net_result=net_result, verbosity=verbosity, &
        dqlknn_out_dinput=dqlknn_out_dinput, net_eb=net_eb)
end subroutine f90wrap_multiply_div_networks

subroutine f90wrap_merge_modes(merge_map, net_result, merged_net_result, verbosity, dqlknn_out_dinput, &
    dqlknn_out_merged_dinput, net_eb, merged_net_eb, n0, n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11, n12, n13, n14, &
    n15)
    use qlknn_primitives, only: merge_modes
    implicit none
    
    integer(8), intent(in), dimension(n0,n1) :: merge_map
    real(8), intent(in), dimension(n2,n3) :: net_result
    real(8), intent(inout), dimension(n4,n5) :: merged_net_result
    integer(8), intent(in) :: verbosity
    real(8), optional, intent(in), dimension(n6,n7,n8) :: dqlknn_out_dinput
    real(8), optional, intent(inout), dimension(n9,n10,n11) :: dqlknn_out_merged_dinput
    real(8), optional, intent(in), dimension(n12,n13) :: net_eb
    real(8), optional, intent(inout), dimension(n14,n15) :: merged_net_eb
    integer :: n0
    !f2py intent(hide), depend(merge_map) :: n0 = shape(merge_map,0)
    integer :: n1
    !f2py intent(hide), depend(merge_map) :: n1 = shape(merge_map,1)
    integer :: n2
    !f2py intent(hide), depend(net_result) :: n2 = shape(net_result,0)
    integer :: n3
    !f2py intent(hide), depend(net_result) :: n3 = shape(net_result,1)
    integer :: n4
    !f2py intent(hide), depend(merged_net_result) :: n4 = shape(merged_net_result,0)
    integer :: n5
    !f2py intent(hide), depend(merged_net_result) :: n5 = shape(merged_net_result,1)
    integer :: n6
    !f2py intent(hide), depend(dqlknn_out_dinput) :: n6 = shape(dqlknn_out_dinput,0)
    integer :: n7
    !f2py intent(hide), depend(dqlknn_out_dinput) :: n7 = shape(dqlknn_out_dinput,1)
    integer :: n8
    !f2py intent(hide), depend(dqlknn_out_dinput) :: n8 = shape(dqlknn_out_dinput,2)
    integer :: n9
    !f2py intent(hide), depend(dqlknn_out_merged_dinput) :: n9 = shape(dqlknn_out_merged_dinput,0)
    integer :: n10
    !f2py intent(hide), depend(dqlknn_out_merged_dinput) :: n10 = shape(dqlknn_out_merged_dinput,1)
    integer :: n11
    !f2py intent(hide), depend(dqlknn_out_merged_dinput) :: n11 = shape(dqlknn_out_merged_dinput,2)
    integer :: n12
    !f2py intent(hide), depend(net_eb) :: n12 = shape(net_eb,0)
    integer :: n13
    !f2py intent(hide), depend(net_eb) :: n13 = shape(net_eb,1)
    integer :: n14
    !f2py intent(hide), depend(merged_net_eb) :: n14 = shape(merged_net_eb,0)
    integer :: n15
    !f2py intent(hide), depend(merged_net_eb) :: n15 = shape(merged_net_eb,1)
    call merge_modes(merge_map=merge_map, net_result=net_result, merged_net_result=merged_net_result, verbosity=verbosity, &
        dqlknn_out_dinput=dqlknn_out_dinput, dqlknn_out_merged_dinput=dqlknn_out_merged_dinput, net_eb=net_eb, &
        merged_net_eb=merged_net_eb)
end subroutine f90wrap_merge_modes

subroutine f90wrap_merge_committee(net_result, n_members, merged_net_result, merged_net_eb, verbosity, &
    dqlknn_out_dinput, dqlknn_out_merged_dinput, n0, n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11)
    use qlknn_primitives, only: merge_committee
    implicit none
    
    real(8), intent(in), dimension(n0,n1) :: net_result
    integer(8), intent(in) :: n_members
    real(8), intent(inout), dimension(n2,n3) :: merged_net_result
    real(8), intent(inout), dimension(n4,n5) :: merged_net_eb
    integer(8), intent(in) :: verbosity
    real(8), optional, intent(in), dimension(n6,n7,n8) :: dqlknn_out_dinput
    real(8), optional, intent(inout), dimension(n9,n10,n11) :: dqlknn_out_merged_dinput
    integer :: n0
    !f2py intent(hide), depend(net_result) :: n0 = shape(net_result,0)
    integer :: n1
    !f2py intent(hide), depend(net_result) :: n1 = shape(net_result,1)
    integer :: n2
    !f2py intent(hide), depend(merged_net_result) :: n2 = shape(merged_net_result,0)
    integer :: n3
    !f2py intent(hide), depend(merged_net_result) :: n3 = shape(merged_net_result,1)
    integer :: n4
    !f2py intent(hide), depend(merged_net_eb) :: n4 = shape(merged_net_eb,0)
    integer :: n5
    !f2py intent(hide), depend(merged_net_eb) :: n5 = shape(merged_net_eb,1)
    integer :: n6
    !f2py intent(hide), depend(dqlknn_out_dinput) :: n6 = shape(dqlknn_out_dinput,0)
    integer :: n7
    !f2py intent(hide), depend(dqlknn_out_dinput) :: n7 = shape(dqlknn_out_dinput,1)
    integer :: n8
    !f2py intent(hide), depend(dqlknn_out_dinput) :: n8 = shape(dqlknn_out_dinput,2)
    integer :: n9
    !f2py intent(hide), depend(dqlknn_out_merged_dinput) :: n9 = shape(dqlknn_out_merged_dinput,0)
    integer :: n10
    !f2py intent(hide), depend(dqlknn_out_merged_dinput) :: n10 = shape(dqlknn_out_merged_dinput,1)
    integer :: n11
    !f2py intent(hide), depend(dqlknn_out_merged_dinput) :: n11 = shape(dqlknn_out_merged_dinput,2)
    call merge_committee(net_result=net_result, n_members=n_members, merged_net_result=merged_net_result, &
        merged_net_eb=merged_net_eb, verbosity=verbosity, dqlknn_out_dinput=dqlknn_out_dinput, &
        dqlknn_out_merged_dinput=dqlknn_out_merged_dinput)
end subroutine f90wrap_merge_committee

subroutine f90wrap_matr_mult_elemwise(n, a, b, y, n0, n1, n2, n3, n4, n5)
    use qlknn_primitives, only: matr_mult_elemwise
    implicit none
    
    integer(8), intent(in) :: n
    real(8), intent(in), dimension(n0,n1) :: a
    real(8), intent(in), dimension(n2,n3) :: b
    real(8), intent(inout), dimension(n4,n5) :: y
    integer :: n0
    !f2py intent(hide), depend(a) :: n0 = shape(a,0)
    integer :: n1
    !f2py intent(hide), depend(a) :: n1 = shape(a,1)
    integer :: n2
    !f2py intent(hide), depend(b) :: n2 = shape(b,0)
    integer :: n3
    !f2py intent(hide), depend(b) :: n3 = shape(b,1)
    integer :: n4
    !f2py intent(hide), depend(y) :: n4 = shape(y,0)
    integer :: n5
    !f2py intent(hide), depend(y) :: n5 = shape(y,1)
    call matr_mult_elemwise(n=n, a=a, b=b, y=y)
end subroutine f90wrap_matr_mult_elemwise

subroutine f90wrap_matr_vec_mult_elemwise(n, a, b, y, n0, n1, n2, n3, n4)
    use qlknn_primitives, only: matr_vec_mult_elemwise
    implicit none
    
    integer(8), intent(in) :: n
    real(8), intent(in), dimension(n0,n1) :: a
    real(8), intent(in), dimension(n2) :: b
    real(8), intent(inout), dimension(n3,n4) :: y
    integer :: n0
    !f2py intent(hide), depend(a) :: n0 = shape(a,0)
    integer :: n1
    !f2py intent(hide), depend(a) :: n1 = shape(a,1)
    integer :: n2
    !f2py intent(hide), depend(b) :: n2 = shape(b,0)
    integer :: n3
    !f2py intent(hide), depend(y) :: n3 = shape(y,0)
    integer :: n4
    !f2py intent(hide), depend(y) :: n4 = shape(y,1)
    call matr_vec_mult_elemwise(n=n, a=a, b=b, y=y)
end subroutine f90wrap_matr_vec_mult_elemwise

subroutine f90wrap_vdmul(n, a, b, y, n0, n1, n2)
    use qlknn_primitives, only: vdmul
    implicit none
    
    integer(8), intent(in) :: n
    real(8), intent(in), dimension(n0) :: a
    real(8), intent(in), dimension(n1) :: b
    real(8), intent(inout), dimension(n2) :: y
    integer :: n0
    !f2py intent(hide), depend(a) :: n0 = shape(a,0)
    integer :: n1
    !f2py intent(hide), depend(b) :: n1 = shape(b,0)
    integer :: n2
    !f2py intent(hide), depend(y) :: n2 = shape(y,0)
    call vdmul(n=n, a=a, b=b, y=y)
end subroutine f90wrap_vdmul

subroutine f90wrap_dgemm(transa, transb, m, n, k, alpha, a, lda, b, ldb, beta, c, ldc, n0, n1, n2, n3, n4, n5)
    use qlknn_primitives, only: dgemm
    implicit none
    
    character(1), intent(in) :: transa
    character(1), intent(in) :: transb
    integer(8), intent(in) :: m
    integer(8), intent(in) :: n
    integer(8), intent(in) :: k
    real(8), intent(in) :: alpha
    real(8), intent(in), dimension(n0,n1) :: a
    integer(8), intent(in) :: lda
    real(8), intent(in), dimension(n2,n3) :: b
    integer(8), intent(in) :: ldb
    real(8), intent(in) :: beta
    real(8), intent(inout), dimension(n4,n5) :: c
    integer(8), intent(in) :: ldc
    integer :: n0
    !f2py intent(hide), depend(a) :: n0 = shape(a,0)
    integer :: n1
    !f2py intent(hide), depend(a) :: n1 = shape(a,1)
    integer :: n2
    !f2py intent(hide), depend(b) :: n2 = shape(b,0)
    integer :: n3
    !f2py intent(hide), depend(b) :: n3 = shape(b,1)
    integer :: n4
    !f2py intent(hide), depend(c) :: n4 = shape(c,0)
    integer :: n5
    !f2py intent(hide), depend(c) :: n5 = shape(c,1)
    call dgemm(transa=transa, transb=transb, m=m, n=n, k=k, alpha=alpha, a=a, lda=lda, b=b, ldb=ldb, beta=beta, c=c, &
        ldc=ldc)
end subroutine f90wrap_dgemm

subroutine f90wrap_vdtanh(n, a, y, n0, n1, n2, n3)
    use qlknn_primitives, only: vdtanh
    implicit none
    
    integer(8), intent(in) :: n
    real(8), intent(in), dimension(n0,n1) :: a
    real(8), intent(inout), dimension(n2,n3) :: y
    integer :: n0
    !f2py intent(hide), depend(a) :: n0 = shape(a,0)
    integer :: n1
    !f2py intent(hide), depend(a) :: n1 = shape(a,1)
    integer :: n2
    !f2py intent(hide), depend(y) :: n2 = shape(y,0)
    integer :: n3
    !f2py intent(hide), depend(y) :: n3 = shape(y,1)
    call vdtanh(n=n, a=a, y=y)
end subroutine f90wrap_vdtanh

subroutine f90wrap_relu(n, a, y, n0, n1)
    use qlknn_primitives, only: relu
    implicit none
    
    integer(8), intent(in) :: n
    real(8), intent(in), dimension(n0) :: a
    real(8), intent(inout), dimension(n1) :: y
    integer :: n0
    !f2py intent(hide), depend(a) :: n0 = shape(a,0)
    integer :: n1
    !f2py intent(hide), depend(y) :: n1 = shape(y,0)
    call relu(n=n, a=a, y=y)
end subroutine f90wrap_relu

subroutine f90wrap_calc_length_lli(start, end, step, length)
    use qlknn_primitives, only: calc_length_lli
    implicit none
    
    integer(8), intent(in) :: start
    integer(8), intent(in) :: end
    integer(8), intent(in) :: step
    integer(8), intent(out) :: length
    call calc_length_lli(start=start, end=end, step=step, length=length)
end subroutine f90wrap_calc_length_lli

subroutine f90wrap_calc_length_li(start, end, step, length)
    use qlknn_primitives, only: calc_length_li
    implicit none
    
    integer(4), intent(in) :: start
    integer(4), intent(in) :: end
    integer(4), intent(in) :: step
    integer(4), intent(out) :: length
    call calc_length_li(start=start, end=end, step=step, length=length)
end subroutine f90wrap_calc_length_li

subroutine f90wrap_calc_length_mixed1(start, end, step, length)
    use qlknn_primitives, only: calc_length_mixed1
    implicit none
    
    integer(4), intent(in) :: start
    integer(8), intent(in) :: end
    integer(4), intent(in) :: step
    integer(4), intent(out) :: length
    call calc_length_mixed1(start=start, end=end, step=step, length=length)
end subroutine f90wrap_calc_length_mixed1

subroutine f90wrap_calc_length_mixed2(start, end, step, length)
    use qlknn_primitives, only: calc_length_mixed2
    implicit none
    
    integer(4), intent(in) :: start
    integer(8), intent(in) :: end
    integer(8), intent(in) :: step
    integer(4), intent(out) :: length
    call calc_length_mixed2(start=start, end=end, step=step, length=length)
end subroutine f90wrap_calc_length_mixed2

subroutine f90wrap_double_1d_0d_is_not_close(arr1, arr2, is_not_close, boundin, n0, n1)
    use qlknn_primitives, only: double_1d_0d_is_not_close
    implicit none
    
    real(8), intent(in), dimension(n0) :: arr1
    real(8), intent(in) :: arr2
    logical, intent(inout), dimension(n1) :: is_not_close
    real(8), intent(in), optional :: boundin
    integer :: n0
    !f2py intent(hide), depend(arr1) :: n0 = shape(arr1,0)
    integer :: n1
    !f2py intent(hide), depend(is_not_close) :: n1 = shape(is_not_close,0)
    call double_1d_0d_is_not_close(arr1=arr1, arr2=arr2, is_not_close=is_not_close, boundin=boundin)
end subroutine f90wrap_double_1d_0d_is_not_close

subroutine f90wrap_double_1d_1d_is_not_close(arr1, arr2, is_not_close, boundin, n0, n1, n2)
    use qlknn_primitives, only: double_1d_1d_is_not_close
    implicit none
    
    real(8), intent(in), dimension(n0) :: arr1
    real(8), intent(in), dimension(n1) :: arr2
    logical, intent(inout), dimension(n2) :: is_not_close
    real(8), intent(in), optional :: boundin
    integer :: n0
    !f2py intent(hide), depend(arr1) :: n0 = shape(arr1,0)
    integer :: n1
    !f2py intent(hide), depend(arr2) :: n1 = shape(arr2,0)
    integer :: n2
    !f2py intent(hide), depend(is_not_close) :: n2 = shape(is_not_close,0)
    call double_1d_1d_is_not_close(arr1=arr1, arr2=arr2, is_not_close=is_not_close, boundin=boundin)
end subroutine f90wrap_double_1d_1d_is_not_close

subroutine f90wrap_double_2d_2d_is_not_close(arr1, arr2, is_not_close, boundin, n0, n1, n2, n3, n4, n5)
    use qlknn_primitives, only: double_2d_2d_is_not_close
    implicit none
    
    real(8), intent(in), dimension(n0,n1) :: arr1
    real(8), intent(in), dimension(n2,n3) :: arr2
    logical, intent(inout), dimension(n4,n5) :: is_not_close
    real(8), intent(in), optional :: boundin
    integer :: n0
    !f2py intent(hide), depend(arr1) :: n0 = shape(arr1,0)
    integer :: n1
    !f2py intent(hide), depend(arr1) :: n1 = shape(arr1,1)
    integer :: n2
    !f2py intent(hide), depend(arr2) :: n2 = shape(arr2,0)
    integer :: n3
    !f2py intent(hide), depend(arr2) :: n3 = shape(arr2,1)
    integer :: n4
    !f2py intent(hide), depend(is_not_close) :: n4 = shape(is_not_close,0)
    integer :: n5
    !f2py intent(hide), depend(is_not_close) :: n5 = shape(is_not_close,1)
    call double_2d_2d_is_not_close(arr1=arr1, arr2=arr2, is_not_close=is_not_close, boundin=boundin)
end subroutine f90wrap_double_2d_2d_is_not_close

! End of module qlknn_primitives defined in file /builds/qualikiz-group/QLKNN-fortran/src/core/qlknn_primitives.f90

