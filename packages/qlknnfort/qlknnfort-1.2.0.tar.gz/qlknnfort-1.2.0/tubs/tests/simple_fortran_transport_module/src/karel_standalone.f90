program karel_standalone
  use karel_model, only: predict_transport
  use karel_types, only: karel_dp
  implicit none

  integer :: n_rho
  integer :: ii
  integer :: verbosity
  real(karel_dp), dimension(:), allocatable :: rhotorn, te, ti
  real(karel_dp), dimension(:,:), allocatable :: plasma_state
  real(karel_dp), dimension(:,:), allocatable :: transport_prediction

  print *, 'Running binary karel_standalone'

  ! Define the plasma state.
  n_rho = 24
  allocate(rhotorn(n_rho), te(n_rho), ti(n_rho))
  rhotorn(:) = (/ (real(ii, karel_dp)/(n_rho-1), ii=0, n_rho) /)
  te = 8 ! keV
  ti = 8 ! keV

  allocate(plasma_state(24, 3))
  plasma_state(:, 1) = rhotorn
  plasma_state(:, 2) = te
  plasma_state(:, 3) = ti

  verbosity = 1
  ! Optionally print plasma state
  if (verbosity >= 1) then
    print *, 'Plasma state is: [rhotorn, te, ti]'
    do ii = 1, n_rho
      print *, plasma_state(ii, :)
    enddo
  endif

  ! Get transport prediction
  call predict_transport(plasma_state, transport_prediction)

  ! Optionally report result to user
  if (verbosity >= 1) then
    print *, 'Transport result is: [chi_e, chi_i, Gamma_e]'
    do ii = 1, n_rho
      print *, transport_prediction(ii, :)
    enddo
  endif

  print *, 'Done running binary karel_standalone'

end program karel_standalone
