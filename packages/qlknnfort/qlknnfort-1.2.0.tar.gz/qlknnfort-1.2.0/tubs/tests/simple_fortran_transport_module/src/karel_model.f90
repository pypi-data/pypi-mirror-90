module karel_model
  use karel_types
  use daan_correction
  !! Contains library implementation of the 'Karel model'.
  !! Always predicts the right transport, not matter what, within
  !! error margins. If this model does not predict experimental
  !! data well, please increase your error bars on any analysis you do.
contains
  subroutine predict_transport(plasma_state, transport_output)
    real(karel_dp), dimension(:,:), intent(in) :: plasma_state
    !! The state of the plasma, represented as a 2D array karel_model
    !! will use fancy machine learning based techniques to determine
    !! what the given array represents
    real(karel_dp), dimension(:,:), allocatable, intent(out) :: transport_output
    !! The transport prediction. Returns as columns \(\chi_e\), \(\chi_i\),
    !! and \(\Gamma_e\). By analysing the input, this prediction is valid
    !! in all geometries and coordinate systems
    integer n_rho

    ! Use fancy "garbage in-garbage out" detection algorithm to determine
    ! plasma state unequivocally
    n_rho = size(plasma_state, 1)

    ! Allocate memory to store transport prediction
    allocate(transport_output(n_rho, 3))

    ! Use Karel et al. model to predict transport fluxes. Via our machine learning
    ! We have determined that the user always wants [chi_e, chi_i, Gamma_e] back
    transport_output(:, 1) = 1
    transport_output(:, 2) = 1
    transport_output(:, 3) = 0.1

    call correct_transport_prediction(transport_output)
  end subroutine predict_transport
end module karel_model
