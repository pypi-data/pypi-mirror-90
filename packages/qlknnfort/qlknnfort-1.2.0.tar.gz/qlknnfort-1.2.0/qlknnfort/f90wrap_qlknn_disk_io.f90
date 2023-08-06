! Module qlknn_disk_io defined in file /builds/qualikiz-group/QLKNN-fortran/src/core/qlknn_disk_io.f90

subroutine f90wrap_load_qlknn_hyper_nets_from_disk(folder, verbosityin)
    use qlknn_disk_io, only: load_qlknn_hyper_nets_from_disk
    implicit none
    
    character(*), intent(in) :: folder
    integer(8), optional, intent(in) :: verbosityin
    call load_qlknn_hyper_nets_from_disk(folder=folder, verbosityin=verbosityin)
end subroutine f90wrap_load_qlknn_hyper_nets_from_disk

subroutine f90wrap_load_fullflux_nets_from_disk(folder, verbosityin)
    use qlknn_disk_io, only: load_fullflux_nets_from_disk
    implicit none
    
    character(*), intent(in) :: folder
    integer(8), optional, intent(in) :: verbosityin
    call load_fullflux_nets_from_disk(folder=folder, verbosityin=verbosityin)
end subroutine f90wrap_load_fullflux_nets_from_disk

subroutine f90wrap_load_jetexp_nets_from_disk(folder, n_members, verbosityin)
    use qlknn_disk_io, only: load_jetexp_nets_from_disk
    implicit none
    
    character(*), intent(in) :: folder
    integer(8), intent(in) :: n_members
    integer(8), optional, intent(in) :: verbosityin
    call load_jetexp_nets_from_disk(folder=folder, n_members=n_members, verbosityin=verbosityin)
end subroutine f90wrap_load_jetexp_nets_from_disk

subroutine f90wrap_load_hornnet_nets_from_disk(folder, verbosityin)
    use qlknn_disk_io, only: load_hornnet_nets_from_disk
    implicit none
    
    character(*), intent(in) :: folder
    integer(8), optional, intent(in) :: verbosityin
    call load_hornnet_nets_from_disk(folder=folder, verbosityin=verbosityin)
end subroutine f90wrap_load_hornnet_nets_from_disk

subroutine f90wrap_load_multinet_from_disk(netlist, folder, verbosityin, stylein, n0)
    use qlknn_disk_io, only: load_multinet_from_disk
    implicit none
    
    character(*), intent(in), dimension(n0) :: netlist
    character(*), intent(in) :: folder
    integer(8), optional, intent(in) :: verbosityin
    integer(8), optional, intent(in) :: stylein
    integer :: n0
    !f2py intent(hide), depend(netlist) :: n0 = shape(netlist,0)
    call load_multinet_from_disk(netlist=netlist, folder=folder, verbosityin=verbosityin, stylein=stylein)
end subroutine f90wrap_load_multinet_from_disk

subroutine f90wrap_load_net_from_disk(filename, net)
    use qlknn_types, only: networktype
    use qlknn_disk_io, only: load_net_from_disk
    implicit none
    
    type networktype_ptr_type
        type(networktype), pointer :: p => NULL()
    end type networktype_ptr_type
    character(*), intent(in) :: filename
    type(networktype_ptr_type) :: net_ptr
    integer, intent(out), dimension(2) :: net
    allocate(net_ptr%p)
    call load_net_from_disk(filename=filename, net=net_ptr%p)
    net = transfer(net_ptr, net)
end subroutine f90wrap_load_net_from_disk

subroutine f90wrap_load_hornnet_output_block_from_disk(filename, output_block)
    use qlknn_disk_io, only: load_hornnet_output_block_from_disk
    use qlknn_types, only: hornnet_output_block
    implicit none
    
    type hornnet_output_block_ptr_type
        type(hornnet_output_block), pointer :: p => NULL()
    end type hornnet_output_block_ptr_type
    character(*), intent(in) :: filename
    type(hornnet_output_block_ptr_type) :: output_block_ptr
    integer, intent(out), dimension(2) :: output_block
    allocate(output_block_ptr%p)
    call load_hornnet_output_block_from_disk(filename=filename, output_block=output_block_ptr%p)
    output_block = transfer(output_block_ptr, output_block)
end subroutine f90wrap_load_hornnet_output_block_from_disk

subroutine f90wrap_load_hornnet_input_block_from_disk(filename, input_block)
    use qlknn_types, only: hornnet_input_block
    use qlknn_disk_io, only: load_hornnet_input_block_from_disk
    implicit none
    
    type hornnet_input_block_ptr_type
        type(hornnet_input_block), pointer :: p => NULL()
    end type hornnet_input_block_ptr_type
    character(*), intent(in) :: filename
    type(hornnet_input_block_ptr_type) :: input_block_ptr
    integer, intent(out), dimension(2) :: input_block
    allocate(input_block_ptr%p)
    call load_hornnet_input_block_from_disk(filename=filename, input_block=input_block_ptr%p)
    input_block = transfer(input_block_ptr, input_block)
end subroutine f90wrap_load_hornnet_input_block_from_disk

subroutine f90wrap_qlknn_disk_io__get__nets(f90wrap_nets)
    use qlknn_types, only: net_collection
    use qlknn_disk_io, only: qlknn_disk_io_nets => nets
    implicit none
    type net_collection_ptr_type
        type(net_collection), pointer :: p => NULL()
    end type net_collection_ptr_type
    integer, intent(out) :: f90wrap_nets(2)
    type(net_collection_ptr_type) :: nets_ptr
    
    nets_ptr%p => qlknn_disk_io_nets
    f90wrap_nets = transfer(nets_ptr,f90wrap_nets)
end subroutine f90wrap_qlknn_disk_io__get__nets

subroutine f90wrap_qlknn_disk_io__set__nets(f90wrap_nets)
    use qlknn_types, only: net_collection
    use qlknn_disk_io, only: qlknn_disk_io_nets => nets
    implicit none
    type net_collection_ptr_type
        type(net_collection), pointer :: p => NULL()
    end type net_collection_ptr_type
    integer, intent(in) :: f90wrap_nets(2)
    type(net_collection_ptr_type) :: nets_ptr
    
    nets_ptr = transfer(f90wrap_nets,nets_ptr)
    qlknn_disk_io_nets = nets_ptr%p
end subroutine f90wrap_qlknn_disk_io__set__nets

subroutine f90wrap_qlknn_disk_io__get__blocks(f90wrap_blocks)
    use qlknn_types, only: block_collection
    use qlknn_disk_io, only: qlknn_disk_io_blocks => blocks
    implicit none
    type block_collection_ptr_type
        type(block_collection), pointer :: p => NULL()
    end type block_collection_ptr_type
    integer, intent(out) :: f90wrap_blocks(2)
    type(block_collection_ptr_type) :: blocks_ptr
    
    blocks_ptr%p => qlknn_disk_io_blocks
    f90wrap_blocks = transfer(blocks_ptr,f90wrap_blocks)
end subroutine f90wrap_qlknn_disk_io__get__blocks

subroutine f90wrap_qlknn_disk_io__set__blocks(f90wrap_blocks)
    use qlknn_types, only: block_collection
    use qlknn_disk_io, only: qlknn_disk_io_blocks => blocks
    implicit none
    type block_collection_ptr_type
        type(block_collection), pointer :: p => NULL()
    end type block_collection_ptr_type
    integer, intent(in) :: f90wrap_blocks(2)
    type(block_collection_ptr_type) :: blocks_ptr
    
    blocks_ptr = transfer(f90wrap_blocks,blocks_ptr)
    qlknn_disk_io_blocks = blocks_ptr%p
end subroutine f90wrap_qlknn_disk_io__set__blocks

! End of module qlknn_disk_io defined in file /builds/qualikiz-group/QLKNN-fortran/src/core/qlknn_disk_io.f90

