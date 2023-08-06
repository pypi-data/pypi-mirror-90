! This file is part of QLKNN-fortran
! You should have received the QLKNN-fortran LICENSE in the root of the project
module qlknn_10d_source_net
#include "preprocessor.inc"
  use qlknn_types
  use net_efeetg_gb              !  ,only: get_net_efeetg_gb
  use net_efeitg_gb_div_efiitg_gb!  ,only: get_net_efeitg_gb_div_efiitg_gb
  use net_efetem_gb              !  ,only: get_net_efetem_gb
  use net_efiitg_gb              !  ,only: get_net_efiitg_gb
  use net_efitem_gb_div_efetem_gb!  ,only: get_net_efitem_gb_div_efetem_gb
  use net_pfeitg_gb_div_efiitg_gb!  ,only: get_net_pfeitg_gb_div_efiitg_gb
  use net_pfetem_gb_div_efetem_gb!  ,only: get_net_pfetem_gb_div_efetem_gb
  use net_dfeitg_gb_div_efiitg_gb!  ,only: get_net_dfeitg_gb_div_efiitg_gb
  use net_dfetem_gb_div_efetem_gb!  ,only: get_net_dfetem_gb_div_efetem_gb
  use net_vteitg_gb_div_efiitg_gb!  ,only: get_net_vteitg_gb_div_efiitg_gb
  use net_vtetem_gb_div_efetem_gb!  ,only: get_net_vtetem_gb_div_efetem_gb
  use net_vceitg_gb_div_efiitg_gb!  ,only: get_net_vceitg_gb_div_efiitg_gb
  use net_vcetem_gb_div_efetem_gb!  ,only: get_net_vcetem_gb_div_efetem_gb
  use net_dfiitg_gb_div_efiitg_gb!  ,only: get_net_dfiitg_gb_div_efiitg_gb
  use net_dfitem_gb_div_efetem_gb!  ,only: get_net_dfitem_gb_div_efetem_gb
  use net_vtiitg_gb_div_efiitg_gb!  ,only: get_net_vtiitg_gb_div_efiitg_gb
  use net_vtitem_gb_div_efetem_gb!  ,only: get_net_vtitem_gb_div_efetem_gb
  use net_vciitg_gb_div_efiitg_gb!  ,only: get_net_vciitg_gb_div_efiitg_gb
  use net_vcitem_gb_div_efetem_gb!  ,only: get_net_vcitem_gb_div_efetem_gb
  use net_gam_leq_gb             !  ,only: get_net_gam_leq_gb

  implicit none
  type(net_collection), save, target :: nets
contains
  subroutine init_all_nets()
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
    nets%a = 1.
    nets%R_0 = 3.

    allocate(nets%nets(20))
    nets%nets(1)  = get_efeetg_gb()
    nets%nets(2)  = get_efeitg_gb_div_efiitg_gb()
    nets%nets(3)  = get_efetem_gb()
    nets%nets(4)  = get_efiitg_gb()
    nets%nets(5)  = get_efitem_gb_div_efetem_gb()
    nets%nets(6)  = get_pfeitg_gb_div_efiitg_gb()
    nets%nets(7)  = get_pfetem_gb_div_efetem_gb()
    nets%nets(8)  = get_dfeitg_gb_div_efiitg_gb()
    nets%nets(9)  = get_dfetem_gb_div_efetem_gb()
    nets%nets(10) = get_vteitg_gb_div_efiitg_gb()
    nets%nets(11) = get_vtetem_gb_div_efetem_gb()
    nets%nets(12) = get_vceitg_gb_div_efiitg_gb()
    nets%nets(13) = get_vcetem_gb_div_efetem_gb()
    nets%nets(14) = get_dfiitg_gb_div_efiitg_gb()
    nets%nets(15) = get_dfitem_gb_div_efetem_gb()
    nets%nets(16) = get_vtiitg_gb_div_efiitg_gb()
    nets%nets(17) = get_vtitem_gb_div_efetem_gb()
    nets%nets(18) = get_vciitg_gb_div_efiitg_gb()
    nets%nets(19) = get_vcitem_gb_div_efetem_gb()
    nets%nets(20) = get_gam_leq_gb()
  end subroutine init_all_nets
end module qlknn_10d_source_net
