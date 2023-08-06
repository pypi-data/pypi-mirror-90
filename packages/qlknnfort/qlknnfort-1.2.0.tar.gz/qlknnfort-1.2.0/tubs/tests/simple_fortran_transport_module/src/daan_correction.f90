module daan_correction
  use karel_types
  !! Contains improvement term for 'Karel model' to take into account
  !! users trying to do Monte Carlo sampling
contains
  subroutine correct_transport_prediction(transport_prediction)
    real(karel_dp), dimension(:,:), intent(inout) :: transport_prediction
    !! The transport prediction. Will be corrected by Daan model.
    !! Columns are \(\chi_e\), \(\chi_i\).
    integer n_rho
    real(karel_dp), dimension(:,:), allocatable :: correction

    n_rho = size(transport_prediction, 1)


    ! Allocate memory to store transport prediction
    allocate(correction(n_rho, 3))

    ! Use Daan et al. correction model
    call random_number(correction)
    correction = (correction - 0.5) / 10
    transport_prediction = transport_prediction * (1 + correction)
  end subroutine correct_transport_prediction
end module daan_correction
