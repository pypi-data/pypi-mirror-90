! Module qlknn_types defined in file /builds/qualikiz-group/QLKNN-fortran/src/core/qlknn_types.f90

subroutine f90wrap_ragged_weights_array__array__weight_layer(this, nd, dtype, dshape, dloc)
    use qlknn_types, only: ragged_weights_array
    implicit none
    type ragged_weights_array_ptr_type
        type(ragged_weights_array), pointer :: p => NULL()
    end type ragged_weights_array_ptr_type
    integer, intent(in) :: this(2)
    type(ragged_weights_array_ptr_type) :: this_ptr
    integer, intent(out) :: nd
    integer, intent(out) :: dtype
    integer, dimension(10), intent(out) :: dshape
    integer*8, intent(out) :: dloc
    
    nd = 2
    dtype = 12
    this_ptr = transfer(this, this_ptr)
    if (allocated(this_ptr%p%weight_layer)) then
        dshape(1:2) = shape(this_ptr%p%weight_layer)
        dloc = loc(this_ptr%p%weight_layer)
    else
        dloc = 0
    end if
end subroutine f90wrap_ragged_weights_array__array__weight_layer

subroutine f90wrap_ragged_weights_array_initialise(this)
    use qlknn_types, only: ragged_weights_array
    implicit none
    
    type ragged_weights_array_ptr_type
        type(ragged_weights_array), pointer :: p => NULL()
    end type ragged_weights_array_ptr_type
    type(ragged_weights_array_ptr_type) :: this_ptr
    integer, intent(out), dimension(2) :: this
    allocate(this_ptr%p)
    this = transfer(this_ptr, this)
end subroutine f90wrap_ragged_weights_array_initialise

subroutine f90wrap_ragged_weights_array_finalise(this)
    use qlknn_types, only: ragged_weights_array
    implicit none
    
    type ragged_weights_array_ptr_type
        type(ragged_weights_array), pointer :: p => NULL()
    end type ragged_weights_array_ptr_type
    type(ragged_weights_array_ptr_type) :: this_ptr
    integer, intent(in), dimension(2) :: this
    this_ptr = transfer(this, this_ptr)
    deallocate(this_ptr%p)
end subroutine f90wrap_ragged_weights_array_finalise

subroutine f90wrap_ragged_biases_array__array__bias_layer(this, nd, dtype, dshape, dloc)
    use qlknn_types, only: ragged_biases_array
    implicit none
    type ragged_biases_array_ptr_type
        type(ragged_biases_array), pointer :: p => NULL()
    end type ragged_biases_array_ptr_type
    integer, intent(in) :: this(2)
    type(ragged_biases_array_ptr_type) :: this_ptr
    integer, intent(out) :: nd
    integer, intent(out) :: dtype
    integer, dimension(10), intent(out) :: dshape
    integer*8, intent(out) :: dloc
    
    nd = 1
    dtype = 12
    this_ptr = transfer(this, this_ptr)
    if (allocated(this_ptr%p%bias_layer)) then
        dshape(1:1) = shape(this_ptr%p%bias_layer)
        dloc = loc(this_ptr%p%bias_layer)
    else
        dloc = 0
    end if
end subroutine f90wrap_ragged_biases_array__array__bias_layer

subroutine f90wrap_ragged_biases_array_initialise(this)
    use qlknn_types, only: ragged_biases_array
    implicit none
    
    type ragged_biases_array_ptr_type
        type(ragged_biases_array), pointer :: p => NULL()
    end type ragged_biases_array_ptr_type
    type(ragged_biases_array_ptr_type) :: this_ptr
    integer, intent(out), dimension(2) :: this
    allocate(this_ptr%p)
    this = transfer(this_ptr, this)
end subroutine f90wrap_ragged_biases_array_initialise

subroutine f90wrap_ragged_biases_array_finalise(this)
    use qlknn_types, only: ragged_biases_array
    implicit none
    
    type ragged_biases_array_ptr_type
        type(ragged_biases_array), pointer :: p => NULL()
    end type ragged_biases_array_ptr_type
    type(ragged_biases_array_ptr_type) :: this_ptr
    integer, intent(in), dimension(2) :: this
    this_ptr = transfer(this, this_ptr)
    deallocate(this_ptr%p)
end subroutine f90wrap_ragged_biases_array_finalise

subroutine f90wrap_networktype__get__n_hidden_layers(this, f90wrap_n_hidden_layers)
    use qlknn_types, only: networktype
    implicit none
    type networktype_ptr_type
        type(networktype), pointer :: p => NULL()
    end type networktype_ptr_type
    integer, intent(in)   :: this(2)
    type(networktype_ptr_type) :: this_ptr
    integer(8), intent(out) :: f90wrap_n_hidden_layers
    
    this_ptr = transfer(this, this_ptr)
    f90wrap_n_hidden_layers = this_ptr%p%n_hidden_layers
end subroutine f90wrap_networktype__get__n_hidden_layers

subroutine f90wrap_networktype__set__n_hidden_layers(this, f90wrap_n_hidden_layers)
    use qlknn_types, only: networktype
    implicit none
    type networktype_ptr_type
        type(networktype), pointer :: p => NULL()
    end type networktype_ptr_type
    integer, intent(in)   :: this(2)
    type(networktype_ptr_type) :: this_ptr
    integer(8), intent(in) :: f90wrap_n_hidden_layers
    
    this_ptr = transfer(this, this_ptr)
    this_ptr%p%n_hidden_layers = f90wrap_n_hidden_layers
end subroutine f90wrap_networktype__set__n_hidden_layers

subroutine f90wrap_networktype__get__n_max_nodes(this, f90wrap_n_max_nodes)
    use qlknn_types, only: networktype
    implicit none
    type networktype_ptr_type
        type(networktype), pointer :: p => NULL()
    end type networktype_ptr_type
    integer, intent(in)   :: this(2)
    type(networktype_ptr_type) :: this_ptr
    integer(8), intent(out) :: f90wrap_n_max_nodes
    
    this_ptr = transfer(this, this_ptr)
    f90wrap_n_max_nodes = this_ptr%p%n_max_nodes
end subroutine f90wrap_networktype__get__n_max_nodes

subroutine f90wrap_networktype__set__n_max_nodes(this, f90wrap_n_max_nodes)
    use qlknn_types, only: networktype
    implicit none
    type networktype_ptr_type
        type(networktype), pointer :: p => NULL()
    end type networktype_ptr_type
    integer, intent(in)   :: this(2)
    type(networktype_ptr_type) :: this_ptr
    integer(8), intent(in) :: f90wrap_n_max_nodes
    
    this_ptr = transfer(this, this_ptr)
    this_ptr%p%n_max_nodes = f90wrap_n_max_nodes
end subroutine f90wrap_networktype__set__n_max_nodes

subroutine f90wrap_networktype__array__weights_input(this, nd, dtype, dshape, dloc)
    use qlknn_types, only: networktype
    implicit none
    type networktype_ptr_type
        type(networktype), pointer :: p => NULL()
    end type networktype_ptr_type
    integer, intent(in) :: this(2)
    type(networktype_ptr_type) :: this_ptr
    integer, intent(out) :: nd
    integer, intent(out) :: dtype
    integer, dimension(10), intent(out) :: dshape
    integer*8, intent(out) :: dloc
    
    nd = 2
    dtype = 12
    this_ptr = transfer(this, this_ptr)
    if (allocated(this_ptr%p%weights_input)) then
        dshape(1:2) = shape(this_ptr%p%weights_input)
        dloc = loc(this_ptr%p%weights_input)
    else
        dloc = 0
    end if
end subroutine f90wrap_networktype__array__weights_input

subroutine f90wrap_networktype__array__biases_input(this, nd, dtype, dshape, dloc)
    use qlknn_types, only: networktype
    implicit none
    type networktype_ptr_type
        type(networktype), pointer :: p => NULL()
    end type networktype_ptr_type
    integer, intent(in) :: this(2)
    type(networktype_ptr_type) :: this_ptr
    integer, intent(out) :: nd
    integer, intent(out) :: dtype
    integer, dimension(10), intent(out) :: dshape
    integer*8, intent(out) :: dloc
    
    nd = 1
    dtype = 12
    this_ptr = transfer(this, this_ptr)
    if (allocated(this_ptr%p%biases_input)) then
        dshape(1:1) = shape(this_ptr%p%biases_input)
        dloc = loc(this_ptr%p%biases_input)
    else
        dloc = 0
    end if
end subroutine f90wrap_networktype__array__biases_input

subroutine f90wrap_networktype__array_getitem__weights_hidden(f90wrap_this, f90wrap_i, weights_hiddenitem)
    
    use qlknn_types, only: ragged_weights_array, networktype
    implicit none
    
    type networktype_ptr_type
        type(networktype), pointer :: p => NULL()
    end type networktype_ptr_type
    type ragged_weights_array_ptr_type
        type(ragged_weights_array), pointer :: p => NULL()
    end type ragged_weights_array_ptr_type
    integer, intent(in) :: f90wrap_this(2)
    type(networktype_ptr_type) :: this_ptr
    integer, intent(in) :: f90wrap_i
    integer, intent(out) :: weights_hiddenitem(2)
    type(ragged_weights_array_ptr_type) :: weights_hidden_ptr
    
    this_ptr = transfer(f90wrap_this, this_ptr)
    if (allocated(this_ptr%p%weights_hidden)) then
        if (f90wrap_i < 1 .or. f90wrap_i > size(this_ptr%p%weights_hidden)) then
            call f90wrap_abort("array index out of range")
        else
            weights_hidden_ptr%p => this_ptr%p%weights_hidden(f90wrap_i)
            weights_hiddenitem = transfer(weights_hidden_ptr,weights_hiddenitem)
        endif
    else
        call f90wrap_abort("derived type array not allocated")
    end if
end subroutine f90wrap_networktype__array_getitem__weights_hidden

subroutine f90wrap_networktype__array_setitem__weights_hidden(f90wrap_this, f90wrap_i, weights_hiddenitem)
    
    use qlknn_types, only: ragged_weights_array, networktype
    implicit none
    
    type networktype_ptr_type
        type(networktype), pointer :: p => NULL()
    end type networktype_ptr_type
    type ragged_weights_array_ptr_type
        type(ragged_weights_array), pointer :: p => NULL()
    end type ragged_weights_array_ptr_type
    integer, intent(in) :: f90wrap_this(2)
    type(networktype_ptr_type) :: this_ptr
    integer, intent(in) :: f90wrap_i
    integer, intent(in) :: weights_hiddenitem(2)
    type(ragged_weights_array_ptr_type) :: weights_hidden_ptr
    
    this_ptr = transfer(f90wrap_this, this_ptr)
    if (allocated(this_ptr%p%weights_hidden)) then
        if (f90wrap_i < 1 .or. f90wrap_i > size(this_ptr%p%weights_hidden)) then
            call f90wrap_abort("array index out of range")
        else
            weights_hidden_ptr = transfer(weights_hiddenitem,weights_hidden_ptr)
            this_ptr%p%weights_hidden(f90wrap_i) = weights_hidden_ptr%p
        endif
    else
        call f90wrap_abort("derived type array not allocated")
    end if
end subroutine f90wrap_networktype__array_setitem__weights_hidden

subroutine f90wrap_networktype__array_len__weights_hidden(f90wrap_this, f90wrap_n)
    
    use qlknn_types, only: ragged_weights_array, networktype
    implicit none
    
    type networktype_ptr_type
        type(networktype), pointer :: p => NULL()
    end type networktype_ptr_type
    type ragged_weights_array_ptr_type
        type(ragged_weights_array), pointer :: p => NULL()
    end type ragged_weights_array_ptr_type
    integer, intent(out) :: f90wrap_n
    integer, intent(in) :: f90wrap_this(2)
    type(networktype_ptr_type) :: this_ptr
    
    this_ptr = transfer(f90wrap_this, this_ptr)
    if (allocated(this_ptr%p%weights_hidden)) then
        f90wrap_n = size(this_ptr%p%weights_hidden)
    else
        f90wrap_n = 0
    end if
end subroutine f90wrap_networktype__array_len__weights_hidden

subroutine f90wrap_networktype__array_getitem__biases_hidden(f90wrap_this, f90wrap_i, biases_hiddenitem)
    
    use qlknn_types, only: ragged_biases_array, networktype
    implicit none
    
    type networktype_ptr_type
        type(networktype), pointer :: p => NULL()
    end type networktype_ptr_type
    type ragged_biases_array_ptr_type
        type(ragged_biases_array), pointer :: p => NULL()
    end type ragged_biases_array_ptr_type
    integer, intent(in) :: f90wrap_this(2)
    type(networktype_ptr_type) :: this_ptr
    integer, intent(in) :: f90wrap_i
    integer, intent(out) :: biases_hiddenitem(2)
    type(ragged_biases_array_ptr_type) :: biases_hidden_ptr
    
    this_ptr = transfer(f90wrap_this, this_ptr)
    if (allocated(this_ptr%p%biases_hidden)) then
        if (f90wrap_i < 1 .or. f90wrap_i > size(this_ptr%p%biases_hidden)) then
            call f90wrap_abort("array index out of range")
        else
            biases_hidden_ptr%p => this_ptr%p%biases_hidden(f90wrap_i)
            biases_hiddenitem = transfer(biases_hidden_ptr,biases_hiddenitem)
        endif
    else
        call f90wrap_abort("derived type array not allocated")
    end if
end subroutine f90wrap_networktype__array_getitem__biases_hidden

subroutine f90wrap_networktype__array_setitem__biases_hidden(f90wrap_this, f90wrap_i, biases_hiddenitem)
    
    use qlknn_types, only: ragged_biases_array, networktype
    implicit none
    
    type networktype_ptr_type
        type(networktype), pointer :: p => NULL()
    end type networktype_ptr_type
    type ragged_biases_array_ptr_type
        type(ragged_biases_array), pointer :: p => NULL()
    end type ragged_biases_array_ptr_type
    integer, intent(in) :: f90wrap_this(2)
    type(networktype_ptr_type) :: this_ptr
    integer, intent(in) :: f90wrap_i
    integer, intent(in) :: biases_hiddenitem(2)
    type(ragged_biases_array_ptr_type) :: biases_hidden_ptr
    
    this_ptr = transfer(f90wrap_this, this_ptr)
    if (allocated(this_ptr%p%biases_hidden)) then
        if (f90wrap_i < 1 .or. f90wrap_i > size(this_ptr%p%biases_hidden)) then
            call f90wrap_abort("array index out of range")
        else
            biases_hidden_ptr = transfer(biases_hiddenitem,biases_hidden_ptr)
            this_ptr%p%biases_hidden(f90wrap_i) = biases_hidden_ptr%p
        endif
    else
        call f90wrap_abort("derived type array not allocated")
    end if
end subroutine f90wrap_networktype__array_setitem__biases_hidden

subroutine f90wrap_networktype__array_len__biases_hidden(f90wrap_this, f90wrap_n)
    
    use qlknn_types, only: ragged_biases_array, networktype
    implicit none
    
    type networktype_ptr_type
        type(networktype), pointer :: p => NULL()
    end type networktype_ptr_type
    type ragged_biases_array_ptr_type
        type(ragged_biases_array), pointer :: p => NULL()
    end type ragged_biases_array_ptr_type
    integer, intent(out) :: f90wrap_n
    integer, intent(in) :: f90wrap_this(2)
    type(networktype_ptr_type) :: this_ptr
    
    this_ptr = transfer(f90wrap_this, this_ptr)
    if (allocated(this_ptr%p%biases_hidden)) then
        f90wrap_n = size(this_ptr%p%biases_hidden)
    else
        f90wrap_n = 0
    end if
end subroutine f90wrap_networktype__array_len__biases_hidden

subroutine f90wrap_networktype__array__weights_output(this, nd, dtype, dshape, dloc)
    use qlknn_types, only: networktype
    implicit none
    type networktype_ptr_type
        type(networktype), pointer :: p => NULL()
    end type networktype_ptr_type
    integer, intent(in) :: this(2)
    type(networktype_ptr_type) :: this_ptr
    integer, intent(out) :: nd
    integer, intent(out) :: dtype
    integer, dimension(10), intent(out) :: dshape
    integer*8, intent(out) :: dloc
    
    nd = 2
    dtype = 12
    this_ptr = transfer(this, this_ptr)
    if (allocated(this_ptr%p%weights_output)) then
        dshape(1:2) = shape(this_ptr%p%weights_output)
        dloc = loc(this_ptr%p%weights_output)
    else
        dloc = 0
    end if
end subroutine f90wrap_networktype__array__weights_output

subroutine f90wrap_networktype__array__biases_output(this, nd, dtype, dshape, dloc)
    use qlknn_types, only: networktype
    implicit none
    type networktype_ptr_type
        type(networktype), pointer :: p => NULL()
    end type networktype_ptr_type
    integer, intent(in) :: this(2)
    type(networktype_ptr_type) :: this_ptr
    integer, intent(out) :: nd
    integer, intent(out) :: dtype
    integer, dimension(10), intent(out) :: dshape
    integer*8, intent(out) :: dloc
    
    nd = 1
    dtype = 12
    this_ptr = transfer(this, this_ptr)
    if (allocated(this_ptr%p%biases_output)) then
        dshape(1:1) = shape(this_ptr%p%biases_output)
        dloc = loc(this_ptr%p%biases_output)
    else
        dloc = 0
    end if
end subroutine f90wrap_networktype__array__biases_output

subroutine f90wrap_networktype__array__hidden_activation(this, nd, dtype, dshape, dloc)
    use qlknn_types, only: networktype
    implicit none
    type networktype_ptr_type
        type(networktype), pointer :: p => NULL()
    end type networktype_ptr_type
    integer, intent(in) :: this(2)
    type(networktype_ptr_type) :: this_ptr
    integer, intent(out) :: nd
    integer, intent(out) :: dtype
    integer, dimension(10), intent(out) :: dshape
    integer*8, intent(out) :: dloc
    
    nd = 2
    dtype = 2
    this_ptr = transfer(this, this_ptr)
    if (allocated(this_ptr%p%hidden_activation)) then
        dshape(1:2) = (/len(this_ptr%p%hidden_activation(1)), shape(this_ptr%p%hidden_activation)/)
        dloc = loc(this_ptr%p%hidden_activation)
    else
        dloc = 0
    end if
end subroutine f90wrap_networktype__array__hidden_activation

subroutine f90wrap_networktype__array__feature_prescale_bias(this, nd, dtype, dshape, dloc)
    use qlknn_types, only: networktype
    implicit none
    type networktype_ptr_type
        type(networktype), pointer :: p => NULL()
    end type networktype_ptr_type
    integer, intent(in) :: this(2)
    type(networktype_ptr_type) :: this_ptr
    integer, intent(out) :: nd
    integer, intent(out) :: dtype
    integer, dimension(10), intent(out) :: dshape
    integer*8, intent(out) :: dloc
    
    nd = 1
    dtype = 12
    this_ptr = transfer(this, this_ptr)
    if (allocated(this_ptr%p%feature_prescale_bias)) then
        dshape(1:1) = shape(this_ptr%p%feature_prescale_bias)
        dloc = loc(this_ptr%p%feature_prescale_bias)
    else
        dloc = 0
    end if
end subroutine f90wrap_networktype__array__feature_prescale_bias

subroutine f90wrap_networktype__array__feature_prescale_factor(this, nd, dtype, dshape, dloc)
    use qlknn_types, only: networktype
    implicit none
    type networktype_ptr_type
        type(networktype), pointer :: p => NULL()
    end type networktype_ptr_type
    integer, intent(in) :: this(2)
    type(networktype_ptr_type) :: this_ptr
    integer, intent(out) :: nd
    integer, intent(out) :: dtype
    integer, dimension(10), intent(out) :: dshape
    integer*8, intent(out) :: dloc
    
    nd = 1
    dtype = 12
    this_ptr = transfer(this, this_ptr)
    if (allocated(this_ptr%p%feature_prescale_factor)) then
        dshape(1:1) = shape(this_ptr%p%feature_prescale_factor)
        dloc = loc(this_ptr%p%feature_prescale_factor)
    else
        dloc = 0
    end if
end subroutine f90wrap_networktype__array__feature_prescale_factor

subroutine f90wrap_networktype__array__target_prescale_bias(this, nd, dtype, dshape, dloc)
    use qlknn_types, only: networktype
    implicit none
    type networktype_ptr_type
        type(networktype), pointer :: p => NULL()
    end type networktype_ptr_type
    integer, intent(in) :: this(2)
    type(networktype_ptr_type) :: this_ptr
    integer, intent(out) :: nd
    integer, intent(out) :: dtype
    integer, dimension(10), intent(out) :: dshape
    integer*8, intent(out) :: dloc
    
    nd = 1
    dtype = 12
    this_ptr = transfer(this, this_ptr)
    if (allocated(this_ptr%p%target_prescale_bias)) then
        dshape(1:1) = shape(this_ptr%p%target_prescale_bias)
        dloc = loc(this_ptr%p%target_prescale_bias)
    else
        dloc = 0
    end if
end subroutine f90wrap_networktype__array__target_prescale_bias

subroutine f90wrap_networktype__array__target_prescale_factor(this, nd, dtype, dshape, dloc)
    use qlknn_types, only: networktype
    implicit none
    type networktype_ptr_type
        type(networktype), pointer :: p => NULL()
    end type networktype_ptr_type
    integer, intent(in) :: this(2)
    type(networktype_ptr_type) :: this_ptr
    integer, intent(out) :: nd
    integer, intent(out) :: dtype
    integer, dimension(10), intent(out) :: dshape
    integer*8, intent(out) :: dloc
    
    nd = 1
    dtype = 12
    this_ptr = transfer(this, this_ptr)
    if (allocated(this_ptr%p%target_prescale_factor)) then
        dshape(1:1) = shape(this_ptr%p%target_prescale_factor)
        dloc = loc(this_ptr%p%target_prescale_factor)
    else
        dloc = 0
    end if
end subroutine f90wrap_networktype__array__target_prescale_factor

subroutine f90wrap_networktype_deallocate(net)
    use qlknn_types, only: networktype, networktype_deallocate
    implicit none
    
    type networktype_ptr_type
        type(networktype), pointer :: p => NULL()
    end type networktype_ptr_type
    type(networktype_ptr_type) :: net_ptr
    integer, intent(in), dimension(2) :: net
    net_ptr = transfer(net, net_ptr)
    call networktype_deallocate(net=net_ptr%p)
    deallocate(net_ptr%p)
end subroutine f90wrap_networktype_deallocate

subroutine f90wrap_networktype_initialise(this)
    use qlknn_types, only: networktype
    implicit none
    
    type networktype_ptr_type
        type(networktype), pointer :: p => NULL()
    end type networktype_ptr_type
    type(networktype_ptr_type) :: this_ptr
    integer, intent(out), dimension(2) :: this
    allocate(this_ptr%p)
    this = transfer(this_ptr, this)
end subroutine f90wrap_networktype_initialise

subroutine f90wrap_net_collection__array_getitem__nets(f90wrap_this, f90wrap_i, netsitem)
    
    use qlknn_types, only: net_collection, networktype
    implicit none
    
    type net_collection_ptr_type
        type(net_collection), pointer :: p => NULL()
    end type net_collection_ptr_type
    type networktype_ptr_type
        type(networktype), pointer :: p => NULL()
    end type networktype_ptr_type
    integer, intent(in) :: f90wrap_this(2)
    type(net_collection_ptr_type) :: this_ptr
    integer, intent(in) :: f90wrap_i
    integer, intent(out) :: netsitem(2)
    type(networktype_ptr_type) :: nets_ptr
    
    this_ptr = transfer(f90wrap_this, this_ptr)
    if (allocated(this_ptr%p%nets)) then
        if (f90wrap_i < 1 .or. f90wrap_i > size(this_ptr%p%nets)) then
            call f90wrap_abort("array index out of range")
        else
            nets_ptr%p => this_ptr%p%nets(f90wrap_i)
            netsitem = transfer(nets_ptr,netsitem)
        endif
    else
        call f90wrap_abort("derived type array not allocated")
    end if
end subroutine f90wrap_net_collection__array_getitem__nets

subroutine f90wrap_net_collection__array_setitem__nets(f90wrap_this, f90wrap_i, netsitem)
    
    use qlknn_types, only: net_collection, networktype
    implicit none
    
    type net_collection_ptr_type
        type(net_collection), pointer :: p => NULL()
    end type net_collection_ptr_type
    type networktype_ptr_type
        type(networktype), pointer :: p => NULL()
    end type networktype_ptr_type
    integer, intent(in) :: f90wrap_this(2)
    type(net_collection_ptr_type) :: this_ptr
    integer, intent(in) :: f90wrap_i
    integer, intent(in) :: netsitem(2)
    type(networktype_ptr_type) :: nets_ptr
    
    this_ptr = transfer(f90wrap_this, this_ptr)
    if (allocated(this_ptr%p%nets)) then
        if (f90wrap_i < 1 .or. f90wrap_i > size(this_ptr%p%nets)) then
            call f90wrap_abort("array index out of range")
        else
            nets_ptr = transfer(netsitem,nets_ptr)
            this_ptr%p%nets(f90wrap_i) = nets_ptr%p
        endif
    else
        call f90wrap_abort("derived type array not allocated")
    end if
end subroutine f90wrap_net_collection__array_setitem__nets

subroutine f90wrap_net_collection__array_len__nets(f90wrap_this, f90wrap_n)
    
    use qlknn_types, only: net_collection, networktype
    implicit none
    
    type net_collection_ptr_type
        type(net_collection), pointer :: p => NULL()
    end type net_collection_ptr_type
    type networktype_ptr_type
        type(networktype), pointer :: p => NULL()
    end type networktype_ptr_type
    integer, intent(out) :: f90wrap_n
    integer, intent(in) :: f90wrap_this(2)
    type(net_collection_ptr_type) :: this_ptr
    
    this_ptr = transfer(f90wrap_this, this_ptr)
    if (allocated(this_ptr%p%nets)) then
        f90wrap_n = size(this_ptr%p%nets)
    else
        f90wrap_n = 0
    end if
end subroutine f90wrap_net_collection__array_len__nets

subroutine f90wrap_net_collection__get__Zeff_ind(this, f90wrap_Zeff_ind)
    use qlknn_types, only: net_collection
    implicit none
    type net_collection_ptr_type
        type(net_collection), pointer :: p => NULL()
    end type net_collection_ptr_type
    integer, intent(in)   :: this(2)
    type(net_collection_ptr_type) :: this_ptr
    integer(8), intent(out) :: f90wrap_Zeff_ind
    
    this_ptr = transfer(this, this_ptr)
    f90wrap_Zeff_ind = this_ptr%p%Zeff_ind
end subroutine f90wrap_net_collection__get__Zeff_ind

subroutine f90wrap_net_collection__set__Zeff_ind(this, f90wrap_Zeff_ind)
    use qlknn_types, only: net_collection
    implicit none
    type net_collection_ptr_type
        type(net_collection), pointer :: p => NULL()
    end type net_collection_ptr_type
    integer, intent(in)   :: this(2)
    type(net_collection_ptr_type) :: this_ptr
    integer(8), intent(in) :: f90wrap_Zeff_ind
    
    this_ptr = transfer(this, this_ptr)
    this_ptr%p%Zeff_ind = f90wrap_Zeff_ind
end subroutine f90wrap_net_collection__set__Zeff_ind

subroutine f90wrap_net_collection__get__Ati_ind(this, f90wrap_Ati_ind)
    use qlknn_types, only: net_collection
    implicit none
    type net_collection_ptr_type
        type(net_collection), pointer :: p => NULL()
    end type net_collection_ptr_type
    integer, intent(in)   :: this(2)
    type(net_collection_ptr_type) :: this_ptr
    integer(8), intent(out) :: f90wrap_Ati_ind
    
    this_ptr = transfer(this, this_ptr)
    f90wrap_Ati_ind = this_ptr%p%Ati_ind
end subroutine f90wrap_net_collection__get__Ati_ind

subroutine f90wrap_net_collection__set__Ati_ind(this, f90wrap_Ati_ind)
    use qlknn_types, only: net_collection
    implicit none
    type net_collection_ptr_type
        type(net_collection), pointer :: p => NULL()
    end type net_collection_ptr_type
    integer, intent(in)   :: this(2)
    type(net_collection_ptr_type) :: this_ptr
    integer(8), intent(in) :: f90wrap_Ati_ind
    
    this_ptr = transfer(this, this_ptr)
    this_ptr%p%Ati_ind = f90wrap_Ati_ind
end subroutine f90wrap_net_collection__set__Ati_ind

subroutine f90wrap_net_collection__get__Ate_ind(this, f90wrap_Ate_ind)
    use qlknn_types, only: net_collection
    implicit none
    type net_collection_ptr_type
        type(net_collection), pointer :: p => NULL()
    end type net_collection_ptr_type
    integer, intent(in)   :: this(2)
    type(net_collection_ptr_type) :: this_ptr
    integer(8), intent(out) :: f90wrap_Ate_ind
    
    this_ptr = transfer(this, this_ptr)
    f90wrap_Ate_ind = this_ptr%p%Ate_ind
end subroutine f90wrap_net_collection__get__Ate_ind

subroutine f90wrap_net_collection__set__Ate_ind(this, f90wrap_Ate_ind)
    use qlknn_types, only: net_collection
    implicit none
    type net_collection_ptr_type
        type(net_collection), pointer :: p => NULL()
    end type net_collection_ptr_type
    integer, intent(in)   :: this(2)
    type(net_collection_ptr_type) :: this_ptr
    integer(8), intent(in) :: f90wrap_Ate_ind
    
    this_ptr = transfer(this, this_ptr)
    this_ptr%p%Ate_ind = f90wrap_Ate_ind
end subroutine f90wrap_net_collection__set__Ate_ind

subroutine f90wrap_net_collection__get__An_ind(this, f90wrap_An_ind)
    use qlknn_types, only: net_collection
    implicit none
    type net_collection_ptr_type
        type(net_collection), pointer :: p => NULL()
    end type net_collection_ptr_type
    integer, intent(in)   :: this(2)
    type(net_collection_ptr_type) :: this_ptr
    integer(8), intent(out) :: f90wrap_An_ind
    
    this_ptr = transfer(this, this_ptr)
    f90wrap_An_ind = this_ptr%p%An_ind
end subroutine f90wrap_net_collection__get__An_ind

subroutine f90wrap_net_collection__set__An_ind(this, f90wrap_An_ind)
    use qlknn_types, only: net_collection
    implicit none
    type net_collection_ptr_type
        type(net_collection), pointer :: p => NULL()
    end type net_collection_ptr_type
    integer, intent(in)   :: this(2)
    type(net_collection_ptr_type) :: this_ptr
    integer(8), intent(in) :: f90wrap_An_ind
    
    this_ptr = transfer(this, this_ptr)
    this_ptr%p%An_ind = f90wrap_An_ind
end subroutine f90wrap_net_collection__set__An_ind

subroutine f90wrap_net_collection__get__q_ind(this, f90wrap_q_ind)
    use qlknn_types, only: net_collection
    implicit none
    type net_collection_ptr_type
        type(net_collection), pointer :: p => NULL()
    end type net_collection_ptr_type
    integer, intent(in)   :: this(2)
    type(net_collection_ptr_type) :: this_ptr
    integer(8), intent(out) :: f90wrap_q_ind
    
    this_ptr = transfer(this, this_ptr)
    f90wrap_q_ind = this_ptr%p%q_ind
end subroutine f90wrap_net_collection__get__q_ind

subroutine f90wrap_net_collection__set__q_ind(this, f90wrap_q_ind)
    use qlknn_types, only: net_collection
    implicit none
    type net_collection_ptr_type
        type(net_collection), pointer :: p => NULL()
    end type net_collection_ptr_type
    integer, intent(in)   :: this(2)
    type(net_collection_ptr_type) :: this_ptr
    integer(8), intent(in) :: f90wrap_q_ind
    
    this_ptr = transfer(this, this_ptr)
    this_ptr%p%q_ind = f90wrap_q_ind
end subroutine f90wrap_net_collection__set__q_ind

subroutine f90wrap_net_collection__get__smag_ind(this, f90wrap_smag_ind)
    use qlknn_types, only: net_collection
    implicit none
    type net_collection_ptr_type
        type(net_collection), pointer :: p => NULL()
    end type net_collection_ptr_type
    integer, intent(in)   :: this(2)
    type(net_collection_ptr_type) :: this_ptr
    integer(8), intent(out) :: f90wrap_smag_ind
    
    this_ptr = transfer(this, this_ptr)
    f90wrap_smag_ind = this_ptr%p%smag_ind
end subroutine f90wrap_net_collection__get__smag_ind

subroutine f90wrap_net_collection__set__smag_ind(this, f90wrap_smag_ind)
    use qlknn_types, only: net_collection
    implicit none
    type net_collection_ptr_type
        type(net_collection), pointer :: p => NULL()
    end type net_collection_ptr_type
    integer, intent(in)   :: this(2)
    type(net_collection_ptr_type) :: this_ptr
    integer(8), intent(in) :: f90wrap_smag_ind
    
    this_ptr = transfer(this, this_ptr)
    this_ptr%p%smag_ind = f90wrap_smag_ind
end subroutine f90wrap_net_collection__set__smag_ind

subroutine f90wrap_net_collection__get__x_ind(this, f90wrap_x_ind)
    use qlknn_types, only: net_collection
    implicit none
    type net_collection_ptr_type
        type(net_collection), pointer :: p => NULL()
    end type net_collection_ptr_type
    integer, intent(in)   :: this(2)
    type(net_collection_ptr_type) :: this_ptr
    integer(8), intent(out) :: f90wrap_x_ind
    
    this_ptr = transfer(this, this_ptr)
    f90wrap_x_ind = this_ptr%p%x_ind
end subroutine f90wrap_net_collection__get__x_ind

subroutine f90wrap_net_collection__set__x_ind(this, f90wrap_x_ind)
    use qlknn_types, only: net_collection
    implicit none
    type net_collection_ptr_type
        type(net_collection), pointer :: p => NULL()
    end type net_collection_ptr_type
    integer, intent(in)   :: this(2)
    type(net_collection_ptr_type) :: this_ptr
    integer(8), intent(in) :: f90wrap_x_ind
    
    this_ptr = transfer(this, this_ptr)
    this_ptr%p%x_ind = f90wrap_x_ind
end subroutine f90wrap_net_collection__set__x_ind

subroutine f90wrap_net_collection__get__Ti_Te_ind(this, f90wrap_Ti_Te_ind)
    use qlknn_types, only: net_collection
    implicit none
    type net_collection_ptr_type
        type(net_collection), pointer :: p => NULL()
    end type net_collection_ptr_type
    integer, intent(in)   :: this(2)
    type(net_collection_ptr_type) :: this_ptr
    integer(8), intent(out) :: f90wrap_Ti_Te_ind
    
    this_ptr = transfer(this, this_ptr)
    f90wrap_Ti_Te_ind = this_ptr%p%Ti_Te_ind
end subroutine f90wrap_net_collection__get__Ti_Te_ind

subroutine f90wrap_net_collection__set__Ti_Te_ind(this, f90wrap_Ti_Te_ind)
    use qlknn_types, only: net_collection
    implicit none
    type net_collection_ptr_type
        type(net_collection), pointer :: p => NULL()
    end type net_collection_ptr_type
    integer, intent(in)   :: this(2)
    type(net_collection_ptr_type) :: this_ptr
    integer(8), intent(in) :: f90wrap_Ti_Te_ind
    
    this_ptr = transfer(this, this_ptr)
    this_ptr%p%Ti_Te_ind = f90wrap_Ti_Te_ind
end subroutine f90wrap_net_collection__set__Ti_Te_ind

subroutine f90wrap_net_collection__get__logNustar_ind(this, f90wrap_logNustar_ind)
    use qlknn_types, only: net_collection
    implicit none
    type net_collection_ptr_type
        type(net_collection), pointer :: p => NULL()
    end type net_collection_ptr_type
    integer, intent(in)   :: this(2)
    type(net_collection_ptr_type) :: this_ptr
    integer(8), intent(out) :: f90wrap_logNustar_ind
    
    this_ptr = transfer(this, this_ptr)
    f90wrap_logNustar_ind = this_ptr%p%logNustar_ind
end subroutine f90wrap_net_collection__get__logNustar_ind

subroutine f90wrap_net_collection__set__logNustar_ind(this, f90wrap_logNustar_ind)
    use qlknn_types, only: net_collection
    implicit none
    type net_collection_ptr_type
        type(net_collection), pointer :: p => NULL()
    end type net_collection_ptr_type
    integer, intent(in)   :: this(2)
    type(net_collection_ptr_type) :: this_ptr
    integer(8), intent(in) :: f90wrap_logNustar_ind
    
    this_ptr = transfer(this, this_ptr)
    this_ptr%p%logNustar_ind = f90wrap_logNustar_ind
end subroutine f90wrap_net_collection__set__logNustar_ind

subroutine f90wrap_net_collection__get__gammaE_ind(this, f90wrap_gammaE_ind)
    use qlknn_types, only: net_collection
    implicit none
    type net_collection_ptr_type
        type(net_collection), pointer :: p => NULL()
    end type net_collection_ptr_type
    integer, intent(in)   :: this(2)
    type(net_collection_ptr_type) :: this_ptr
    integer(8), intent(out) :: f90wrap_gammaE_ind
    
    this_ptr = transfer(this, this_ptr)
    f90wrap_gammaE_ind = this_ptr%p%gammaE_ind
end subroutine f90wrap_net_collection__get__gammaE_ind

subroutine f90wrap_net_collection__set__gammaE_ind(this, f90wrap_gammaE_ind)
    use qlknn_types, only: net_collection
    implicit none
    type net_collection_ptr_type
        type(net_collection), pointer :: p => NULL()
    end type net_collection_ptr_type
    integer, intent(in)   :: this(2)
    type(net_collection_ptr_type) :: this_ptr
    integer(8), intent(in) :: f90wrap_gammaE_ind
    
    this_ptr = transfer(this, this_ptr)
    this_ptr%p%gammaE_ind = f90wrap_gammaE_ind
end subroutine f90wrap_net_collection__set__gammaE_ind

subroutine f90wrap_net_collection__get__Te_ind(this, f90wrap_Te_ind)
    use qlknn_types, only: net_collection
    implicit none
    type net_collection_ptr_type
        type(net_collection), pointer :: p => NULL()
    end type net_collection_ptr_type
    integer, intent(in)   :: this(2)
    type(net_collection_ptr_type) :: this_ptr
    integer(8), intent(out) :: f90wrap_Te_ind
    
    this_ptr = transfer(this, this_ptr)
    f90wrap_Te_ind = this_ptr%p%Te_ind
end subroutine f90wrap_net_collection__get__Te_ind

subroutine f90wrap_net_collection__set__Te_ind(this, f90wrap_Te_ind)
    use qlknn_types, only: net_collection
    implicit none
    type net_collection_ptr_type
        type(net_collection), pointer :: p => NULL()
    end type net_collection_ptr_type
    integer, intent(in)   :: this(2)
    type(net_collection_ptr_type) :: this_ptr
    integer(8), intent(in) :: f90wrap_Te_ind
    
    this_ptr = transfer(this, this_ptr)
    this_ptr%p%Te_ind = f90wrap_Te_ind
end subroutine f90wrap_net_collection__set__Te_ind

subroutine f90wrap_net_collection__get__Ane_ind(this, f90wrap_Ane_ind)
    use qlknn_types, only: net_collection
    implicit none
    type net_collection_ptr_type
        type(net_collection), pointer :: p => NULL()
    end type net_collection_ptr_type
    integer, intent(in)   :: this(2)
    type(net_collection_ptr_type) :: this_ptr
    integer(8), intent(out) :: f90wrap_Ane_ind
    
    this_ptr = transfer(this, this_ptr)
    f90wrap_Ane_ind = this_ptr%p%Ane_ind
end subroutine f90wrap_net_collection__get__Ane_ind

subroutine f90wrap_net_collection__set__Ane_ind(this, f90wrap_Ane_ind)
    use qlknn_types, only: net_collection
    implicit none
    type net_collection_ptr_type
        type(net_collection), pointer :: p => NULL()
    end type net_collection_ptr_type
    integer, intent(in)   :: this(2)
    type(net_collection_ptr_type) :: this_ptr
    integer(8), intent(in) :: f90wrap_Ane_ind
    
    this_ptr = transfer(this, this_ptr)
    this_ptr%p%Ane_ind = f90wrap_Ane_ind
end subroutine f90wrap_net_collection__set__Ane_ind

subroutine f90wrap_net_collection__get__Machtor_ind(this, f90wrap_Machtor_ind)
    use qlknn_types, only: net_collection
    implicit none
    type net_collection_ptr_type
        type(net_collection), pointer :: p => NULL()
    end type net_collection_ptr_type
    integer, intent(in)   :: this(2)
    type(net_collection_ptr_type) :: this_ptr
    integer(8), intent(out) :: f90wrap_Machtor_ind
    
    this_ptr = transfer(this, this_ptr)
    f90wrap_Machtor_ind = this_ptr%p%Machtor_ind
end subroutine f90wrap_net_collection__get__Machtor_ind

subroutine f90wrap_net_collection__set__Machtor_ind(this, f90wrap_Machtor_ind)
    use qlknn_types, only: net_collection
    implicit none
    type net_collection_ptr_type
        type(net_collection), pointer :: p => NULL()
    end type net_collection_ptr_type
    integer, intent(in)   :: this(2)
    type(net_collection_ptr_type) :: this_ptr
    integer(8), intent(in) :: f90wrap_Machtor_ind
    
    this_ptr = transfer(this, this_ptr)
    this_ptr%p%Machtor_ind = f90wrap_Machtor_ind
end subroutine f90wrap_net_collection__set__Machtor_ind

subroutine f90wrap_net_collection__get__Autor_ind(this, f90wrap_Autor_ind)
    use qlknn_types, only: net_collection
    implicit none
    type net_collection_ptr_type
        type(net_collection), pointer :: p => NULL()
    end type net_collection_ptr_type
    integer, intent(in)   :: this(2)
    type(net_collection_ptr_type) :: this_ptr
    integer(8), intent(out) :: f90wrap_Autor_ind
    
    this_ptr = transfer(this, this_ptr)
    f90wrap_Autor_ind = this_ptr%p%Autor_ind
end subroutine f90wrap_net_collection__get__Autor_ind

subroutine f90wrap_net_collection__set__Autor_ind(this, f90wrap_Autor_ind)
    use qlknn_types, only: net_collection
    implicit none
    type net_collection_ptr_type
        type(net_collection), pointer :: p => NULL()
    end type net_collection_ptr_type
    integer, intent(in)   :: this(2)
    type(net_collection_ptr_type) :: this_ptr
    integer(8), intent(in) :: f90wrap_Autor_ind
    
    this_ptr = transfer(this, this_ptr)
    this_ptr%p%Autor_ind = f90wrap_Autor_ind
end subroutine f90wrap_net_collection__set__Autor_ind

subroutine f90wrap_net_collection__get__alpha_ind(this, f90wrap_alpha_ind)
    use qlknn_types, only: net_collection
    implicit none
    type net_collection_ptr_type
        type(net_collection), pointer :: p => NULL()
    end type net_collection_ptr_type
    integer, intent(in)   :: this(2)
    type(net_collection_ptr_type) :: this_ptr
    integer(8), intent(out) :: f90wrap_alpha_ind
    
    this_ptr = transfer(this, this_ptr)
    f90wrap_alpha_ind = this_ptr%p%alpha_ind
end subroutine f90wrap_net_collection__get__alpha_ind

subroutine f90wrap_net_collection__set__alpha_ind(this, f90wrap_alpha_ind)
    use qlknn_types, only: net_collection
    implicit none
    type net_collection_ptr_type
        type(net_collection), pointer :: p => NULL()
    end type net_collection_ptr_type
    integer, intent(in)   :: this(2)
    type(net_collection_ptr_type) :: this_ptr
    integer(8), intent(in) :: f90wrap_alpha_ind
    
    this_ptr = transfer(this, this_ptr)
    this_ptr%p%alpha_ind = f90wrap_alpha_ind
end subroutine f90wrap_net_collection__set__alpha_ind

subroutine f90wrap_net_collection__get__Ani0_ind(this, f90wrap_Ani0_ind)
    use qlknn_types, only: net_collection
    implicit none
    type net_collection_ptr_type
        type(net_collection), pointer :: p => NULL()
    end type net_collection_ptr_type
    integer, intent(in)   :: this(2)
    type(net_collection_ptr_type) :: this_ptr
    integer(8), intent(out) :: f90wrap_Ani0_ind
    
    this_ptr = transfer(this, this_ptr)
    f90wrap_Ani0_ind = this_ptr%p%Ani0_ind
end subroutine f90wrap_net_collection__get__Ani0_ind

subroutine f90wrap_net_collection__set__Ani0_ind(this, f90wrap_Ani0_ind)
    use qlknn_types, only: net_collection
    implicit none
    type net_collection_ptr_type
        type(net_collection), pointer :: p => NULL()
    end type net_collection_ptr_type
    integer, intent(in)   :: this(2)
    type(net_collection_ptr_type) :: this_ptr
    integer(8), intent(in) :: f90wrap_Ani0_ind
    
    this_ptr = transfer(this, this_ptr)
    this_ptr%p%Ani0_ind = f90wrap_Ani0_ind
end subroutine f90wrap_net_collection__set__Ani0_ind

subroutine f90wrap_net_collection__get__Ani1_ind(this, f90wrap_Ani1_ind)
    use qlknn_types, only: net_collection
    implicit none
    type net_collection_ptr_type
        type(net_collection), pointer :: p => NULL()
    end type net_collection_ptr_type
    integer, intent(in)   :: this(2)
    type(net_collection_ptr_type) :: this_ptr
    integer(8), intent(out) :: f90wrap_Ani1_ind
    
    this_ptr = transfer(this, this_ptr)
    f90wrap_Ani1_ind = this_ptr%p%Ani1_ind
end subroutine f90wrap_net_collection__get__Ani1_ind

subroutine f90wrap_net_collection__set__Ani1_ind(this, f90wrap_Ani1_ind)
    use qlknn_types, only: net_collection
    implicit none
    type net_collection_ptr_type
        type(net_collection), pointer :: p => NULL()
    end type net_collection_ptr_type
    integer, intent(in)   :: this(2)
    type(net_collection_ptr_type) :: this_ptr
    integer(8), intent(in) :: f90wrap_Ani1_ind
    
    this_ptr = transfer(this, this_ptr)
    this_ptr%p%Ani1_ind = f90wrap_Ani1_ind
end subroutine f90wrap_net_collection__set__Ani1_ind

subroutine f90wrap_net_collection__get__Ati0_ind(this, f90wrap_Ati0_ind)
    use qlknn_types, only: net_collection
    implicit none
    type net_collection_ptr_type
        type(net_collection), pointer :: p => NULL()
    end type net_collection_ptr_type
    integer, intent(in)   :: this(2)
    type(net_collection_ptr_type) :: this_ptr
    integer(8), intent(out) :: f90wrap_Ati0_ind
    
    this_ptr = transfer(this, this_ptr)
    f90wrap_Ati0_ind = this_ptr%p%Ati0_ind
end subroutine f90wrap_net_collection__get__Ati0_ind

subroutine f90wrap_net_collection__set__Ati0_ind(this, f90wrap_Ati0_ind)
    use qlknn_types, only: net_collection
    implicit none
    type net_collection_ptr_type
        type(net_collection), pointer :: p => NULL()
    end type net_collection_ptr_type
    integer, intent(in)   :: this(2)
    type(net_collection_ptr_type) :: this_ptr
    integer(8), intent(in) :: f90wrap_Ati0_ind
    
    this_ptr = transfer(this, this_ptr)
    this_ptr%p%Ati0_ind = f90wrap_Ati0_ind
end subroutine f90wrap_net_collection__set__Ati0_ind

subroutine f90wrap_net_collection__get__normni0_ind(this, f90wrap_normni0_ind)
    use qlknn_types, only: net_collection
    implicit none
    type net_collection_ptr_type
        type(net_collection), pointer :: p => NULL()
    end type net_collection_ptr_type
    integer, intent(in)   :: this(2)
    type(net_collection_ptr_type) :: this_ptr
    integer(8), intent(out) :: f90wrap_normni0_ind
    
    this_ptr = transfer(this, this_ptr)
    f90wrap_normni0_ind = this_ptr%p%normni0_ind
end subroutine f90wrap_net_collection__get__normni0_ind

subroutine f90wrap_net_collection__set__normni0_ind(this, f90wrap_normni0_ind)
    use qlknn_types, only: net_collection
    implicit none
    type net_collection_ptr_type
        type(net_collection), pointer :: p => NULL()
    end type net_collection_ptr_type
    integer, intent(in)   :: this(2)
    type(net_collection_ptr_type) :: this_ptr
    integer(8), intent(in) :: f90wrap_normni0_ind
    
    this_ptr = transfer(this, this_ptr)
    this_ptr%p%normni0_ind = f90wrap_normni0_ind
end subroutine f90wrap_net_collection__set__normni0_ind

subroutine f90wrap_net_collection__get__normni1_ind(this, f90wrap_normni1_ind)
    use qlknn_types, only: net_collection
    implicit none
    type net_collection_ptr_type
        type(net_collection), pointer :: p => NULL()
    end type net_collection_ptr_type
    integer, intent(in)   :: this(2)
    type(net_collection_ptr_type) :: this_ptr
    integer(8), intent(out) :: f90wrap_normni1_ind
    
    this_ptr = transfer(this, this_ptr)
    f90wrap_normni1_ind = this_ptr%p%normni1_ind
end subroutine f90wrap_net_collection__get__normni1_ind

subroutine f90wrap_net_collection__set__normni1_ind(this, f90wrap_normni1_ind)
    use qlknn_types, only: net_collection
    implicit none
    type net_collection_ptr_type
        type(net_collection), pointer :: p => NULL()
    end type net_collection_ptr_type
    integer, intent(in)   :: this(2)
    type(net_collection_ptr_type) :: this_ptr
    integer(8), intent(in) :: f90wrap_normni1_ind
    
    this_ptr = transfer(this, this_ptr)
    this_ptr%p%normni1_ind = f90wrap_normni1_ind
end subroutine f90wrap_net_collection__set__normni1_ind

subroutine f90wrap_net_collection__get__Ti_Te0_ind(this, f90wrap_Ti_Te0_ind)
    use qlknn_types, only: net_collection
    implicit none
    type net_collection_ptr_type
        type(net_collection), pointer :: p => NULL()
    end type net_collection_ptr_type
    integer, intent(in)   :: this(2)
    type(net_collection_ptr_type) :: this_ptr
    integer(8), intent(out) :: f90wrap_Ti_Te0_ind
    
    this_ptr = transfer(this, this_ptr)
    f90wrap_Ti_Te0_ind = this_ptr%p%Ti_Te0_ind
end subroutine f90wrap_net_collection__get__Ti_Te0_ind

subroutine f90wrap_net_collection__set__Ti_Te0_ind(this, f90wrap_Ti_Te0_ind)
    use qlknn_types, only: net_collection
    implicit none
    type net_collection_ptr_type
        type(net_collection), pointer :: p => NULL()
    end type net_collection_ptr_type
    integer, intent(in)   :: this(2)
    type(net_collection_ptr_type) :: this_ptr
    integer(8), intent(in) :: f90wrap_Ti_Te0_ind
    
    this_ptr = transfer(this, this_ptr)
    this_ptr%p%Ti_Te0_ind = f90wrap_Ti_Te0_ind
end subroutine f90wrap_net_collection__set__Ti_Te0_ind

subroutine f90wrap_net_collection__get__a(this, f90wrap_a)
    use qlknn_types, only: net_collection
    implicit none
    type net_collection_ptr_type
        type(net_collection), pointer :: p => NULL()
    end type net_collection_ptr_type
    integer, intent(in)   :: this(2)
    type(net_collection_ptr_type) :: this_ptr
    real(8), intent(out) :: f90wrap_a
    
    this_ptr = transfer(this, this_ptr)
    f90wrap_a = this_ptr%p%a
end subroutine f90wrap_net_collection__get__a

subroutine f90wrap_net_collection__set__a(this, f90wrap_a)
    use qlknn_types, only: net_collection
    implicit none
    type net_collection_ptr_type
        type(net_collection), pointer :: p => NULL()
    end type net_collection_ptr_type
    integer, intent(in)   :: this(2)
    type(net_collection_ptr_type) :: this_ptr
    real(8), intent(in) :: f90wrap_a
    
    this_ptr = transfer(this, this_ptr)
    this_ptr%p%a = f90wrap_a
end subroutine f90wrap_net_collection__set__a

subroutine f90wrap_net_collection__get__R_0(this, f90wrap_R_0)
    use qlknn_types, only: net_collection
    implicit none
    type net_collection_ptr_type
        type(net_collection), pointer :: p => NULL()
    end type net_collection_ptr_type
    integer, intent(in)   :: this(2)
    type(net_collection_ptr_type) :: this_ptr
    real(8), intent(out) :: f90wrap_R_0
    
    this_ptr = transfer(this, this_ptr)
    f90wrap_R_0 = this_ptr%p%R_0
end subroutine f90wrap_net_collection__get__R_0

subroutine f90wrap_net_collection__set__R_0(this, f90wrap_R_0)
    use qlknn_types, only: net_collection
    implicit none
    type net_collection_ptr_type
        type(net_collection), pointer :: p => NULL()
    end type net_collection_ptr_type
    integer, intent(in)   :: this(2)
    type(net_collection_ptr_type) :: this_ptr
    real(8), intent(in) :: f90wrap_R_0
    
    this_ptr = transfer(this, this_ptr)
    this_ptr%p%R_0 = f90wrap_R_0
end subroutine f90wrap_net_collection__set__R_0

subroutine f90wrap_all_networktype_deallocate(net_coll)
    use qlknn_types, only: net_collection, all_networktype_deallocate
    implicit none
    
    type net_collection_ptr_type
        type(net_collection), pointer :: p => NULL()
    end type net_collection_ptr_type
    type(net_collection_ptr_type) :: net_coll_ptr
    integer, intent(in), dimension(2) :: net_coll
    net_coll_ptr = transfer(net_coll, net_coll_ptr)
    call all_networktype_deallocate(net_coll=net_coll_ptr%p)
    deallocate(net_coll_ptr%p)
end subroutine f90wrap_all_networktype_deallocate

subroutine f90wrap_net_collection_initialise(this)
    use qlknn_types, only: net_collection
    implicit none
    
    type net_collection_ptr_type
        type(net_collection), pointer :: p => NULL()
    end type net_collection_ptr_type
    type(net_collection_ptr_type) :: this_ptr
    integer, intent(out), dimension(2) :: this
    allocate(this_ptr%p)
    this = transfer(this_ptr, this)
end subroutine f90wrap_net_collection_initialise

subroutine f90wrap_hornnet_output_block__array_getitem__weights_hidden(f90wrap_this, f90wrap_i, weights_hiddenitem)
    
    use qlknn_types, only: ragged_weights_array, hornnet_output_block
    implicit none
    
    type hornnet_output_block_ptr_type
        type(hornnet_output_block), pointer :: p => NULL()
    end type hornnet_output_block_ptr_type
    type ragged_weights_array_ptr_type
        type(ragged_weights_array), pointer :: p => NULL()
    end type ragged_weights_array_ptr_type
    integer, intent(in) :: f90wrap_this(2)
    type(hornnet_output_block_ptr_type) :: this_ptr
    integer, intent(in) :: f90wrap_i
    integer, intent(out) :: weights_hiddenitem(2)
    type(ragged_weights_array_ptr_type) :: weights_hidden_ptr
    
    this_ptr = transfer(f90wrap_this, this_ptr)
    if (allocated(this_ptr%p%weights_hidden)) then
        if (f90wrap_i < 1 .or. f90wrap_i > size(this_ptr%p%weights_hidden)) then
            call f90wrap_abort("array index out of range")
        else
            weights_hidden_ptr%p => this_ptr%p%weights_hidden(f90wrap_i)
            weights_hiddenitem = transfer(weights_hidden_ptr,weights_hiddenitem)
        endif
    else
        call f90wrap_abort("derived type array not allocated")
    end if
end subroutine f90wrap_hornnet_output_block__array_getitem__weights_hidden

subroutine f90wrap_hornnet_output_block__array_setitem__weights_hidden(f90wrap_this, f90wrap_i, weights_hiddenitem)
    
    use qlknn_types, only: ragged_weights_array, hornnet_output_block
    implicit none
    
    type hornnet_output_block_ptr_type
        type(hornnet_output_block), pointer :: p => NULL()
    end type hornnet_output_block_ptr_type
    type ragged_weights_array_ptr_type
        type(ragged_weights_array), pointer :: p => NULL()
    end type ragged_weights_array_ptr_type
    integer, intent(in) :: f90wrap_this(2)
    type(hornnet_output_block_ptr_type) :: this_ptr
    integer, intent(in) :: f90wrap_i
    integer, intent(in) :: weights_hiddenitem(2)
    type(ragged_weights_array_ptr_type) :: weights_hidden_ptr
    
    this_ptr = transfer(f90wrap_this, this_ptr)
    if (allocated(this_ptr%p%weights_hidden)) then
        if (f90wrap_i < 1 .or. f90wrap_i > size(this_ptr%p%weights_hidden)) then
            call f90wrap_abort("array index out of range")
        else
            weights_hidden_ptr = transfer(weights_hiddenitem,weights_hidden_ptr)
            this_ptr%p%weights_hidden(f90wrap_i) = weights_hidden_ptr%p
        endif
    else
        call f90wrap_abort("derived type array not allocated")
    end if
end subroutine f90wrap_hornnet_output_block__array_setitem__weights_hidden

subroutine f90wrap_hornnet_output_block__array_len__weights_hidden(f90wrap_this, f90wrap_n)
    
    use qlknn_types, only: ragged_weights_array, hornnet_output_block
    implicit none
    
    type hornnet_output_block_ptr_type
        type(hornnet_output_block), pointer :: p => NULL()
    end type hornnet_output_block_ptr_type
    type ragged_weights_array_ptr_type
        type(ragged_weights_array), pointer :: p => NULL()
    end type ragged_weights_array_ptr_type
    integer, intent(out) :: f90wrap_n
    integer, intent(in) :: f90wrap_this(2)
    type(hornnet_output_block_ptr_type) :: this_ptr
    
    this_ptr = transfer(f90wrap_this, this_ptr)
    if (allocated(this_ptr%p%weights_hidden)) then
        f90wrap_n = size(this_ptr%p%weights_hidden)
    else
        f90wrap_n = 0
    end if
end subroutine f90wrap_hornnet_output_block__array_len__weights_hidden

subroutine f90wrap_hornnet_output_block__array_getitem__biases_hidden(f90wrap_this, f90wrap_i, biases_hiddenitem)
    
    use qlknn_types, only: ragged_biases_array, hornnet_output_block
    implicit none
    
    type hornnet_output_block_ptr_type
        type(hornnet_output_block), pointer :: p => NULL()
    end type hornnet_output_block_ptr_type
    type ragged_biases_array_ptr_type
        type(ragged_biases_array), pointer :: p => NULL()
    end type ragged_biases_array_ptr_type
    integer, intent(in) :: f90wrap_this(2)
    type(hornnet_output_block_ptr_type) :: this_ptr
    integer, intent(in) :: f90wrap_i
    integer, intent(out) :: biases_hiddenitem(2)
    type(ragged_biases_array_ptr_type) :: biases_hidden_ptr
    
    this_ptr = transfer(f90wrap_this, this_ptr)
    if (allocated(this_ptr%p%biases_hidden)) then
        if (f90wrap_i < 1 .or. f90wrap_i > size(this_ptr%p%biases_hidden)) then
            call f90wrap_abort("array index out of range")
        else
            biases_hidden_ptr%p => this_ptr%p%biases_hidden(f90wrap_i)
            biases_hiddenitem = transfer(biases_hidden_ptr,biases_hiddenitem)
        endif
    else
        call f90wrap_abort("derived type array not allocated")
    end if
end subroutine f90wrap_hornnet_output_block__array_getitem__biases_hidden

subroutine f90wrap_hornnet_output_block__array_setitem__biases_hidden(f90wrap_this, f90wrap_i, biases_hiddenitem)
    
    use qlknn_types, only: ragged_biases_array, hornnet_output_block
    implicit none
    
    type hornnet_output_block_ptr_type
        type(hornnet_output_block), pointer :: p => NULL()
    end type hornnet_output_block_ptr_type
    type ragged_biases_array_ptr_type
        type(ragged_biases_array), pointer :: p => NULL()
    end type ragged_biases_array_ptr_type
    integer, intent(in) :: f90wrap_this(2)
    type(hornnet_output_block_ptr_type) :: this_ptr
    integer, intent(in) :: f90wrap_i
    integer, intent(in) :: biases_hiddenitem(2)
    type(ragged_biases_array_ptr_type) :: biases_hidden_ptr
    
    this_ptr = transfer(f90wrap_this, this_ptr)
    if (allocated(this_ptr%p%biases_hidden)) then
        if (f90wrap_i < 1 .or. f90wrap_i > size(this_ptr%p%biases_hidden)) then
            call f90wrap_abort("array index out of range")
        else
            biases_hidden_ptr = transfer(biases_hiddenitem,biases_hidden_ptr)
            this_ptr%p%biases_hidden(f90wrap_i) = biases_hidden_ptr%p
        endif
    else
        call f90wrap_abort("derived type array not allocated")
    end if
end subroutine f90wrap_hornnet_output_block__array_setitem__biases_hidden

subroutine f90wrap_hornnet_output_block__array_len__biases_hidden(f90wrap_this, f90wrap_n)
    
    use qlknn_types, only: ragged_biases_array, hornnet_output_block
    implicit none
    
    type hornnet_output_block_ptr_type
        type(hornnet_output_block), pointer :: p => NULL()
    end type hornnet_output_block_ptr_type
    type ragged_biases_array_ptr_type
        type(ragged_biases_array), pointer :: p => NULL()
    end type ragged_biases_array_ptr_type
    integer, intent(out) :: f90wrap_n
    integer, intent(in) :: f90wrap_this(2)
    type(hornnet_output_block_ptr_type) :: this_ptr
    
    this_ptr = transfer(f90wrap_this, this_ptr)
    if (allocated(this_ptr%p%biases_hidden)) then
        f90wrap_n = size(this_ptr%p%biases_hidden)
    else
        f90wrap_n = 0
    end if
end subroutine f90wrap_hornnet_output_block__array_len__biases_hidden

subroutine f90wrap_hornnet_output_block__array__weights_output(this, nd, dtype, dshape, dloc)
    use qlknn_types, only: hornnet_output_block
    implicit none
    type hornnet_output_block_ptr_type
        type(hornnet_output_block), pointer :: p => NULL()
    end type hornnet_output_block_ptr_type
    integer, intent(in) :: this(2)
    type(hornnet_output_block_ptr_type) :: this_ptr
    integer, intent(out) :: nd
    integer, intent(out) :: dtype
    integer, dimension(10), intent(out) :: dshape
    integer*8, intent(out) :: dloc
    
    nd = 2
    dtype = 12
    this_ptr = transfer(this, this_ptr)
    if (allocated(this_ptr%p%weights_output)) then
        dshape(1:2) = shape(this_ptr%p%weights_output)
        dloc = loc(this_ptr%p%weights_output)
    else
        dloc = 0
    end if
end subroutine f90wrap_hornnet_output_block__array__weights_output

subroutine f90wrap_hornnet_output_block__array__biases_output(this, nd, dtype, dshape, dloc)
    use qlknn_types, only: hornnet_output_block
    implicit none
    type hornnet_output_block_ptr_type
        type(hornnet_output_block), pointer :: p => NULL()
    end type hornnet_output_block_ptr_type
    integer, intent(in) :: this(2)
    type(hornnet_output_block_ptr_type) :: this_ptr
    integer, intent(out) :: nd
    integer, intent(out) :: dtype
    integer, dimension(10), intent(out) :: dshape
    integer*8, intent(out) :: dloc
    
    nd = 1
    dtype = 12
    this_ptr = transfer(this, this_ptr)
    if (allocated(this_ptr%p%biases_output)) then
        dshape(1:1) = shape(this_ptr%p%biases_output)
        dloc = loc(this_ptr%p%biases_output)
    else
        dloc = 0
    end if
end subroutine f90wrap_hornnet_output_block__array__biases_output

subroutine f90wrap_hornnet_output_block__array__hidden_activation(this, nd, dtype, dshape, dloc)
    use qlknn_types, only: hornnet_output_block
    implicit none
    type hornnet_output_block_ptr_type
        type(hornnet_output_block), pointer :: p => NULL()
    end type hornnet_output_block_ptr_type
    integer, intent(in) :: this(2)
    type(hornnet_output_block_ptr_type) :: this_ptr
    integer, intent(out) :: nd
    integer, intent(out) :: dtype
    integer, dimension(10), intent(out) :: dshape
    integer*8, intent(out) :: dloc
    
    nd = 2
    dtype = 2
    this_ptr = transfer(this, this_ptr)
    if (allocated(this_ptr%p%hidden_activation)) then
        dshape(1:2) = (/len(this_ptr%p%hidden_activation(1)), shape(this_ptr%p%hidden_activation)/)
        dloc = loc(this_ptr%p%hidden_activation)
    else
        dloc = 0
    end if
end subroutine f90wrap_hornnet_output_block__array__hidden_activation

subroutine f90wrap_hornnet_output_block__get__blockname(this, f90wrap_blockname)
    use qlknn_types, only: hornnet_output_block
    implicit none
    type hornnet_output_block_ptr_type
        type(hornnet_output_block), pointer :: p => NULL()
    end type hornnet_output_block_ptr_type
    integer, intent(in)   :: this(2)
    type(hornnet_output_block_ptr_type) :: this_ptr
    character(20), intent(out) :: f90wrap_blockname
    
    this_ptr = transfer(this, this_ptr)
    f90wrap_blockname = this_ptr%p%blockname
end subroutine f90wrap_hornnet_output_block__get__blockname

subroutine f90wrap_hornnet_output_block__set__blockname(this, f90wrap_blockname)
    use qlknn_types, only: hornnet_output_block
    implicit none
    type hornnet_output_block_ptr_type
        type(hornnet_output_block), pointer :: p => NULL()
    end type hornnet_output_block_ptr_type
    integer, intent(in)   :: this(2)
    type(hornnet_output_block_ptr_type) :: this_ptr
    character(20), intent(in) :: f90wrap_blockname
    
    this_ptr = transfer(this, this_ptr)
    this_ptr%p%blockname = f90wrap_blockname
end subroutine f90wrap_hornnet_output_block__set__blockname

subroutine f90wrap_hornnet_output_block_initialise(this)
    use qlknn_types, only: hornnet_output_block
    implicit none
    
    type hornnet_output_block_ptr_type
        type(hornnet_output_block), pointer :: p => NULL()
    end type hornnet_output_block_ptr_type
    type(hornnet_output_block_ptr_type) :: this_ptr
    integer, intent(out), dimension(2) :: this
    allocate(this_ptr%p)
    this = transfer(this_ptr, this)
end subroutine f90wrap_hornnet_output_block_initialise

subroutine f90wrap_hornnet_output_block_finalise(this)
    use qlknn_types, only: hornnet_output_block
    implicit none
    
    type hornnet_output_block_ptr_type
        type(hornnet_output_block), pointer :: p => NULL()
    end type hornnet_output_block_ptr_type
    type(hornnet_output_block_ptr_type) :: this_ptr
    integer, intent(in), dimension(2) :: this
    this_ptr = transfer(this, this_ptr)
    deallocate(this_ptr%p)
end subroutine f90wrap_hornnet_output_block_finalise

subroutine f90wrap_hornnet_input_block__array__weights_input(this, nd, dtype, dshape, dloc)
    use qlknn_types, only: hornnet_input_block
    implicit none
    type hornnet_input_block_ptr_type
        type(hornnet_input_block), pointer :: p => NULL()
    end type hornnet_input_block_ptr_type
    integer, intent(in) :: this(2)
    type(hornnet_input_block_ptr_type) :: this_ptr
    integer, intent(out) :: nd
    integer, intent(out) :: dtype
    integer, dimension(10), intent(out) :: dshape
    integer*8, intent(out) :: dloc
    
    nd = 2
    dtype = 12
    this_ptr = transfer(this, this_ptr)
    if (allocated(this_ptr%p%weights_input)) then
        dshape(1:2) = shape(this_ptr%p%weights_input)
        dloc = loc(this_ptr%p%weights_input)
    else
        dloc = 0
    end if
end subroutine f90wrap_hornnet_input_block__array__weights_input

subroutine f90wrap_hornnet_input_block__array__biases_input(this, nd, dtype, dshape, dloc)
    use qlknn_types, only: hornnet_input_block
    implicit none
    type hornnet_input_block_ptr_type
        type(hornnet_input_block), pointer :: p => NULL()
    end type hornnet_input_block_ptr_type
    integer, intent(in) :: this(2)
    type(hornnet_input_block_ptr_type) :: this_ptr
    integer, intent(out) :: nd
    integer, intent(out) :: dtype
    integer, dimension(10), intent(out) :: dshape
    integer*8, intent(out) :: dloc
    
    nd = 1
    dtype = 12
    this_ptr = transfer(this, this_ptr)
    if (allocated(this_ptr%p%biases_input)) then
        dshape(1:1) = shape(this_ptr%p%biases_input)
        dloc = loc(this_ptr%p%biases_input)
    else
        dloc = 0
    end if
end subroutine f90wrap_hornnet_input_block__array__biases_input

subroutine f90wrap_hornnet_input_block__array__feature_prescale_bias(this, nd, dtype, dshape, dloc)
    use qlknn_types, only: hornnet_input_block
    implicit none
    type hornnet_input_block_ptr_type
        type(hornnet_input_block), pointer :: p => NULL()
    end type hornnet_input_block_ptr_type
    integer, intent(in) :: this(2)
    type(hornnet_input_block_ptr_type) :: this_ptr
    integer, intent(out) :: nd
    integer, intent(out) :: dtype
    integer, dimension(10), intent(out) :: dshape
    integer*8, intent(out) :: dloc
    
    nd = 1
    dtype = 12
    this_ptr = transfer(this, this_ptr)
    if (allocated(this_ptr%p%feature_prescale_bias)) then
        dshape(1:1) = shape(this_ptr%p%feature_prescale_bias)
        dloc = loc(this_ptr%p%feature_prescale_bias)
    else
        dloc = 0
    end if
end subroutine f90wrap_hornnet_input_block__array__feature_prescale_bias

subroutine f90wrap_hornnet_input_block__array__feature_prescale_factor(this, nd, dtype, dshape, dloc)
    use qlknn_types, only: hornnet_input_block
    implicit none
    type hornnet_input_block_ptr_type
        type(hornnet_input_block), pointer :: p => NULL()
    end type hornnet_input_block_ptr_type
    integer, intent(in) :: this(2)
    type(hornnet_input_block_ptr_type) :: this_ptr
    integer, intent(out) :: nd
    integer, intent(out) :: dtype
    integer, dimension(10), intent(out) :: dshape
    integer*8, intent(out) :: dloc
    
    nd = 1
    dtype = 12
    this_ptr = transfer(this, this_ptr)
    if (allocated(this_ptr%p%feature_prescale_factor)) then
        dshape(1:1) = shape(this_ptr%p%feature_prescale_factor)
        dloc = loc(this_ptr%p%feature_prescale_factor)
    else
        dloc = 0
    end if
end subroutine f90wrap_hornnet_input_block__array__feature_prescale_factor

subroutine f90wrap_hornnet_input_block__array__target_prescale_bias(this, nd, dtype, dshape, dloc)
    use qlknn_types, only: hornnet_input_block
    implicit none
    type hornnet_input_block_ptr_type
        type(hornnet_input_block), pointer :: p => NULL()
    end type hornnet_input_block_ptr_type
    integer, intent(in) :: this(2)
    type(hornnet_input_block_ptr_type) :: this_ptr
    integer, intent(out) :: nd
    integer, intent(out) :: dtype
    integer, dimension(10), intent(out) :: dshape
    integer*8, intent(out) :: dloc
    
    nd = 1
    dtype = 12
    this_ptr = transfer(this, this_ptr)
    if (allocated(this_ptr%p%target_prescale_bias)) then
        dshape(1:1) = shape(this_ptr%p%target_prescale_bias)
        dloc = loc(this_ptr%p%target_prescale_bias)
    else
        dloc = 0
    end if
end subroutine f90wrap_hornnet_input_block__array__target_prescale_bias

subroutine f90wrap_hornnet_input_block__array__target_prescale_factor(this, nd, dtype, dshape, dloc)
    use qlknn_types, only: hornnet_input_block
    implicit none
    type hornnet_input_block_ptr_type
        type(hornnet_input_block), pointer :: p => NULL()
    end type hornnet_input_block_ptr_type
    integer, intent(in) :: this(2)
    type(hornnet_input_block_ptr_type) :: this_ptr
    integer, intent(out) :: nd
    integer, intent(out) :: dtype
    integer, dimension(10), intent(out) :: dshape
    integer*8, intent(out) :: dloc
    
    nd = 1
    dtype = 12
    this_ptr = transfer(this, this_ptr)
    if (allocated(this_ptr%p%target_prescale_factor)) then
        dshape(1:1) = shape(this_ptr%p%target_prescale_factor)
        dloc = loc(this_ptr%p%target_prescale_factor)
    else
        dloc = 0
    end if
end subroutine f90wrap_hornnet_input_block__array__target_prescale_factor

subroutine f90wrap_hornnet_input_block_initialise(this)
    use qlknn_types, only: hornnet_input_block
    implicit none
    
    type hornnet_input_block_ptr_type
        type(hornnet_input_block), pointer :: p => NULL()
    end type hornnet_input_block_ptr_type
    type(hornnet_input_block_ptr_type) :: this_ptr
    integer, intent(out), dimension(2) :: this
    allocate(this_ptr%p)
    this = transfer(this_ptr, this)
end subroutine f90wrap_hornnet_input_block_initialise

subroutine f90wrap_hornnet_input_block_finalise(this)
    use qlknn_types, only: hornnet_input_block
    implicit none
    
    type hornnet_input_block_ptr_type
        type(hornnet_input_block), pointer :: p => NULL()
    end type hornnet_input_block_ptr_type
    type(hornnet_input_block_ptr_type) :: this_ptr
    integer, intent(in), dimension(2) :: this
    this_ptr = transfer(this, this_ptr)
    deallocate(this_ptr%p)
end subroutine f90wrap_hornnet_input_block_finalise

subroutine f90wrap_block_collection__array_getitem__output_blocks(f90wrap_this, f90wrap_i, output_blocksitem)
    
    use qlknn_types, only: block_collection, hornnet_output_block
    implicit none
    
    type block_collection_ptr_type
        type(block_collection), pointer :: p => NULL()
    end type block_collection_ptr_type
    type hornnet_output_block_ptr_type
        type(hornnet_output_block), pointer :: p => NULL()
    end type hornnet_output_block_ptr_type
    integer, intent(in) :: f90wrap_this(2)
    type(block_collection_ptr_type) :: this_ptr
    integer, intent(in) :: f90wrap_i
    integer, intent(out) :: output_blocksitem(2)
    type(hornnet_output_block_ptr_type) :: output_blocks_ptr
    
    this_ptr = transfer(f90wrap_this, this_ptr)
    if (allocated(this_ptr%p%output_blocks)) then
        if (f90wrap_i < 1 .or. f90wrap_i > size(this_ptr%p%output_blocks)) then
            call f90wrap_abort("array index out of range")
        else
            output_blocks_ptr%p => this_ptr%p%output_blocks(f90wrap_i)
            output_blocksitem = transfer(output_blocks_ptr,output_blocksitem)
        endif
    else
        call f90wrap_abort("derived type array not allocated")
    end if
end subroutine f90wrap_block_collection__array_getitem__output_blocks

subroutine f90wrap_block_collection__array_setitem__output_blocks(f90wrap_this, f90wrap_i, output_blocksitem)
    
    use qlknn_types, only: block_collection, hornnet_output_block
    implicit none
    
    type block_collection_ptr_type
        type(block_collection), pointer :: p => NULL()
    end type block_collection_ptr_type
    type hornnet_output_block_ptr_type
        type(hornnet_output_block), pointer :: p => NULL()
    end type hornnet_output_block_ptr_type
    integer, intent(in) :: f90wrap_this(2)
    type(block_collection_ptr_type) :: this_ptr
    integer, intent(in) :: f90wrap_i
    integer, intent(in) :: output_blocksitem(2)
    type(hornnet_output_block_ptr_type) :: output_blocks_ptr
    
    this_ptr = transfer(f90wrap_this, this_ptr)
    if (allocated(this_ptr%p%output_blocks)) then
        if (f90wrap_i < 1 .or. f90wrap_i > size(this_ptr%p%output_blocks)) then
            call f90wrap_abort("array index out of range")
        else
            output_blocks_ptr = transfer(output_blocksitem,output_blocks_ptr)
            this_ptr%p%output_blocks(f90wrap_i) = output_blocks_ptr%p
        endif
    else
        call f90wrap_abort("derived type array not allocated")
    end if
end subroutine f90wrap_block_collection__array_setitem__output_blocks

subroutine f90wrap_block_collection__array_len__output_blocks(f90wrap_this, f90wrap_n)
    
    use qlknn_types, only: block_collection, hornnet_output_block
    implicit none
    
    type block_collection_ptr_type
        type(block_collection), pointer :: p => NULL()
    end type block_collection_ptr_type
    type hornnet_output_block_ptr_type
        type(hornnet_output_block), pointer :: p => NULL()
    end type hornnet_output_block_ptr_type
    integer, intent(out) :: f90wrap_n
    integer, intent(in) :: f90wrap_this(2)
    type(block_collection_ptr_type) :: this_ptr
    
    this_ptr = transfer(f90wrap_this, this_ptr)
    if (allocated(this_ptr%p%output_blocks)) then
        f90wrap_n = size(this_ptr%p%output_blocks)
    else
        f90wrap_n = 0
    end if
end subroutine f90wrap_block_collection__array_len__output_blocks

subroutine f90wrap_block_collection__array_getitem__input_blocks(f90wrap_this, f90wrap_i, input_blocksitem)
    
    use qlknn_types, only: block_collection, hornnet_input_block
    implicit none
    
    type block_collection_ptr_type
        type(block_collection), pointer :: p => NULL()
    end type block_collection_ptr_type
    type hornnet_input_block_ptr_type
        type(hornnet_input_block), pointer :: p => NULL()
    end type hornnet_input_block_ptr_type
    integer, intent(in) :: f90wrap_this(2)
    type(block_collection_ptr_type) :: this_ptr
    integer, intent(in) :: f90wrap_i
    integer, intent(out) :: input_blocksitem(2)
    type(hornnet_input_block_ptr_type) :: input_blocks_ptr
    
    this_ptr = transfer(f90wrap_this, this_ptr)
    if (allocated(this_ptr%p%input_blocks)) then
        if (f90wrap_i < 1 .or. f90wrap_i > size(this_ptr%p%input_blocks)) then
            call f90wrap_abort("array index out of range")
        else
            input_blocks_ptr%p => this_ptr%p%input_blocks(f90wrap_i)
            input_blocksitem = transfer(input_blocks_ptr,input_blocksitem)
        endif
    else
        call f90wrap_abort("derived type array not allocated")
    end if
end subroutine f90wrap_block_collection__array_getitem__input_blocks

subroutine f90wrap_block_collection__array_setitem__input_blocks(f90wrap_this, f90wrap_i, input_blocksitem)
    
    use qlknn_types, only: block_collection, hornnet_input_block
    implicit none
    
    type block_collection_ptr_type
        type(block_collection), pointer :: p => NULL()
    end type block_collection_ptr_type
    type hornnet_input_block_ptr_type
        type(hornnet_input_block), pointer :: p => NULL()
    end type hornnet_input_block_ptr_type
    integer, intent(in) :: f90wrap_this(2)
    type(block_collection_ptr_type) :: this_ptr
    integer, intent(in) :: f90wrap_i
    integer, intent(in) :: input_blocksitem(2)
    type(hornnet_input_block_ptr_type) :: input_blocks_ptr
    
    this_ptr = transfer(f90wrap_this, this_ptr)
    if (allocated(this_ptr%p%input_blocks)) then
        if (f90wrap_i < 1 .or. f90wrap_i > size(this_ptr%p%input_blocks)) then
            call f90wrap_abort("array index out of range")
        else
            input_blocks_ptr = transfer(input_blocksitem,input_blocks_ptr)
            this_ptr%p%input_blocks(f90wrap_i) = input_blocks_ptr%p
        endif
    else
        call f90wrap_abort("derived type array not allocated")
    end if
end subroutine f90wrap_block_collection__array_setitem__input_blocks

subroutine f90wrap_block_collection__array_len__input_blocks(f90wrap_this, f90wrap_n)
    
    use qlknn_types, only: block_collection, hornnet_input_block
    implicit none
    
    type block_collection_ptr_type
        type(block_collection), pointer :: p => NULL()
    end type block_collection_ptr_type
    type hornnet_input_block_ptr_type
        type(hornnet_input_block), pointer :: p => NULL()
    end type hornnet_input_block_ptr_type
    integer, intent(out) :: f90wrap_n
    integer, intent(in) :: f90wrap_this(2)
    type(block_collection_ptr_type) :: this_ptr
    
    this_ptr = transfer(f90wrap_this, this_ptr)
    if (allocated(this_ptr%p%input_blocks)) then
        f90wrap_n = size(this_ptr%p%input_blocks)
    else
        f90wrap_n = 0
    end if
end subroutine f90wrap_block_collection__array_len__input_blocks

subroutine f90wrap_block_collection_initialise(this)
    use qlknn_types, only: block_collection
    implicit none
    
    type block_collection_ptr_type
        type(block_collection), pointer :: p => NULL()
    end type block_collection_ptr_type
    type(block_collection_ptr_type) :: this_ptr
    integer, intent(out), dimension(2) :: this
    allocate(this_ptr%p)
    this = transfer(this_ptr, this)
end subroutine f90wrap_block_collection_initialise

subroutine f90wrap_block_collection_finalise(this)
    use qlknn_types, only: block_collection
    implicit none
    
    type block_collection_ptr_type
        type(block_collection), pointer :: p => NULL()
    end type block_collection_ptr_type
    type(block_collection_ptr_type) :: this_ptr
    integer, intent(in), dimension(2) :: this
    this_ptr = transfer(this, this_ptr)
    deallocate(this_ptr%p)
end subroutine f90wrap_block_collection_finalise

subroutine f90wrap_qlknn_options__get__use_ion_diffusivity_networks(this, f90wrap_use_ion_diffusivity_networks)
    use qlknn_types, only: qlknn_options
    implicit none
    type qlknn_options_ptr_type
        type(qlknn_options), pointer :: p => NULL()
    end type qlknn_options_ptr_type
    integer, intent(in)   :: this(2)
    type(qlknn_options_ptr_type) :: this_ptr
    logical, intent(out) :: f90wrap_use_ion_diffusivity_networks
    
    this_ptr = transfer(this, this_ptr)
    f90wrap_use_ion_diffusivity_networks = this_ptr%p%use_ion_diffusivity_networks
end subroutine f90wrap_qlknn_options__get__use_ion_diffusivity_networks

subroutine f90wrap_qlknn_options__set__use_ion_diffusivity_networks(this, f90wrap_use_ion_diffusivity_networks)
    use qlknn_types, only: qlknn_options
    implicit none
    type qlknn_options_ptr_type
        type(qlknn_options), pointer :: p => NULL()
    end type qlknn_options_ptr_type
    integer, intent(in)   :: this(2)
    type(qlknn_options_ptr_type) :: this_ptr
    logical, intent(in) :: f90wrap_use_ion_diffusivity_networks
    
    this_ptr = transfer(this, this_ptr)
    this_ptr%p%use_ion_diffusivity_networks = f90wrap_use_ion_diffusivity_networks
end subroutine f90wrap_qlknn_options__set__use_ion_diffusivity_networks

subroutine f90wrap_qlknn_options__get__apply_victor_rule(this, f90wrap_apply_victor_rule)
    use qlknn_types, only: qlknn_options
    implicit none
    type qlknn_options_ptr_type
        type(qlknn_options), pointer :: p => NULL()
    end type qlknn_options_ptr_type
    integer, intent(in)   :: this(2)
    type(qlknn_options_ptr_type) :: this_ptr
    logical, intent(out) :: f90wrap_apply_victor_rule
    
    this_ptr = transfer(this, this_ptr)
    f90wrap_apply_victor_rule = this_ptr%p%apply_victor_rule
end subroutine f90wrap_qlknn_options__get__apply_victor_rule

subroutine f90wrap_qlknn_options__set__apply_victor_rule(this, f90wrap_apply_victor_rule)
    use qlknn_types, only: qlknn_options
    implicit none
    type qlknn_options_ptr_type
        type(qlknn_options), pointer :: p => NULL()
    end type qlknn_options_ptr_type
    integer, intent(in)   :: this(2)
    type(qlknn_options_ptr_type) :: this_ptr
    logical, intent(in) :: f90wrap_apply_victor_rule
    
    this_ptr = transfer(this, this_ptr)
    this_ptr%p%apply_victor_rule = f90wrap_apply_victor_rule
end subroutine f90wrap_qlknn_options__set__apply_victor_rule

subroutine f90wrap_qlknn_options__get__use_effective_diffusivity(this, f90wrap_use_effective_diffusivity)
    use qlknn_types, only: qlknn_options
    implicit none
    type qlknn_options_ptr_type
        type(qlknn_options), pointer :: p => NULL()
    end type qlknn_options_ptr_type
    integer, intent(in)   :: this(2)
    type(qlknn_options_ptr_type) :: this_ptr
    logical, intent(out) :: f90wrap_use_effective_diffusivity
    
    this_ptr = transfer(this, this_ptr)
    f90wrap_use_effective_diffusivity = this_ptr%p%use_effective_diffusivity
end subroutine f90wrap_qlknn_options__get__use_effective_diffusivity

subroutine f90wrap_qlknn_options__set__use_effective_diffusivity(this, f90wrap_use_effective_diffusivity)
    use qlknn_types, only: qlknn_options
    implicit none
    type qlknn_options_ptr_type
        type(qlknn_options), pointer :: p => NULL()
    end type qlknn_options_ptr_type
    integer, intent(in)   :: this(2)
    type(qlknn_options_ptr_type) :: this_ptr
    logical, intent(in) :: f90wrap_use_effective_diffusivity
    
    this_ptr = transfer(this, this_ptr)
    this_ptr%p%use_effective_diffusivity = f90wrap_use_effective_diffusivity
end subroutine f90wrap_qlknn_options__set__use_effective_diffusivity

subroutine f90wrap_qlknn_options__get__calc_heat_transport(this, f90wrap_calc_heat_transport)
    use qlknn_types, only: qlknn_options
    implicit none
    type qlknn_options_ptr_type
        type(qlknn_options), pointer :: p => NULL()
    end type qlknn_options_ptr_type
    integer, intent(in)   :: this(2)
    type(qlknn_options_ptr_type) :: this_ptr
    logical, intent(out) :: f90wrap_calc_heat_transport
    
    this_ptr = transfer(this, this_ptr)
    f90wrap_calc_heat_transport = this_ptr%p%calc_heat_transport
end subroutine f90wrap_qlknn_options__get__calc_heat_transport

subroutine f90wrap_qlknn_options__set__calc_heat_transport(this, f90wrap_calc_heat_transport)
    use qlknn_types, only: qlknn_options
    implicit none
    type qlknn_options_ptr_type
        type(qlknn_options), pointer :: p => NULL()
    end type qlknn_options_ptr_type
    integer, intent(in)   :: this(2)
    type(qlknn_options_ptr_type) :: this_ptr
    logical, intent(in) :: f90wrap_calc_heat_transport
    
    this_ptr = transfer(this, this_ptr)
    this_ptr%p%calc_heat_transport = f90wrap_calc_heat_transport
end subroutine f90wrap_qlknn_options__set__calc_heat_transport

subroutine f90wrap_qlknn_options__get__calc_part_transport(this, f90wrap_calc_part_transport)
    use qlknn_types, only: qlknn_options
    implicit none
    type qlknn_options_ptr_type
        type(qlknn_options), pointer :: p => NULL()
    end type qlknn_options_ptr_type
    integer, intent(in)   :: this(2)
    type(qlknn_options_ptr_type) :: this_ptr
    logical, intent(out) :: f90wrap_calc_part_transport
    
    this_ptr = transfer(this, this_ptr)
    f90wrap_calc_part_transport = this_ptr%p%calc_part_transport
end subroutine f90wrap_qlknn_options__get__calc_part_transport

subroutine f90wrap_qlknn_options__set__calc_part_transport(this, f90wrap_calc_part_transport)
    use qlknn_types, only: qlknn_options
    implicit none
    type qlknn_options_ptr_type
        type(qlknn_options), pointer :: p => NULL()
    end type qlknn_options_ptr_type
    integer, intent(in)   :: this(2)
    type(qlknn_options_ptr_type) :: this_ptr
    logical, intent(in) :: f90wrap_calc_part_transport
    
    this_ptr = transfer(this, this_ptr)
    this_ptr%p%calc_part_transport = f90wrap_calc_part_transport
end subroutine f90wrap_qlknn_options__set__calc_part_transport

subroutine f90wrap_qlknn_options__get__use_ETG(this, f90wrap_use_ETG)
    use qlknn_types, only: qlknn_options
    implicit none
    type qlknn_options_ptr_type
        type(qlknn_options), pointer :: p => NULL()
    end type qlknn_options_ptr_type
    integer, intent(in)   :: this(2)
    type(qlknn_options_ptr_type) :: this_ptr
    logical, intent(out) :: f90wrap_use_ETG
    
    this_ptr = transfer(this, this_ptr)
    f90wrap_use_ETG = this_ptr%p%use_ETG
end subroutine f90wrap_qlknn_options__get__use_ETG

subroutine f90wrap_qlknn_options__set__use_ETG(this, f90wrap_use_ETG)
    use qlknn_types, only: qlknn_options
    implicit none
    type qlknn_options_ptr_type
        type(qlknn_options), pointer :: p => NULL()
    end type qlknn_options_ptr_type
    integer, intent(in)   :: this(2)
    type(qlknn_options_ptr_type) :: this_ptr
    logical, intent(in) :: f90wrap_use_ETG
    
    this_ptr = transfer(this, this_ptr)
    this_ptr%p%use_ETG = f90wrap_use_ETG
end subroutine f90wrap_qlknn_options__set__use_ETG

subroutine f90wrap_qlknn_options__get__use_ITG(this, f90wrap_use_ITG)
    use qlknn_types, only: qlknn_options
    implicit none
    type qlknn_options_ptr_type
        type(qlknn_options), pointer :: p => NULL()
    end type qlknn_options_ptr_type
    integer, intent(in)   :: this(2)
    type(qlknn_options_ptr_type) :: this_ptr
    logical, intent(out) :: f90wrap_use_ITG
    
    this_ptr = transfer(this, this_ptr)
    f90wrap_use_ITG = this_ptr%p%use_ITG
end subroutine f90wrap_qlknn_options__get__use_ITG

subroutine f90wrap_qlknn_options__set__use_ITG(this, f90wrap_use_ITG)
    use qlknn_types, only: qlknn_options
    implicit none
    type qlknn_options_ptr_type
        type(qlknn_options), pointer :: p => NULL()
    end type qlknn_options_ptr_type
    integer, intent(in)   :: this(2)
    type(qlknn_options_ptr_type) :: this_ptr
    logical, intent(in) :: f90wrap_use_ITG
    
    this_ptr = transfer(this, this_ptr)
    this_ptr%p%use_ITG = f90wrap_use_ITG
end subroutine f90wrap_qlknn_options__set__use_ITG

subroutine f90wrap_qlknn_options__get__use_TEM(this, f90wrap_use_TEM)
    use qlknn_types, only: qlknn_options
    implicit none
    type qlknn_options_ptr_type
        type(qlknn_options), pointer :: p => NULL()
    end type qlknn_options_ptr_type
    integer, intent(in)   :: this(2)
    type(qlknn_options_ptr_type) :: this_ptr
    logical, intent(out) :: f90wrap_use_TEM
    
    this_ptr = transfer(this, this_ptr)
    f90wrap_use_TEM = this_ptr%p%use_TEM
end subroutine f90wrap_qlknn_options__get__use_TEM

subroutine f90wrap_qlknn_options__set__use_TEM(this, f90wrap_use_TEM)
    use qlknn_types, only: qlknn_options
    implicit none
    type qlknn_options_ptr_type
        type(qlknn_options), pointer :: p => NULL()
    end type qlknn_options_ptr_type
    integer, intent(in)   :: this(2)
    type(qlknn_options_ptr_type) :: this_ptr
    logical, intent(in) :: f90wrap_use_TEM
    
    this_ptr = transfer(this, this_ptr)
    this_ptr%p%use_TEM = f90wrap_use_TEM
end subroutine f90wrap_qlknn_options__set__use_TEM

subroutine f90wrap_qlknn_options__get__apply_stability_clipping(this, f90wrap_apply_stability_clipping)
    use qlknn_types, only: qlknn_options
    implicit none
    type qlknn_options_ptr_type
        type(qlknn_options), pointer :: p => NULL()
    end type qlknn_options_ptr_type
    integer, intent(in)   :: this(2)
    type(qlknn_options_ptr_type) :: this_ptr
    logical, intent(out) :: f90wrap_apply_stability_clipping
    
    this_ptr = transfer(this, this_ptr)
    f90wrap_apply_stability_clipping = this_ptr%p%apply_stability_clipping
end subroutine f90wrap_qlknn_options__get__apply_stability_clipping

subroutine f90wrap_qlknn_options__set__apply_stability_clipping(this, f90wrap_apply_stability_clipping)
    use qlknn_types, only: qlknn_options
    implicit none
    type qlknn_options_ptr_type
        type(qlknn_options), pointer :: p => NULL()
    end type qlknn_options_ptr_type
    integer, intent(in)   :: this(2)
    type(qlknn_options_ptr_type) :: this_ptr
    logical, intent(in) :: f90wrap_apply_stability_clipping
    
    this_ptr = transfer(this, this_ptr)
    this_ptr%p%apply_stability_clipping = f90wrap_apply_stability_clipping
end subroutine f90wrap_qlknn_options__set__apply_stability_clipping

subroutine f90wrap_qlknn_options__array__constrain_inputs(this, nd, dtype, dshape, dloc)
    use qlknn_types, only: qlknn_options
    implicit none
    type qlknn_options_ptr_type
        type(qlknn_options), pointer :: p => NULL()
    end type qlknn_options_ptr_type
    integer, intent(in) :: this(2)
    type(qlknn_options_ptr_type) :: this_ptr
    integer, intent(out) :: nd
    integer, intent(out) :: dtype
    integer, dimension(10), intent(out) :: dshape
    integer*8, intent(out) :: dloc
    
    nd = 1
    dtype = 5
    this_ptr = transfer(this, this_ptr)
    if (allocated(this_ptr%p%constrain_inputs)) then
        dshape(1:1) = shape(this_ptr%p%constrain_inputs)
        dloc = loc(this_ptr%p%constrain_inputs)
    else
        dloc = 0
    end if
end subroutine f90wrap_qlknn_options__array__constrain_inputs

subroutine f90wrap_qlknn_options__array__min_input(this, nd, dtype, dshape, dloc)
    use qlknn_types, only: qlknn_options
    implicit none
    type qlknn_options_ptr_type
        type(qlknn_options), pointer :: p => NULL()
    end type qlknn_options_ptr_type
    integer, intent(in) :: this(2)
    type(qlknn_options_ptr_type) :: this_ptr
    integer, intent(out) :: nd
    integer, intent(out) :: dtype
    integer, dimension(10), intent(out) :: dshape
    integer*8, intent(out) :: dloc
    
    nd = 1
    dtype = 12
    this_ptr = transfer(this, this_ptr)
    if (allocated(this_ptr%p%min_input)) then
        dshape(1:1) = shape(this_ptr%p%min_input)
        dloc = loc(this_ptr%p%min_input)
    else
        dloc = 0
    end if
end subroutine f90wrap_qlknn_options__array__min_input

subroutine f90wrap_qlknn_options__array__max_input(this, nd, dtype, dshape, dloc)
    use qlknn_types, only: qlknn_options
    implicit none
    type qlknn_options_ptr_type
        type(qlknn_options), pointer :: p => NULL()
    end type qlknn_options_ptr_type
    integer, intent(in) :: this(2)
    type(qlknn_options_ptr_type) :: this_ptr
    integer, intent(out) :: nd
    integer, intent(out) :: dtype
    integer, dimension(10), intent(out) :: dshape
    integer*8, intent(out) :: dloc
    
    nd = 1
    dtype = 12
    this_ptr = transfer(this, this_ptr)
    if (allocated(this_ptr%p%max_input)) then
        dshape(1:1) = shape(this_ptr%p%max_input)
        dloc = loc(this_ptr%p%max_input)
    else
        dloc = 0
    end if
end subroutine f90wrap_qlknn_options__array__max_input

subroutine f90wrap_qlknn_options__array__margin_input(this, nd, dtype, dshape, dloc)
    use qlknn_types, only: qlknn_options
    implicit none
    type qlknn_options_ptr_type
        type(qlknn_options), pointer :: p => NULL()
    end type qlknn_options_ptr_type
    integer, intent(in) :: this(2)
    type(qlknn_options_ptr_type) :: this_ptr
    integer, intent(out) :: nd
    integer, intent(out) :: dtype
    integer, dimension(10), intent(out) :: dshape
    integer*8, intent(out) :: dloc
    
    nd = 1
    dtype = 12
    this_ptr = transfer(this, this_ptr)
    if (allocated(this_ptr%p%margin_input)) then
        dshape(1:1) = shape(this_ptr%p%margin_input)
        dloc = loc(this_ptr%p%margin_input)
    else
        dloc = 0
    end if
end subroutine f90wrap_qlknn_options__array__margin_input

subroutine f90wrap_qlknn_options__array__constrain_outputs(this, nd, dtype, dshape, dloc)
    use qlknn_types, only: qlknn_options
    implicit none
    type qlknn_options_ptr_type
        type(qlknn_options), pointer :: p => NULL()
    end type qlknn_options_ptr_type
    integer, intent(in) :: this(2)
    type(qlknn_options_ptr_type) :: this_ptr
    integer, intent(out) :: nd
    integer, intent(out) :: dtype
    integer, dimension(10), intent(out) :: dshape
    integer*8, intent(out) :: dloc
    
    nd = 1
    dtype = 5
    this_ptr = transfer(this, this_ptr)
    if (allocated(this_ptr%p%constrain_outputs)) then
        dshape(1:1) = shape(this_ptr%p%constrain_outputs)
        dloc = loc(this_ptr%p%constrain_outputs)
    else
        dloc = 0
    end if
end subroutine f90wrap_qlknn_options__array__constrain_outputs

subroutine f90wrap_qlknn_options__array__min_output(this, nd, dtype, dshape, dloc)
    use qlknn_types, only: qlknn_options
    implicit none
    type qlknn_options_ptr_type
        type(qlknn_options), pointer :: p => NULL()
    end type qlknn_options_ptr_type
    integer, intent(in) :: this(2)
    type(qlknn_options_ptr_type) :: this_ptr
    integer, intent(out) :: nd
    integer, intent(out) :: dtype
    integer, dimension(10), intent(out) :: dshape
    integer*8, intent(out) :: dloc
    
    nd = 1
    dtype = 12
    this_ptr = transfer(this, this_ptr)
    if (allocated(this_ptr%p%min_output)) then
        dshape(1:1) = shape(this_ptr%p%min_output)
        dloc = loc(this_ptr%p%min_output)
    else
        dloc = 0
    end if
end subroutine f90wrap_qlknn_options__array__min_output

subroutine f90wrap_qlknn_options__array__max_output(this, nd, dtype, dshape, dloc)
    use qlknn_types, only: qlknn_options
    implicit none
    type qlknn_options_ptr_type
        type(qlknn_options), pointer :: p => NULL()
    end type qlknn_options_ptr_type
    integer, intent(in) :: this(2)
    type(qlknn_options_ptr_type) :: this_ptr
    integer, intent(out) :: nd
    integer, intent(out) :: dtype
    integer, dimension(10), intent(out) :: dshape
    integer*8, intent(out) :: dloc
    
    nd = 1
    dtype = 12
    this_ptr = transfer(this, this_ptr)
    if (allocated(this_ptr%p%max_output)) then
        dshape(1:1) = shape(this_ptr%p%max_output)
        dloc = loc(this_ptr%p%max_output)
    else
        dloc = 0
    end if
end subroutine f90wrap_qlknn_options__array__max_output

subroutine f90wrap_qlknn_options__array__margin_output(this, nd, dtype, dshape, dloc)
    use qlknn_types, only: qlknn_options
    implicit none
    type qlknn_options_ptr_type
        type(qlknn_options), pointer :: p => NULL()
    end type qlknn_options_ptr_type
    integer, intent(in) :: this(2)
    type(qlknn_options_ptr_type) :: this_ptr
    integer, intent(out) :: nd
    integer, intent(out) :: dtype
    integer, dimension(10), intent(out) :: dshape
    integer*8, intent(out) :: dloc
    
    nd = 1
    dtype = 12
    this_ptr = transfer(this, this_ptr)
    if (allocated(this_ptr%p%margin_output)) then
        dshape(1:1) = shape(this_ptr%p%margin_output)
        dloc = loc(this_ptr%p%margin_output)
    else
        dloc = 0
    end if
end subroutine f90wrap_qlknn_options__array__margin_output

subroutine f90wrap_qlknn_options__get__merge_modes(this, f90wrap_merge_modes)
    use qlknn_types, only: qlknn_options
    implicit none
    type qlknn_options_ptr_type
        type(qlknn_options), pointer :: p => NULL()
    end type qlknn_options_ptr_type
    integer, intent(in)   :: this(2)
    type(qlknn_options_ptr_type) :: this_ptr
    logical, intent(out) :: f90wrap_merge_modes
    
    this_ptr = transfer(this, this_ptr)
    f90wrap_merge_modes = this_ptr%p%merge_modes
end subroutine f90wrap_qlknn_options__get__merge_modes

subroutine f90wrap_qlknn_options__set__merge_modes(this, f90wrap_merge_modes)
    use qlknn_types, only: qlknn_options
    implicit none
    type qlknn_options_ptr_type
        type(qlknn_options), pointer :: p => NULL()
    end type qlknn_options_ptr_type
    integer, intent(in)   :: this(2)
    type(qlknn_options_ptr_type) :: this_ptr
    logical, intent(in) :: f90wrap_merge_modes
    
    this_ptr = transfer(this, this_ptr)
    this_ptr%p%merge_modes = f90wrap_merge_modes
end subroutine f90wrap_qlknn_options__set__merge_modes

subroutine f90wrap_qlknn_options__get__force_evaluate_all(this, f90wrap_force_evaluate_all)
    use qlknn_types, only: qlknn_options
    implicit none
    type qlknn_options_ptr_type
        type(qlknn_options), pointer :: p => NULL()
    end type qlknn_options_ptr_type
    integer, intent(in)   :: this(2)
    type(qlknn_options_ptr_type) :: this_ptr
    logical, intent(out) :: f90wrap_force_evaluate_all
    
    this_ptr = transfer(this, this_ptr)
    f90wrap_force_evaluate_all = this_ptr%p%force_evaluate_all
end subroutine f90wrap_qlknn_options__get__force_evaluate_all

subroutine f90wrap_qlknn_options__set__force_evaluate_all(this, f90wrap_force_evaluate_all)
    use qlknn_types, only: qlknn_options
    implicit none
    type qlknn_options_ptr_type
        type(qlknn_options), pointer :: p => NULL()
    end type qlknn_options_ptr_type
    integer, intent(in)   :: this(2)
    type(qlknn_options_ptr_type) :: this_ptr
    logical, intent(in) :: f90wrap_force_evaluate_all
    
    this_ptr = transfer(this, this_ptr)
    this_ptr%p%force_evaluate_all = f90wrap_force_evaluate_all
end subroutine f90wrap_qlknn_options__set__force_evaluate_all

subroutine f90wrap_qlknn_options_initialise(this)
    use qlknn_types, only: qlknn_options
    implicit none
    
    type qlknn_options_ptr_type
        type(qlknn_options), pointer :: p => NULL()
    end type qlknn_options_ptr_type
    type(qlknn_options_ptr_type) :: this_ptr
    integer, intent(out), dimension(2) :: this
    allocate(this_ptr%p)
    this = transfer(this_ptr, this)
end subroutine f90wrap_qlknn_options_initialise

subroutine f90wrap_qlknn_options_finalise(this)
    use qlknn_types, only: qlknn_options
    implicit none
    
    type qlknn_options_ptr_type
        type(qlknn_options), pointer :: p => NULL()
    end type qlknn_options_ptr_type
    type(qlknn_options_ptr_type) :: this_ptr
    integer, intent(in), dimension(2) :: this
    this_ptr = transfer(this, this_ptr)
    deallocate(this_ptr%p)
end subroutine f90wrap_qlknn_options_finalise

subroutine f90wrap_qlknn_normpars__get__a(this, f90wrap_a)
    use qlknn_types, only: qlknn_normpars
    implicit none
    type qlknn_normpars_ptr_type
        type(qlknn_normpars), pointer :: p => NULL()
    end type qlknn_normpars_ptr_type
    integer, intent(in)   :: this(2)
    type(qlknn_normpars_ptr_type) :: this_ptr
    real(8), intent(out) :: f90wrap_a
    
    this_ptr = transfer(this, this_ptr)
    f90wrap_a = this_ptr%p%a
end subroutine f90wrap_qlknn_normpars__get__a

subroutine f90wrap_qlknn_normpars__set__a(this, f90wrap_a)
    use qlknn_types, only: qlknn_normpars
    implicit none
    type qlknn_normpars_ptr_type
        type(qlknn_normpars), pointer :: p => NULL()
    end type qlknn_normpars_ptr_type
    integer, intent(in)   :: this(2)
    type(qlknn_normpars_ptr_type) :: this_ptr
    real(8), intent(in) :: f90wrap_a
    
    this_ptr = transfer(this, this_ptr)
    this_ptr%p%a = f90wrap_a
end subroutine f90wrap_qlknn_normpars__set__a

subroutine f90wrap_qlknn_normpars__get__R0(this, f90wrap_R0)
    use qlknn_types, only: qlknn_normpars
    implicit none
    type qlknn_normpars_ptr_type
        type(qlknn_normpars), pointer :: p => NULL()
    end type qlknn_normpars_ptr_type
    integer, intent(in)   :: this(2)
    type(qlknn_normpars_ptr_type) :: this_ptr
    real(8), intent(out) :: f90wrap_R0
    
    this_ptr = transfer(this, this_ptr)
    f90wrap_R0 = this_ptr%p%R0
end subroutine f90wrap_qlknn_normpars__get__R0

subroutine f90wrap_qlknn_normpars__set__R0(this, f90wrap_R0)
    use qlknn_types, only: qlknn_normpars
    implicit none
    type qlknn_normpars_ptr_type
        type(qlknn_normpars), pointer :: p => NULL()
    end type qlknn_normpars_ptr_type
    integer, intent(in)   :: this(2)
    type(qlknn_normpars_ptr_type) :: this_ptr
    real(8), intent(in) :: f90wrap_R0
    
    this_ptr = transfer(this, this_ptr)
    this_ptr%p%R0 = f90wrap_R0
end subroutine f90wrap_qlknn_normpars__set__R0

subroutine f90wrap_qlknn_normpars__array__A1(this, nd, dtype, dshape, dloc)
    use qlknn_types, only: qlknn_normpars
    implicit none
    type qlknn_normpars_ptr_type
        type(qlknn_normpars), pointer :: p => NULL()
    end type qlknn_normpars_ptr_type
    integer, intent(in) :: this(2)
    type(qlknn_normpars_ptr_type) :: this_ptr
    integer, intent(out) :: nd
    integer, intent(out) :: dtype
    integer, dimension(10), intent(out) :: dshape
    integer*8, intent(out) :: dloc
    
    nd = 1
    dtype = 12
    this_ptr = transfer(this, this_ptr)
    if (allocated(this_ptr%p%A1)) then
        dshape(1:1) = shape(this_ptr%p%A1)
        dloc = loc(this_ptr%p%A1)
    else
        dloc = 0
    end if
end subroutine f90wrap_qlknn_normpars__array__A1

subroutine f90wrap_qlknn_normpars_allocate(qlknn_norms, nrho)
    use qlknn_types, only: qlknn_normpars_allocate, qlknn_normpars
    implicit none
    
    type qlknn_normpars_ptr_type
        type(qlknn_normpars), pointer :: p => NULL()
    end type qlknn_normpars_ptr_type
    type(qlknn_normpars_ptr_type) :: qlknn_norms_ptr
    integer, intent(out), dimension(2) :: qlknn_norms
    integer :: nrho
    allocate(qlknn_norms_ptr%p)
    call qlknn_normpars_allocate(qlknn_norms=qlknn_norms_ptr%p, nrho=nrho)
    qlknn_norms = transfer(qlknn_norms_ptr, qlknn_norms)
end subroutine f90wrap_qlknn_normpars_allocate

subroutine f90wrap_qlknn_normpars_deallocate(qlknn_norms)
    use qlknn_types, only: qlknn_normpars_deallocate, qlknn_normpars
    implicit none
    
    type qlknn_normpars_ptr_type
        type(qlknn_normpars), pointer :: p => NULL()
    end type qlknn_normpars_ptr_type
    type(qlknn_normpars_ptr_type) :: qlknn_norms_ptr
    integer, intent(in), dimension(2) :: qlknn_norms
    qlknn_norms_ptr = transfer(qlknn_norms, qlknn_norms_ptr)
    call qlknn_normpars_deallocate(qlknn_norms=qlknn_norms_ptr%p)
    deallocate(qlknn_norms_ptr%p)
end subroutine f90wrap_qlknn_normpars_deallocate

subroutine f90wrap_default_qlknn_hyper_options(opts)
    use qlknn_types, only: qlknn_options, default_qlknn_hyper_options
    implicit none
    
    type qlknn_options_ptr_type
        type(qlknn_options), pointer :: p => NULL()
    end type qlknn_options_ptr_type
    type(qlknn_options_ptr_type) :: opts_ptr
    integer, intent(out), dimension(2) :: opts
    allocate(opts_ptr%p)
    call default_qlknn_hyper_options(opts=opts_ptr%p)
    opts = transfer(opts_ptr, opts)
end subroutine f90wrap_default_qlknn_hyper_options

subroutine f90wrap_default_qlknn_fullflux_options(opts)
    use qlknn_types, only: qlknn_options, default_qlknn_fullflux_options
    implicit none
    
    type qlknn_options_ptr_type
        type(qlknn_options), pointer :: p => NULL()
    end type qlknn_options_ptr_type
    type(qlknn_options_ptr_type) :: opts_ptr
    integer, intent(out), dimension(2) :: opts
    allocate(opts_ptr%p)
    call default_qlknn_fullflux_options(opts=opts_ptr%p)
    opts = transfer(opts_ptr, opts)
end subroutine f90wrap_default_qlknn_fullflux_options

subroutine f90wrap_default_qlknn_jetexp_options(opts)
    use qlknn_types, only: default_qlknn_jetexp_options, qlknn_options
    implicit none
    
    type qlknn_options_ptr_type
        type(qlknn_options), pointer :: p => NULL()
    end type qlknn_options_ptr_type
    type(qlknn_options_ptr_type) :: opts_ptr
    integer, intent(out), dimension(2) :: opts
    allocate(opts_ptr%p)
    call default_qlknn_jetexp_options(opts=opts_ptr%p)
    opts = transfer(opts_ptr, opts)
end subroutine f90wrap_default_qlknn_jetexp_options

subroutine f90wrap_default_qlknn_hornnet_options(opts)
    use qlknn_types, only: qlknn_options, default_qlknn_hornnet_options
    implicit none
    
    type qlknn_options_ptr_type
        type(qlknn_options), pointer :: p => NULL()
    end type qlknn_options_ptr_type
    type(qlknn_options_ptr_type) :: opts_ptr
    integer, intent(out), dimension(2) :: opts
    allocate(opts_ptr%p)
    call default_qlknn_hornnet_options(opts=opts_ptr%p)
    opts = transfer(opts_ptr, opts)
end subroutine f90wrap_default_qlknn_hornnet_options

subroutine f90wrap_print_qlknn_options(opts)
    use qlknn_types, only: qlknn_options, print_qlknn_options
    implicit none
    
    type qlknn_options_ptr_type
        type(qlknn_options), pointer :: p => NULL()
    end type qlknn_options_ptr_type
    type(qlknn_options_ptr_type) :: opts_ptr
    integer, intent(in), dimension(2) :: opts
    opts_ptr = transfer(opts, opts_ptr)
    call print_qlknn_options(opts=opts_ptr%p)
end subroutine f90wrap_print_qlknn_options

subroutine f90wrap_get_networks_to_evaluate(opts, net_evaluate)
    use qlknn_types, only: qlknn_options, get_networks_to_evaluate
    implicit none
    
    type qlknn_options_ptr_type
        type(qlknn_options), pointer :: p => NULL()
    end type qlknn_options_ptr_type
    type(qlknn_options_ptr_type) :: opts_ptr
    integer, intent(in), dimension(2) :: opts
    logical, dimension(20), intent(inout) :: net_evaluate
    opts_ptr = transfer(opts, opts_ptr)
    call get_networks_to_evaluate(opts=opts_ptr%p, net_evaluate=net_evaluate)
end subroutine f90wrap_get_networks_to_evaluate

subroutine f90wrap_qlknn_types__get__qlknn_dp(f90wrap_qlknn_dp)
    use qlknn_types, only: qlknn_types_qlknn_dp => qlknn_dp
    implicit none
    integer, intent(out) :: f90wrap_qlknn_dp
    
    f90wrap_qlknn_dp = qlknn_types_qlknn_dp
end subroutine f90wrap_qlknn_types__get__qlknn_dp

subroutine f90wrap_qlknn_types__get__lli(f90wrap_lli)
    use qlknn_types, only: qlknn_types_lli => lli
    implicit none
    integer, intent(out) :: f90wrap_lli
    
    f90wrap_lli = qlknn_types_lli
end subroutine f90wrap_qlknn_types__get__lli

subroutine f90wrap_qlknn_types__get__li(f90wrap_li)
    use qlknn_types, only: qlknn_types_li => li
    implicit none
    integer, intent(out) :: f90wrap_li
    
    f90wrap_li = qlknn_types_li
end subroutine f90wrap_qlknn_types__get__li

subroutine f90wrap_qlknn_types__get__stderr(f90wrap_stderr)
    use qlknn_types, only: qlknn_types_stderr => stderr
    implicit none
    integer(8), intent(out) :: f90wrap_stderr
    
    f90wrap_stderr = qlknn_types_stderr
end subroutine f90wrap_qlknn_types__get__stderr

subroutine f90wrap_qlknn_types__get__qe(f90wrap_qe)
    use qlknn_types, only: qlknn_types_qe => qe
    implicit none
    real(8), intent(out) :: f90wrap_qe
    
    f90wrap_qe = qlknn_types_qe
end subroutine f90wrap_qlknn_types__get__qe

subroutine f90wrap_qlknn_types__get__mp(f90wrap_mp)
    use qlknn_types, only: qlknn_types_mp => mp
    implicit none
    real(8), intent(out) :: f90wrap_mp
    
    f90wrap_mp = qlknn_types_mp
end subroutine f90wrap_qlknn_types__get__mp

subroutine f90wrap_qlknn_types__get__c_qlk_ref(f90wrap_c_qlk_ref)
    use qlknn_types, only: qlknn_types_c_qlk_ref => c_qlk_ref
    implicit none
    real(8), intent(out) :: f90wrap_c_qlk_ref
    
    f90wrap_c_qlk_ref = qlknn_types_c_qlk_ref
end subroutine f90wrap_qlknn_types__get__c_qlk_ref

! End of module qlknn_types defined in file /builds/qualikiz-group/QLKNN-fortran/src/core/qlknn_types.f90

