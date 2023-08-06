! This file is part of QLKNN-fortran
! You should have received the QLKNN-fortran LICENSE in the root of the project
module qlknn_disk_io
#include "preprocessor.inc"
    use qlknn_types

    implicit none
    character(len=32), dimension(20), parameter, private :: qlknn_hyper_names = &
        (/ 'net_efeetg_gb                   ', &
           'net_efeitg_gb_div_efiitg_gb     ', &
           'net_efetem_gb                   ', &
           'net_efiitg_gb                   ', &
           'net_efitem_gb_div_efetem_gb     ', &
           'net_pfeitg_gb_div_efiitg_gb     ', &
           'net_pfetem_gb_div_efetem_gb     ', &
           'net_dfeitg_gb_div_efiitg_gb     ', &
           'net_dfetem_gb_div_efetem_gb     ', &
           'net_vteitg_gb_div_efiitg_gb     ', &
           'net_vtetem_gb_div_efetem_gb     ', &
           'net_vceitg_gb_div_efiitg_gb     ', &
           'net_vcetem_gb_div_efetem_gb     ', &
           'net_dfiitg_gb_div_efiitg_gb     ', &
           'net_dfitem_gb_div_efetem_gb     ', &
           'net_vtiitg_gb_div_efiitg_gb     ', &
           'net_vtitem_gb_div_efetem_gb     ', &
           'net_vciitg_gb_div_efiitg_gb     ', &
           'net_vcitem_gb_div_efetem_gb     ', &
           'net_gam_leq_gb                  ' /)

    character(len=13), dimension(3), parameter, private :: fullflux_names = &
        (/ 'net_efe_gb', &
           'net_efi_gb', &
           'net_pfe_gb' /)

    character(len=32), dimension(25), parameter, private :: qlknn_jetexp_names = &
        (/ 'net_efeetg_gb                   ', &
           'net_efeitg_gb_div_efiitg_gb     ', &
           'net_efetem_gb                   ', &
           'net_efiitg_gb                   ', &
           'net_efitem_gb_div_efetem_gb     ', &
           'net_pfeitg_gb_div_efiitg_gb     ', &
           'net_pfetem_gb_div_efetem_gb     ', &
           'net_pfiitg_gb_div_efiitg_gb     ', &
           'net_pfitem_gb_div_efetem_gb     ', &
           'net_vfiitg_gb_div_efiitg_gb     ', &
           'net_vfitem_gb_div_efetem_gb     ', &
           'net_dfeitg_gb_div_efiitg_gb     ', &
           'net_dfetem_gb_div_efetem_gb     ', &
           'net_vteitg_gb_div_efiitg_gb     ', &
           'net_vtetem_gb_div_efetem_gb     ', &
           'net_vceitg_gb_div_efiitg_gb     ', &
           'net_vcetem_gb_div_efetem_gb     ', &
           'net_dfiitg_gb_div_efiitg_gb     ', &
           'net_dfitem_gb_div_efetem_gb     ', &
           'net_vtiitg_gb_div_efiitg_gb     ', &
           'net_vtitem_gb_div_efetem_gb     ', &
           'net_vciitg_gb_div_efiitg_gb     ', &
           'net_vcitem_gb_div_efetem_gb     ', &
           'net_vriitg_gb_div_efiitg_gb     ', &
           'net_vritem_gb_div_efetem_gb     ' /)

    character(len=12), dimension(15), parameter, private :: qlknn_hornnet_output_blocks = &
        (/ 'c1_etg      ', & ! 1
           'c1_itg      ', & ! 2
           'c1_tem      ', & ! 3
           'c2_efeetg_gb', & ! 4
           'c2_efeitg_gb', & ! 5
           'c2_efetem_gb', & ! 6
           'c2_efiitg_gb', & ! 7
           'c2_efitem_gb', & ! 8
           'c3_efeetg_gb', & ! 9
           'c3_efeitg_gb', & ! 10
           'c3_efetem_gb', & ! 11
           'c3_efiitg_gb', & ! 12
           'c3_efitem_gb', & ! 13
           'pfeitg_gb   ', & ! 14
           'pfetem_gb   ' /) ! 15

    character(len=7), dimension(5), parameter, private :: qlknn_hornnet_input_blocks = &
        (/ 'etg    ', &
           'itg    ', &
           'tem    ', &
           'itg_pfe', &
           'tem_pfe' /)

    type(net_collection), save, target :: nets
    type(block_collection), save, target :: blocks
contains
    subroutine load_qlknn_hyper_nets_from_disk(folder, verbosityin)
        character(len=*), intent(in) :: folder
        integer(lli), optional, intent(in) :: verbosityin
        integer(lli) :: verbosity

        if(present(verbosityin)) then
            verbosity=verbosityin
        else
            verbosity = 0
        end if

        ! Constant for all 9D networks
        nets%Zeff_ind = 1
        nets%Ati_ind = 2
        nets%Ate_ind = 3
        nets%An_ind = 4
        nets%q_ind = 5
        nets%smag_ind = 6
        nets%x_ind = 7
        nets%Ti_Te_ind = 8
        nets%logNustar_ind = 9
        nets%gammaE_ind = 10
        nets%Te_ind = 11

        nets%Ane_ind = INTNAN
        nets%Autor_ind = INTNAN
        nets%Machtor_ind = INTNAN
        nets%alpha_ind = INTNAN
        nets%Ani0_ind = INTNAN
        nets%Ani1_ind = INTNAN
        nets%Ati0_ind = INTNAN
        nets%normni0_ind = INTNAN
        nets%normni1_ind = INTNAN
        nets%Ti_Te0_ind = INTNAN

        nets%a = 1.
        nets%R_0 = 3.

        allocate(nets%nets(20))
        call load_multinet_from_disk(qlknn_hyper_names, folder, verbosity)
    end subroutine load_qlknn_hyper_nets_from_disk

    subroutine load_fullflux_nets_from_disk(folder, verbosityin)
        character(len=*), intent(in) :: folder
        integer(lli), optional, intent(in) :: verbosityin
        integer(lli) :: verbosity

        if(present(verbosityin)) then
            verbosity=verbosityin
        else
            verbosity = 0
        end if

        ! Constant for all 9D networks
        nets%Zeff_ind = 1
        nets%Ati_ind = 2
        nets%Ate_ind = 3
        nets%An_ind = 4
        nets%q_ind = 5
        nets%smag_ind = 6
        nets%x_ind = 7
        nets%Ti_Te_ind = 8
        nets%logNustar_ind = 9
        nets%gammaE_ind = 10
        nets%Te_ind = 11

        nets%Ane_ind = INTNAN
        nets%Autor_ind = INTNAN
        nets%Machtor_ind = INTNAN
        nets%alpha_ind = INTNAN
        nets%Ani0_ind = INTNAN
        nets%Ani1_ind = INTNAN
        nets%Ati0_ind = INTNAN
        nets%normni0_ind = INTNAN
        nets%normni1_ind = INTNAN
        nets%Ti_Te0_ind = INTNAN

        nets%a = 1.
        nets%R_0 = 3.

        allocate(nets%nets(3))
        call load_multinet_from_disk(fullflux_names, folder, verbosity)
    end subroutine load_fullflux_nets_from_disk

    subroutine load_jetexp_nets_from_disk(folder, n_members, verbosityin)
        character(len=*), intent(in) :: folder
        integer(lli), intent(in) :: n_members
        integer(lli), optional, intent(in) :: verbosityin
        integer(lli) :: verbosity, n_nets, ii, jj
        character(len=32+1+2) :: filename
        character(len=32+1+2), dimension(:), allocatable :: member_filenames
        character(len=2) :: file_tag

        if(present(verbosityin)) then
            verbosity=verbosityin
        else
            verbosity = 0
        end if

        nets%Ane_ind = 1
        nets%Ate_ind = 2
        nets%Autor_ind = 3
        nets%Machtor_ind = 4
        nets%x_ind = 5
        nets%Zeff_ind = 6
        nets%gammaE_ind = 7
        nets%q_ind = 8
        nets%smag_ind = 9
        nets%alpha_ind = 10
        nets%Ani1_ind = 11
        nets%Ati0_ind = 12
        nets%normni1_ind = 13
        nets%Ti_Te0_ind = 14
        nets%logNustar_ind = 15

        nets%Ani0_ind = INTNAN
        nets%normni0_ind = INTNAN

        nets%a = INTNAN
        nets%R_0 = INTNAN

        ERRORSTOP(n_members > 100, 'Amount of members result in too long filenames, abort')
        n_nets = size(qlknn_jetexp_names)
        allocate(nets%nets(n_nets * n_members))
        allocate(member_filenames(n_nets * n_members))
        do ii = 1, n_nets
          do jj = 1, n_members
            write (file_tag,'(I2.2)') jj
            filename = trim(qlknn_jetexp_names(ii)) // '_' // adjustl(file_tag)
            member_filenames(n_members * (ii - 1) + jj) = filename
            if (verbosity > 4) then
              print *, n_members * (ii - 1) + jj, filename
            endif
          enddo
        enddo
        if (verbosity > 3) then
          do ii = 1, n_nets * n_members
            print *, member_filenames(ii)
          enddo
        endif
        call load_multinet_from_disk(member_filenames, folder, verbosity)
    end subroutine load_jetexp_nets_from_disk

    subroutine load_hornnet_nets_from_disk(folder, verbosityin)
        character(len=*), intent(in) :: folder
        integer(lli), optional, intent(in) :: verbosityin
        integer(lli) :: verbosity

        if(present(verbosityin)) then
            verbosity=verbosityin
        else
            verbosity = 0
        end if

        !! Constant for all 9D networks
        nets%Zeff_ind = 1
        nets%Ati_ind = 2
        nets%Ate_ind = 3
        nets%An_ind = 4
        nets%q_ind = 5
        nets%smag_ind = 6
        nets%x_ind = 7
        nets%Ti_Te_ind = 8
        nets%logNustar_ind = 9
        nets%gammaE_ind = 10
        nets%Te_ind = 11

        !nets%Ane_ind = INTNAN
        !nets%Autor_ind = INTNAN
        !nets%Machtor_ind = INTNAN
        !nets%alpha_ind = INTNAN
        !nets%Ani0_ind = INTNAN
        !nets%Ani1_ind = INTNAN
        !nets%Ati0_imd = INTNAN
        !nets%normni0_ind = INTNAN
        !nets%normni1_ind = INTNAN
        !nets%Ti_Te0 = INTNAN

        !nets%a = 1.
        !nets%R_0 = 3.

        !allocate(nets%nets(3))
        allocate(blocks%output_blocks(15))
        call load_multinet_from_disk(qlknn_hornnet_output_blocks, folder, verbosity, 1_lli)
        allocate(blocks%input_blocks(5))
        call load_multinet_from_disk(qlknn_hornnet_input_blocks, folder, verbosity, 2_lli)
    end subroutine load_hornnet_nets_from_disk

    subroutine load_multinet_from_disk(netlist, folder, verbosityin, stylein)
        character(len=*), intent(in) :: folder
        !! Folder  networe files reside in
        character(len=*), dimension(:), intent(in) :: netlist
        !! List of network files to be loaded
        integer(lli), optional, intent(in) :: verbosityin
        !! Verbosity of this function
        integer(lli), optional, intent(in) :: stylein
        !! Style of NN. 0: regular FFNN, 1: late-fusion NN output block, 2: late-fusion NN input block
        integer(lli) :: style
        character(len=32) :: net_name
        character(len=4096) :: filepath
        integer(lli) :: ii
        integer(lli) :: verbosity
        logical :: file_exists

        if (present(verbosityin)) then
            verbosity=verbosityin
        else
            verbosity = 0
        endif

        if (present(stylein)) then
          style = stylein
        else
          style = 0
        endif

        do ii = 1,size(netlist)
            net_name = netlist(ii)
            filepath = trim(folder) // '/' // trim(net_name) // '.nml'
            inquire(file=filepath, exist=file_exists)
            if (file_exists) then
              if (verbosity >= 1) write(*,*) 'Loading ', trim(filepath)
              select case (style)
              case (0)
                call load_net_from_disk(filepath, nets%nets(ii))
              case (1)
                call load_hornnet_output_block_from_disk(filepath, blocks%output_blocks(ii))
              case (2)
                call load_hornnet_input_block_from_disk(filepath, blocks%input_blocks(ii))
              !case (3)
              !  call load_shaped_net_from_disk(filepath, nets%nets(ii))
              end select
            else
              write(stderr,*) 'Cannot load ', trim(filepath)
              ERRORSTOP(.true., 'NN namelist does not exists')
            endif
        end do
    end subroutine load_multinet_from_disk

    subroutine load_net_from_disk(filename, net)
        integer(lli) :: n_hidden_layers, n_hidden_nodes = 0, n_inputs, n_outputs
        integer(lli), dimension(:), allocatable :: n_hidden_node_vector
        character(len=*), intent(in) :: filename

        real(qlknn_dp), dimension(:,:), allocatable ::   weights_input
        real(qlknn_dp), dimension(:), allocatable ::     biases_input
        real(qlknn_dp), dimension(:,:,:), allocatable :: weights_hidden
        real(qlknn_dp), dimension(:,:), allocatable ::   biases_hidden
        real(qlknn_dp), dimension(:,:), allocatable ::   weights_output
        real(qlknn_dp), dimension(:), allocatable :: biases_output

        character(len=4), dimension(:), allocatable ::      hidden_activation

        real(qlknn_dp), dimension(:), allocatable ::   feature_prescale_bias
        real(qlknn_dp), dimension(:), allocatable ::   feature_prescale_factor
        real(qlknn_dp), dimension(:), allocatable ::   target_prescale_bias
        real(qlknn_dp), dimension(:), allocatable ::   target_prescale_factor

        ! Generate non-uniform dynamically-size arrays
        ! Columns (first index) are neurons in current layer, rows (second index) are neurons in previous layer
        logical :: shaped = .false.
        integer(lli) :: ii, layer_max_cols = 0, layer_max_rows = 0
        type(ragged_weights_array), dimension(:), allocatable :: shaped_weights_hidden
        type(ragged_biases_array), dimension(:), allocatable :: shaped_biases_hidden

        type(networktype), intent(out) :: net
        namelist /sizes/ n_hidden_layers, n_hidden_nodes, n_inputs, n_outputs
        namelist /nodes/ n_hidden_node_vector
        namelist /netfile/ biases_hidden, hidden_activation, weights_input, biases_input, &
            weights_hidden, weights_output, biases_output, &
            feature_prescale_bias, feature_prescale_factor, target_prescale_bias,&
            target_prescale_factor
        open(10,file=filename,ACTION='READ')
        read(10,nml=sizes)

        ! Shaped network detected by having n_hidden_nodes=0 in sizes
        allocate(n_hidden_node_vector(n_hidden_layers))
        if (n_hidden_nodes == 0) then
          shaped = .true.
          read(10,nml=nodes)
        else
          n_hidden_node_vector = n_hidden_nodes
        endif
        if (shaped) then
          do ii = 2, n_hidden_layers
            if (n_hidden_node_vector(ii) == 0) then
              write(stderr,*) 'Cannot load ', trim(filename)
              ERRORSTOP(.true., 'Something went wrong in IO')
            endif
            if (n_hidden_node_vector(ii-1) > layer_max_rows) then
              layer_max_rows = n_hidden_node_vector(ii-1)
            endif
            if (n_hidden_node_vector(ii) > layer_max_cols) then
              layer_max_cols = n_hidden_node_vector(ii)
            endif
          enddo
          if (n_outputs > layer_max_cols) then
            layer_max_cols = n_outputs
          endif
        else
          if (n_hidden_nodes == 0) then
            write(stderr,*) 'Cannot load ', trim(filename)
            ERRORSTOP(.true., 'Something went wrong in IO')
          endif
          layer_max_rows = n_hidden_nodes
          layer_max_cols = n_hidden_nodes
        endif
        !write(*, *) 'n_hidden_layers', n_hidden_layers
        !write(*, *) 'n_hidden_nodes', n_hidden_nodes
        !write(*, *) 'n_inputs', n_inputs
        !write(*, *) 'n_outputs', n_outputs

        allocate(weights_input(n_hidden_node_vector(1), n_inputs))
        allocate(biases_input(n_hidden_node_vector(1)))
        allocate(weights_hidden(layer_max_cols, layer_max_rows, n_hidden_layers-1))
        allocate(biases_hidden(layer_max_cols, n_hidden_layers-1))
        allocate(weights_output(n_outputs, n_hidden_node_vector(n_hidden_layers)))
        allocate(biases_output(n_outputs))
        allocate(hidden_activation(n_hidden_layers))
        allocate(feature_prescale_bias(n_inputs))
        allocate(feature_prescale_factor(n_inputs))
        allocate(target_prescale_bias(n_outputs))
        allocate(target_prescale_factor(n_outputs))
        ! Initialization required for minimal storage solution in .nml files
        weights_input = 0
        biases_input = 0
        weights_hidden = 0
        biases_hidden = 0
        weights_output = 0
        biases_output = 0
        ! Explicitly allocate net structure, needed for ifort
        allocate(net%weights_input(n_hidden_node_vector(1), n_inputs))
        allocate(net%biases_input(n_hidden_node_vector(1)))
        allocate(net%weights_hidden(n_hidden_layers-1))
        allocate(net%biases_hidden(n_hidden_layers-1))
        allocate(net%weights_output(n_outputs, n_hidden_node_vector(n_hidden_layers)))
        allocate(net%biases_output(n_outputs))
        allocate(net%hidden_activation(n_hidden_layers))
        allocate(net%feature_prescale_bias(n_inputs))
        allocate(net%feature_prescale_factor(n_inputs))
        allocate(net%target_prescale_bias(n_outputs))
        allocate(net%target_prescale_factor(n_outputs))
        read(10,nml=netfile)
        close(10)

        ! Allocate and fill shaped hidden layer weights and biases
        allocate(shaped_weights_hidden(n_hidden_layers-1))
        allocate(shaped_biases_hidden(n_hidden_layers-1))
        do ii = 2, n_hidden_layers
          allocate(shaped_weights_hidden(ii-1)%weight_layer(n_hidden_node_vector(ii), n_hidden_node_vector(ii-1)))
          allocate(shaped_biases_hidden(ii-1)%bias_layer(n_hidden_node_vector(ii)))
          ! Explicitly allocate net structure, same as above
          allocate(net%weights_hidden(ii-1)%weight_layer(n_hidden_node_vector(ii),n_hidden_node_vector(ii-1)))
          allocate(net%biases_hidden(ii-1)%bias_layer(n_hidden_node_vector(ii)))
          shaped_weights_hidden(ii-1)%weight_layer = weights_hidden(:n_hidden_node_vector(ii), :n_hidden_node_vector(ii-1), ii-1)
          shaped_biases_hidden(ii-1)%bias_layer = biases_hidden(:n_hidden_node_vector(ii), ii-1)
        enddo

        ! New fields for ease of processing in network evaluation
        net%n_hidden_layers = n_hidden_layers
        net%n_max_nodes = layer_max_cols
        if (layer_max_rows > layer_max_cols) then
          net%n_max_nodes = layer_max_rows
        endif

        !write(*,nml=net)
        net%weights_input = weights_input
        net%biases_input = biases_input
        net%weights_hidden = shaped_weights_hidden
        net%biases_hidden = shaped_biases_hidden
        net%weights_output = weights_output
        net%biases_output = biases_output

        net%hidden_activation = hidden_activation

        net%target_prescale_bias = target_prescale_bias
        net%target_prescale_factor = target_prescale_factor
        net%feature_prescale_bias = feature_prescale_bias
        net%feature_prescale_factor = feature_prescale_factor

        deallocate(weights_hidden)
        deallocate(biases_hidden)

    end subroutine load_net_from_disk

    subroutine load_hornnet_output_block_from_disk(filename, output_block)
      character(len=*), intent(in) :: filename

      integer(lli) :: n_hidden_layers, n_hidden_nodes = 0, n_outputs, slash_idx, lay

      real(qlknn_dp), dimension(:,:,:), allocatable :: weights_hidden
      real(qlknn_dp), dimension(:,:), allocatable ::   biases_hidden
      real(qlknn_dp), dimension(:,:), allocatable ::   weights_output
      real(qlknn_dp), dimension(:), allocatable :: biases_output
      character(len=20) :: blockname

      character(len=4), dimension(:), allocatable ::      hidden_activation

      type(hornnet_output_block), intent(out) :: output_block

      namelist /sizes/ n_hidden_layers, n_hidden_nodes, n_outputs
      namelist /netfile/ biases_hidden, hidden_activation, &
          weights_hidden, weights_output, biases_output
      open(10,file=filename,ACTION='READ')
      read(10,nml=sizes)
      if (n_hidden_nodes == 0) then
        write(stderr,*) 'Cannot load ', trim(filename)
        ERRORSTOP(.true., 'Something went wrong in IO')
      endif
      slash_idx = index(filename,'/',BACK=.TRUE.)
      if (slash_idx /= 0) then
        if (len(blockname) <= len(trim(filename(slash_idx+1:)))) then
          write(stderr,*) 'Warning! blockname too long for saving. Trimming..'
        endif
        blockname = trim(filename(slash_idx+1:))
      else
        if (len(blockname) <= len(trim(filename))) then
          write(stderr,*) 'Warning! blockname too long for saving. Trimming..'
        endif
        blockname = trim(filename)
      endif
      output_block%blockname = blockname
      !write(*, *) 'n_hidden_layers', n_hidden_layers
      !write(*, *) 'n_hidden_nodes', n_hidden_nodes
      !write(*, *) 'n_inputs', n_inputs
      !write(*, *) 'n_outputs', n_outputs
      !write(*,*) n_hidden_layers, n_hidden_nodes
      allocate(weights_hidden(n_hidden_nodes, n_hidden_nodes, n_hidden_layers))
      allocate(biases_hidden(n_hidden_nodes, n_hidden_layers))
      allocate(weights_output(1, n_hidden_nodes))
      allocate(biases_output(n_outputs))
      allocate(hidden_activation(n_hidden_layers))
      ! Explicitly allocate output_block structure, needed for ifort
      allocate(output_block%weights_hidden(n_hidden_layers))
      allocate(output_block%biases_hidden(n_hidden_layers))
      allocate(output_block%weights_output(1, n_hidden_nodes))
      allocate(output_block%biases_output(n_outputs))
      allocate(output_block%hidden_activation(n_hidden_layers))
      read(10,nml=netfile)
      close(10)
      !write(*,nml=output_block)
      do lay = 1, n_hidden_layers
        output_block%biases_hidden(lay)%bias_layer = biases_hidden(:, lay)
        output_block%weights_hidden(lay)%weight_layer = weights_hidden(:, :, lay)
      enddo
      output_block%weights_output = weights_output
      output_block%biases_output = biases_output

      output_block%hidden_activation = hidden_activation

    end subroutine load_hornnet_output_block_from_disk

    subroutine load_hornnet_input_block_from_disk(filename, input_block)
      character(len=*), intent(in) :: filename

      integer(lli) :: n_inputs = 0, n_hidden_nodes, n_target_prescale, n_feature_prescale

      real(qlknn_dp), dimension(:,:), allocatable ::   weights_input
      real(qlknn_dp), dimension(:), allocatable :: biases_input

      real(qlknn_dp), dimension(:), allocatable ::   feature_prescale_bias
      real(qlknn_dp), dimension(:), allocatable ::   feature_prescale_factor
      real(qlknn_dp), dimension(:), allocatable ::   target_prescale_bias
      real(qlknn_dp), dimension(:), allocatable ::   target_prescale_factor


      type(hornnet_input_block), intent(out) :: input_block

      namelist /sizes/ n_inputs, n_hidden_nodes, n_target_prescale, n_feature_prescale
      namelist /netfile/ weights_input, biases_input, &
           target_prescale_factor, target_prescale_bias, feature_prescale_factor, feature_prescale_bias
      open(10,file=filename,ACTION='READ')
      read(10,nml=sizes)
      if (n_inputs == 0) then
        write(stderr,*) 'Cannot load ', trim(filename)
        ERRORSTOP(.true., 'Something went wrong in IO')
      endif

      allocate(weights_input(n_hidden_nodes, n_inputs))
      allocate(biases_input(n_hidden_nodes))
      allocate(feature_prescale_bias(n_feature_prescale))
      allocate(feature_prescale_factor(n_feature_prescale))
      allocate(target_prescale_bias(n_target_prescale))
      allocate(target_prescale_factor(n_target_prescale))
      ! Explicitly allocate net structure, needed for ifort
      allocate(input_block%weights_input(n_hidden_nodes, n_inputs))
      allocate(input_block%biases_input(n_hidden_nodes))
      allocate(input_block%feature_prescale_bias(n_feature_prescale))
      allocate(input_block%feature_prescale_factor(n_feature_prescale))
      allocate(input_block%target_prescale_bias(n_target_prescale))
      allocate(input_block%target_prescale_factor(n_target_prescale))
      read(10,nml=netfile)
      close(10)
      input_block%weights_input = weights_input
      input_block%biases_input = biases_input

      input_block%target_prescale_bias = target_prescale_bias
      input_block%target_prescale_factor = target_prescale_factor
      input_block%feature_prescale_bias = feature_prescale_bias
      input_block%feature_prescale_factor = feature_prescale_factor

    end subroutine load_hornnet_input_block_from_disk
end module qlknn_disk_io
