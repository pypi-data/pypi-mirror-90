from __future__ import print_function, absolute_import, division
import _qlknn_f90wrap
import f90wrap.runtime
import logging

class Qlknn_Disk_Io(f90wrap.runtime.FortranModule):
    """
    Module qlknn_disk_io
    
    
    Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_disk_io.f90 lines 3-523
    
    """
    @staticmethod
    def load_qlknn_hyper_nets_from_disk(folder, verbosityin=None):
        """
        load_qlknn_hyper_nets_from_disk(folder[, verbosityin])
        
        
        Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_disk_io.f90 lines 83-117
        
        Parameters
        ----------
        folder : str
        verbosityin : int
        
        """
        _qlknn_f90wrap.f90wrap_load_qlknn_hyper_nets_from_disk(folder=folder, \
            verbosityin=verbosityin)
    
    @staticmethod
    def load_fullflux_nets_from_disk(folder, verbosityin=None):
        """
        load_fullflux_nets_from_disk(folder[, verbosityin])
        
        
        Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_disk_io.f90 lines 119-153
        
        Parameters
        ----------
        folder : str
        verbosityin : int
        
        """
        _qlknn_f90wrap.f90wrap_load_fullflux_nets_from_disk(folder=folder, \
            verbosityin=verbosityin)
    
    @staticmethod
    def load_jetexp_nets_from_disk(folder, n_members, verbosityin=None):
        """
        load_jetexp_nets_from_disk(folder, n_members[, verbosityin])
        
        
        Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_disk_io.f90 lines 155-206
        
        Parameters
        ----------
        folder : str
        n_members : int
        verbosityin : int
        
        """
        _qlknn_f90wrap.f90wrap_load_jetexp_nets_from_disk(folder=folder, n_members=n_members, \
            verbosityin=verbosityin)
    
    @staticmethod
    def load_hornnet_nets_from_disk(folder, verbosityin=None):
        """
        load_hornnet_nets_from_disk(folder[, verbosityin])
        
        
        Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_disk_io.f90 lines 208-245
        
        Parameters
        ----------
        folder : str
        verbosityin : int
        
        """
        _qlknn_f90wrap.f90wrap_load_hornnet_nets_from_disk(folder=folder, verbosityin=verbosityin)
    
    @staticmethod
    def load_multinet_from_disk(netlist, folder, verbosityin=None, stylein=None):
        """
        load_multinet_from_disk(netlist, folder[, verbosityin, stylein])
        
        
        Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_disk_io.f90 lines 247-292
        
        Parameters
        ----------
        netlist : str array
        folder : str
        verbosityin : int
        stylein : int
        
        """
        _qlknn_f90wrap.f90wrap_load_multinet_from_disk(netlist=netlist, folder=folder, \
            verbosityin=verbosityin, stylein=stylein)
    
    @staticmethod
    def load_net_from_disk(filename):
        """
        net = load_net_from_disk(filename)
        
        
        Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_disk_io.f90 lines 294-423
        
        Parameters
        ----------
        filename : str
        
        Returns
        -------
        net : Networktype
        
        """
        net = _qlknn_f90wrap.f90wrap_load_net_from_disk(filename=filename)
        net = f90wrap.runtime.lookup_class("qlknn_f90wrap.networktype").from_handle(net)
        return net
    
    @staticmethod
    def load_hornnet_output_block_from_disk(filename):
        """
        output_block = load_hornnet_output_block_from_disk(filename)
        
        
        Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_disk_io.f90 lines 425-482
        
        Parameters
        ----------
        filename : str
        
        Returns
        -------
        output_block : Hornnet_Output_Block
        
        """
        output_block = \
            _qlknn_f90wrap.f90wrap_load_hornnet_output_block_from_disk(filename=filename)
        output_block = \
            f90wrap.runtime.lookup_class("qlknn_f90wrap.hornnet_output_block").from_handle(output_block)
        return output_block
    
    @staticmethod
    def load_hornnet_input_block_from_disk(filename):
        """
        input_block = load_hornnet_input_block_from_disk(filename)
        
        
        Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_disk_io.f90 lines 484-523
        
        Parameters
        ----------
        filename : str
        
        Returns
        -------
        input_block : Hornnet_Input_Block
        
        """
        input_block = _qlknn_f90wrap.f90wrap_load_hornnet_input_block_from_disk(filename=filename)
        input_block = \
            f90wrap.runtime.lookup_class("qlknn_f90wrap.hornnet_input_block").from_handle(input_block)
        return input_block
    
    @property
    def nets(self):
        """
        Element nets ftype=type(net_collection) pytype=Net_Collection
        
        
        Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_disk_io.f90 line 80
        
        """
        nets_handle = _qlknn_f90wrap.f90wrap_qlknn_disk_io__get__nets()
        if tuple(nets_handle) in self._objs:
            nets = self._objs[tuple(nets_handle)]
        else:
            nets = qlknn_types.net_collection.from_handle(nets_handle)
            self._objs[tuple(nets_handle)] = nets
        return nets
    
    @nets.setter
    def nets(self, nets):
        nets = nets._handle
        _qlknn_f90wrap.f90wrap_qlknn_disk_io__set__nets(nets)
    
    @property
    def blocks(self):
        """
        Element blocks ftype=type(block_collection) pytype=Block_Collection
        
        
        Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_disk_io.f90 line 81
        
        """
        blocks_handle = _qlknn_f90wrap.f90wrap_qlknn_disk_io__get__blocks()
        if tuple(blocks_handle) in self._objs:
            blocks = self._objs[tuple(blocks_handle)]
        else:
            blocks = qlknn_types.block_collection.from_handle(blocks_handle)
            self._objs[tuple(blocks_handle)] = blocks
        return blocks
    
    @blocks.setter
    def blocks(self, blocks):
        blocks = blocks._handle
        _qlknn_f90wrap.f90wrap_qlknn_disk_io__set__blocks(blocks)
    
    def __str__(self):
        ret = ['<qlknn_disk_io>{\n']
        ret.append('    nets : ')
        ret.append(repr(self.nets))
        ret.append(',\n    blocks : ')
        ret.append(repr(self.blocks))
        ret.append('}')
        return ''.join(ret)
    
    _dt_array_initialisers = []
    

qlknn_disk_io = Qlknn_Disk_Io()

class Qlknn_Primitives(f90wrap.runtime.FortranModule):
    """
    Module qlknn_primitives
    
    
    Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_primitives.f90 lines 3-1033
    
    """
    @staticmethod
    def evaluate_network(input, net, output_1d, verbosityin=None, dnet_out1d_dinput=None):
        """
        evaluate_network(input, net, output_1d[, verbosityin, dnet_out1d_dinput])
        
        
        Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_primitives.f90 lines 26-218
        
        Parameters
        ----------
        input : float array
        net : Networktype
        output_1d : float array
        verbosityin : int
        dnet_out1d_dinput : float array
        
        ----------------------------
         Apply input layer
        """
        _qlknn_f90wrap.f90wrap_evaluate_network(input=input, net=net._handle, output_1d=output_1d, \
            verbosityin=verbosityin, dnet_out1d_dinput=dnet_out1d_dinput)
    
    @staticmethod
    def evaluate_layer(input, weights, biases, activation_func, output, verbosityin=None, \
        doutput_dinput=None):
        """
        evaluate_layer(input, weights, biases, activation_func, output[, verbosityin, \
            doutput_dinput])
        
        
        Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_primitives.f90 lines 330-427
        
        Parameters
        ----------
        input : float array
        weights : float array
        biases : float array
        activation_func : str
        output : float array
        verbosityin : int
        doutput_dinput : float array
        
        """
        _qlknn_f90wrap.f90wrap_evaluate_layer(input=input, weights=weights, biases=biases, \
            activation_func=activation_func, output=output, verbosityin=verbosityin, \
            doutput_dinput=doutput_dinput)
    
    @staticmethod
    def impose_output_constraints(output, opts, verbosity, dnet_out_dinput=None, \
        output_eb=None):
        """
        impose_output_constraints(output, opts, verbosity[, dnet_out_dinput, output_eb])
        
        
        Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_primitives.f90 lines 429-508
        
        Parameters
        ----------
        output : float array
        opts : Qlknn_Options
        verbosity : int
        dnet_out_dinput : float array
        output_eb : float array
        
        """
        _qlknn_f90wrap.f90wrap_impose_output_constraints(output=output, opts=opts._handle, \
            verbosity=verbosity, dnet_out_dinput=dnet_out_dinput, output_eb=output_eb)
    
    @staticmethod
    def apply_stability_clipping(leading_map, net_result, verbosity):
        """
        apply_stability_clipping(leading_map, net_result, verbosity)
        
        
        Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_primitives.f90 lines 568-606
        
        Parameters
        ----------
        leading_map : int array
        net_result : float array
        verbosity : int
        
        """
        _qlknn_f90wrap.f90wrap_apply_stability_clipping(leading_map=leading_map, \
            net_result=net_result, verbosity=verbosity)
    
    @staticmethod
    def impose_leading_flux_constraints(leading_map, net_result, verbosity, \
        dnet_out_dnet_in=None, net_eb=None):
        """
        impose_leading_flux_constraints(leading_map, net_result, verbosity[, dnet_out_dnet_in, \
            net_eb])
        
        
        Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_primitives.f90 lines 608-644
        
        Parameters
        ----------
        leading_map : int array
        net_result : float array
        verbosity : int
        dnet_out_dnet_in : float array
        net_eb : float array
        
        """
        _qlknn_f90wrap.f90wrap_impose_leading_flux_constraints(leading_map=leading_map, \
            net_result=net_result, verbosity=verbosity, dnet_out_dnet_in=dnet_out_dnet_in, \
            net_eb=net_eb)
    
    @staticmethod
    def multiply_div_networks(leading_map, net_result, verbosity, dqlknn_out_dinput=None, \
        net_eb=None):
        """
        multiply_div_networks(leading_map, net_result, verbosity[, dqlknn_out_dinput, net_eb])
        
        
        Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_primitives.f90 lines 646-722
        
        Parameters
        ----------
        leading_map : int array
        net_result : float array
        verbosity : int
        dqlknn_out_dinput : float array
        net_eb : float array
        
        """
        _qlknn_f90wrap.f90wrap_multiply_div_networks(leading_map=leading_map, \
            net_result=net_result, verbosity=verbosity, dqlknn_out_dinput=dqlknn_out_dinput, \
            net_eb=net_eb)
    
    @staticmethod
    def merge_modes(merge_map, net_result, merged_net_result, verbosity, \
        dqlknn_out_dinput=None, dqlknn_out_merged_dinput=None, net_eb=None, \
        merged_net_eb=None):
        """
        merge_modes(merge_map, net_result, merged_net_result, verbosity[, dqlknn_out_dinput, \
            dqlknn_out_merged_dinput, net_eb, merged_net_eb])
        
        
        Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_primitives.f90 lines 724-790
        
        Parameters
        ----------
        merge_map : int array
        net_result : float array
        merged_net_result : float array
        verbosity : int
        dqlknn_out_dinput : float array
        dqlknn_out_merged_dinput : float array
        net_eb : float array
        merged_net_eb : float array
        
        """
        _qlknn_f90wrap.f90wrap_merge_modes(merge_map=merge_map, net_result=net_result, \
            merged_net_result=merged_net_result, verbosity=verbosity, \
            dqlknn_out_dinput=dqlknn_out_dinput, \
            dqlknn_out_merged_dinput=dqlknn_out_merged_dinput, net_eb=net_eb, \
            merged_net_eb=merged_net_eb)
    
    @staticmethod
    def merge_committee(net_result, n_members, merged_net_result, merged_net_eb, verbosity, \
        dqlknn_out_dinput=None, dqlknn_out_merged_dinput=None):
        """
        merge_committee(net_result, n_members, merged_net_result, merged_net_eb, verbosity[, \
            dqlknn_out_dinput, dqlknn_out_merged_dinput])
        
        
        Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_primitives.f90 lines 792-854
        
        Parameters
        ----------
        net_result : float array
        n_members : int
        merged_net_result : float array
        merged_net_eb : float array
        verbosity : int
        dqlknn_out_dinput : float array
        dqlknn_out_merged_dinput : float array
        
        """
        _qlknn_f90wrap.f90wrap_merge_committee(net_result=net_result, n_members=n_members, \
            merged_net_result=merged_net_result, merged_net_eb=merged_net_eb, verbosity=verbosity, \
            dqlknn_out_dinput=dqlknn_out_dinput, \
            dqlknn_out_merged_dinput=dqlknn_out_merged_dinput)
    
    @staticmethod
    def matr_mult_elemwise(n, a, b, y):
        """
        matr_mult_elemwise(n, a, b, y)
        
        
        Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_primitives.f90 lines 856-866
        
        Parameters
        ----------
        n : int
        a : float array
        b : float array
        y : float array
        
        """
        _qlknn_f90wrap.f90wrap_matr_mult_elemwise(n=n, a=a, b=b, y=y)
    
    @staticmethod
    def matr_vec_mult_elemwise(n, a, b, y):
        """
        matr_vec_mult_elemwise(n, a, b, y)
        
        
        Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_primitives.f90 lines 868-879
        
        Parameters
        ----------
        n : int
        a : float array
        b : float array
        y : float array
        
        """
        _qlknn_f90wrap.f90wrap_matr_vec_mult_elemwise(n=n, a=a, b=b, y=y)
    
    @staticmethod
    def vdmul(n, a, b, y):
        """
        vdmul(n, a, b, y)
        
        
        Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_primitives.f90 lines 882-892
        
        Parameters
        ----------
        n : int
        a : float array
        b : float array
        y : float array
        
        """
        _qlknn_f90wrap.f90wrap_vdmul(n=n, a=a, b=b, y=y)
    
    @staticmethod
    def dgemm(transa, transb, m, n, k, alpha, a, lda, b, ldb, beta, c, ldc):
        """
        dgemm(transa, transb, m, n, k, alpha, a, lda, b, ldb, beta, c, ldc)
        
        
        Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_primitives.f90 lines 894-935
        
        Parameters
        ----------
        transa : str
        transb : str
        m : int
        n : int
        k : int
        alpha : float
        a : float array
        lda : int
        b : float array
        ldb : int
        beta : float
        c : float array
        ldc : int
        
        """
        _qlknn_f90wrap.f90wrap_dgemm(transa=transa, transb=transb, m=m, n=n, k=k, alpha=alpha, \
            a=a, lda=lda, b=b, ldb=ldb, beta=beta, c=c, ldc=ldc)
    
    @staticmethod
    def vdtanh(n, a, y):
        """
        vdtanh(n, a, y)
        
        
        Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_primitives.f90 lines 937-947
        
        Parameters
        ----------
        n : int
        a : float array
        y : float array
        
        """
        _qlknn_f90wrap.f90wrap_vdtanh(n=n, a=a, y=y)
    
    @staticmethod
    def relu(n, a, y):
        """
        relu(n, a, y)
        
        
        Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_primitives.f90 lines 950-960
        
        Parameters
        ----------
        n : int
        a : float array
        y : float array
        
        """
        _qlknn_f90wrap.f90wrap_relu(n=n, a=a, y=y)
    
    @staticmethod
    def calc_length_lli(start, end, step):
        """
        length = calc_length_lli(start, end, step)
        
        
        Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_primitives.f90 lines 962-968
        
        Parameters
        ----------
        start : int
        end : int
        step : int
        
        Returns
        -------
        length : int
        
        """
        length = _qlknn_f90wrap.f90wrap_calc_length_lli(start=start, end=end, step=step)
        return length
    
    @staticmethod
    def calc_length_li(start, end, step):
        """
        length = calc_length_li(start, end, step)
        
        
        Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_primitives.f90 lines 970-976
        
        Parameters
        ----------
        start : int
        end : int
        step : int
        
        Returns
        -------
        length : int
        
        """
        length = _qlknn_f90wrap.f90wrap_calc_length_li(start=start, end=end, step=step)
        return length
    
    @staticmethod
    def calc_length_mixed1(start, end, step):
        """
        length = calc_length_mixed1(start, end, step)
        
        
        Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_primitives.f90 lines 978-985
        
        Parameters
        ----------
        start : int
        end : int
        step : int
        
        Returns
        -------
        length : int
        
        """
        length = _qlknn_f90wrap.f90wrap_calc_length_mixed1(start=start, end=end, step=step)
        return length
    
    @staticmethod
    def calc_length_mixed2(start, end, step):
        """
        length = calc_length_mixed2(start, end, step)
        
        
        Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_primitives.f90 lines 987-994
        
        Parameters
        ----------
        start : int
        end : int
        step : int
        
        Returns
        -------
        length : int
        
        """
        length = _qlknn_f90wrap.f90wrap_calc_length_mixed2(start=start, end=end, step=step)
        return length
    
    @staticmethod
    def double_1d_0d_is_not_close(arr1, arr2, is_not_close, boundin=None):
        """
        double_1d_0d_is_not_close(arr1, arr2, is_not_close[, boundin])
        
        
        Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_primitives.f90 lines 996-1007
        
        Parameters
        ----------
        arr1 : float array
        arr2 : float
        is_not_close : bool array
        boundin : float
        
        """
        _qlknn_f90wrap.f90wrap_double_1d_0d_is_not_close(arr1=arr1, arr2=arr2, \
            is_not_close=is_not_close, boundin=boundin)
    
    @staticmethod
    def double_1d_1d_is_not_close(arr1, arr2, is_not_close, boundin=None):
        """
        double_1d_1d_is_not_close(arr1, arr2, is_not_close[, boundin])
        
        
        Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_primitives.f90 lines 1009-1020
        
        Parameters
        ----------
        arr1 : float array
        arr2 : float array
        is_not_close : bool array
        boundin : float
        
        """
        _qlknn_f90wrap.f90wrap_double_1d_1d_is_not_close(arr1=arr1, arr2=arr2, \
            is_not_close=is_not_close, boundin=boundin)
    
    @staticmethod
    def double_2d_2d_is_not_close(arr1, arr2, is_not_close, boundin=None):
        """
        double_2d_2d_is_not_close(arr1, arr2, is_not_close[, boundin])
        
        
        Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_primitives.f90 lines 1022-1033
        
        Parameters
        ----------
        arr1 : float array
        arr2 : float array
        is_not_close : bool array
        boundin : float
        
        """
        _qlknn_f90wrap.f90wrap_double_2d_2d_is_not_close(arr1=arr1, arr2=arr2, \
            is_not_close=is_not_close, boundin=boundin)
    
    _dt_array_initialisers = []
    

qlknn_primitives = Qlknn_Primitives()

class Qlknn_Types(f90wrap.runtime.FortranModule):
    """
    Module qlknn_types
    
    
    Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 lines 3-462
    
    """
    @f90wrap.runtime.register_class("qlknn_f90wrap.ragged_weights_array")
    class ragged_weights_array(f90wrap.runtime.FortranDerivedType):
        """
        Type(name=ragged_weights_array)
        
        
        Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 lines 13-14
        
        """
        def __init__(self, handle=None):
            """
            self = Ragged_Weights_Array()
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 lines 13-14
            
            
            Returns
            -------
            this : Ragged_Weights_Array
            	Object to be constructed
            
            
            Automatically generated constructor for ragged_weights_array
            """
            f90wrap.runtime.FortranDerivedType.__init__(self)
            result = _qlknn_f90wrap.f90wrap_ragged_weights_array_initialise()
            self._handle = result[0] if isinstance(result, tuple) else result
        
        def __del__(self):
            """
            Destructor for class Ragged_Weights_Array
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 lines 13-14
            
            Parameters
            ----------
            this : Ragged_Weights_Array
            	Object to be destructed
            
            
            Automatically generated destructor for ragged_weights_array
            """
            if self._alloc:
                _qlknn_f90wrap.f90wrap_ragged_weights_array_finalise(this=self._handle)
        
        @property
        def weight_layer(self):
            """
            Element weight_layer ftype=real(qlknn_dp) pytype=float
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 line 14
            
            """
            array_ndim, array_type, array_shape, array_handle = \
                _qlknn_f90wrap.f90wrap_ragged_weights_array__array__weight_layer(self._handle)
            if array_handle in self._arrays:
                weight_layer = self._arrays[array_handle]
            else:
                weight_layer = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                        self._handle,
                                        _qlknn_f90wrap.f90wrap_ragged_weights_array__array__weight_layer)
                self._arrays[array_handle] = weight_layer
            return weight_layer
        
        @weight_layer.setter
        def weight_layer(self, weight_layer):
            self.weight_layer[...] = weight_layer
        
        def __str__(self):
            ret = ['<ragged_weights_array>{\n']
            ret.append('    weight_layer : ')
            ret.append(repr(self.weight_layer))
            ret.append('}')
            return ''.join(ret)
        
        _dt_array_initialisers = []
        
    
    @f90wrap.runtime.register_class("qlknn_f90wrap.ragged_biases_array")
    class ragged_biases_array(f90wrap.runtime.FortranDerivedType):
        """
        Type(name=ragged_biases_array)
        
        
        Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 lines 16-17
        
        """
        def __init__(self, handle=None):
            """
            self = Ragged_Biases_Array()
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 lines 16-17
            
            
            Returns
            -------
            this : Ragged_Biases_Array
            	Object to be constructed
            
            
            Automatically generated constructor for ragged_biases_array
            """
            f90wrap.runtime.FortranDerivedType.__init__(self)
            result = _qlknn_f90wrap.f90wrap_ragged_biases_array_initialise()
            self._handle = result[0] if isinstance(result, tuple) else result
        
        def __del__(self):
            """
            Destructor for class Ragged_Biases_Array
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 lines 16-17
            
            Parameters
            ----------
            this : Ragged_Biases_Array
            	Object to be destructed
            
            
            Automatically generated destructor for ragged_biases_array
            """
            if self._alloc:
                _qlknn_f90wrap.f90wrap_ragged_biases_array_finalise(this=self._handle)
        
        @property
        def bias_layer(self):
            """
            Element bias_layer ftype=real(qlknn_dp) pytype=float
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 line 17
            
            """
            array_ndim, array_type, array_shape, array_handle = \
                _qlknn_f90wrap.f90wrap_ragged_biases_array__array__bias_layer(self._handle)
            if array_handle in self._arrays:
                bias_layer = self._arrays[array_handle]
            else:
                bias_layer = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                        self._handle,
                                        _qlknn_f90wrap.f90wrap_ragged_biases_array__array__bias_layer)
                self._arrays[array_handle] = bias_layer
            return bias_layer
        
        @bias_layer.setter
        def bias_layer(self, bias_layer):
            self.bias_layer[...] = bias_layer
        
        def __str__(self):
            ret = ['<ragged_biases_array>{\n']
            ret.append('    bias_layer : ')
            ret.append(repr(self.bias_layer))
            ret.append('}')
            return ''.join(ret)
        
        _dt_array_initialisers = []
        
    
    @f90wrap.runtime.register_class("qlknn_f90wrap.networktype")
    class networktype(f90wrap.runtime.FortranDerivedType):
        """
        Type(name=networktype)
        
        
        Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 lines 50-80
        
        """
        def __del__(self):
            """
            Destructor for class Networktype
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 lines 422-445
            
            Parameters
            ----------
            net : Networktype
            
            """
            if self._alloc:
                _qlknn_f90wrap.f90wrap_networktype_deallocate(net=self._handle)
        
        def __init__(self, handle=None):
            """
            self = Networktype()
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 lines 50-80
            
            
            Returns
            -------
            this : Networktype
            	Object to be constructed
            
            
            Automatically generated constructor for networktype
            """
            f90wrap.runtime.FortranDerivedType.__init__(self)
            result = _qlknn_f90wrap.f90wrap_networktype_initialise()
            self._handle = result[0] if isinstance(result, tuple) else result
        
        @property
        def n_hidden_layers(self):
            """
            Element n_hidden_layers ftype=integer(lli) pytype=int
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 line 52
            
            """
            return _qlknn_f90wrap.f90wrap_networktype__get__n_hidden_layers(self._handle)
        
        @n_hidden_layers.setter
        def n_hidden_layers(self, n_hidden_layers):
            _qlknn_f90wrap.f90wrap_networktype__set__n_hidden_layers(self._handle, n_hidden_layers)
        
        @property
        def n_max_nodes(self):
            """
            Element n_max_nodes ftype=integer(lli) pytype=int
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 line 54
            
            """
            return _qlknn_f90wrap.f90wrap_networktype__get__n_max_nodes(self._handle)
        
        @n_max_nodes.setter
        def n_max_nodes(self, n_max_nodes):
            _qlknn_f90wrap.f90wrap_networktype__set__n_max_nodes(self._handle, n_max_nodes)
        
        @property
        def weights_input(self):
            """
            Element weights_input ftype=real(qlknn_dp) pytype=float
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 line 59
            
            """
            array_ndim, array_type, array_shape, array_handle = \
                _qlknn_f90wrap.f90wrap_networktype__array__weights_input(self._handle)
            if array_handle in self._arrays:
                weights_input = self._arrays[array_handle]
            else:
                weights_input = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                        self._handle,
                                        _qlknn_f90wrap.f90wrap_networktype__array__weights_input)
                self._arrays[array_handle] = weights_input
            return weights_input
        
        @weights_input.setter
        def weights_input(self, weights_input):
            self.weights_input[...] = weights_input
        
        @property
        def biases_input(self):
            """
            Element biases_input ftype=real(qlknn_dp) pytype=float
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 line 61
            
            """
            array_ndim, array_type, array_shape, array_handle = \
                _qlknn_f90wrap.f90wrap_networktype__array__biases_input(self._handle)
            if array_handle in self._arrays:
                biases_input = self._arrays[array_handle]
            else:
                biases_input = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                        self._handle,
                                        _qlknn_f90wrap.f90wrap_networktype__array__biases_input)
                self._arrays[array_handle] = biases_input
            return biases_input
        
        @biases_input.setter
        def biases_input(self, biases_input):
            self.biases_input[...] = biases_input
        
        def init_array_weights_hidden(self):
            self.weights_hidden = f90wrap.runtime.FortranDerivedTypeArray(self,
                                            _qlknn_f90wrap.f90wrap_networktype__array_getitem__weights_hidden,
                                            _qlknn_f90wrap.f90wrap_networktype__array_setitem__weights_hidden,
                                            _qlknn_f90wrap.f90wrap_networktype__array_len__weights_hidden,
                                            """
            Element weights_hidden ftype=type(ragged_weights_array) pytype=Ragged_Weights_Array
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 line 63
            
            """, qlknn_types.ragged_weights_array)
            return self.weights_hidden
        
        def init_array_biases_hidden(self):
            self.biases_hidden = f90wrap.runtime.FortranDerivedTypeArray(self,
                                            _qlknn_f90wrap.f90wrap_networktype__array_getitem__biases_hidden,
                                            _qlknn_f90wrap.f90wrap_networktype__array_setitem__biases_hidden,
                                            _qlknn_f90wrap.f90wrap_networktype__array_len__biases_hidden,
                                            """
            Element biases_hidden ftype=type(ragged_biases_array) pytype=Ragged_Biases_Array
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 line 65
            
            """, qlknn_types.ragged_biases_array)
            return self.biases_hidden
        
        @property
        def weights_output(self):
            """
            Element weights_output ftype=real(qlknn_dp) pytype=float
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 line 67
            
            """
            array_ndim, array_type, array_shape, array_handle = \
                _qlknn_f90wrap.f90wrap_networktype__array__weights_output(self._handle)
            if array_handle in self._arrays:
                weights_output = self._arrays[array_handle]
            else:
                weights_output = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                        self._handle,
                                        _qlknn_f90wrap.f90wrap_networktype__array__weights_output)
                self._arrays[array_handle] = weights_output
            return weights_output
        
        @weights_output.setter
        def weights_output(self, weights_output):
            self.weights_output[...] = weights_output
        
        @property
        def biases_output(self):
            """
            Element biases_output ftype=real(qlknn_dp) pytype=float
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 line 69
            
            """
            array_ndim, array_type, array_shape, array_handle = \
                _qlknn_f90wrap.f90wrap_networktype__array__biases_output(self._handle)
            if array_handle in self._arrays:
                biases_output = self._arrays[array_handle]
            else:
                biases_output = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                        self._handle,
                                        _qlknn_f90wrap.f90wrap_networktype__array__biases_output)
                self._arrays[array_handle] = biases_output
            return biases_output
        
        @biases_output.setter
        def biases_output(self, biases_output):
            self.biases_output[...] = biases_output
        
        @property
        def hidden_activation(self):
            """
            Element hidden_activation ftype=character(len=4) pytype=str
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 line 71
            
            """
            array_ndim, array_type, array_shape, array_handle = \
                _qlknn_f90wrap.f90wrap_networktype__array__hidden_activation(self._handle)
            if array_handle in self._arrays:
                hidden_activation = self._arrays[array_handle]
            else:
                hidden_activation = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                        self._handle,
                                        _qlknn_f90wrap.f90wrap_networktype__array__hidden_activation)
                self._arrays[array_handle] = hidden_activation
            return hidden_activation
        
        @hidden_activation.setter
        def hidden_activation(self, hidden_activation):
            self.hidden_activation[...] = hidden_activation
        
        @property
        def feature_prescale_bias(self):
            """
            Element feature_prescale_bias ftype=real(qlknn_dp) pytype=float
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 line 73
            
            """
            array_ndim, array_type, array_shape, array_handle = \
                _qlknn_f90wrap.f90wrap_networktype__array__feature_prescale_bias(self._handle)
            if array_handle in self._arrays:
                feature_prescale_bias = self._arrays[array_handle]
            else:
                feature_prescale_bias = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                        self._handle,
                                        _qlknn_f90wrap.f90wrap_networktype__array__feature_prescale_bias)
                self._arrays[array_handle] = feature_prescale_bias
            return feature_prescale_bias
        
        @feature_prescale_bias.setter
        def feature_prescale_bias(self, feature_prescale_bias):
            self.feature_prescale_bias[...] = feature_prescale_bias
        
        @property
        def feature_prescale_factor(self):
            """
            Element feature_prescale_factor ftype=real(qlknn_dp) pytype=float
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 line 75
            
            """
            array_ndim, array_type, array_shape, array_handle = \
                _qlknn_f90wrap.f90wrap_networktype__array__feature_prescale_factor(self._handle)
            if array_handle in self._arrays:
                feature_prescale_factor = self._arrays[array_handle]
            else:
                feature_prescale_factor = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                        self._handle,
                                        _qlknn_f90wrap.f90wrap_networktype__array__feature_prescale_factor)
                self._arrays[array_handle] = feature_prescale_factor
            return feature_prescale_factor
        
        @feature_prescale_factor.setter
        def feature_prescale_factor(self, feature_prescale_factor):
            self.feature_prescale_factor[...] = feature_prescale_factor
        
        @property
        def target_prescale_bias(self):
            """
            Element target_prescale_bias ftype=real(qlknn_dp) pytype=float
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 line 77
            
            """
            array_ndim, array_type, array_shape, array_handle = \
                _qlknn_f90wrap.f90wrap_networktype__array__target_prescale_bias(self._handle)
            if array_handle in self._arrays:
                target_prescale_bias = self._arrays[array_handle]
            else:
                target_prescale_bias = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                        self._handle,
                                        _qlknn_f90wrap.f90wrap_networktype__array__target_prescale_bias)
                self._arrays[array_handle] = target_prescale_bias
            return target_prescale_bias
        
        @target_prescale_bias.setter
        def target_prescale_bias(self, target_prescale_bias):
            self.target_prescale_bias[...] = target_prescale_bias
        
        @property
        def target_prescale_factor(self):
            """
            Element target_prescale_factor ftype=real(qlknn_dp) pytype=float
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 line 79
            
            """
            array_ndim, array_type, array_shape, array_handle = \
                _qlknn_f90wrap.f90wrap_networktype__array__target_prescale_factor(self._handle)
            if array_handle in self._arrays:
                target_prescale_factor = self._arrays[array_handle]
            else:
                target_prescale_factor = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                        self._handle,
                                        _qlknn_f90wrap.f90wrap_networktype__array__target_prescale_factor)
                self._arrays[array_handle] = target_prescale_factor
            return target_prescale_factor
        
        @target_prescale_factor.setter
        def target_prescale_factor(self, target_prescale_factor):
            self.target_prescale_factor[...] = target_prescale_factor
        
        def __str__(self):
            ret = ['<networktype>{\n']
            ret.append('    n_hidden_layers : ')
            ret.append(repr(self.n_hidden_layers))
            ret.append(',\n    n_max_nodes : ')
            ret.append(repr(self.n_max_nodes))
            ret.append(',\n    weights_input : ')
            ret.append(repr(self.weights_input))
            ret.append(',\n    biases_input : ')
            ret.append(repr(self.biases_input))
            ret.append(',\n    weights_output : ')
            ret.append(repr(self.weights_output))
            ret.append(',\n    biases_output : ')
            ret.append(repr(self.biases_output))
            ret.append(',\n    hidden_activation : ')
            ret.append(repr(self.hidden_activation))
            ret.append(',\n    feature_prescale_bias : ')
            ret.append(repr(self.feature_prescale_bias))
            ret.append(',\n    feature_prescale_factor : ')
            ret.append(repr(self.feature_prescale_factor))
            ret.append(',\n    target_prescale_bias : ')
            ret.append(repr(self.target_prescale_bias))
            ret.append(',\n    target_prescale_factor : ')
            ret.append(repr(self.target_prescale_factor))
            ret.append('}')
            return ''.join(ret)
        
        _dt_array_initialisers = [init_array_weights_hidden, init_array_biases_hidden]
        
    
    @f90wrap.runtime.register_class("qlknn_f90wrap.net_collection")
    class net_collection(f90wrap.runtime.FortranDerivedType):
        """
        Type(name=net_collection)
        
        
        Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 lines 82-135
        
        """
        def __del__(self):
            """
            Destructor for class Net_Collection
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 lines 447-453
            
            Parameters
            ----------
            net_coll : Net_Collection
            
            """
            if self._alloc:
                _qlknn_f90wrap.f90wrap_all_networktype_deallocate(net_coll=self._handle)
        
        def __init__(self, handle=None):
            """
            self = Net_Collection()
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 lines 82-135
            
            
            Returns
            -------
            this : Net_Collection
            	Object to be constructed
            
            
            Automatically generated constructor for net_collection
            """
            f90wrap.runtime.FortranDerivedType.__init__(self)
            result = _qlknn_f90wrap.f90wrap_net_collection_initialise()
            self._handle = result[0] if isinstance(result, tuple) else result
        
        def init_array_nets(self):
            self.nets = f90wrap.runtime.FortranDerivedTypeArray(self,
                                            _qlknn_f90wrap.f90wrap_net_collection__array_getitem__nets,
                                            _qlknn_f90wrap.f90wrap_net_collection__array_setitem__nets,
                                            _qlknn_f90wrap.f90wrap_net_collection__array_len__nets,
                                            """
            Element nets ftype=type(networktype) pytype=Networktype
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 line 88
            
            """, qlknn_types.networktype)
            return self.nets
        
        @property
        def zeff_ind(self):
            """
            Element zeff_ind ftype=integer(lli) pytype=int
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 line 90
            
            """
            return _qlknn_f90wrap.f90wrap_net_collection__get__zeff_ind(self._handle)
        
        @zeff_ind.setter
        def zeff_ind(self, zeff_ind):
            _qlknn_f90wrap.f90wrap_net_collection__set__zeff_ind(self._handle, zeff_ind)
        
        @property
        def ati_ind(self):
            """
            Element ati_ind ftype=integer(lli) pytype=int
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 line 92
            
            """
            return _qlknn_f90wrap.f90wrap_net_collection__get__ati_ind(self._handle)
        
        @ati_ind.setter
        def ati_ind(self, ati_ind):
            _qlknn_f90wrap.f90wrap_net_collection__set__ati_ind(self._handle, ati_ind)
        
        @property
        def ate_ind(self):
            """
            Element ate_ind ftype=integer(lli) pytype=int
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 line 94
            
            """
            return _qlknn_f90wrap.f90wrap_net_collection__get__ate_ind(self._handle)
        
        @ate_ind.setter
        def ate_ind(self, ate_ind):
            _qlknn_f90wrap.f90wrap_net_collection__set__ate_ind(self._handle, ate_ind)
        
        @property
        def an_ind(self):
            """
            Element an_ind ftype=integer(lli) pytype=int
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 line 96
            
            """
            return _qlknn_f90wrap.f90wrap_net_collection__get__an_ind(self._handle)
        
        @an_ind.setter
        def an_ind(self, an_ind):
            _qlknn_f90wrap.f90wrap_net_collection__set__an_ind(self._handle, an_ind)
        
        @property
        def q_ind(self):
            """
            Element q_ind ftype=integer(lli) pytype=int
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 line 98
            
            """
            return _qlknn_f90wrap.f90wrap_net_collection__get__q_ind(self._handle)
        
        @q_ind.setter
        def q_ind(self, q_ind):
            _qlknn_f90wrap.f90wrap_net_collection__set__q_ind(self._handle, q_ind)
        
        @property
        def smag_ind(self):
            """
            Element smag_ind ftype=integer(lli) pytype=int
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 line 100
            
            """
            return _qlknn_f90wrap.f90wrap_net_collection__get__smag_ind(self._handle)
        
        @smag_ind.setter
        def smag_ind(self, smag_ind):
            _qlknn_f90wrap.f90wrap_net_collection__set__smag_ind(self._handle, smag_ind)
        
        @property
        def x_ind(self):
            """
            Element x_ind ftype=integer(lli) pytype=int
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 line 102
            
            """
            return _qlknn_f90wrap.f90wrap_net_collection__get__x_ind(self._handle)
        
        @x_ind.setter
        def x_ind(self, x_ind):
            _qlknn_f90wrap.f90wrap_net_collection__set__x_ind(self._handle, x_ind)
        
        @property
        def ti_te_ind(self):
            """
            Element ti_te_ind ftype=integer(lli) pytype=int
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 line 104
            
            """
            return _qlknn_f90wrap.f90wrap_net_collection__get__ti_te_ind(self._handle)
        
        @ti_te_ind.setter
        def ti_te_ind(self, ti_te_ind):
            _qlknn_f90wrap.f90wrap_net_collection__set__ti_te_ind(self._handle, ti_te_ind)
        
        @property
        def lognustar_ind(self):
            """
            Element lognustar_ind ftype=integer(lli) pytype=int
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 line 106
            
            """
            return _qlknn_f90wrap.f90wrap_net_collection__get__lognustar_ind(self._handle)
        
        @lognustar_ind.setter
        def lognustar_ind(self, lognustar_ind):
            _qlknn_f90wrap.f90wrap_net_collection__set__lognustar_ind(self._handle, lognustar_ind)
        
        @property
        def gammae_ind(self):
            """
            Element gammae_ind ftype=integer(lli) pytype=int
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 line 108
            
            """
            return _qlknn_f90wrap.f90wrap_net_collection__get__gammae_ind(self._handle)
        
        @gammae_ind.setter
        def gammae_ind(self, gammae_ind):
            _qlknn_f90wrap.f90wrap_net_collection__set__gammae_ind(self._handle, gammae_ind)
        
        @property
        def te_ind(self):
            """
            Element te_ind ftype=integer(lli) pytype=int
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 line 110
            
            """
            return _qlknn_f90wrap.f90wrap_net_collection__get__te_ind(self._handle)
        
        @te_ind.setter
        def te_ind(self, te_ind):
            _qlknn_f90wrap.f90wrap_net_collection__set__te_ind(self._handle, te_ind)
        
        @property
        def ane_ind(self):
            """
            Element ane_ind ftype=integer(lli) pytype=int
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 line 112
            
            """
            return _qlknn_f90wrap.f90wrap_net_collection__get__ane_ind(self._handle)
        
        @ane_ind.setter
        def ane_ind(self, ane_ind):
            _qlknn_f90wrap.f90wrap_net_collection__set__ane_ind(self._handle, ane_ind)
        
        @property
        def machtor_ind(self):
            """
            Element machtor_ind ftype=integer(lli) pytype=int
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 line 114
            
            """
            return _qlknn_f90wrap.f90wrap_net_collection__get__machtor_ind(self._handle)
        
        @machtor_ind.setter
        def machtor_ind(self, machtor_ind):
            _qlknn_f90wrap.f90wrap_net_collection__set__machtor_ind(self._handle, machtor_ind)
        
        @property
        def autor_ind(self):
            """
            Element autor_ind ftype=integer(lli) pytype=int
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 line 116
            
            """
            return _qlknn_f90wrap.f90wrap_net_collection__get__autor_ind(self._handle)
        
        @autor_ind.setter
        def autor_ind(self, autor_ind):
            _qlknn_f90wrap.f90wrap_net_collection__set__autor_ind(self._handle, autor_ind)
        
        @property
        def alpha_ind(self):
            """
            Element alpha_ind ftype=integer(lli) pytype=int
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 line 118
            
            """
            return _qlknn_f90wrap.f90wrap_net_collection__get__alpha_ind(self._handle)
        
        @alpha_ind.setter
        def alpha_ind(self, alpha_ind):
            _qlknn_f90wrap.f90wrap_net_collection__set__alpha_ind(self._handle, alpha_ind)
        
        @property
        def ani0_ind(self):
            """
            Element ani0_ind ftype=integer(lli) pytype=int
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 line 120
            
            """
            return _qlknn_f90wrap.f90wrap_net_collection__get__ani0_ind(self._handle)
        
        @ani0_ind.setter
        def ani0_ind(self, ani0_ind):
            _qlknn_f90wrap.f90wrap_net_collection__set__ani0_ind(self._handle, ani0_ind)
        
        @property
        def ani1_ind(self):
            """
            Element ani1_ind ftype=integer(lli) pytype=int
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 line 122
            
            """
            return _qlknn_f90wrap.f90wrap_net_collection__get__ani1_ind(self._handle)
        
        @ani1_ind.setter
        def ani1_ind(self, ani1_ind):
            _qlknn_f90wrap.f90wrap_net_collection__set__ani1_ind(self._handle, ani1_ind)
        
        @property
        def ati0_ind(self):
            """
            Element ati0_ind ftype=integer(lli) pytype=int
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 line 124
            
            """
            return _qlknn_f90wrap.f90wrap_net_collection__get__ati0_ind(self._handle)
        
        @ati0_ind.setter
        def ati0_ind(self, ati0_ind):
            _qlknn_f90wrap.f90wrap_net_collection__set__ati0_ind(self._handle, ati0_ind)
        
        @property
        def normni0_ind(self):
            """
            Element normni0_ind ftype=integer(lli) pytype=int
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 line 126
            
            """
            return _qlknn_f90wrap.f90wrap_net_collection__get__normni0_ind(self._handle)
        
        @normni0_ind.setter
        def normni0_ind(self, normni0_ind):
            _qlknn_f90wrap.f90wrap_net_collection__set__normni0_ind(self._handle, normni0_ind)
        
        @property
        def normni1_ind(self):
            """
            Element normni1_ind ftype=integer(lli) pytype=int
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 line 128
            
            """
            return _qlknn_f90wrap.f90wrap_net_collection__get__normni1_ind(self._handle)
        
        @normni1_ind.setter
        def normni1_ind(self, normni1_ind):
            _qlknn_f90wrap.f90wrap_net_collection__set__normni1_ind(self._handle, normni1_ind)
        
        @property
        def ti_te0_ind(self):
            """
            Element ti_te0_ind ftype=integer(lli) pytype=int
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 line 130
            
            """
            return _qlknn_f90wrap.f90wrap_net_collection__get__ti_te0_ind(self._handle)
        
        @ti_te0_ind.setter
        def ti_te0_ind(self, ti_te0_ind):
            _qlknn_f90wrap.f90wrap_net_collection__set__ti_te0_ind(self._handle, ti_te0_ind)
        
        @property
        def a(self):
            """
            Element a ftype=real(qlknn_dp) pytype=float
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 line 132
            
            """
            return _qlknn_f90wrap.f90wrap_net_collection__get__a(self._handle)
        
        @a.setter
        def a(self, a):
            _qlknn_f90wrap.f90wrap_net_collection__set__a(self._handle, a)
        
        @property
        def r_0(self):
            """
            Element r_0 ftype=real(qlknn_dp) pytype=float
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 line 134
            
            """
            return _qlknn_f90wrap.f90wrap_net_collection__get__r_0(self._handle)
        
        @r_0.setter
        def r_0(self, r_0):
            _qlknn_f90wrap.f90wrap_net_collection__set__r_0(self._handle, r_0)
        
        def __str__(self):
            ret = ['<net_collection>{\n']
            ret.append('    zeff_ind : ')
            ret.append(repr(self.zeff_ind))
            ret.append(',\n    ati_ind : ')
            ret.append(repr(self.ati_ind))
            ret.append(',\n    ate_ind : ')
            ret.append(repr(self.ate_ind))
            ret.append(',\n    an_ind : ')
            ret.append(repr(self.an_ind))
            ret.append(',\n    q_ind : ')
            ret.append(repr(self.q_ind))
            ret.append(',\n    smag_ind : ')
            ret.append(repr(self.smag_ind))
            ret.append(',\n    x_ind : ')
            ret.append(repr(self.x_ind))
            ret.append(',\n    ti_te_ind : ')
            ret.append(repr(self.ti_te_ind))
            ret.append(',\n    lognustar_ind : ')
            ret.append(repr(self.lognustar_ind))
            ret.append(',\n    gammae_ind : ')
            ret.append(repr(self.gammae_ind))
            ret.append(',\n    te_ind : ')
            ret.append(repr(self.te_ind))
            ret.append(',\n    ane_ind : ')
            ret.append(repr(self.ane_ind))
            ret.append(',\n    machtor_ind : ')
            ret.append(repr(self.machtor_ind))
            ret.append(',\n    autor_ind : ')
            ret.append(repr(self.autor_ind))
            ret.append(',\n    alpha_ind : ')
            ret.append(repr(self.alpha_ind))
            ret.append(',\n    ani0_ind : ')
            ret.append(repr(self.ani0_ind))
            ret.append(',\n    ani1_ind : ')
            ret.append(repr(self.ani1_ind))
            ret.append(',\n    ati0_ind : ')
            ret.append(repr(self.ati0_ind))
            ret.append(',\n    normni0_ind : ')
            ret.append(repr(self.normni0_ind))
            ret.append(',\n    normni1_ind : ')
            ret.append(repr(self.normni1_ind))
            ret.append(',\n    ti_te0_ind : ')
            ret.append(repr(self.ti_te0_ind))
            ret.append(',\n    a : ')
            ret.append(repr(self.a))
            ret.append(',\n    r_0 : ')
            ret.append(repr(self.r_0))
            ret.append('}')
            return ''.join(ret)
        
        _dt_array_initialisers = [init_array_nets]
        
    
    @f90wrap.runtime.register_class("qlknn_f90wrap.hornnet_output_block")
    class hornnet_output_block(f90wrap.runtime.FortranDerivedType):
        """
        Type(name=hornnet_output_block)
        
        
        Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 lines 137-154
        
        """
        def __init__(self, handle=None):
            """
            self = Hornnet_Output_Block()
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 lines 137-154
            
            
            Returns
            -------
            this : Hornnet_Output_Block
            	Object to be constructed
            
            
            Automatically generated constructor for hornnet_output_block
            """
            f90wrap.runtime.FortranDerivedType.__init__(self)
            result = _qlknn_f90wrap.f90wrap_hornnet_output_block_initialise()
            self._handle = result[0] if isinstance(result, tuple) else result
        
        def __del__(self):
            """
            Destructor for class Hornnet_Output_Block
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 lines 137-154
            
            Parameters
            ----------
            this : Hornnet_Output_Block
            	Object to be destructed
            
            
            Automatically generated destructor for hornnet_output_block
            """
            if self._alloc:
                _qlknn_f90wrap.f90wrap_hornnet_output_block_finalise(this=self._handle)
        
        def init_array_weights_hidden(self):
            self.weights_hidden = f90wrap.runtime.FortranDerivedTypeArray(self,
                                            _qlknn_f90wrap.f90wrap_hornnet_output_block__array_getitem__weights_hidden,
                                            _qlknn_f90wrap.f90wrap_hornnet_output_block__array_setitem__weights_hidden,
                                            _qlknn_f90wrap.f90wrap_hornnet_output_block__array_len__weights_hidden,
                                            """
            Element weights_hidden ftype=type(ragged_weights_array) pytype=Ragged_Weights_Array
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 line 143
            
            """, qlknn_types.ragged_weights_array)
            return self.weights_hidden
        
        def init_array_biases_hidden(self):
            self.biases_hidden = f90wrap.runtime.FortranDerivedTypeArray(self,
                                            _qlknn_f90wrap.f90wrap_hornnet_output_block__array_getitem__biases_hidden,
                                            _qlknn_f90wrap.f90wrap_hornnet_output_block__array_setitem__biases_hidden,
                                            _qlknn_f90wrap.f90wrap_hornnet_output_block__array_len__biases_hidden,
                                            """
            Element biases_hidden ftype=type(ragged_biases_array) pytype=Ragged_Biases_Array
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 line 145
            
            """, qlknn_types.ragged_biases_array)
            return self.biases_hidden
        
        @property
        def weights_output(self):
            """
            Element weights_output ftype=real(qlknn_dp) pytype=float
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 line 147
            
            """
            array_ndim, array_type, array_shape, array_handle = \
                _qlknn_f90wrap.f90wrap_hornnet_output_block__array__weights_output(self._handle)
            if array_handle in self._arrays:
                weights_output = self._arrays[array_handle]
            else:
                weights_output = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                        self._handle,
                                        _qlknn_f90wrap.f90wrap_hornnet_output_block__array__weights_output)
                self._arrays[array_handle] = weights_output
            return weights_output
        
        @weights_output.setter
        def weights_output(self, weights_output):
            self.weights_output[...] = weights_output
        
        @property
        def biases_output(self):
            """
            Element biases_output ftype=real(qlknn_dp) pytype=float
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 line 149
            
            """
            array_ndim, array_type, array_shape, array_handle = \
                _qlknn_f90wrap.f90wrap_hornnet_output_block__array__biases_output(self._handle)
            if array_handle in self._arrays:
                biases_output = self._arrays[array_handle]
            else:
                biases_output = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                        self._handle,
                                        _qlknn_f90wrap.f90wrap_hornnet_output_block__array__biases_output)
                self._arrays[array_handle] = biases_output
            return biases_output
        
        @biases_output.setter
        def biases_output(self, biases_output):
            self.biases_output[...] = biases_output
        
        @property
        def hidden_activation(self):
            """
            Element hidden_activation ftype=character(len=4) pytype=str
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 line 151
            
            """
            array_ndim, array_type, array_shape, array_handle = \
                _qlknn_f90wrap.f90wrap_hornnet_output_block__array__hidden_activation(self._handle)
            if array_handle in self._arrays:
                hidden_activation = self._arrays[array_handle]
            else:
                hidden_activation = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                        self._handle,
                                        _qlknn_f90wrap.f90wrap_hornnet_output_block__array__hidden_activation)
                self._arrays[array_handle] = hidden_activation
            return hidden_activation
        
        @hidden_activation.setter
        def hidden_activation(self, hidden_activation):
            self.hidden_activation[...] = hidden_activation
        
        @property
        def blockname(self):
            """
            Element blockname ftype=character(len=20) pytype=str
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 line 153
            
            """
            return _qlknn_f90wrap.f90wrap_hornnet_output_block__get__blockname(self._handle)
        
        @blockname.setter
        def blockname(self, blockname):
            _qlknn_f90wrap.f90wrap_hornnet_output_block__set__blockname(self._handle, blockname)
        
        def __str__(self):
            ret = ['<hornnet_output_block>{\n']
            ret.append('    weights_output : ')
            ret.append(repr(self.weights_output))
            ret.append(',\n    biases_output : ')
            ret.append(repr(self.biases_output))
            ret.append(',\n    hidden_activation : ')
            ret.append(repr(self.hidden_activation))
            ret.append(',\n    blockname : ')
            ret.append(repr(self.blockname))
            ret.append('}')
            return ''.join(ret)
        
        _dt_array_initialisers = [init_array_weights_hidden, init_array_biases_hidden]
        
    
    @f90wrap.runtime.register_class("qlknn_f90wrap.hornnet_input_block")
    class hornnet_input_block(f90wrap.runtime.FortranDerivedType):
        """
        Type(name=hornnet_input_block)
        
        
        Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 lines 156-173
        
        """
        def __init__(self, handle=None):
            """
            self = Hornnet_Input_Block()
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 lines 156-173
            
            
            Returns
            -------
            this : Hornnet_Input_Block
            	Object to be constructed
            
            
            Automatically generated constructor for hornnet_input_block
            """
            f90wrap.runtime.FortranDerivedType.__init__(self)
            result = _qlknn_f90wrap.f90wrap_hornnet_input_block_initialise()
            self._handle = result[0] if isinstance(result, tuple) else result
        
        def __del__(self):
            """
            Destructor for class Hornnet_Input_Block
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 lines 156-173
            
            Parameters
            ----------
            this : Hornnet_Input_Block
            	Object to be destructed
            
            
            Automatically generated destructor for hornnet_input_block
            """
            if self._alloc:
                _qlknn_f90wrap.f90wrap_hornnet_input_block_finalise(this=self._handle)
        
        @property
        def weights_input(self):
            """
            Element weights_input ftype=real(qlknn_dp) pytype=float
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 line 162
            
            """
            array_ndim, array_type, array_shape, array_handle = \
                _qlknn_f90wrap.f90wrap_hornnet_input_block__array__weights_input(self._handle)
            if array_handle in self._arrays:
                weights_input = self._arrays[array_handle]
            else:
                weights_input = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                        self._handle,
                                        _qlknn_f90wrap.f90wrap_hornnet_input_block__array__weights_input)
                self._arrays[array_handle] = weights_input
            return weights_input
        
        @weights_input.setter
        def weights_input(self, weights_input):
            self.weights_input[...] = weights_input
        
        @property
        def biases_input(self):
            """
            Element biases_input ftype=real(qlknn_dp) pytype=float
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 line 164
            
            """
            array_ndim, array_type, array_shape, array_handle = \
                _qlknn_f90wrap.f90wrap_hornnet_input_block__array__biases_input(self._handle)
            if array_handle in self._arrays:
                biases_input = self._arrays[array_handle]
            else:
                biases_input = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                        self._handle,
                                        _qlknn_f90wrap.f90wrap_hornnet_input_block__array__biases_input)
                self._arrays[array_handle] = biases_input
            return biases_input
        
        @biases_input.setter
        def biases_input(self, biases_input):
            self.biases_input[...] = biases_input
        
        @property
        def feature_prescale_bias(self):
            """
            Element feature_prescale_bias ftype=real(qlknn_dp) pytype=float
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 line 166
            
            """
            array_ndim, array_type, array_shape, array_handle = \
                _qlknn_f90wrap.f90wrap_hornnet_input_block__array__feature_prescale_bias(self._handle)
            if array_handle in self._arrays:
                feature_prescale_bias = self._arrays[array_handle]
            else:
                feature_prescale_bias = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                        self._handle,
                                        _qlknn_f90wrap.f90wrap_hornnet_input_block__array__feature_prescale_bias)
                self._arrays[array_handle] = feature_prescale_bias
            return feature_prescale_bias
        
        @feature_prescale_bias.setter
        def feature_prescale_bias(self, feature_prescale_bias):
            self.feature_prescale_bias[...] = feature_prescale_bias
        
        @property
        def feature_prescale_factor(self):
            """
            Element feature_prescale_factor ftype=real(qlknn_dp) pytype=float
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 line 168
            
            """
            array_ndim, array_type, array_shape, array_handle = \
                _qlknn_f90wrap.f90wrap_hornnet_input_block__array__feature_prescale_factor(self._handle)
            if array_handle in self._arrays:
                feature_prescale_factor = self._arrays[array_handle]
            else:
                feature_prescale_factor = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                        self._handle,
                                        _qlknn_f90wrap.f90wrap_hornnet_input_block__array__feature_prescale_factor)
                self._arrays[array_handle] = feature_prescale_factor
            return feature_prescale_factor
        
        @feature_prescale_factor.setter
        def feature_prescale_factor(self, feature_prescale_factor):
            self.feature_prescale_factor[...] = feature_prescale_factor
        
        @property
        def target_prescale_bias(self):
            """
            Element target_prescale_bias ftype=real(qlknn_dp) pytype=float
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 line 170
            
            """
            array_ndim, array_type, array_shape, array_handle = \
                _qlknn_f90wrap.f90wrap_hornnet_input_block__array__target_prescale_bias(self._handle)
            if array_handle in self._arrays:
                target_prescale_bias = self._arrays[array_handle]
            else:
                target_prescale_bias = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                        self._handle,
                                        _qlknn_f90wrap.f90wrap_hornnet_input_block__array__target_prescale_bias)
                self._arrays[array_handle] = target_prescale_bias
            return target_prescale_bias
        
        @target_prescale_bias.setter
        def target_prescale_bias(self, target_prescale_bias):
            self.target_prescale_bias[...] = target_prescale_bias
        
        @property
        def target_prescale_factor(self):
            """
            Element target_prescale_factor ftype=real(qlknn_dp) pytype=float
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 line 172
            
            """
            array_ndim, array_type, array_shape, array_handle = \
                _qlknn_f90wrap.f90wrap_hornnet_input_block__array__target_prescale_factor(self._handle)
            if array_handle in self._arrays:
                target_prescale_factor = self._arrays[array_handle]
            else:
                target_prescale_factor = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                        self._handle,
                                        _qlknn_f90wrap.f90wrap_hornnet_input_block__array__target_prescale_factor)
                self._arrays[array_handle] = target_prescale_factor
            return target_prescale_factor
        
        @target_prescale_factor.setter
        def target_prescale_factor(self, target_prescale_factor):
            self.target_prescale_factor[...] = target_prescale_factor
        
        def __str__(self):
            ret = ['<hornnet_input_block>{\n']
            ret.append('    weights_input : ')
            ret.append(repr(self.weights_input))
            ret.append(',\n    biases_input : ')
            ret.append(repr(self.biases_input))
            ret.append(',\n    feature_prescale_bias : ')
            ret.append(repr(self.feature_prescale_bias))
            ret.append(',\n    feature_prescale_factor : ')
            ret.append(repr(self.feature_prescale_factor))
            ret.append(',\n    target_prescale_bias : ')
            ret.append(repr(self.target_prescale_bias))
            ret.append(',\n    target_prescale_factor : ')
            ret.append(repr(self.target_prescale_factor))
            ret.append('}')
            return ''.join(ret)
        
        _dt_array_initialisers = []
        
    
    @f90wrap.runtime.register_class("qlknn_f90wrap.block_collection")
    class block_collection(f90wrap.runtime.FortranDerivedType):
        """
        Type(name=block_collection)
        
        
        Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 lines 175-178
        
        """
        def __init__(self, handle=None):
            """
            self = Block_Collection()
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 lines 175-178
            
            
            Returns
            -------
            this : Block_Collection
            	Object to be constructed
            
            
            Automatically generated constructor for block_collection
            """
            f90wrap.runtime.FortranDerivedType.__init__(self)
            result = _qlknn_f90wrap.f90wrap_block_collection_initialise()
            self._handle = result[0] if isinstance(result, tuple) else result
        
        def __del__(self):
            """
            Destructor for class Block_Collection
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 lines 175-178
            
            Parameters
            ----------
            this : Block_Collection
            	Object to be destructed
            
            
            Automatically generated destructor for block_collection
            """
            if self._alloc:
                _qlknn_f90wrap.f90wrap_block_collection_finalise(this=self._handle)
        
        def init_array_output_blocks(self):
            self.output_blocks = f90wrap.runtime.FortranDerivedTypeArray(self,
                                            _qlknn_f90wrap.f90wrap_block_collection__array_getitem__output_blocks,
                                            _qlknn_f90wrap.f90wrap_block_collection__array_setitem__output_blocks,
                                            _qlknn_f90wrap.f90wrap_block_collection__array_len__output_blocks,
                                            """
            Element output_blocks ftype=type(hornnet_output_block) pytype=Hornnet_Output_Block
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 line 177
            
            """, qlknn_types.hornnet_output_block)
            return self.output_blocks
        
        def init_array_input_blocks(self):
            self.input_blocks = f90wrap.runtime.FortranDerivedTypeArray(self,
                                            _qlknn_f90wrap.f90wrap_block_collection__array_getitem__input_blocks,
                                            _qlknn_f90wrap.f90wrap_block_collection__array_setitem__input_blocks,
                                            _qlknn_f90wrap.f90wrap_block_collection__array_len__input_blocks,
                                            """
            Element input_blocks ftype=type(hornnet_input_block) pytype=Hornnet_Input_Block
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 line 178
            
            """, qlknn_types.hornnet_input_block)
            return self.input_blocks
        
        _dt_array_initialisers = [init_array_output_blocks, init_array_input_blocks]
        
    
    @f90wrap.runtime.register_class("qlknn_f90wrap.qlknn_options")
    class qlknn_options(f90wrap.runtime.FortranDerivedType):
        """
        Type(name=qlknn_options)
        
        
        Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 lines 180-219
        
        """
        def __init__(self, handle=None):
            """
            self = Qlknn_Options()
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 lines 180-219
            
            
            Returns
            -------
            this : Qlknn_Options
            	Object to be constructed
            
            
            Automatically generated constructor for qlknn_options
            """
            f90wrap.runtime.FortranDerivedType.__init__(self)
            result = _qlknn_f90wrap.f90wrap_qlknn_options_initialise()
            self._handle = result[0] if isinstance(result, tuple) else result
        
        def __del__(self):
            """
            Destructor for class Qlknn_Options
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 lines 180-219
            
            Parameters
            ----------
            this : Qlknn_Options
            	Object to be destructed
            
            
            Automatically generated destructor for qlknn_options
            """
            if self._alloc:
                _qlknn_f90wrap.f90wrap_qlknn_options_finalise(this=self._handle)
        
        @property
        def use_ion_diffusivity_networks(self):
            """
            Element use_ion_diffusivity_networks ftype=logical pytype=bool
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 line 182
            
            """
            return \
                _qlknn_f90wrap.f90wrap_qlknn_options__get__use_ion_diffusivity_networks(self._handle)
        
        @use_ion_diffusivity_networks.setter
        def use_ion_diffusivity_networks(self, use_ion_diffusivity_networks):
            _qlknn_f90wrap.f90wrap_qlknn_options__set__use_ion_diffusivity_networks(self._handle, \
                use_ion_diffusivity_networks)
        
        @property
        def apply_victor_rule(self):
            """
            Element apply_victor_rule ftype=logical pytype=bool
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 line 184
            
            """
            return _qlknn_f90wrap.f90wrap_qlknn_options__get__apply_victor_rule(self._handle)
        
        @apply_victor_rule.setter
        def apply_victor_rule(self, apply_victor_rule):
            _qlknn_f90wrap.f90wrap_qlknn_options__set__apply_victor_rule(self._handle, \
                apply_victor_rule)
        
        @property
        def use_effective_diffusivity(self):
            """
            Element use_effective_diffusivity ftype=logical pytype=bool
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 line 186
            
            """
            return _qlknn_f90wrap.f90wrap_qlknn_options__get__use_effective_diffusivity(self._handle)
        
        @use_effective_diffusivity.setter
        def use_effective_diffusivity(self, use_effective_diffusivity):
            _qlknn_f90wrap.f90wrap_qlknn_options__set__use_effective_diffusivity(self._handle, \
                use_effective_diffusivity)
        
        @property
        def calc_heat_transport(self):
            """
            Element calc_heat_transport ftype=logical pytype=bool
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 line 188
            
            """
            return _qlknn_f90wrap.f90wrap_qlknn_options__get__calc_heat_transport(self._handle)
        
        @calc_heat_transport.setter
        def calc_heat_transport(self, calc_heat_transport):
            _qlknn_f90wrap.f90wrap_qlknn_options__set__calc_heat_transport(self._handle, \
                calc_heat_transport)
        
        @property
        def calc_part_transport(self):
            """
            Element calc_part_transport ftype=logical pytype=bool
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 line 190
            
            """
            return _qlknn_f90wrap.f90wrap_qlknn_options__get__calc_part_transport(self._handle)
        
        @calc_part_transport.setter
        def calc_part_transport(self, calc_part_transport):
            _qlknn_f90wrap.f90wrap_qlknn_options__set__calc_part_transport(self._handle, \
                calc_part_transport)
        
        @property
        def use_etg(self):
            """
            Element use_etg ftype=logical pytype=bool
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 line 192
            
            """
            return _qlknn_f90wrap.f90wrap_qlknn_options__get__use_etg(self._handle)
        
        @use_etg.setter
        def use_etg(self, use_etg):
            _qlknn_f90wrap.f90wrap_qlknn_options__set__use_etg(self._handle, use_etg)
        
        @property
        def use_itg(self):
            """
            Element use_itg ftype=logical pytype=bool
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 line 194
            
            """
            return _qlknn_f90wrap.f90wrap_qlknn_options__get__use_itg(self._handle)
        
        @use_itg.setter
        def use_itg(self, use_itg):
            _qlknn_f90wrap.f90wrap_qlknn_options__set__use_itg(self._handle, use_itg)
        
        @property
        def use_tem(self):
            """
            Element use_tem ftype=logical pytype=bool
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 line 196
            
            """
            return _qlknn_f90wrap.f90wrap_qlknn_options__get__use_tem(self._handle)
        
        @use_tem.setter
        def use_tem(self, use_tem):
            _qlknn_f90wrap.f90wrap_qlknn_options__set__use_tem(self._handle, use_tem)
        
        @property
        def apply_stability_clipping(self):
            """
            Element apply_stability_clipping ftype=logical pytype=bool
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 line 198
            
            """
            return _qlknn_f90wrap.f90wrap_qlknn_options__get__apply_stability_clipping(self._handle)
        
        @apply_stability_clipping.setter
        def apply_stability_clipping(self, apply_stability_clipping):
            _qlknn_f90wrap.f90wrap_qlknn_options__set__apply_stability_clipping(self._handle, \
                apply_stability_clipping)
        
        @property
        def constrain_inputs(self):
            """
            Element constrain_inputs ftype=logical pytype=bool
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 line 200
            
            """
            array_ndim, array_type, array_shape, array_handle = \
                _qlknn_f90wrap.f90wrap_qlknn_options__array__constrain_inputs(self._handle)
            if array_handle in self._arrays:
                constrain_inputs = self._arrays[array_handle]
            else:
                constrain_inputs = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                        self._handle,
                                        _qlknn_f90wrap.f90wrap_qlknn_options__array__constrain_inputs)
                self._arrays[array_handle] = constrain_inputs
            return constrain_inputs
        
        @constrain_inputs.setter
        def constrain_inputs(self, constrain_inputs):
            self.constrain_inputs[...] = constrain_inputs
        
        @property
        def min_input(self):
            """
            Element min_input ftype=real(qlknn_dp) pytype=float
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 line 202
            
            """
            array_ndim, array_type, array_shape, array_handle = \
                _qlknn_f90wrap.f90wrap_qlknn_options__array__min_input(self._handle)
            if array_handle in self._arrays:
                min_input = self._arrays[array_handle]
            else:
                min_input = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                        self._handle,
                                        _qlknn_f90wrap.f90wrap_qlknn_options__array__min_input)
                self._arrays[array_handle] = min_input
            return min_input
        
        @min_input.setter
        def min_input(self, min_input):
            self.min_input[...] = min_input
        
        @property
        def max_input(self):
            """
            Element max_input ftype=real(qlknn_dp) pytype=float
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 line 204
            
            """
            array_ndim, array_type, array_shape, array_handle = \
                _qlknn_f90wrap.f90wrap_qlknn_options__array__max_input(self._handle)
            if array_handle in self._arrays:
                max_input = self._arrays[array_handle]
            else:
                max_input = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                        self._handle,
                                        _qlknn_f90wrap.f90wrap_qlknn_options__array__max_input)
                self._arrays[array_handle] = max_input
            return max_input
        
        @max_input.setter
        def max_input(self, max_input):
            self.max_input[...] = max_input
        
        @property
        def margin_input(self):
            """
            Element margin_input ftype=real(qlknn_dp) pytype=float
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 line 206
            
            """
            array_ndim, array_type, array_shape, array_handle = \
                _qlknn_f90wrap.f90wrap_qlknn_options__array__margin_input(self._handle)
            if array_handle in self._arrays:
                margin_input = self._arrays[array_handle]
            else:
                margin_input = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                        self._handle,
                                        _qlknn_f90wrap.f90wrap_qlknn_options__array__margin_input)
                self._arrays[array_handle] = margin_input
            return margin_input
        
        @margin_input.setter
        def margin_input(self, margin_input):
            self.margin_input[...] = margin_input
        
        @property
        def constrain_outputs(self):
            """
            Element constrain_outputs ftype=logical pytype=bool
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 line 208
            
            """
            array_ndim, array_type, array_shape, array_handle = \
                _qlknn_f90wrap.f90wrap_qlknn_options__array__constrain_outputs(self._handle)
            if array_handle in self._arrays:
                constrain_outputs = self._arrays[array_handle]
            else:
                constrain_outputs = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                        self._handle,
                                        _qlknn_f90wrap.f90wrap_qlknn_options__array__constrain_outputs)
                self._arrays[array_handle] = constrain_outputs
            return constrain_outputs
        
        @constrain_outputs.setter
        def constrain_outputs(self, constrain_outputs):
            self.constrain_outputs[...] = constrain_outputs
        
        @property
        def min_output(self):
            """
            Element min_output ftype=real(qlknn_dp) pytype=float
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 line 210
            
            """
            array_ndim, array_type, array_shape, array_handle = \
                _qlknn_f90wrap.f90wrap_qlknn_options__array__min_output(self._handle)
            if array_handle in self._arrays:
                min_output = self._arrays[array_handle]
            else:
                min_output = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                        self._handle,
                                        _qlknn_f90wrap.f90wrap_qlknn_options__array__min_output)
                self._arrays[array_handle] = min_output
            return min_output
        
        @min_output.setter
        def min_output(self, min_output):
            self.min_output[...] = min_output
        
        @property
        def max_output(self):
            """
            Element max_output ftype=real(qlknn_dp) pytype=float
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 line 212
            
            """
            array_ndim, array_type, array_shape, array_handle = \
                _qlknn_f90wrap.f90wrap_qlknn_options__array__max_output(self._handle)
            if array_handle in self._arrays:
                max_output = self._arrays[array_handle]
            else:
                max_output = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                        self._handle,
                                        _qlknn_f90wrap.f90wrap_qlknn_options__array__max_output)
                self._arrays[array_handle] = max_output
            return max_output
        
        @max_output.setter
        def max_output(self, max_output):
            self.max_output[...] = max_output
        
        @property
        def margin_output(self):
            """
            Element margin_output ftype=real(qlknn_dp) pytype=float
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 line 214
            
            """
            array_ndim, array_type, array_shape, array_handle = \
                _qlknn_f90wrap.f90wrap_qlknn_options__array__margin_output(self._handle)
            if array_handle in self._arrays:
                margin_output = self._arrays[array_handle]
            else:
                margin_output = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                        self._handle,
                                        _qlknn_f90wrap.f90wrap_qlknn_options__array__margin_output)
                self._arrays[array_handle] = margin_output
            return margin_output
        
        @margin_output.setter
        def margin_output(self, margin_output):
            self.margin_output[...] = margin_output
        
        @property
        def merge_modes(self):
            """
            Element merge_modes ftype=logical pytype=bool
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 line 216
            
            """
            return _qlknn_f90wrap.f90wrap_qlknn_options__get__merge_modes(self._handle)
        
        @merge_modes.setter
        def merge_modes(self, merge_modes):
            _qlknn_f90wrap.f90wrap_qlknn_options__set__merge_modes(self._handle, merge_modes)
        
        @property
        def force_evaluate_all(self):
            """
            Element force_evaluate_all ftype=logical pytype=bool
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 line 218
            
            """
            return _qlknn_f90wrap.f90wrap_qlknn_options__get__force_evaluate_all(self._handle)
        
        @force_evaluate_all.setter
        def force_evaluate_all(self, force_evaluate_all):
            _qlknn_f90wrap.f90wrap_qlknn_options__set__force_evaluate_all(self._handle, \
                force_evaluate_all)
        
        def __str__(self):
            ret = ['<qlknn_options>{\n']
            ret.append('    use_ion_diffusivity_networks : ')
            ret.append(repr(self.use_ion_diffusivity_networks))
            ret.append(',\n    apply_victor_rule : ')
            ret.append(repr(self.apply_victor_rule))
            ret.append(',\n    use_effective_diffusivity : ')
            ret.append(repr(self.use_effective_diffusivity))
            ret.append(',\n    calc_heat_transport : ')
            ret.append(repr(self.calc_heat_transport))
            ret.append(',\n    calc_part_transport : ')
            ret.append(repr(self.calc_part_transport))
            ret.append(',\n    use_etg : ')
            ret.append(repr(self.use_etg))
            ret.append(',\n    use_itg : ')
            ret.append(repr(self.use_itg))
            ret.append(',\n    use_tem : ')
            ret.append(repr(self.use_tem))
            ret.append(',\n    apply_stability_clipping : ')
            ret.append(repr(self.apply_stability_clipping))
            ret.append(',\n    constrain_inputs : ')
            ret.append(repr(self.constrain_inputs))
            ret.append(',\n    min_input : ')
            ret.append(repr(self.min_input))
            ret.append(',\n    max_input : ')
            ret.append(repr(self.max_input))
            ret.append(',\n    margin_input : ')
            ret.append(repr(self.margin_input))
            ret.append(',\n    constrain_outputs : ')
            ret.append(repr(self.constrain_outputs))
            ret.append(',\n    min_output : ')
            ret.append(repr(self.min_output))
            ret.append(',\n    max_output : ')
            ret.append(repr(self.max_output))
            ret.append(',\n    margin_output : ')
            ret.append(repr(self.margin_output))
            ret.append(',\n    merge_modes : ')
            ret.append(repr(self.merge_modes))
            ret.append(',\n    force_evaluate_all : ')
            ret.append(repr(self.force_evaluate_all))
            ret.append('}')
            return ''.join(ret)
        
        _dt_array_initialisers = []
        
    
    @f90wrap.runtime.register_class("qlknn_f90wrap.qlknn_normpars")
    class qlknn_normpars(f90wrap.runtime.FortranDerivedType):
        """
        Type(name=qlknn_normpars)
        
        
        Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 lines 221-230
        
        """
        def __init__(self, nrho, handle=None):
            """
            self = Qlknn_Normpars(nrho)
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 lines 455-458
            
            Parameters
            ----------
            nrho : int
            
            Returns
            -------
            qlknn_norms : Qlknn_Normpars
            
            """
            f90wrap.runtime.FortranDerivedType.__init__(self)
            result = _qlknn_f90wrap.f90wrap_qlknn_normpars_allocate(nrho=nrho)
            self._handle = result[0] if isinstance(result, tuple) else result
        
        def __del__(self):
            """
            Destructor for class Qlknn_Normpars
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 lines 460-462
            
            Parameters
            ----------
            qlknn_norms : Qlknn_Normpars
            
            """
            if self._alloc:
                _qlknn_f90wrap.f90wrap_qlknn_normpars_deallocate(qlknn_norms=self._handle)
        
        @property
        def a(self):
            """
            Element a ftype=real(qlknn_dp) pytype=float
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 line 225
            
            """
            return _qlknn_f90wrap.f90wrap_qlknn_normpars__get__a(self._handle)
        
        @a.setter
        def a(self, a):
            _qlknn_f90wrap.f90wrap_qlknn_normpars__set__a(self._handle, a)
        
        @property
        def r0(self):
            """
            Element r0 ftype=real(qlknn_dp) pytype=float
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 line 227
            
            """
            return _qlknn_f90wrap.f90wrap_qlknn_normpars__get__r0(self._handle)
        
        @r0.setter
        def r0(self, r0):
            _qlknn_f90wrap.f90wrap_qlknn_normpars__set__r0(self._handle, r0)
        
        @property
        def a1(self):
            """
            Element a1 ftype=real(qlknn_dp) pytype=float
            
            
            Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 line 229
            
            """
            array_ndim, array_type, array_shape, array_handle = \
                _qlknn_f90wrap.f90wrap_qlknn_normpars__array__a1(self._handle)
            if array_handle in self._arrays:
                a1 = self._arrays[array_handle]
            else:
                a1 = f90wrap.runtime.get_array(f90wrap.runtime.sizeof_fortran_t,
                                        self._handle,
                                        _qlknn_f90wrap.f90wrap_qlknn_normpars__array__a1)
                self._arrays[array_handle] = a1
            return a1
        
        @a1.setter
        def a1(self, a1):
            self.a1[...] = a1
        
        def __str__(self):
            ret = ['<qlknn_normpars>{\n']
            ret.append('    a : ')
            ret.append(repr(self.a))
            ret.append(',\n    r0 : ')
            ret.append(repr(self.r0))
            ret.append(',\n    a1 : ')
            ret.append(repr(self.a1))
            ret.append('}')
            return ''.join(ret)
        
        _dt_array_initialisers = []
        
    
    @staticmethod
    def default_qlknn_hyper_options():
        """
        opts = default_qlknn_hyper_options()
        
        
        Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 lines 233-261
        
        
        Returns
        -------
        opts : Qlknn_Options
        
        """
        opts = _qlknn_f90wrap.f90wrap_default_qlknn_hyper_options()
        opts = f90wrap.runtime.lookup_class("qlknn_f90wrap.qlknn_options").from_handle(opts)
        return opts
    
    @staticmethod
    def default_qlknn_fullflux_options():
        """
        opts = default_qlknn_fullflux_options()
        
        
        Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 lines 263-291
        
        
        Returns
        -------
        opts : Qlknn_Options
        
        """
        opts = _qlknn_f90wrap.f90wrap_default_qlknn_fullflux_options()
        opts = f90wrap.runtime.lookup_class("qlknn_f90wrap.qlknn_options").from_handle(opts)
        return opts
    
    @staticmethod
    def default_qlknn_jetexp_options():
        """
        opts = default_qlknn_jetexp_options()
        
        
        Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 lines 293-321
        
        
        Returns
        -------
        opts : Qlknn_Options
        
        """
        opts = _qlknn_f90wrap.f90wrap_default_qlknn_jetexp_options()
        opts = f90wrap.runtime.lookup_class("qlknn_f90wrap.qlknn_options").from_handle(opts)
        return opts
    
    @staticmethod
    def default_qlknn_hornnet_options():
        """
        opts = default_qlknn_hornnet_options()
        
        
        Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 lines 323-351
        
        
        Returns
        -------
        opts : Qlknn_Options
        
        """
        opts = _qlknn_f90wrap.f90wrap_default_qlknn_hornnet_options()
        opts = f90wrap.runtime.lookup_class("qlknn_f90wrap.qlknn_options").from_handle(opts)
        return opts
    
    @staticmethod
    def print_qlknn_options(opts):
        """
        print_qlknn_options(opts)
        
        
        Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 lines 353-376
        
        Parameters
        ----------
        opts : Qlknn_Options
        
        """
        _qlknn_f90wrap.f90wrap_print_qlknn_options(opts=opts._handle)
    
    @staticmethod
    def get_networks_to_evaluate(opts, net_evaluate):
        """
        get_networks_to_evaluate(opts, net_evaluate)
        
        
        Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 lines 378-420
        
        Parameters
        ----------
        opts : Qlknn_Options
        net_evaluate : bool array
        
        """
        _qlknn_f90wrap.f90wrap_get_networks_to_evaluate(opts=opts._handle, \
            net_evaluate=net_evaluate)
    
    @property
    def qlknn_dp(self):
        """
        Element qlknn_dp ftype=integer pytype=int
        
        
        Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 line 6
        
        """
        return _qlknn_f90wrap.f90wrap_qlknn_types__get__qlknn_dp()
    
    @property
    def lli(self):
        """
        Element lli ftype=integer pytype=int
        
        
        Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 line 7
        
        """
        return _qlknn_f90wrap.f90wrap_qlknn_types__get__lli()
    
    @property
    def li(self):
        """
        Element li ftype=integer pytype=int
        
        
        Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 line 8
        
        """
        return _qlknn_f90wrap.f90wrap_qlknn_types__get__li()
    
    @property
    def stderr(self):
        """
        Element stderr ftype=integer(lli) pytype=int
        
        
        Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 line 9
        
        """
        return _qlknn_f90wrap.f90wrap_qlknn_types__get__stderr()
    
    @property
    def qe(self):
        """
        Element qe ftype=real(qlknn_dp) pytype=float
        
        
        Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 line 10
        
        """
        return _qlknn_f90wrap.f90wrap_qlknn_types__get__qe()
    
    @property
    def mp(self):
        """
        Element mp ftype=real(qlknn_dp) pytype=float
        
        
        Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 line 11
        
        """
        return _qlknn_f90wrap.f90wrap_qlknn_types__get__mp()
    
    @property
    def c_qlk_ref(self):
        """
        Element c_qlk_ref ftype=real(qlknn_dp) pytype=float
        
        
        Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_types.f90 line 12
        
        """
        return _qlknn_f90wrap.f90wrap_qlknn_types__get__c_qlk_ref()
    
    def __str__(self):
        ret = ['<qlknn_types>{\n']
        ret.append('    qlknn_dp : ')
        ret.append(repr(self.qlknn_dp))
        ret.append(',\n    lli : ')
        ret.append(repr(self.lli))
        ret.append(',\n    li : ')
        ret.append(repr(self.li))
        ret.append(',\n    stderr : ')
        ret.append(repr(self.stderr))
        ret.append(',\n    qe : ')
        ret.append(repr(self.qe))
        ret.append(',\n    mp : ')
        ret.append(repr(self.mp))
        ret.append(',\n    c_qlk_ref : ')
        ret.append(repr(self.c_qlk_ref))
        ret.append('}')
        return ''.join(ret)
    
    _dt_array_initialisers = []
    

qlknn_types = Qlknn_Types()

class Qlknn_Victor_Rule(f90wrap.runtime.FortranModule):
    """
    Module qlknn_victor_rule
    
    
    Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_victor_rule.f90 lines 3-224
    
    """
    @staticmethod
    def get_f_victorthesis(input, nets, f_victorthesis, dthesis_dinput=None):
        """
        get_f_victorthesis(input, nets, f_victorthesis[, dthesis_dinput])
        
        
        Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_victor_rule.f90 lines 17-33
        
        Parameters
        ----------
        input : float array
        nets : Net_Collection
        f_victorthesis : float array
        dthesis_dinput : float array
        
        """
        _qlknn_f90wrap.f90wrap_get_f_victorthesis(input=input, nets=nets._handle, \
            f_victorthesis=f_victorthesis, dthesis_dinput=dthesis_dinput)
    
    @staticmethod
    def get_f_vic(input, nets, qlknn_norms, f_vic, verbosity=None, df_vic_dinput=None):
        """
        get_f_vic(input, nets, qlknn_norms, f_vic[, verbosity, df_vic_dinput])
        
        
        Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_victor_rule.f90 lines 35-153
        
        Parameters
        ----------
        input : float array
        nets : Net_Collection
        qlknn_norms : Qlknn_Normpars
        f_vic : float array
        verbosity : int
        df_vic_dinput : float array
        
        """
        _qlknn_f90wrap.f90wrap_get_f_vic(input=input, nets=nets._handle, \
            qlknn_norms=qlknn_norms._handle, f_vic=f_vic, verbosity=verbosity, \
            df_vic_dinput=df_vic_dinput)
    
    @staticmethod
    def scale_with_victor(leading_map, input, nets, qlknn_norms, net_result, verbosity=None, \
        dnet_out_dinput=None):
        """
        scale_with_victor(leading_map, input, nets, qlknn_norms, net_result[, verbosity, \
            dnet_out_dinput])
        
        
        Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_victor_rule.f90 lines 155-224
        
        Parameters
        ----------
        leading_map : int array
        input : float array
        nets : Net_Collection
        qlknn_norms : Qlknn_Normpars
        net_result : float array
        verbosity : int
        dnet_out_dinput : float array
        
        """
        _qlknn_f90wrap.f90wrap_scale_with_victor(leading_map=leading_map, input=input, \
            nets=nets._handle, qlknn_norms=qlknn_norms._handle, net_result=net_result, \
            verbosity=verbosity, dnet_out_dinput=dnet_out_dinput)
    
    @property
    def c_1(self):
        """
        Element c_1 ftype=real(qlknn_dp) pytype=float
        
        
        Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_victor_rule.f90 line 7
        
        """
        return _qlknn_f90wrap.f90wrap_qlknn_victor_rule__get__c_1()
    
    @property
    def c_2(self):
        """
        Element c_2 ftype=real(qlknn_dp) pytype=float
        
        
        Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_victor_rule.f90 line 7
        
        """
        return _qlknn_f90wrap.f90wrap_qlknn_victor_rule__get__c_2()
    
    @property
    def c_3(self):
        """
        Element c_3 ftype=real(qlknn_dp) pytype=float
        
        
        Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_victor_rule.f90 line 7
        
        """
        return _qlknn_f90wrap.f90wrap_qlknn_victor_rule__get__c_3()
    
    @property
    def c_4(self):
        """
        Element c_4 ftype=real(qlknn_dp) pytype=float
        
        
        Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_victor_rule.f90 line 7
        
        """
        return _qlknn_f90wrap.f90wrap_qlknn_victor_rule__get__c_4()
    
    @property
    def gamma0_lower_bound(self):
        """
        Element gamma0_lower_bound ftype=real(qlknn_dp) pytype=float
        
        
        Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_victor_rule.f90 line 8
        
        """
        return _qlknn_f90wrap.f90wrap_qlknn_victor_rule__get__gamma0_lower_bound()
    
    @property
    def victor_te_norm(self):
        """
        Element victor_te_norm ftype=real(qlknn_dp) pytype=float
        
        
        Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_victor_rule.f90 line 9
        
        """
        return _qlknn_f90wrap.f90wrap_qlknn_victor_rule__get__victor_te_norm()
    
    def __str__(self):
        ret = ['<qlknn_victor_rule>{\n']
        ret.append('    c_1 : ')
        ret.append(repr(self.c_1))
        ret.append(',\n    c_2 : ')
        ret.append(repr(self.c_2))
        ret.append(',\n    c_3 : ')
        ret.append(repr(self.c_3))
        ret.append(',\n    c_4 : ')
        ret.append(repr(self.c_4))
        ret.append(',\n    gamma0_lower_bound : ')
        ret.append(repr(self.gamma0_lower_bound))
        ret.append(',\n    victor_te_norm : ')
        ret.append(repr(self.victor_te_norm))
        ret.append('}')
        return ''.join(ret)
    
    _dt_array_initialisers = []
    

qlknn_victor_rule = Qlknn_Victor_Rule()

class Qlknn_Error_Filter(f90wrap.runtime.FortranModule):
    """
    Module qlknn_error_filter
    
    
    Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_error_filter.f90 lines 3-116
    
    """
    @staticmethod
    def determine_validity_with_eb(abs_limits, rel_limits, net_out, net_eb, validity, \
        verbosity, mask=None):
        """
        determine_validity_with_eb(abs_limits, rel_limits, net_out, net_eb, validity, verbosity[, \
            mask])
        
        
        Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_error_filter.f90 lines 11-48
        
        Parameters
        ----------
        abs_limits : float array
        rel_limits : float array
        net_out : float array
        net_eb : float array
        validity : bool array
        verbosity : int
        mask : bool array
        
        """
        _qlknn_f90wrap.f90wrap_determine_validity_with_eb(abs_limits=abs_limits, \
            rel_limits=rel_limits, net_out=net_out, net_eb=net_eb, validity=validity, \
            verbosity=verbosity, mask=mask)
    
    @staticmethod
    def determine_validity_multiplied_networks(leading_map, validity, verbosity):
        """
        determine_validity_multiplied_networks(leading_map, validity, verbosity)
        
        
        Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_error_filter.f90 lines 50-85
        
        Parameters
        ----------
        leading_map : int array
        validity : bool array
        verbosity : int
        
        """
        _qlknn_f90wrap.f90wrap_determine_validity_multiplied_networks(leading_map=leading_map, \
            validity=validity, verbosity=verbosity)
    
    @staticmethod
    def determine_validity_merged_modes(merge_map, validity, merged_validity, verbosity):
        """
        determine_validity_merged_modes(merge_map, validity, merged_validity, verbosity)
        
        
        Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_error_filter.f90 lines 87-116
        
        Parameters
        ----------
        merge_map : int array
        validity : bool array
        merged_validity : bool array
        verbosity : int
        
        """
        _qlknn_f90wrap.f90wrap_determine_validity_merged_modes(merge_map=merge_map, \
            validity=validity, merged_validity=merged_validity, verbosity=verbosity)
    
    _dt_array_initialisers = []
    

qlknn_error_filter = Qlknn_Error_Filter()

class Qlknn_Python(f90wrap.runtime.FortranModule):
    """
    Module qlknn_python
    
    
    Defined at /tmp/pip-req-build-lkkusb0q/src/qlknn_python.f90 lines 3-48
    
    """
    @staticmethod
    def evaluate_qlknn_10d_direct(qlknn_path, input, qlknn_out, verbosityin=None, optsin=None, \
        qlknn_normsin=None):
        """
        evaluate_qlknn_10d_direct(qlknn_path, input, qlknn_out[, verbosityin, optsin, \
            qlknn_normsin])
        
        
        Defined at /tmp/pip-req-build-lkkusb0q/src/qlknn_python.f90 lines 8-20
        
        Parameters
        ----------
        qlknn_path : str
        input : float array
        qlknn_out : float array
        verbosityin : int
        optsin : Qlknn_Options
        qlknn_normsin : Qlknn_Normpars
        
        """
        _qlknn_f90wrap.f90wrap_evaluate_qlknn_10d_direct(qlknn_path=qlknn_path, input=input, \
            qlknn_out=qlknn_out, verbosityin=verbosityin, optsin=None if optsin is None else \
            optsin._handle, qlknn_normsin=None if qlknn_normsin is None else \
            qlknn_normsin._handle)
    
    @staticmethod
    def finalize():
        """
        finalize()
        
        
        Defined at /tmp/pip-req-build-lkkusb0q/src/qlknn_python.f90 lines 22-23
        
        
        """
        _qlknn_f90wrap.f90wrap_finalize()
    
    @staticmethod
    def abort(msg):
        """
        abort(msg)
        
        
        Defined at /tmp/pip-req-build-lkkusb0q/src/qlknn_python.f90 lines 46-48
        
        Parameters
        ----------
        msg : str
        
        """
        _qlknn_f90wrap.f90wrap_abort(msg=msg)
    
    _dt_array_initialisers = []
    

qlknn_python = Qlknn_Python()

class Qlknn_Evaluate_Nets(f90wrap.runtime.FortranModule):
    """
    Module qlknn_evaluate_nets
    
    
    Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_evaluate_nets.f90 lines 3-1988
    
    """
    @staticmethod
    def evaluate_qlknn_10d(input, nets, qlknn_out, verbosityin=None, optsin=None, \
        qlknn_normsin=None, dqlknn_out_dinput=None):
        """
        evaluate_qlknn_10d(input, nets, qlknn_out[, verbosityin, optsin, qlknn_normsin, \
            dqlknn_out_dinput])
        
        
        Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_evaluate_nets.f90 lines 14-245
        
        Parameters
        ----------
        input : float array
        nets : Net_Collection
        qlknn_out : float array
        verbosityin : int
        optsin : Qlknn_Options
        qlknn_normsin : Qlknn_Normpars
        dqlknn_out_dinput : float array
        
        """
        _qlknn_f90wrap.f90wrap_evaluate_qlknn_10d(input=input, nets=nets._handle, \
            qlknn_out=qlknn_out, verbosityin=verbosityin, optsin=None if optsin is None else \
            optsin._handle, qlknn_normsin=None if qlknn_normsin is None else \
            qlknn_normsin._handle, dqlknn_out_dinput=dqlknn_out_dinput)
    
    @staticmethod
    def evaluate_fullflux_net(input, nets, qlknn_out, verbosityin=None, optsin=None, \
        dqlknn_out_dinput=None):
        """
        evaluate_fullflux_net(input, nets, qlknn_out[, verbosityin, optsin, dqlknn_out_dinput])
        
        
        Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_evaluate_nets.f90 lines 247-382
        
        Parameters
        ----------
        input : float array
        nets : Net_Collection
        qlknn_out : float array
        verbosityin : int
        optsin : Qlknn_Options
        dqlknn_out_dinput : float array
        
        """
        _qlknn_f90wrap.f90wrap_evaluate_fullflux_net(input=input, nets=nets._handle, \
            qlknn_out=qlknn_out, verbosityin=verbosityin, optsin=None if optsin is None else \
            optsin._handle, dqlknn_out_dinput=dqlknn_out_dinput)
    
    @staticmethod
    def evaluate_jetexp_net(input, nets, n_members, qlknn_out, qlknn_eb, verbosityin=None, \
        optsin=None, dqlknn_out_dinput=None, qlknn_validity=None):
        """
        evaluate_jetexp_net(input, nets, n_members, qlknn_out, qlknn_eb[, verbosityin, optsin, \
            dqlknn_out_dinput, qlknn_validity])
        
        
        Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_evaluate_nets.f90 lines 384-722
        
        Parameters
        ----------
        input : float array
        nets : Net_Collection
        n_members : int
        qlknn_out : float array
        qlknn_eb : float array
        verbosityin : int
        optsin : Qlknn_Options
        dqlknn_out_dinput : float array
        qlknn_validity : bool array
        
        """
        _qlknn_f90wrap.f90wrap_evaluate_jetexp_net(input=input, nets=nets._handle, \
            n_members=n_members, qlknn_out=qlknn_out, qlknn_eb=qlknn_eb, verbosityin=verbosityin, \
            optsin=None if optsin is None else optsin._handle, \
            dqlknn_out_dinput=dqlknn_out_dinput, qlknn_validity=qlknn_validity)
    
    @staticmethod
    def hornnet_flux_from_constants(input, blocks, hornnet_constants, flux_out, \
        verbosityin=None, optsin=None, qlknn_normsin=None, dflux_dhornnet_constants=None, \
        dflux_dinput=None):
        """
        hornnet_flux_from_constants(input, blocks, hornnet_constants, flux_out[, verbosityin, \
            optsin, qlknn_normsin, dflux_dhornnet_constants, dflux_dinput])
        
        
        Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_evaluate_nets.f90 lines 724-1184
        
        Parameters
        ----------
        input : float array
        blocks : Block_Collection
        hornnet_constants : float array
        flux_out : float array
        verbosityin : int
        optsin : Qlknn_Options
        qlknn_normsin : Qlknn_Normpars
        dflux_dhornnet_constants : float array
        dflux_dinput : float array
        
        ------------------------
         Denormalize output
        """
        _qlknn_f90wrap.f90wrap_hornnet_flux_from_constants(input=input, blocks=blocks._handle, \
            hornnet_constants=hornnet_constants, flux_out=flux_out, verbosityin=verbosityin, \
            optsin=None if optsin is None else optsin._handle, qlknn_normsin=None if qlknn_normsin \
            is None else qlknn_normsin._handle, dflux_dhornnet_constants=dflux_dhornnet_constants, \
            dflux_dinput=dflux_dinput)
    
    @staticmethod
    def hornnet_multiply_jacobians(dhornnet_constants_dinput, dflux_dhornnet_constants, \
        dflux_dinput, dqlknn_out_dinput, verbosityin=None):
        """
        hornnet_multiply_jacobians(dhornnet_constants_dinput, dflux_dhornnet_constants, \
            dflux_dinput, dqlknn_out_dinput[, verbosityin])
        
        
        Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_evaluate_nets.f90 lines 1186-1248
        
        Parameters
        ----------
        dhornnet_constants_dinput : float array
        dflux_dhornnet_constants : float array
        dflux_dinput : float array
        dqlknn_out_dinput : float array
        verbosityin : int
        
        """
        \
            _qlknn_f90wrap.f90wrap_hornnet_multiply_jacobians(dhornnet_constants_dinput=dhornnet_constants_dinput, \
            dflux_dhornnet_constants=dflux_dhornnet_constants, dflux_dinput=dflux_dinput, \
            dqlknn_out_dinput=dqlknn_out_dinput, verbosityin=verbosityin)
    
    @staticmethod
    def hornnet_multiplier(heaviside_function_times, clip_by_value, hornnet_constants, \
        sepflux_out, outp, pow_idx, block_idx, slope_idx, f, g, h, \
        drelu_dhornnet_constants=None, drelu_dinput=None, \
        dclip_by_value_dhornnet_constants=None, dclip_by_value_dinput=None, \
        df_dhornnet_constants=None, df_dinput=None, dg_dhornnet_constants=None, \
        dg_dinput=None, dh_dhornnet_constants=None):
        """
        hornnet_multiplier(heaviside_function_times, clip_by_value, hornnet_constants, \
            sepflux_out, outp, pow_idx, block_idx, slope_idx, f, g, h[, drelu_dhornnet_constants, \
            drelu_dinput, dclip_by_value_dhornnet_constants, dclip_by_value_dinput, \
            df_dhornnet_constants, df_dinput, dg_dhornnet_constants, dg_dinput, \
            dh_dhornnet_constants])
        
        
        Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_evaluate_nets.f90 lines 1250-1292
        
        Parameters
        ----------
        heaviside_function_times : float array
        clip_by_value : float array
        hornnet_constants : float array
        sepflux_out : float array
        outp : int
        pow_idx : int
        block_idx : int
        slope_idx : int
        f : float array
        g : float array
        h : float array
        drelu_dhornnet_constants : float array
        drelu_dinput : float array
        dclip_by_value_dhornnet_constants : float array
        dclip_by_value_dinput : float array
        df_dhornnet_constants : float array
        df_dinput : float array
        dg_dhornnet_constants : float array
        dg_dinput : float array
        dh_dhornnet_constants : float array
        
        """
        \
            _qlknn_f90wrap.f90wrap_hornnet_multiplier(heaviside_function_times=heaviside_function_times, \
            clip_by_value=clip_by_value, hornnet_constants=hornnet_constants, \
            sepflux_out=sepflux_out, outp=outp, pow_idx=pow_idx, block_idx=block_idx, \
            slope_idx=slope_idx, f=f, g=g, h=h, drelu_dhornnet_constants=drelu_dhornnet_constants, \
            drelu_dinput=drelu_dinput, \
            dclip_by_value_dhornnet_constants=dclip_by_value_dhornnet_constants, \
            dclip_by_value_dinput=dclip_by_value_dinput, \
            df_dhornnet_constants=df_dhornnet_constants, df_dinput=df_dinput, \
            dg_dhornnet_constants=dg_dhornnet_constants, dg_dinput=dg_dinput, \
            dh_dhornnet_constants=dh_dhornnet_constants)
    
    @staticmethod
    def evaluate_hornnet_constants(input, blocks, qlknn_out, verbosityin=None, optsin=None, \
        qlknn_normsin=None, dqlknn_out_dinput=None):
        """
        evaluate_hornnet_constants(input, blocks, qlknn_out[, verbosityin, optsin, qlknn_normsin, \
            dqlknn_out_dinput])
        
        
        Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_evaluate_nets.f90 lines 1294-1813
        
        Parameters
        ----------
        input : float array
        blocks : Block_Collection
        qlknn_out : float array
        verbosityin : int
        optsin : Qlknn_Options
        qlknn_normsin : Qlknn_Normpars
        dqlknn_out_dinput : float array
        
        """
        _qlknn_f90wrap.f90wrap_evaluate_hornnet_constants(input=input, blocks=blocks._handle, \
            qlknn_out=qlknn_out, verbosityin=verbosityin, optsin=None if optsin is None else \
            optsin._handle, qlknn_normsin=None if qlknn_normsin is None else \
            qlknn_normsin._handle, dqlknn_out_dinput=dqlknn_out_dinput)
    
    @staticmethod
    def evaluate_multinet(net_input, nets, net_evaluate, net_result, verbosityin=None, \
        dnet_out_dnet_in=None):
        """
        evaluate_multinet(net_input, nets, net_evaluate, net_result[, verbosityin, \
            dnet_out_dnet_in])
        
        
        Defined at /tmp/pip-req-build-lkkusb0q/src/core/qlknn_evaluate_nets.f90 lines 1815-1988
        
        Parameters
        ----------
        net_input : float array
        nets : Net_Collection
        net_evaluate : bool array
        net_result : float array
        verbosityin : int
        dnet_out_dnet_in : float array
        
        """
        _qlknn_f90wrap.f90wrap_evaluate_multinet(net_input=net_input, nets=nets._handle, \
            net_evaluate=net_evaluate, net_result=net_result, verbosityin=verbosityin, \
            dnet_out_dnet_in=dnet_out_dnet_in)
    
    _dt_array_initialisers = []
    

qlknn_evaluate_nets = Qlknn_Evaluate_Nets()

