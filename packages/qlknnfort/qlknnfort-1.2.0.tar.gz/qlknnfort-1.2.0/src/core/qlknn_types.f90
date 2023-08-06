! This file is part of QLKNN-fortran
! You should have received the QLKNN-fortran LICENSE in the root of the project
module qlknn_types
  use iso_c_binding
  implicit none

  integer, parameter :: qlknn_dp=c_double
  integer, parameter :: lli=c_int64_t
  integer, parameter :: li=c_int32_t

  integer(lli), parameter :: stderr = 0

  real(qlknn_dp), parameter :: qe = 1.602176565e-19 !SI electron charge
  real(qlknn_dp), parameter :: mp = 1.672621777e-27 !SI protonmass
  real(qlknn_dp), parameter :: c_qlk_ref = sqrt(qe*1e3/mp)

  type ragged_weights_array
     real(qlknn_dp), dimension(:,:), allocatable :: weight_layer
  end type ragged_weights_array

  type ragged_biases_array
     real(qlknn_dp), dimension(:), allocatable :: bias_layer
  end type ragged_biases_array

!  type networktype
!    !! Type that defines a single feed-forward neural network.
!
!    !! Assumes the input vector \( x_{in} \) first has to be scaled with
!    !! \( a_{in} x_{in} + b_{in} \) and the network output \( y_{out} \)
!    !! has to be de-scaled using \( \frac{1}{a_{out}} y_{out} - b_{out} \)
!     real(qlknn_dp), dimension(:,:), allocatable :: weights_input
!     !! Input layer weights
!     real(qlknn_dp), dimension(:), allocatable ::   biases_input
!     !! Input layer biases
!     real(qlknn_dp), dimension(:,:,:), allocatable :: weights_hidden
!     !! Hidden layer weights
!     real(qlknn_dp), dimension(:,:), allocatable ::  biases_hidden
!     !! Hidden layer biases
!     real(qlknn_dp), dimension(:,:), allocatable :: weights_output
!     !! Output layer weights
!     real(qlknn_dp), dimension(:), allocatable ::   biases_output
!     !! Output layer biases
!
!     character(len=4), dimension(:), allocatable :: hidden_activation
!     !! Activation function of the activation layers. Can be only tanh
!
!     real(qlknn_dp), dimension(:), allocatable ::   feature_prescale_bias
!     !! Standardization bias \( b_{in} \) of the input features
!     real(qlknn_dp), dimension(:), allocatable ::   feature_prescale_factor
!     !! Standardization factor \( a_{in} \) of the input features
!     real(qlknn_dp), dimension(:), allocatable ::   target_prescale_bias
!     !! Standardization bias \( b_{out} \) of the output targets
!     real(qlknn_dp), dimension(:), allocatable ::   target_prescale_factor
!     !! Standardization factor \( a_{out} \) of the output targets
!  end type networktype

  type networktype
    !! Type that defines a single feed-forward neural network.

     integer(lli) :: n_hidden_layers
     !! Number of hidden layers (includes input layer)
     integer(lli) :: n_max_nodes
     !! Maximum number of layer nodes in NN, for easy memory allocation

    !! Assumes the input vector \( x_{in} \) first has to be scaled with
    !! \( a_{in} x_{in} + b_{in} \) and the network output \( y_{out} \)
    !! has to be de-scaled using \( \frac{1}{a_{out}} y_{out} - b_{out} \)
     real(qlknn_dp), dimension(:,:), allocatable :: weights_input
     !! Input layer weights
     real(qlknn_dp), dimension(:), allocatable ::   biases_input
     !! Input layer biases
     type(ragged_weights_array), dimension(:), allocatable :: weights_hidden
     !! Hidden layer weights
     type(ragged_biases_array), dimension(:), allocatable ::  biases_hidden
     !! Hidden layer biases
     real(qlknn_dp), dimension(:,:), allocatable :: weights_output
     !! Output layer weights
     real(qlknn_dp), dimension(:), allocatable ::   biases_output
     !! Output layer biases

     character(len=4), dimension(:), allocatable :: hidden_activation
     !! Activation function of the activation layers. Can be only tanh

     real(qlknn_dp), dimension(:), allocatable ::   feature_prescale_bias
     !! Standardization bias \( b_{in} \) of the input features
     real(qlknn_dp), dimension(:), allocatable ::   feature_prescale_factor
     !! Standardization factor \( a_{in} \) of the input features
     real(qlknn_dp), dimension(:), allocatable ::   target_prescale_bias
     !! Standardization bias \( b_{out} \) of the output targets
     real(qlknn_dp), dimension(:), allocatable ::   target_prescale_factor
     !! Standardization factor \( a_{out} \) of the output targets
  end type networktype

  type net_collection
    !! Type to collect multiple similar networks in a single structure
    !!
    !! Assumes all networks have the same input variables at the same
    !! index in the input array. Can be INTNAN if the index is not used
    !! for these networks. For normalizations, see qualikiz.com
     type(networktype), dimension(:), allocatable :: nets
     !! Array with feed-forward neural networks
     integer(lli) :: Zeff_ind
     !! Index of the effective charge \( Z_{eff} \)
     integer(lli) :: Ati_ind
     !! Index of the normalized logarithmic ion temperature gradient \( R/L_{T_i} \)
     integer(lli) :: Ate_ind
     !! Index of the normalized logarithmic electron temperature gradient \( R/L_{T_e} \)
     integer(lli) :: An_ind
     !! Index of the normalized logarithmic density gradient \( R/L_{n_e} = R/L_{n_i} \)
     integer(lli) :: q_ind
     !! Index of the safety factor \( q \)
     integer(lli) :: smag_ind
     !! Index of the normalized magnetic shear \( \hat{s} \)
     integer(lli) :: x_ind
     !! Index of the inverse aspect ratio \( r_{minor} / R_0 \)
     integer(lli) :: Ti_Te_ind
     !! Index of the temperature ratio \( T_i / T_e \)
     integer(lli) :: logNustar_ind
     !! Index of the logarithmic collision frequency \( \nu^* \)
     integer(lli) :: gammaE_ind
     !! Index of the ExB shearing rate \( \gamma_{E \times B} \)
     integer(lli) :: Te_ind
     !! Index of the electron temperature \( T_e \)
     integer(lli) :: Ane_ind
     !! Index of the normalized logarithmic electron density gradient \( R/L_{n_e} \neq R/L_{n_i} \)
     integer(lli) :: Machtor_ind
     !! Index of the normalized toroidal velocity \( v_{tor} / c_{ref} \)
     integer(lli) :: Autor_ind
     !! Index of the normalized toroidal velocity gradient \( R/L_{u_{tor}} \)
     integer(lli) :: alpha_ind
     !! Index of the MHD alpha \( \alpha_{MHD} \)
     integer(lli) :: Ani0_ind
     !! Index of the normalized logarithmic density gradient of the main ion \( R/L_{n_{i,0}} \)
     integer(lli) :: Ani1_ind
     !! Index of the normalized logarithmic density gradient of the main impurity \( R/L_{n_{i,1}} \)
     integer(lli) :: Ati0_ind
     !! Index of the normalized temperature gradient of the main ion \( R/L_{T_{i,0}} \)
     integer(lli) :: normni0_ind
     !! Index of the normalized density of the main ion \( n_{i,0} / n_e \)
     integer(lli) :: normni1_ind
     !! Index of the normalized density of the main impurity \( n_{i,1} / n_e \)
     integer(lli) :: Ti_Te0_ind
     !! Index of the temperature ratio (renamed, pending removal) \( T_i / T_e \)
     real(qlknn_dp) :: a
     !! Midplane-averaged minor radius of last-closed-flux-surface of the trained networks \( R_{min} \)
     real(qlknn_dp) :: R_0
     !! Midplane-averaged major radius of last-closed-flux-surface of the trained networks \( R_0 \)
  end type net_collection

  type hornnet_output_block
    !! Type representing a common block inside a late-fusion NN
    !!
    !! Collects hidden layers and output layers with similar shapes
    !! A single late-fusion net typically consists of multiples of
    !! these blocks, and a differently shaped input block
    type(ragged_weights_array), dimension(:), allocatable :: weights_hidden
    !! Hidden layer weights in ragged array
    type(ragged_biases_array), dimension(:), allocatable :: biases_hidden
    !! Hidden layer biases in ragged array
    real(qlknn_dp), dimension(:,:), allocatable ::   weights_output
    !! Output layer weights
    real(qlknn_dp), dimension(:), allocatable :: biases_output
    !! Output layer biases

    character(len=4), dimension(:), allocatable :: hidden_activation
    !! Activation function of the activation layers. Can be only tanh

    character(len=20) :: blockname
    !! Name of the block, useful for debugging
  end type hornnet_output_block

  type hornnet_input_block
    !! Type representing a common block inside a late-fusion NN
    !!
    !! Collects input layers and hidden layers with similar shapes
    !! A single late-fusion net typically consists of one of
    !! these blocks, and multile differently shaped output blocks
    real(qlknn_dp), dimension(:,:), allocatable ::   weights_input
    !! Input layer weights
    real(qlknn_dp), dimension(:), allocatable ::     biases_input
    !! Input layer biases

    real(qlknn_dp), dimension(:), allocatable ::   feature_prescale_bias
    !! Standardization bias \( b_{in} \) of the input features
    real(qlknn_dp), dimension(:), allocatable ::   feature_prescale_factor
    !! Standardization factor \( a_{in} \) of the input features
    real(qlknn_dp), dimension(:), allocatable ::   target_prescale_bias
    !! Standardization bias \( b_{out} \) of the output targets
    real(qlknn_dp), dimension(:), allocatable ::   target_prescale_factor
    !! Standardization factor \( a_{out} \) of the output targets
  end type hornnet_input_block

  type block_collection
    !! Type to collect late-fusion blocks
    type(hornnet_output_block), dimension(:), allocatable :: output_blocks
    type(hornnet_input_block), dimension(:), allocatable :: input_blocks
  end type block_collection

  type qlknn_options
    !! Common options for QLKNN
     logical :: use_ion_diffusivity_networks
     !! Use the networks predicting \( D_i, V_i \) instead of \( D_e, V_e \)
     logical :: apply_victor_rule
     !! Apply the 'victor rule' to include rotation
     logical :: use_effective_diffusivity
     !! Use the networks predicting \( \Gamma \) instead of \( D, V \)
     logical :: calc_heat_transport
     !! Evaluate the heat-predicting networks
     logical :: calc_part_transport
     !! Evaluate the particle-predicting networks
     logical :: use_ETG
     !! Evaluate the ETG-predicting networks
     logical :: use_ITG
     !! Evaluate the ITG-predicting networks
     logical :: use_TEM
     !! Evaluate the TEM-predicting networks
     logical :: apply_stability_clipping
     !! Clip all transport if leading flux is 0, see [apply_stability_clipping](|url|/proc/apply_stability_clipping.html)
     logical, dimension(:), allocatable :: constrain_inputs
     !! Clip inputs to given bounds if True, see [impose_input_constraints](|url|/proc/impose_input_constraints.html)
     real(qlknn_dp), dimension(:), allocatable :: min_input
     !! Input minimum \( c_{min} \), see [impose_input_constraints](|url|/proc/impose_input_constraints.html)
     real(qlknn_dp), dimension(:), allocatable :: max_input
     !! Input maximum \( c_{max} \), see [impose_input_constraints](|url|/proc/impose_input_constraints.html)
     real(qlknn_dp), dimension(:), allocatable :: margin_input
     !! Input bound margin \( c_{margin} \), see [impose_input_constraints](|url|/proc/impose_input_constraints.html)
     logical, dimension(:), allocatable :: constrain_outputs
     !! Clip outputs to given bounds if True, see [impose_output_constraints](|url|/proc/impose_output_constraints.html)
     real(qlknn_dp), dimension(:), allocatable :: min_output
     !! Output minimum \( c_{min} \), see [impose_output_constraints](|url|/proc/impose_output_constraints.html)
     real(qlknn_dp), dimension(:), allocatable :: max_output
     !! Output maximum \( c_{max} \), see [impose_output_constraints](|url|/proc/impose_output_constraints.html)
     real(qlknn_dp), dimension(:), allocatable :: margin_output
     !! Output bound margin \( c_{margin} \), see [impose_output_constraints](|url|/proc/impose_output_constraints.html)
     logical :: merge_modes
     !! Merge ETG/ITG/TEM of the same transport variable together, see [merge_modes](|url|/proc/merge_modes.html)
     logical :: force_evaluate_all
     !! Force evaluation of all networks regardless of other settings
  end type qlknn_options

  type qlknn_normpars
    !! Normalisation parameters for rotation shear conversion
    !!
    !! Needed to apply the [victor rule](|url|/proc/scale_with_victor.html)
     real(qlknn_dp) :: a
     !! Current midplane-averaged minor radius of last-closed-flux-surface \( R_{min} \)
     real(qlknn_dp) :: R0
     !! Current midplane-averaged major radius of last-closed-flux-surface \( R_{0} \)
     real(qlknn_dp), dimension(:), allocatable :: A1
     !! Main ion mass in amu
  end type qlknn_normpars

contains
  subroutine default_qlknn_hyper_options(opts)
    type (qlknn_options), intent(out) :: opts

    allocate(opts%constrain_inputs(11))
    allocate(opts%min_input(11))
    allocate(opts%max_input(11))
    allocate(opts%margin_input(11))
    allocate(opts%constrain_outputs(20))
    allocate(opts%min_output(20))
    allocate(opts%max_output(20))
    allocate(opts%margin_output(20))

    opts%use_ion_diffusivity_networks = .false.
    opts%apply_victor_rule = .false.
    opts%use_effective_diffusivity = .false.
    opts%calc_heat_transport = .true.
    opts%calc_part_transport = .true.
    opts%use_etg = .true.
    opts%use_itg = .true.
    opts%use_tem = .true.
    opts%apply_stability_clipping = .true.
    opts%constrain_inputs = .true.
    opts%min_input = (/1., 0., 0., -5., 0.66, -1., .09, 0.25, -5., -100., -100./)
    opts%max_input = (/3., 14., 14., 6., 15., 5., .99, 2.5, 0., 100., 100./)
    opts%margin_input = 0.95
    opts%constrain_outputs = .true.
    opts%min_output = -300
    opts%max_output = 300
    opts%margin_output = 1.
    opts%merge_modes = .true.
    opts%force_evaluate_all = .false.
  end subroutine default_qlknn_hyper_options

  subroutine default_qlknn_fullflux_options(opts)
    type (qlknn_options), intent(out) :: opts

    allocate(opts%constrain_inputs(11))
    allocate(opts%min_input(11))
    allocate(opts%max_input(11))
    allocate(opts%margin_input(11))
    allocate(opts%constrain_outputs(3))
    allocate(opts%min_output(3))
    allocate(opts%max_output(3))
    allocate(opts%margin_output(3))

    opts%use_ion_diffusivity_networks = .false. ! Does not exists for fullflux nets
    opts%apply_victor_rule = .false. ! Cannot apply for fullflux nets
    opts%use_effective_diffusivity = .true. ! Always true for fullflux nets
    opts%calc_heat_transport = .true.
    opts%calc_part_transport = .true.
    opts%use_etg = .true. ! Always true for fullflux nets
    opts%use_itg = .true. ! Always true for fullflux nets
    opts%use_tem = .true. ! Always true for fullflux nets
    opts%apply_stability_clipping = .false. ! Does not exists for fullflux nets
    opts%constrain_inputs = .true.
    opts%min_input = (/1., 0., 0., -5., 0.66, -1., .09, 0.25, -5., -100., -100./)
    opts%max_input = (/3., 14., 14., 6., 15., 5., .99, 2.5, 0., 100., 100./)
    opts%margin_input = 0.95
    opts%constrain_outputs = .true.
    opts%min_output = -300
    opts%max_output = 300
    opts%margin_output = 1.
    opts%merge_modes = .true.
    opts%force_evaluate_all = .false.
  end subroutine default_qlknn_fullflux_options

  subroutine default_qlknn_jetexp_options(opts)
    type (qlknn_options), intent(out) :: opts

    allocate(opts%constrain_inputs(15))
    allocate(opts%min_input(15))
    allocate(opts%max_input(15))
    allocate(opts%margin_input(15))
    allocate(opts%constrain_outputs(25))
    allocate(opts%min_output(25))
    allocate(opts%max_output(25))
    allocate(opts%margin_output(25))

    opts%use_ion_diffusivity_networks = .false.
    opts%apply_victor_rule = .false. ! Cannot apply for jetexp nets
    opts%use_effective_diffusivity = .true.
    opts%calc_heat_transport = .true.
    opts%calc_part_transport = .true.
    opts%use_etg = .true.
    opts%use_itg = .true.
    opts%use_tem = .true.
    opts%apply_stability_clipping = .false. ! Does not exists for jetexp nets
    opts%constrain_inputs = .true.
    opts%min_input = -99999
    opts%max_input = 99999
    opts%margin_input = 0.95
    opts%constrain_outputs = .true.
    opts%min_output = -300
    opts%max_output = 300
    opts%margin_output = 1.
    opts%merge_modes = .true.
    opts%force_evaluate_all = .false.
  end subroutine default_qlknn_jetexp_options

  subroutine default_qlknn_hornnet_options(opts)
    type (qlknn_options), intent(out) :: opts

    allocate(opts%constrain_inputs(11))
    allocate(opts%min_input(11))
    allocate(opts%max_input(11))
    allocate(opts%margin_input(11))
    allocate(opts%constrain_outputs(7))
    allocate(opts%min_output(7))
    allocate(opts%max_output(7))
    allocate(opts%margin_output(7))

    opts%use_ion_diffusivity_networks = .false. ! Only have Gamma_e
    opts%apply_victor_rule = .false.
    opts%use_effective_diffusivity = .true. ! Only have Gamma_e
    opts%calc_heat_transport = .true.
    opts%calc_part_transport = .true.
    opts%use_etg = .true.
    opts%use_itg = .true.
    opts%use_tem = .true.
    opts%apply_stability_clipping = .false. ! Does not exists for fusion nets
    opts%constrain_inputs = .true.
    opts%min_input = -999
    opts%max_input = 999
    opts%margin_input = 0.95
    opts%constrain_outputs = .true.
    opts%min_output = -300
    opts%max_output = 300
    opts%margin_output = 1.
    opts%merge_modes = .true.
    opts%force_evaluate_all = .false.
  end subroutine default_qlknn_hornnet_options

  subroutine print_qlknn_options(opts)
    type (qlknn_options), intent(in) :: opts
    integer(lli) :: i, n_in, n_out

    n_in = size(opts%min_input)
    n_out = size(opts%min_output)
    WRITE(*,*) 'use_ion_diffusivity_networks', opts%use_ion_diffusivity_networks
    WRITE(*,*) 'apply_victor_rule'           , opts%apply_victor_rule
    WRITE(*,*) 'use_effective_diffusivity'   , opts%use_effective_diffusivity
    WRITE(*,*) 'calc_heat_transport'         , opts%calc_heat_transport
    WRITE(*,*) 'calc_part_transport'         , opts%calc_part_transport
    WRITE(*,*) 'use_etg'                     , opts%use_etg
    WRITE(*,*) 'use_itg'                     , opts%use_itg
    WRITE(*,*) 'use_tem'                     , opts%use_tem
    WRITE(*,*) 'apply_stability_clipping'    , opts%apply_stability_clipping
    WRITE(*,*) 'constrain_inputs'            , opts%constrain_inputs
    WRITE(*,'(A,14(F8.3, 1X))') 'min_input'   , (opts%min_input(i), i=1,n_in)
    WRITE(*,'(A,14(F8.3, 1X))') 'max_input'   , (opts%max_input(i), i=1,n_in)
    WRITE(*,'(A,14(F8.3, 1X))') 'margin_input', (opts%margin_input(i), i=1,n_in)
    WRITE(*,*) 'constrain_outputs'           , opts%constrain_outputs
    WRITE(*,'(A,25(F6.1, 1X))') 'min_output'  , (opts%min_output(i), i=1,n_out)
    WRITE(*,'(A,25(F6.1, 1X))') 'max_output'  , (opts%max_output(i), i=1,n_out)
    WRITE(*,'(A,25(F6.1, 1X))') 'margin_output', (opts%margin_output(i), i=1,n_out)
    WRITE(*,*) 'merge_modes'                  , opts%merge_modes
    WRITE(*,*) 'force_evaluate_all'           , opts%force_evaluate_all
  end subroutine print_qlknn_options

  subroutine get_networks_to_evaluate(opts, net_evaluate)
    type (qlknn_options), intent(in) :: opts
    logical, dimension(20), intent(out) :: net_evaluate
    if (opts%force_evaluate_all) then
       net_evaluate(:) = .TRUE.
    else
       net_evaluate(:) = .FALSE.
       if (opts%use_etg) then
          net_evaluate(1) = .TRUE.
       end if
       if (opts%use_itg) then
          net_evaluate(2:4:2) = .TRUE.
       end if
       if (opts%use_tem) then
          net_evaluate(3:5:2) = .TRUE.
       end if

       if (opts%use_itg) then
          net_evaluate(6) = .TRUE.
       end if
       if (opts%use_tem) then
          net_evaluate(7) = .TRUE.
       end if

       if (.not. opts%use_effective_diffusivity) then
          if (opts%use_ion_diffusivity_networks) then
             if (opts%use_itg) then
                net_evaluate(14) = .TRUE.
             end if
             if (opts%use_tem) then
                net_evaluate(15) = .TRUE.
             end if
          else ! if not use_ion_diffusivity_networks
             if (opts%use_itg) then
                net_evaluate(8) = .TRUE.
             end if
             if (opts%use_tem) then
                net_evaluate(9) = .TRUE.
             end if
          end if !opts%use_ion_diffusivity_networks
       end if ! opts%use_effective_diffusivity

       if (opts%apply_victor_rule) then
          net_evaluate(20) = .TRUE.
       end if
    end if ! Force evaluate all
  end subroutine get_networks_to_evaluate

  subroutine networktype_deallocate(net)
    type(networktype), INTENT(inout) :: net
    integer :: ii
    if (allocated(net%weights_input)) deallocate(net%weights_input)
    if (allocated(net%biases_input)) deallocate(net%biases_input)
    if (allocated(net%weights_hidden)) then
      do ii = 1, size(net%weights_hidden)
        if (allocated(net%weights_hidden(ii)%weight_layer)) deallocate(net%weights_hidden(ii)%weight_layer)
      end do
      deallocate(net%weights_hidden)
    end if
    if (allocated(net%biases_hidden)) then
      do ii = 1, size(net%biases_hidden)
        if (allocated(net%biases_hidden(ii)%bias_layer)) deallocate(net%biases_hidden(ii)%bias_layer)
      end do
      deallocate(net%biases_hidden)
    end if
    if (allocated(net%weights_output)) deallocate(net%weights_output)
    if (allocated(net%biases_output)) deallocate(net%biases_output)

    if (allocated(net%hidden_activation)) deallocate(net%hidden_activation)

    if (allocated(net%feature_prescale_bias)) deallocate(net%feature_prescale_bias)
    if (allocated(net%feature_prescale_factor)) deallocate(net%feature_prescale_factor)
    if (allocated(net%target_prescale_bias)) deallocate(net%target_prescale_bias)
    if (allocated(net%target_prescale_factor)) deallocate(net%target_prescale_factor)
  end subroutine networktype_deallocate

  subroutine all_networktype_deallocate(net_coll)
    type(net_collection), intent(inout) :: net_coll
    integer :: ii
    do ii = 1, size(net_coll%nets)
       call networktype_deallocate(net_coll%nets(ii))
    end do
    deallocate(net_coll%nets)
  end subroutine all_networktype_deallocate

  subroutine qlknn_normpars_allocate(qlknn_norms, nrho)
    type(qlknn_normpars), intent(inout) :: qlknn_norms
    integer :: nrho
    allocate(qlknn_norms%A1(nrho))
  end subroutine qlknn_normpars_allocate

  subroutine qlknn_normpars_deallocate(qlknn_norms)
    type(qlknn_normpars), intent(inout) :: qlknn_norms
    if (allocated(qlknn_norms%A1)) deallocate(qlknn_norms%A1)
  end subroutine qlknn_normpars_deallocate

end module qlknn_types
