! This file is part of QLKNN-fortran
! You should have received the QLKNN-fortran LICENSE in the root of the project
module qlknn_evaluate_nets
#include "preprocessor.inc"
  use qlknn_types
  use qlknn_primitives
  use qlknn_victor_rule
  use qlknn_error_filter, only: determine_validity_with_eb, determine_validity_multiplied_networks, determine_validity_merged_modes

#ifdef MPI
  use mpi
#endif
  implicit none
contains
  subroutine evaluate_QLKNN_10D(input, nets, qlknn_out, verbosityin, optsin, qlknn_normsin, dqlknn_out_dinput)
    real(qlknn_dp), dimension(:,:), intent(in) :: input
    real(qlknn_dp), dimension(:,:), allocatable :: input_clipped
    integer(lli), optional, intent(in) :: verbosityin
    type(net_collection), intent(in) :: nets
    type(qlknn_options), optional, intent(in) :: optsin
    type(qlknn_normpars), optional, intent(in) :: qlknn_normsin

    real(qlknn_dp), dimension(:,:), intent(out) :: qlknn_out
    real(qlknn_dp), dimension(:,:,:), optional, intent(out) :: dqlknn_out_dinput

    type(qlknn_normpars) :: qlknn_norms

    integer(lli) :: ii, rho, verbosity, outp
    integer(li) :: n_rho, n_outputs, n_total_inputs
    integer(li), parameter :: n_nets = 20
    real(qlknn_dp), dimension(:), allocatable :: res
    real(qlknn_dp), dimension(:,:), allocatable :: net_result
    real(qlknn_dp), dimension(:,:), allocatable :: net_input
    real(qlknn_dp), dimension(:,:,:), allocatable :: dnet_out_dnet_in, dnet_out_dinput
    logical, dimension(:,:), allocatable :: jacobian_clipmask
    type(qlknn_options) :: opts
    logical, dimension(n_nets) :: net_evaluate
    logical :: calcder
    character(len=100) :: fmt_tmp
#if (defined(LLI) && defined(__INTEL_COMPILER)) || defined(MEXING)
    integer(lli) :: my_world_rank
#else
    integer(li) :: my_world_rank
#endif
#ifdef MPI
#if (defined(LLI) && defined(__INTEL_COMPILER)) || defined(MEXING)
    integer(lli) :: mpi_ierr, world_size
#else
    integer(li) :: mpi_ierr, world_size
#endif
#endif
    integer(lli), dimension(10,3), parameter :: merge_map = reshape( (/ &
         1, 1, 4, 6, 8, 10, 12, 14, 16, 18, &
         2, 0, 5, 7, 9, 11, 13, 15, 17, 19, &
         3, 0, 0, 0, 0,  0,  0,  0,  0,  0 &
         /), (/ 10,3 /))
         !  1 efe_GB
         !  2 efeETG_GB
         !  3 efi_GB
         !  4 pfe_GB
         !  5 dfe_GB
         !  6 vte_GB
         !  7 vce_GB
         !  8 dfi_GB
         !  9 vti_GB
         ! 10 vci_GB
    integer(lli), dimension(9,3) :: leading_map
    leading_map = reshape( (/ &
         1, 0, 0, 0,  0,  0,  0,  0,  0, & ! ETG
         3, 5, 7, 9, 11, 13, 15, 17, 19, & ! TEM
         4, 2, 6, 8, 10, 12, 14, 16, 18  & ! ITG
         /), (/ 9, 3 /))

    ! zeff ati  ate   an         q      smag         x  ti_te logNustar
    !1.0   2.000000  5.0  2.0  0.660156  0.399902  0.449951    1.0      0.001
    !1.0  13.000000  5.0  2.0  0.660156  0.399902  0.449951    1.0      0.001
    if(present(verbosityin)) then
       verbosity=verbosityin
    else
       verbosity = 0
    end if

#ifdef MPI
    call MPI_COMM_SIZE(MPI_COMM_WORLD, world_size, mpi_ierr)
    call MPI_COMM_RANK(MPI_COMM_WORLD, my_world_rank, mpi_ierr)
    if (my_world_rank == 0) then
       if (verbosity >= 2) write(*,*) 'World size is ', world_size
    end if
    if (verbosity >= 2) write(*,*) 'Hello world from rank ', my_world_rank
#else
    my_world_rank = 0
#endif

    if(present(dqlknn_out_dinput)) then
      calcder = .true.
    else
      calcder = .false.
    end if

    n_total_inputs = int(size(input, 1), li)
    n_rho = int(size(input, 2), li)
    n_outputs = int(size(qlknn_out, 2), li)
    allocate(net_input(9, n_rho))
    allocate(net_result(n_rho, n_nets))

    allocate(res(n_rho)) !Debug

    if (calcder) then
      allocate(dnet_out_dnet_in(n_nets, n_rho, 9))
      dnet_out_dnet_in = 0
    end if

    if (.NOT. (n_rho == size(qlknn_out, 1))) then
       write(stderr,*) 'size(qlknn_out, 1)=', size(qlknn_out, 1),', nrho=', n_rho

       ERRORSTOP(.true., 'Rows of qlknn_out should be equal to number of radial points!')
    end if

    ! set options according to optsin if present from calling program. Otherwise set default
    if(present(optsin)) then
       opts=optsin
    else
       CALL default_qlknn_hyper_options(opts)
    end if

    if (verbosity >= 1 .and. my_world_rank == 0) then
       call print_qlknn_options(opts)
       write(*,*) 'input, n_rho=', n_rho
       do rho = 1, n_rho
          WRITE(*,'(11(F7.2, 1X))') (input(ii, rho), ii=1,n_total_inputs)
       end do
    end if

    if (opts%merge_modes .AND. .NOT. (n_outputs == size(qlknn_out, 2))) then
       write(stderr,*) 'size(qlknn_out, 2)=', size(qlknn_out, 2),', n_outputs=', n_outputs
       ERRORSTOP(.true., 'Columns of qlknn_out should be equal to number of outputs!')
    elseif (.NOT. opts%merge_modes .AND. .NOT. (n_nets == size(qlknn_out, 2))) then
       write(stderr,*) 'size(qlknn_out, 2)=', size(qlknn_out, 2),', n_nets=', n_nets
       ERRORSTOP(.true., 'Columns of qlknn_out should be equal to number of nets!')
    end if

    if (opts%apply_victor_rule .AND. .NOT. present(qlknn_normsin)) then
       ERRORSTOP(.true., 'Need to pass qlknn_normsin when applying Victor rule')
    else if (present(qlknn_normsin)) then
       qlknn_norms = qlknn_normsin
    end if



    ! Impose input constants
    if (calcder) then
      call impose_input_constraints(input, input_clipped, opts, verbosity, jacobian_clipmask)
    else
      call impose_input_constraints(input, input_clipped, opts, verbosity)
    endif

    net_input = input_clipped((/ nets%Zeff_ind, nets%Ati_ind, nets%Ate_ind, &
         nets%An_ind, nets%q_ind, nets%smag_ind, nets%x_ind, &
         nets%Ti_Te_ind, nets%logNustar_ind /), :)

    if (verbosity >= 2 .and. my_world_rank == 0) then
       write(*,*) 'net_input(:,1)'
       write(*,*) net_input(:,1)
    end if
    call get_networks_to_evaluate(opts, net_evaluate)

    if (verbosity >= 2 .and. my_world_rank == 0) then
       write(*,*) 'Evaluate networks:'
       write(*,*) net_evaluate
    end if


    ! Evaluate all neural networks
    if (calcder) then
      call evaluate_multinet(net_input, nets, net_evaluate, net_result, verbosity, dnet_out_dnet_in)
    else
      call evaluate_multinet(net_input, nets, net_evaluate, net_result, verbosity)
    endif

    if (calcder) then
      allocate(dnet_out_dinput(n_nets, n_rho, n_total_inputs))
      dnet_out_dinput(:, :, 1:size(dnet_out_dinput, 3) - 2) = dnet_out_dnet_in
      dnet_out_dinput(:, :, size(dnet_out_dinput, 3) - 1:size(dnet_out_dinput, 3)) = 0
    endif

    ! Clip leading fluxes to 0
    if (calcder) then
      call impose_leading_flux_constraints(leading_map, net_result, verbosity, dnet_out_dinput)
    else
      call impose_leading_flux_constraints(leading_map, net_result, verbosity)
    endif
    if (verbosity >= 3 .and. my_world_rank == 0) then
       WRITE(*,*) 'net_result (pre-div-multiplicate)'
       WRITE(fmt_tmp,'(A,I0,A)') '(', n_nets, '(F7.2,X))'
       do rho = 1, n_rho
          WRITE(*, fmt_tmp) (net_result(rho, ii), ii=1,n_nets)
       end do
    end if

    if (calcder) then
      call multiply_div_networks(leading_map, net_result, verbosity, dnet_out_dinput)
    else
      call multiply_div_networks(leading_map, net_result, verbosity)
    endif

    if (verbosity >= 3 .and. my_world_rank == 0) then
       WRITE(*,'(A)') 'net_result'
       do rho = 1, n_rho
          WRITE(fmt_tmp,'(A,I0,A)') '(', n_nets, '(F7.2,X))'
          WRITE(*,fmt_tmp) (net_result(rho, ii), ii=1,n_nets)
       end do
    end if

    if (opts%apply_victor_rule) then
      if (calcder) then
        call scale_with_victor(leading_map, input_clipped, nets, qlknn_norms, net_result, verbosity, dnet_out_dinput)
      else
        call scale_with_victor(leading_map, input_clipped, nets, qlknn_norms, net_result, verbosity)
      endif
    end if

    ! Clip based on leading
    call apply_stability_clipping(leading_map, net_result, verbosity)
    if (verbosity >= 3 .and. my_world_rank == 0) then
       WRITE(*,'(A)') 'with rotation stability clipped'
       do rho = 1, n_rho
          WRITE(fmt_tmp,'(A,I0,A)') '(', n_nets, '(F7.2,X))'
          WRITE(*,fmt_tmp) (net_result(rho, ii), ii=1,n_nets)
       end do
    end if

    ! Zero out Jacobians of clipped inputs
    if (calcder) then
     do outp = 1, n_nets
       !dqlknn_out_dinput(n_outputs, n_rho, total_n_in)
       where(transpose(jacobian_clipmask)) dnet_out_dinput(outp, :, :) = 0
     enddo
    endif

    if (calcder) then
      call impose_output_constraints(net_result, opts, verbosity, dnet_out_dinput)
    else
      call impose_output_constraints(net_result, opts, verbosity)
    endif
    if (verbosity >= 2 .and. my_world_rank == 0) then
       WRITE(*,'(A)') 'with rotation output clipped'
       do rho = 1, n_rho
          WRITE(fmt_tmp,'(A,I0,A)') '(', n_nets, '(F7.2,X))'
          WRITE(*,fmt_tmp) (net_result(rho, ii), ii=1,n_nets)
       end do
    end if

    ! Merge ETG/ITG/TEM modes together
    if (opts%merge_modes) then
       if (calcder) then
         call merge_modes(merge_map, net_result, qlknn_out, verbosity, dnet_out_dinput, dqlknn_out_dinput)
       else
         call merge_modes(merge_map, net_result, qlknn_out, verbosity)
       endif
       if (verbosity >= 1 .and. my_world_rank == 0) then
          WRITE(*,*) 'with rotation modes merged'
          do rho = 1, n_rho
             WRITE(*,'(10(F7.2, 1X))') (qlknn_out(rho, ii), ii=1,10)
          end do
       end if
    else
       qlknn_out = net_result
       if (calcder) then
         dqlknn_out_dinput = dnet_out_dinput
       endif
       if (verbosity >= 1 .and. my_world_rank == 0) then
          WRITE(*,*) 'with rotation modes non-merged'
          WRITE(fmt_tmp,'(A,I0,A)') '(', n_nets, '(F7.2,X))'
          do rho = 1, n_rho
             WRITE(*,fmt_tmp) (qlknn_out(rho, ii), ii=1,n_nets)
          end do
       end if
    end if

  end subroutine evaluate_QLKNN_10D

  subroutine evaluate_fullflux_net(input, nets, qlknn_out, verbosityin, optsin, dqlknn_out_dinput)
    real(qlknn_dp), dimension(:,:), intent(in) :: input
    real(qlknn_dp), dimension(:,:), allocatable :: input_clipped
    integer(lli), optional, intent(in) :: verbosityin
    type(net_collection), intent(in) :: nets
    type(qlknn_options), optional, intent(in) :: optsin

    real(qlknn_dp), dimension(:,:), intent(out) :: qlknn_out
    real(qlknn_dp), dimension(:,:,:), optional, intent(out) :: dqlknn_out_dinput

    integer(lli) ii, rho, verbosity, outp
    integer(li) :: n_outputs = 3
    integer(li) n_rho, n_in
    real(qlknn_dp), dimension(:), allocatable :: res
    real(qlknn_dp), dimension(:,:), allocatable :: net_result
    real(qlknn_dp), dimension(:,:), allocatable :: net_input
    real(qlknn_dp), dimension(:,:,:), allocatable :: dnet_out_dnet_in, dnet_out_dinput
    logical, dimension(:,:), allocatable :: jacobian_clipmask
    type(qlknn_options) :: opts
    logical, dimension(3) :: net_evaluate
    logical :: calcder
    character(len=100) :: fmt_tmp
#if (defined(LLI) && defined(__INTEL_COMPILER)) || defined(MEXING)
    integer(lli) :: my_world_rank
#else
    integer(li) :: my_world_rank
#endif
#ifdef MPI
#if (defined(LLI) && defined(__INTEL_COMPILER)) || defined(MEXING)
    integer(lli) :: mpi_ierr, world_size
#else
    integer(li) :: mpi_ierr, world_size
#endif
#endif
    net_evaluate = .true.

    ! zeff ati  ate   an         q      smag         x  ti_te logNustar
    !1.0   2.000000  5.0  2.0  0.660156  0.399902  0.449951    1.0      0.001
    !1.0  13.000000  5.0  2.0  0.660156  0.399902  0.449951    1.0      0.001
    if(present(verbosityin)) then
       verbosity=verbosityin
    else
       verbosity = 0
    end if

#ifdef MPI
    call MPI_COMM_SIZE(MPI_COMM_WORLD, world_size, mpi_ierr)
    call MPI_COMM_RANK(MPI_COMM_WORLD, my_world_rank, mpi_ierr)
    if (my_world_rank == 0) then
       if (verbosity >= 2) write(*,*) 'World size in evaluate_fullflux_net is ', world_size
    end if
    if (verbosity >= 2) write(*,*) 'Hello world from evaluate_fullflux_net rank ', my_world_rank
#else
    my_world_rank = 0
#endif

    if(present(dqlknn_out_dinput)) then
      calcder = .true.
    else
      calcder = .false.
    end if

    n_rho = int(size(input, 2), li)
    n_in = int(size(input, 1), li)
    allocate(net_input(9, n_rho))
    allocate(net_result(n_rho, n_outputs))

    allocate(res(n_rho)) !Debug

    if (calcder) then
      allocate(dnet_out_dnet_in(n_outputs, n_rho, 9))
      dnet_out_dnet_in = 0
    end if

    if (.NOT. (n_rho == size(qlknn_out, 1))) then
       write(stderr,*) 'size(qlknn_out, 1)=', size(qlknn_out, 1),', nrho=', n_rho

       ERRORSTOP(.true., 'Rows of qlknn_out should be equal to number of radial points!')
    end if

    ! set options according to optsin if present from calling program. Otherwise set default
    if(present(optsin)) then
       opts=optsin
    else
       CALL default_qlknn_fullflux_options(opts)
    end if

    if (verbosity >= 1 .and. my_world_rank == 0) then
       call print_qlknn_options(opts)
       write(*,*) 'input, n_rho=', n_rho
       do rho = 1, n_rho
          WRITE(*,'(11(F7.2, 1X))') (input(ii, rho), ii=1,n_in)
       end do
    end if

    if (opts%merge_modes .AND. .NOT. (n_outputs == size(qlknn_out, 2))) then
       write(stderr,*) 'size(qlknn_out, 2)=', size(qlknn_out, 2),', n_outputs=', n_outputs
       ERRORSTOP(.true., 'Columns of qlknn_out should be equal to number of outputs!')
     endif

    ! Impose input constants
    if (calcder) then
      call impose_input_constraints(input, input_clipped, opts, verbosity, jacobian_clipmask)
    else
      call impose_input_constraints(input, input_clipped, opts, verbosity)
    endif

    net_input = input_clipped((/ nets%Zeff_ind, nets%Ati_ind, nets%Ate_ind, &
         nets%An_ind, nets%q_ind, nets%smag_ind, nets%x_ind, &
         nets%Ti_Te_ind, nets%logNustar_ind /), :)

    if (verbosity >= 2 .and. my_world_rank == 0) then
       write(*,*) 'net_input(:,1)'
       write(*,*) net_input(:,1)
    end if

    if (verbosity >= 2 .and. my_world_rank == 0) then
       write(*,*) 'Evaluate networks:'
       write(*,*) net_evaluate
    end if


    ! Evaluate all neural networks
    if (calcder) then
      call evaluate_multinet(net_input, nets, net_evaluate, net_result, verbosity, dnet_out_dnet_in)
    else
      call evaluate_multinet(net_input, nets, net_evaluate, net_result, verbosity)
    endif

    !TODO check
    if (calcder) then
      allocate(dnet_out_dinput(n_outputs, n_rho, n_in))
      dnet_out_dinput(:, :, 1:size(dnet_out_dinput, 3) - 2) = dnet_out_dnet_in
      dnet_out_dinput(:, :, size(dnet_out_dinput, 3) - 1:size(dnet_out_dinput, 3)) = 0
    endif

    ! Zero out Jacobians of clipped inputs
    if (calcder) then
     do outp = 1, n_outputs
       !dqlknn_out_dinput(n_outputs, n_rho, n_in)
       where(transpose(jacobian_clipmask)) dnet_out_dinput(outp, :, :) = 0
     enddo
    endif

    if (calcder) then
      call impose_output_constraints(net_result, opts, verbosity, dnet_out_dinput)
      dqlknn_out_dinput = dnet_out_dinput
    else
      call impose_output_constraints(net_result, opts, verbosity)
    endif
    if (verbosity >= 1 .and. my_world_rank == 0) then
       WRITE(*,'(A)') 'with rotation output clipped'
       do rho = 1, n_rho
          WRITE(fmt_tmp,'(A,I0,A)') '(', n_outputs, '(F7.2,X))'
          WRITE(*,fmt_tmp) (net_result(rho, ii), ii=1,n_outputs)
       end do
    end if

    qlknn_out = net_result
  end subroutine evaluate_fullflux_net

  subroutine evaluate_jetexp_net(input, nets, n_members, qlknn_out, qlknn_eb, verbosityin, optsin, dqlknn_out_dinput, qlknn_validity)
    real(qlknn_dp), dimension(:,:), intent(in) :: input
    real(qlknn_dp), dimension(:,:), allocatable :: input_clipped
    integer(lli), optional, intent(in) :: verbosityin
    type(net_collection), intent(in) :: nets
    integer(lli), intent(in) :: n_members
    type(qlknn_options), optional, intent(in) :: optsin

    real(qlknn_dp), dimension(:,:), intent(out) :: qlknn_out, qlknn_eb
    real(qlknn_dp), dimension(:,:,:), optional, intent(out) :: dqlknn_out_dinput
    !logical, dimension(:,:), optional, intent(out) :: qlknn_validity
    logical, dimension(:,:), optional, intent(out) :: qlknn_validity

    integer(lli) ii, rho, verbosity, outp
    integer(li) :: n_outputs, n_net_outputs
    integer(li) n_rho, n_in, n_post_committee_outputs
    real(qlknn_dp), dimension(:), allocatable :: res
    real(qlknn_dp), dimension(:,:), allocatable :: net_out, committee_out, committee_eb
    real(qlknn_dp), dimension(:,:,:), allocatable :: dnet_out_dinput, dcommittee_out_dinput
    logical, dimension(:,:), allocatable :: jacobian_clipmask
    !logical, dimension(:,:), allocatable :: committee_validity
    logical, dimension(:,:), allocatable :: committee_validity
    type(qlknn_options) :: opts
    logical, dimension(:), allocatable :: net_evaluate
    logical :: calcder
    character(len=100) :: fmt_tmp
#if (defined(LLI) && defined(__INTEL_COMPILER)) || defined(MEXING)
    integer(lli) :: my_world_rank
#else
    integer(li) :: my_world_rank
#endif
#ifdef MPI
#if (defined(LLI) && defined(__INTEL_COMPILER)) || defined(MEXING)
    integer(lli) :: mpi_ierr, world_size
#else
    integer(li) :: mpi_ierr, world_size
#endif
#endif
    integer(lli), dimension(13,3), parameter :: merge_map = reshape( (/ &
         1, 1, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, &
         2, 0, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, &
         3, 0, 0, 0, 0,  0,  0,  0,  0,  0,  0,  0,  0  &
         /), (/ 13, 3/))
         !  1 efe_GB
         !  2 efeETG_GB
         !  3 efi_GB
         !  4 pfe_GB
         !  5 pfi_GB
         !  6 vfi_GB
         !  7 dfe_GB
         !  8 vte_GB
         !  9 vce_GB
         ! 10 dfi_GB
         ! 11 vti_GB
         ! 12 vci_GB
         ! 13 vri_GB
    integer(lli), dimension(12,3), parameter :: leading_map = reshape( (/ &
         1, 0, 0, 0,  0,  0,  0,  0,  0,  0,  0,  0, & ! ETG
         3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, & ! TEM
         4, 2, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24  & ! ITG
         /), (/ 12,3 /))
    ! New variance thresholds (15D NN)
    ! Determined from quantiles of 10000 random samples: 90% abs, 50% rel
    real(qlknn_dp), dimension(25):: aeb_limits = (/ &
         8.4,  5.6,  9.0, & ! efe_GB
              13.0,  8.6, & ! efi_GB
               3.4,  3.6, & ! pfe_GB
               5.6,  5.0, & ! pfi_GB
               2.3,  2.3, & ! vfi_GB
               4.1,  3.2, & ! dfe_GB
               4.6,  2.0, & ! vte_GB
               1.6,  1.3, & ! vce_GB
               8.0,  9.5, & ! dfi_GB
               8.7,  9.0, & ! vti_GB
               3.0,  3.2, & ! vci_GB
               1.0,  1.0  & ! vri_GB
         /)
         ! 1 ETG
         ! 2 ITG
         ! 3 TEM
    real(qlknn_dp), dimension(25):: reb_limits = (/ &
         0.5,  1.0,  0.9, & ! efe_GB
               0.4,  1.4, & ! efi_GB
               2.5,  2.1, & ! pfe_GB
               3.2,  2.5, & ! pfi_GB
               1.9,  2.5, & ! vfi_GB
               2.5,  2.4, & ! dfe_GB
               2.4,  1.5, & ! vte_GB
               2.6,  1.2, & ! vce_GB
               3.0,  2.8, & ! dfi_GB
               2.0,  2.5, & ! vti_GB
               2.3,  2.6, & ! vci_GB
               0.1,  0.1  & ! vri_GB
         /)
         ! 1 ETG
         ! 2 ITG
         ! 3 TEM
!    ! Old variance threshold (14D NN)
!    ! Determined from quantiles of 10000 random samples: 90% abs, 50% rel
!    real(qlknn_dp), dimension(25):: aeb_limits = (/ &
!         8.0,  7.0, 11.5, & ! efe_GB
!              12.5, 11.5, & ! efi_GB
!               8.4,  6.9, & ! pfe_GB
!              11.6,  8.2, & ! pfi_GB
!               2.5,  5.5, & ! vfi_GB
!               6.4,  8.1, & ! dfe_GB
!               7.2,  6.2, & ! vte_GB
!               2.3,  3.7, & ! vce_GB
!              11.7, 14.5, & ! dfi_GB
!              12.2, 11.7, & ! vti_GB
!               4.2,  4.3, & ! vci_GB
!              20.0, 20.0  & ! vri_GB
!         /)
         ! 1 ETG
         ! 2 ITG
         ! 3 TEM
!    real(qlknn_dp), dimension(25):: reb_limits = (/ &
!         0.5,  1.6,  1.1, & ! efe_GB
!               0.5,  1.5, & ! efi_GB
!               2.7,  2.3, & ! pfe_GB
!               3.0,  2.2, & ! pfi_GB
!               1.1,  1.4, & ! vfi_GB
!               2.2,  2.0, & ! dfe_GB
!               2.2,  1.8, & ! vte_GB
!               2.9,  2.1, & ! vce_GB
!               2.3,  2.1, & ! dfi_GB
!               2.5,  2.0, & ! vti_GB
!               2.0,  2.0, & ! vci_GB
!              10.0, 10.0  & ! vri_GB
!         /)
         ! 1 ETG
         ! 2 ITG
         ! 3 TEM
    if(present(verbosityin)) then
       verbosity=verbosityin
    else
       verbosity = 0
    end if

#ifdef MPI
    call MPI_COMM_SIZE(MPI_COMM_WORLD, world_size, mpi_ierr)
    call MPI_COMM_RANK(MPI_COMM_WORLD, my_world_rank, mpi_ierr)
    if (my_world_rank == 0) then
       if (verbosity >= 2) write(*,*) 'World size in evaluate_jetexp_net is ', world_size
    end if
    if (verbosity >= 2) write(*,*) 'Hello world from evaluate_jetexp_net rank ', my_world_rank
#else
    my_world_rank = 0
#endif

    if(present(dqlknn_out_dinput)) then
      calcder = .true.
    else
      calcder = .false.
    end if

    n_rho = int(size(input, 2), li)
    n_in = int(size(input, 1), li)
    n_outputs = int(size(qlknn_out, 2), li)
    n_net_outputs = int(size(nets%nets), li)
    n_post_committee_outputs = n_net_outputs / int(n_members, li)
    allocate(net_out(n_rho, n_net_outputs))
    allocate(net_evaluate(n_net_outputs))
    net_evaluate = .true.

    allocate(res(n_rho)) !Debug

    ERRORSTOP(.not. all(shape(qlknn_out) == shape(qlknn_eb)), 'Errorbound array should be the same size as out array')
    if (present(qlknn_validity)) then
       ERRORSTOP(.not. all(shape(qlknn_out) == shape(qlknn_validity)), 'Validity array should be the same size as out array')
    end if

    if (.NOT. (n_rho == size(qlknn_out, 1))) then
       write(stderr,*) 'size(qlknn_out, 1)=', size(qlknn_out, 1),', nrho=', n_rho

       ERRORSTOP(.true., 'Rows of qlknn_out should be equal to number of radial points!')
    end if

    ! set options according to optsin if present from calling program. Otherwise set default
    if(present(optsin)) then
       opts=optsin
    else
       CALL default_qlknn_jetexp_options(opts)
    end if

    if (verbosity >= 1 .and. my_world_rank == 0) then
       call print_qlknn_options(opts)
       write(fmt_tmp, '(A,I0,A)') '(', n_in, '(F7.2,X))'
       write(*,*) 'input, n_rho=', n_rho
       do rho = 1, n_rho
          WRITE(*, fmt_tmp) (input(ii, rho), ii=1,n_in)
       end do
    end if

    ! Impose input constants
    allocate(input_clipped(n_in, n_rho))
    if (calcder) then
      call impose_input_constraints(input, input_clipped, opts, verbosity, jacobian_clipmask)
    else
      call impose_input_constraints(input, input_clipped, opts, verbosity)
    endif

    if (verbosity >= 2 .and. my_world_rank == 0) then
       write(*,*) 'input_clipped(:,1)'
       write(*,*) input_clipped(:,1)
    end if

    if (verbosity >= 2 .and. my_world_rank == 0) then
       write(*,*) 'Evaluate networks:'
       write(*,*) net_evaluate
    end if

    if (calcder) then
      allocate(dnet_out_dinput(n_net_outputs, n_rho, n_in))
      dnet_out_dinput = 0
    end if

    ! Evaluate all neural networks
    if (calcder) then
      call evaluate_multinet(input_clipped, nets, net_evaluate, net_out, verbosityin, dnet_out_dinput)
    else
      call evaluate_multinet(input_clipped, nets, net_evaluate, net_out, verbosityin)
    endif

    ! Zero out Jacobians of clipped inputs
    if (calcder) then
     do outp = 1, n_net_outputs
       where(transpose(jacobian_clipmask))
         dnet_out_dinput(outp, :, :) = 0
       endwhere
     enddo
    endif

    if (verbosity >= 3 .and. my_world_rank == 0) then
       WRITE(*,'(A)') 'After evaluation'
       do rho = 1, n_rho
          WRITE(fmt_tmp,'(A,I0,A)') '(', n_net_outputs, '(F7.2,X))'
          WRITE(*,fmt_tmp) (net_out(rho, ii), ii=1,n_net_outputs)
       end do
    end if

    ! Merge committee members together
    allocate(committee_out(n_rho, n_post_committee_outputs))
    allocate(committee_eb(n_rho, n_post_committee_outputs))
    if (calcder) then
      allocate(dcommittee_out_dinput(n_post_committee_outputs, n_rho, n_in))
      call merge_committee(net_out, n_members, committee_out, committee_eb, verbosity, dnet_out_dinput, dcommittee_out_dinput)
    else
      call merge_committee(net_out, n_members, committee_out, committee_eb, verbosity)
    endif

    if (verbosity >= 2 .and. my_world_rank == 0) then
       WRITE(*,'(A)') 'After committee merge'
       do rho = 1, n_rho
          WRITE(fmt_tmp,'(A,I0,A)') '(', n_post_committee_outputs, '(F7.2,X))'
          WRITE(*,fmt_tmp) (committee_out(rho, ii), ii=1,n_post_committee_outputs)
       end do
       WRITE(*,'(A)') 'With error bound'
       do rho = 1, n_rho
          WRITE(fmt_tmp,'(A,I0,A)') '(', n_post_committee_outputs, '(F7.2,X))'
          WRITE(*,fmt_tmp) (committee_eb(rho, ii), ii=1,n_post_committee_outputs)
       end do
    end if

    ! Clip leading fluxes to 0
    if (calcder) then
      call impose_leading_flux_constraints(leading_map, committee_out, verbosity, dnet_out_dinput, net_eb=committee_eb)
    else
      call impose_leading_flux_constraints(leading_map, committee_out, verbosity, net_eb=committee_eb)
    endif
    if (verbosity >= 3 .and. my_world_rank == 0) then
       write(*,*) 'net_result (pre-div-multiplication)'
       do rho = 1, n_rho
          write(fmt_tmp,'(a,i0,a)') '(', n_post_committee_outputs, '(f7.2,x))'
          write(*,fmt_tmp) (committee_out(rho, ii), ii=1,n_post_committee_outputs)
       end do
       write(*,'(a)') 'with error bound'
       do rho = 1, n_rho
          write(fmt_tmp,'(a,i0,a)') '(', n_post_committee_outputs, '(f7.2,x))'
          write(*,fmt_tmp) (committee_eb(rho, ii), ii=1,n_post_committee_outputs)
       end do
    end if

    if (calcder) then
      call multiply_div_networks(leading_map, committee_out, verbosity, dcommittee_out_dinput, net_eb=committee_eb)
    else
      call multiply_div_networks(leading_map, committee_out, verbosity, net_eb=committee_eb)
    endif

    if (verbosity >= 3 .and. my_world_rank == 0) then
       write(*,*) 'net_result (post-div-multiplication)'
       do rho = 1, n_rho
          write(fmt_tmp,'(a,i0,a)') '(', n_post_committee_outputs, '(f7.2,x))'
          write(*,fmt_tmp) (committee_out(rho, ii), ii=1,n_post_committee_outputs)
       end do
       write(*,'(a)') 'with error bound'
       do rho = 1, n_rho
          write(fmt_tmp,'(a,i0,a)') '(', n_post_committee_outputs, '(f7.2,x))'
          write(*,fmt_tmp) (committee_eb(rho, ii), ii=1,n_post_committee_outputs)
       end do
    end if

    allocate(committee_validity(n_rho, n_post_committee_outputs))
    call determine_validity_with_eb(aeb_limits, reb_limits, committee_out, committee_eb, committee_validity, verbosity)
    if (verbosity >= 3 .and. my_world_rank == 0) then
       write(*,'(a)') 'net_validity (post-div-multiplication)'
       do rho = 1, n_rho
          write(fmt_tmp,'(a,i0,a)') '(', n_post_committee_outputs, '(L2,x))'
          write(*,fmt_tmp) (committee_validity(rho, ii), ii=1,n_post_committee_outputs)
       end do
       write(*,'(a)') 'applied absolute validity limit'
       write(fmt_tmp,'(a,i0,a)') '(', n_post_committee_outputs, '(f7.2,x))'
       write(*,fmt_tmp) (aeb_limits(ii), ii=1,n_post_committee_outputs)
       write(*,'(a)') 'applied relative validity limit'
       write(fmt_tmp,'(a,i0,a)') '(', n_post_committee_outputs, '(f7.2,x))'
       write(*,fmt_tmp) (reb_limits(ii), ii=1,n_post_committee_outputs)
    end if

    ! Merge ETG/ITG/TEM modes together
    if (opts%merge_modes) then
      if (calcder) then
        call merge_modes(merge_map, committee_out, qlknn_out, verbosity, dcommittee_out_dinput, dqlknn_out_dinput, net_eb=committee_eb, merged_net_eb=qlknn_eb)
      else
        call merge_modes(merge_map, committee_out, qlknn_out, verbosity, net_eb=committee_eb, merged_net_eb=qlknn_eb)
      endif
      if (verbosity >= 1 .and. my_world_rank == 0) then
        write(*,*) 'With modes merged'
        write(fmt_tmp,'(a,i0,a)') '(', n_outputs, '(f7.2,x))'
        do rho = 1, n_rho
          write(*,fmt_tmp) (qlknn_out(rho, ii), ii=1,n_outputs)
        end do
        write(*,'(a)') 'And error bound'
        do rho = 1, n_rho
          write(*,fmt_tmp) (qlknn_eb(rho, ii), ii=1,n_outputs)
        end do
      end if

      call determine_validity_merged_modes(merge_map, committee_validity, qlknn_validity, verbosity)
      if (verbosity >= 1 .and. my_world_rank == 0) then
        write(*,'(a)') 'net_validity (modes merged)'
        do rho = 1, n_rho
          write(fmt_tmp,'(a,i0,a)') '(', n_outputs, '(L2,x))'
          write(*,fmt_tmp) (qlknn_validity(rho, ii), ii=1,n_outputs)
        end do
      end if
    else
       qlknn_out = committee_out
       qlknn_eb = committee_eb
       qlknn_validity = committee_validity
       if (calcder) then
         dqlknn_out_dinput = dcommittee_out_dinput
       endif
       if (verbosity >= 1 .and. my_world_rank == 0) then
          WRITE(*,*) 'without modes merged'
          WRITE(fmt_tmp,'(A,I0,A)') '(', n_post_committee_outputs, '(F7.2,X))'
          do rho = 1, n_rho
             WRITE(*,fmt_tmp) (qlknn_out(rho, ii), ii=1,n_post_committee_outputs)
          end do
          WRITE(*,'(A)') 'And error bound'
          do rho = 1, n_rho
             WRITE(fmt_tmp,'(A,I0,A)') '(', n_post_committee_outputs, '(F7.2,X))'
             WRITE(*,fmt_tmp) (qlknn_eb(rho, ii), ii=1,n_post_committee_outputs)
          end do
       end if
    end if

  end subroutine evaluate_jetexp_net

  subroutine hornnet_flux_from_constants(input, blocks, hornnet_constants, flux_out, verbosityin, optsin, qlknn_normsin, dflux_dhornnet_constants, dflux_dinput)
    !! Calculate the transport fluxes as predicted by the given HornNet
    !! weights and biases

    real(qlknn_dp), dimension(:,:), intent(in) :: input
    !! Global input to the NN. Same as [[evaluate_QLKNN_10D]]
    type(block_collection), intent(in) :: blocks
    !! Blocks of NN layers to evaluate.
    !! Usually loaded with [[load_hornnet_nets_from_disk]]
    real(qlknn_dp), dimension(:,:), intent(in) :: hornnet_constants
    !! C* constants from [[evaluate_hornnet_constants]]
    integer(lli), optional, intent(in) :: verbosityin
    type(qlknn_options), optional, intent(in) :: optsin
    !! Options to be used while evaluating the nets
    !! Usually initialized with [[default_qlknn_hornnet_options]]
    type(qlknn_normpars), optional, intent(in) :: qlknn_normsin
    !! Normalizations needed for the Victor rule, see [[scale_with_victor]]

    real(qlknn_dp), dimension(:,:), intent(out) :: flux_out
    !! Fluxes as calculated by HornNet. Columns when opts%merge_modes = .true.
    !!
    !! - \( q_e, q_{e, ETG}, q_i, \Gamma_e \)
    !!
    !! If opts%merge_modes = .false.
    !!
    !! - \( q_{e, ETG}, q_{e, ITG}, q_{e, TEM}, q_{i, ITG}, q_{i, TEM} \)
    !! - \( \Gamma_{e, ITG}, \Gamma_{e, TEM} \)
    real(qlknn_dp), dimension(:,:,:), optional, intent(out) :: dflux_dhornnet_constants
    !! Jacobians for flux_out vs C*
    real(qlknn_dp), dimension(:,:,:), optional, intent(out) :: dflux_dinput
    !! Jacobians for flux_out vs input

    type(qlknn_normpars) :: qlknn_norms
    type(qlknn_options)  :: opts

    integer(lli), dimension(4,3), parameter :: merge_map = reshape( (/ &
         1, 1, 4, 6, &
         2, 0, 5, 7, &
         3, 0, 0, 0 &
         /), (/ 4, 3 /))
    ! efe_GB 1
    ! efeETG_gb 2
    ! efi_GB 3
    ! pfe_GB 4

    !integer(lli), dimension(15), parameter :: late_fuse_var_map = &
    !     (/ 3, 2, 3, 3, 2, 3, 2, 3, 3, 2, 3, 2, 3, 2, 3 /)

    integer(lli), dimension(3,3) :: output_mode_map
    integer(lli), dimension(:), allocatable :: output_mode_local
    !integer(lli) :: ii, rho, verbosity, outp
    integer(lli) :: ii, rho, verbosity, n_rho, outp, n_sep_out, inp, pow_idx, block_idx, slope_idx
    !integer(li) :: n_rho, n_outputs, n_total_inputs, n_common_out, n_hidden_in, n_hidden_out, n_output_out
    integer(li) :: n_outputs, n_total_inputs
    logical :: calcder

    real(qlknn_dp), dimension(:,:), allocatable :: special_input
    real(qlknn_dp), dimension(:,:), allocatable :: difference
    real(qlknn_dp), dimension(:,:), allocatable :: heaviside_function_times
    real(qlknn_dp), dimension(:,:), allocatable :: clip_by_value
    real(qlknn_dp), dimension(:,:), allocatable :: input_clipped
    real(qlknn_dp), dimension(:,:), allocatable :: sepflux_out
    real(qlknn_dp), dimension(:,:), allocatable :: sepflux_out_descaled
    logical, dimension(:,:), allocatable :: jacobian_clipmask

    real(qlknn_dp), dimension(:,:,:), allocatable :: dsepflux_dinput
    real(qlknn_dp), dimension(:,:,:), allocatable :: dsepflux_dhornnet_constants

    real(qlknn_dp), dimension(:,:,:), allocatable :: dclip_by_value_dinput
    real(qlknn_dp), dimension(:,:,:), allocatable :: drelu_dinput

    real(qlknn_dp), dimension(:,:,:), allocatable :: dclip_by_value_dhornnet_constants
    real(qlknn_dp), dimension(:,:,:), allocatable :: drelu_dhornnet_constants

    real(qlknn_dp), dimension(:,:), allocatable :: f, g, h
    real(qlknn_dp), dimension(:,:,:), allocatable :: df_dhornnet_constants, dg_dhornnet_constants, dh_dhornnet_constants
    real(qlknn_dp), dimension(:,:,:), allocatable :: df_dinput, dg_dinput


    output_mode_map = reshape( (/ &
         1, 0, 0, & ! ETG
         2, 4, 6, & ! ITG
         3, 5, 7  & ! TEM
         /), (/ 3, 3 /))


    if(present(verbosityin)) then
       verbosity = verbosityin
    else
       verbosity = 0
    end if

    if(present(dflux_dhornnet_constants)) then
      calcder = .true.
    else
      calcder = .false.
    end if

    if (calcder .and. .not. present(dflux_dinput)) then
      ERRORSTOP(.true., 'Also give dflux_dinput if dflux_dhornnet_constants is given')
    endif

    if (calcder) then
      dflux_dhornnet_constants = 0
      dflux_dinput = 0
    endif

    n_total_inputs = int(size(input, 1), li)
    n_rho = int(size(input, 2), lli)
    n_outputs = int(size(flux_out, 2), li)
    n_sep_out = 7

    if (verbosity >= 1) then
      write(*, '(A,I2,A,I3,A,I3,A,I3,A,I3)') 'Calculating c* constants from input with n_hornet_constants=', 15, ', n_total_inputs=', n_total_inputs, ', n_outputs=', n_outputs, ', n_rho=', n_rho, ', n_sep_out=', n_sep_out
    endif
    ! set options according to optsin if present from calling program. Otherwise set default
    if(present(optsin)) then
       opts=optsin
    else
       CALL default_qlknn_hornnet_options(opts)
    end if

    ! Check sizes
    if (.NOT. (n_rho == size(flux_out, 1))) then
       write(stderr,*) 'size(flux_out, 1)=', size(flux_out, 1), ', nrho=', n_rho

       ERRORSTOP(.true., 'Rows of flux_out should be equal to number of radial points!')
    endif
    if (opts%merge_modes .and. 4 /= n_outputs) then
       write(stderr,*) 'size(flux_out, 2)=', size(flux_out, 2)
       ERRORSTOP(.true., 'Columns of flux_out should be 4!')
    endif
    if (.not. opts%merge_modes .and. n_sep_out /= n_outputs) then
       write(stderr,*) 'size(flux_out, 2)=', size(flux_out, 2), ', n_sep_out=', n_sep_out
       ERRORSTOP(.true., 'Columns of flux_out should be n_sep_out!')
    endif

    if (calcder) then
      if (n_outputs /= size(dflux_dhornnet_constants, 1)) then
        write(stderr,*) 'size(dflux_dhornnet_constants, 1)=', size(dflux_dhornnet_constants, 1)
        ERRORSTOP(.true., 'Rows of dflux_dhornnet_constants should be equal to n_outputs!')
      endif
      if (n_rho /= size(dflux_dhornnet_constants, 2)) then
        write(stderr,*) 'size(dflux_dhornnet_constants, 2)=', size(dflux_dhornnet_constants, 2), ', nrho=', n_rho
        ERRORSTOP(.true., 'Columns of dflux_dhornnet_constants should be equal to number of radial points!')
      endif
      if (15 /= size(dflux_dhornnet_constants, 3)) then
        write(stderr,*) 'size(dflux_dhornnet_constants, 3)=', size(dflux_dhornnet_constants, 3)
        ERRORSTOP(.true., 'Pages of dflux_dhornnet_constants should be equal to 15!')
      endif
    endif

    if (opts%apply_victor_rule .AND. .NOT. present(qlknn_normsin)) then
       ERRORSTOP(.true., 'Need to pass qlknn_normsin when applying Victor rule')
    else if (present(qlknn_normsin)) then
       qlknn_norms = qlknn_normsin
    end if
    ERRORSTOP(opts%apply_victor_rule, 'Victor rule not implemented yet')

    ! Impose input constants
    if (calcder) then
      call impose_input_constraints(input, input_clipped, opts, verbosity, jacobian_clipmask)
    else
      call impose_input_constraints(input, input_clipped, opts, verbosity)
    endif

    if (verbosity >= 3) then
      write(*,*) 'input_clipped:'
      do rho = 1, n_rho
        write(*,'(11(f7.4, 1x))') input_clipped(:, rho)
      enddo
    endif
    allocate(special_input(3, n_rho))
    ! Assuming all blocks have the same scaling/dataset
    special_input(1, :) =  blocks%input_blocks(1)%feature_prescale_factor(3) * input_clipped(3, :) + &
       blocks%input_blocks(1)%feature_prescale_bias(3) ! ETG needs Ate
    special_input(2, :) =  blocks%input_blocks(1)%feature_prescale_factor(2) * input_clipped(2, :) + &
       blocks%input_blocks(1)%feature_prescale_bias(2) ! ITG needs Ati
    special_input(3, :) =  blocks%input_blocks(1)%feature_prescale_factor(3) * input_clipped(3, :) + &
       blocks%input_blocks(1)%feature_prescale_bias(3) ! TEM needs Ate
    if (verbosity >= 3) then
      write(*,*) 'special_input:'
      do rho = 1, n_rho
        write(*,'(3(f7.4, 1x))') special_input(:, rho)
      enddo
    endif

    ! Sepflux out
    ! c1 == threshold
    ! c2 == power bending
    ! c3 == linear bending
    ! efeetg_gb 1
    ! efeitg_gb 2
    ! efetem_gb 3
    ! efiitg_gb 4
    ! efitem_gb 5
    ! pfeitg_gb 6
    ! pfetem_gb 7

    allocate(sepflux_out(n_rho, 7))
    allocate(difference(n_rho, 3))
    allocate(clip_by_value(n_rho, 3))
    allocate(heaviside_function_times(n_rho, 3))
    if (calcder) then
      allocate(dclip_by_value_dhornnet_constants(n_sep_out, n_rho, 15))
      allocate(drelu_dhornnet_constants(n_sep_out, n_rho, 15))
      allocate(dclip_by_value_dinput(3, n_rho, n_total_inputs))
      allocate(drelu_dinput(3, n_rho, n_total_inputs))
      dclip_by_value_dhornnet_constants = 0.
      drelu_dhornnet_constants = 0.
      dclip_by_value_dinput = 0.
      drelu_dinput = 0.
      dclip_by_value_dinput(1, :, 3) = blocks%input_blocks(1)%feature_prescale_factor(3)
      dclip_by_value_dinput(2, :, 2) = blocks%input_blocks(1)%feature_prescale_factor(2)
      dclip_by_value_dinput(3, :, 3) = blocks%input_blocks(1)%feature_prescale_factor(3)
      drelu_dinput(1, :, 3) = blocks%input_blocks(1)%feature_prescale_factor(3)
      drelu_dinput(2, :, 2) = blocks%input_blocks(1)%feature_prescale_factor(2)
      drelu_dinput(3, :, 3) = blocks%input_blocks(1)%feature_prescale_factor(3)
    endif
    do ii = 1, 3
      difference(:, ii) = special_input(ii, :) - hornnet_constants(:, ii)
      ! TODO: Not implemented in tf_op_layer_clip_by_values final values are the tf_op_layer_clip_by_valye/Mimumum and tf_op_layer_clip_by_value layers. Ask Philipp what they do
      clip_by_value(:, ii) = abs(difference(:, ii))
      call relu(n_rho, difference(:, ii), heaviside_function_times(:, ii))
      if (calcder) then
        if (ii == 1) then
          dclip_by_value_dhornnet_constants((/ 1 /), :, ii) = -1 !ddifference_dhornet_constants
        elseif (ii == 2) then
          dclip_by_value_dhornnet_constants((/ 2, 4, 6 /), :, ii) = -1 !ddifference_dhornet_constants
        elseif (ii == 3) then
          dclip_by_value_dhornnet_constants((/ 3, 5, 7 /), :, ii) = -1 !ddifference_dhornet_constants
        endif
        ! dclip_by_value_dhornet_constants. Does not exist at x != 0, put zero  in the 'bigger than 0' camp
        do outp = 1, n_sep_out
          where (difference(:, ii) < 0.)
            dclip_by_value_dhornnet_constants(outp, :, ii) = -1 * dclip_by_value_dhornnet_constants(outp, :, ii)
            dclip_by_value_dinput(ii, :, 2) = -1 * dclip_by_value_dinput(ii, :, 2)
            dclip_by_value_dinput(ii, :, 3) = -1 * dclip_by_value_dinput(ii, :, 3)
          endwhere
          where (difference(:, ii) >= 0.)
            dclip_by_value_dhornnet_constants(outp, :, ii) = 1 * dclip_by_value_dhornnet_constants(outp, :, ii)
            dclip_by_value_dinput(ii, :, 2) = 1 * dclip_by_value_dinput(ii, :, 2)
            dclip_by_value_dinput(ii, :, 3) = 1 * dclip_by_value_dinput(ii, :, 3)
          endwhere
        enddo
        ! drelu_dhornnet_constants
        if (ii == 1) then
          drelu_dhornnet_constants((/ 1 /), :, ii) = -1 !ddifference_dhornet_constants
        elseif (ii == 2) then
          drelu_dhornnet_constants((/ 2, 4, 6 /), :, ii) = -1 !ddifference_dhornet_constants
        elseif (ii == 3) then
          drelu_dhornnet_constants((/ 3, 5, 7 /), :, ii) = -1 !ddifference_dhornet_constants
        endif
        ! dclip_by_value_dhornet_constants. Does not exist at x != 0, let's take 0 to be sure
        do outp = 1, n_sep_out
          where (difference(:, ii) < 0.)
            drelu_dhornnet_constants(outp, :, ii) = 0
            drelu_dinput(ii, :, 2) = 0
            drelu_dinput(ii, :, 3) = 0
          endwhere
          where (difference(:, ii) >= 0.)
            drelu_dhornnet_constants(outp, :, ii) = 1 * drelu_dhornnet_constants(outp, :, ii)
            drelu_dinput(ii, :, 2) = 1 * drelu_dinput(ii, :, 2)
            drelu_dinput(ii, :, 3) = 1 * drelu_dinput(ii, :, 3)
          endwhere
        enddo
      endif
    enddo

    ! Initialize temp variables
    allocate(f(n_rho, n_sep_out))
    allocate(g(n_rho, n_sep_out))
    allocate(h(n_rho, n_sep_out))
    if (calcder) then
      allocate(dsepflux_dhornnet_constants(n_sep_out, n_rho, 15))
      allocate(dsepflux_dinput(n_sep_out, n_rho, n_total_inputs))
      allocate(df_dhornnet_constants(n_sep_out, n_rho, 15))
      allocate(dg_dhornnet_constants(n_sep_out, n_rho, 15))
      allocate(dh_dhornnet_constants(n_sep_out, n_rho, 15))
      allocate(df_dinput(n_sep_out, n_rho, n_total_inputs))
      allocate(dg_dinput(n_sep_out, n_rho, n_total_inputs))
      dsepflux_dhornnet_constants = 0.
      df_dhornnet_constants = 0.
      dg_dhornnet_constants = 0.
      dh_dhornnet_constants = 0.
      df_dinput = 0.
      dg_dinput = 0.
    endif

    ! ETG network
    outp = 1 ! efeetg_gb
    pow_idx = 4
    block_idx = 1
    slope_idx = 9
    if (calcder) then
      call hornnet_multiplier(heaviside_function_times, clip_by_value, hornnet_constants, sepflux_out, outp, pow_idx, block_idx, slope_idx, f, g, h, drelu_dhornnet_constants, drelu_dinput, &
         dclip_by_value_dhornnet_constants, dclip_by_value_dinput, df_dhornnet_constants, df_dinput, dg_dhornnet_constants, dg_dinput, dh_dhornnet_constants)
    else
      call hornnet_multiplier(heaviside_function_times, clip_by_value, hornnet_constants, sepflux_out, outp, pow_idx, block_idx, slope_idx, f, g, h)
    endif


    ! ITG network
    outp = 2 ! efeitg_gb
    pow_idx = 5
    block_idx = 2
    slope_idx = 10
    if (calcder) then
      call hornnet_multiplier(heaviside_function_times, clip_by_value, hornnet_constants, sepflux_out, outp, pow_idx, block_idx, slope_idx, f, g, h, drelu_dhornnet_constants, drelu_dinput, &
         dclip_by_value_dhornnet_constants, dclip_by_value_dinput, df_dhornnet_constants, df_dinput, dg_dhornnet_constants, dg_dinput, dh_dhornnet_constants)
    else
      call hornnet_multiplier(heaviside_function_times, clip_by_value, hornnet_constants, sepflux_out, outp, pow_idx, block_idx, slope_idx, f, g, h)
    endif

    outp = 4 ! efiitg_gb
    pow_idx = 7
    block_idx = 2
    slope_idx = 12
    if (calcder) then
      call hornnet_multiplier(heaviside_function_times, clip_by_value, hornnet_constants, sepflux_out, outp, pow_idx, block_idx, slope_idx, f, g, h, drelu_dhornnet_constants, drelu_dinput, &
         dclip_by_value_dhornnet_constants, dclip_by_value_dinput, df_dhornnet_constants, df_dinput, dg_dhornnet_constants, dg_dinput, dh_dhornnet_constants)
    else
      call hornnet_multiplier(heaviside_function_times, clip_by_value, hornnet_constants, sepflux_out, outp, pow_idx, block_idx, slope_idx, f, g, h)
    endif

    outp = 6 ! pfeitg_gb
    block_idx = 2
    slope_idx = 14 ! Misuse slope_idx, it's actually a full net, not a slope
    f(:, outp) = heaviside_function_times(:, block_idx)
    g(:, outp) = 0.
    h(:, outp) = hornnet_constants(:, slope_idx)
    if (calcder) then
      df_dhornnet_constants(outp, :, :) = drelu_dhornnet_constants(outp, :, :)
      df_dinput(outp, :, :) = drelu_dinput(block_idx, : , :)
      dh_dhornnet_constants(outp, :, slope_idx) = 1.
    endif
    sepflux_out(:, outp) = f(:, outp) * h(:, outp)


    ! TEM network
    outp = 3 ! efetem_gb
    pow_idx = 6
    block_idx = 3
    slope_idx = 11
    if (calcder) then
      call hornnet_multiplier(heaviside_function_times, clip_by_value, hornnet_constants, sepflux_out, outp, pow_idx, block_idx, slope_idx, f, g, h, drelu_dhornnet_constants, drelu_dinput, &
         dclip_by_value_dhornnet_constants, dclip_by_value_dinput, df_dhornnet_constants, df_dinput, dg_dhornnet_constants, dg_dinput, dh_dhornnet_constants)
    else
      call hornnet_multiplier(heaviside_function_times, clip_by_value, hornnet_constants, sepflux_out, outp, pow_idx, block_idx, slope_idx, f, g, h)
    endif

    outp = 5 ! efetem_gb
    pow_idx = 8
    block_idx = 3
    slope_idx = 13
    if (calcder) then
      call hornnet_multiplier(heaviside_function_times, clip_by_value, hornnet_constants, sepflux_out, outp, pow_idx, block_idx, slope_idx, f, g, h, drelu_dhornnet_constants, drelu_dinput, &
         dclip_by_value_dhornnet_constants, dclip_by_value_dinput, df_dhornnet_constants, df_dinput, dg_dhornnet_constants, dg_dinput, dh_dhornnet_constants)
    else
      call hornnet_multiplier(heaviside_function_times, clip_by_value, hornnet_constants, sepflux_out, outp, pow_idx, block_idx, slope_idx, f, g, h)
    endif

    outp = 7 ! pfetem_gb
    block_idx = 3
    slope_idx = 15 ! Misuse slope_idx, it's actually a full net, not a slope
    f(:, outp) = heaviside_function_times(:, block_idx)
    g(:, outp) = 0.
    h(:, outp) = hornnet_constants(:, slope_idx)
    if (calcder) then
      df_dhornnet_constants(outp, :, :) = drelu_dhornnet_constants(outp, :, :)
      df_dinput(outp, :, :) = drelu_dinput(block_idx, : , :)
      dh_dhornnet_constants(outp, :, slope_idx) = 1.
    endif
    sepflux_out(:, outp) = f(:, outp) * h(:, outp)

    if (calcder) then
      do outp = 1, n_sep_out - 2
        do inp = 1, 15
          ! Only f
          !dsepflux_dhornnet_constants(outp, :, inp) = df_dhornnet_constants(outp, :, inp)
          ! Only h
          !dsepflux_dhornnet_constants(outp, :, inp) = dh_dhornnet_constants(outp, :, inp)
          ! f * g
          !dsepflux_dhornnet_constants(outp, :, inp) = df_dhornnet_constants(outp, :, inp) * g(:, outp) + &
          !     f(:, outp) * dg_dhornnet_constants(outp, :, inp)
          ! f * h
          !dsepflux_dhornnet_constants(outp, :, inp) = df_dhornnet_constants(outp, :, inp) * h(:, outp) + &
          !     f(:, outp) * dh_dhornnet_constants(outp, :, inp)
          ! f * g * h
          dsepflux_dhornnet_constants(outp, :, inp) = df_dhornnet_constants(outp, :, inp) * g(:, outp) * h(:, outp) + &
               f(:, outp) * dg_dhornnet_constants(outp, :, inp) * h(:, outp) + &
               f(:, outp) * g(:, outp) * dh_dhornnet_constants(outp, :, inp)
        enddo
        do inp = 1, n_total_inputs
          ! Only f
          !dsepflux_dinput(outp, :, inp) = df_dinput(outp, :, inp)
          ! f * g
          !dsepflux_dinput(outp, :, inp) = df_dinput(outp, :, inp) * g(:, outp) + &
          !     f(:, outp) * dg_dinput(outp, :, inp)
          ! f * h
          !dsepflux_dinput(outp, :, inp) = df_dinput(outp, :, inp) * h(:, outp) ! + 0
          ! f * g * h
          dsepflux_dinput(outp, :, inp) = df_dinput(outp, :, inp) * g(:, outp) * h(:, outp) + &
               f(:, outp) * dg_dinput(outp, :, inp) * h(:, outp) ! + 0
        enddo
      enddo
      ! pfe* are special, we only have f and h
      do outp = n_sep_out - 1, n_sep_out
        do inp = 1, 15
          ! Only f
          !dsepflux_dhornnet_constants(outp, :, inp) = df_dhornnet_constants(outp, :, inp)
          ! Only h
          !dsepflux_dhornnet_constants(outp, :, inp) = dh_dhornnet_constants(outp, :, inp)
          ! f * h
          dsepflux_dhornnet_constants(outp, :, inp) = df_dhornnet_constants(outp, :, inp) * h(:, outp) + &
               f(:, outp) * dh_dhornnet_constants(outp, :, inp)
        enddo
        do inp = 1, n_total_inputs
          ! Only f
          !dsepflux_dinput(outp, :, inp) = df_dinput(outp, :, inp)
          ! f * h
          dsepflux_dinput(outp, :, inp) = df_dinput(outp, :, inp) * h(:, outp) ! + 0
        enddo
      enddo
    endif


    if (verbosity >= 3) then
      write(*,*) 'sepflux_out:'
      do rho = 1, n_rho
        write(*,'(7(f7.3, 1x))') sepflux_out(rho, :)
      enddo
    endif

    if (verbosity >= 3) then
      write(*,*) 'sepflux_out ITG:'
      do rho = 1, n_rho
        write(*,'(7(f7.3, 1x))') sepflux_out(rho, (/ 2, 4, 6 /))
      enddo
    endif

    !------------------------
    ! Denormalize output
    allocate(sepflux_out_descaled(n_rho, 7))
    do ii = 1, 3
      allocate(output_mode_local(count(output_mode_map(:, ii)/=0)))
      output_mode_local = pack(output_mode_map(:, ii), output_mode_map(:, ii) /=0)
      do rho = 1, n_rho
        sepflux_out_descaled(rho, output_mode_local) = 1/blocks%input_blocks(ii)%target_prescale_factor * &
             (sepflux_out(rho, output_mode_local) - blocks%input_blocks(ii)%target_prescale_bias)
        if (calcder) then
          do inp = 1, 15
            dsepflux_dhornnet_constants(output_mode_local, rho, inp) = dsepflux_dhornnet_constants(output_mode_local, rho, inp) / blocks%input_blocks(ii)%target_prescale_factor
          enddo
          do inp = 1, n_total_inputs
            dsepflux_dinput(output_mode_local, rho, inp) = dsepflux_dinput(output_mode_local, rho, inp) / blocks%input_blocks(ii)%target_prescale_factor
          enddo
        endif
      end do
      deallocate(output_mode_local)
    enddo
    if (verbosity >= 2) then
      write(*,*) 'sepflux_out_descaled:'
      do rho = 1, n_rho
        write(*,'(7(f7.3, 1x))') sepflux_out_descaled(rho, :)
      enddo
    endif

    if (calcder) then
    else
      call impose_output_constraints(sepflux_out_descaled, opts, verbosity)
    endif
    if (verbosity >= 2) then
       write(*,*) 'with output clipped'
       do rho = 1, n_rho
        write(*,'(7(f7.3, 1x))') sepflux_out_descaled(rho, :)
       end do
    end if

    ! Merge ETG/ITG/TEM modes together
    if (opts%merge_modes) then
       if (calcder) then
         call merge_modes(merge_map, sepflux_out_descaled, flux_out, verbosity, dsepflux_dhornnet_constants, dflux_dhornnet_constants)
         call merge_modes(merge_map, sepflux_out_descaled, flux_out, verbosity, dsepflux_dinput, dflux_dinput)
       else
         call merge_modes(merge_map, sepflux_out_descaled, flux_out, verbosity)
       endif
       if (verbosity >= 1) then
          write(*,*) 'with modes merged'
          do rho = 1, n_rho
            write(*,'(4(f7.3, 1x))') flux_out(rho, :)
          end do
       end if
    else
       flux_out = sepflux_out_descaled
       if (calcder) then
         dflux_dhornnet_constants = dsepflux_dhornnet_constants
         dflux_dinput = dsepflux_dinput
       endif
       if (verbosity >= 1) then
          write(*,*) 'with modes non-merged'
          do rho = 1, n_rho
            write(*,'(7(f7.3, 1x))') flux_out(rho, :)
          end do
       end if
    end if
  end subroutine hornnet_flux_from_constants

  subroutine hornnet_multiply_jacobians(dhornnet_constants_dinput, dflux_dhornnet_constants, dflux_dinput, dqlknn_out_dinput, verbosityin)
    !! Multiply the Jacobians as calculated by [[hornnet_flux_from_constants]] and [[evaluate_hornnet_constants]]
    real(qlknn_dp), dimension(:,:,:), intent(in) :: dhornnet_constants_dinput
    real(qlknn_dp), dimension(:,:,:), intent(in) :: dflux_dhornnet_constants
    real(qlknn_dp), dimension(:,:,:), intent(in) :: dflux_dinput
    integer(lli), intent(in), optional :: verbosityin
    real(qlknn_dp), dimension(:,:,:), intent(out) :: dqlknn_out_dinput

    integer(lli) :: ii, verbosity, n_rho, outp, inp, n_hornet_constants, n_in, n_out
    logical, dimension(:), allocatable :: is_nonzero
    character(len=200) :: error_msg

    if(present(verbosityin)) then
       verbosity=verbosityin
    else
       verbosity = 0
    end if

    ! Check all shapes
    n_hornet_constants = size(dhornnet_constants_dinput, 1)
    n_out = size(dflux_dinput, 1)
    n_rho = size(dflux_dinput, 2)
    n_in = size(dflux_dinput, 3)

    if (verbosity >= 1) then
      write(*, '(A,I2,A,I3,A,I3,A,I3)') 'Multiplying HornNet Jacobians with n_hornet_constants=', n_hornet_constants, ', n_in=', n_in, ', n_out=', n_out, ', n_rho=', n_rho
    endif

    ERRORSTOP(size(dqlknn_out_dinput, 1) /= n_out, 'Passed dqlknn_out_dinput has wrong amount of rows')
    ERRORSTOP(size(dqlknn_out_dinput, 2) /= n_rho, 'Passed dqlknn_out_dinput has wrong amount of columns')
    ERRORSTOP(size(dqlknn_out_dinput, 3) /= n_in, 'Passed dqlknn_out_dinput has wrong amount of pages')

    ERRORSTOP(size(dflux_dhornnet_constants, 1) /= n_out, 'Passed dflux_dhornnet_constants has wrong amount of rows')

    ERRORSTOP(size(dhornnet_constants_dinput, 2) /= n_rho, 'Passed dhornnet_constants_dinput has wrong amount of columns')
    ERRORSTOP(size(dflux_dhornnet_constants, 2) /= n_rho, 'Passed dflux_dhornnet_constants has wrong amount of columns')

    ERRORSTOP(size(dflux_dhornnet_constants, 3) /= n_hornet_constants, 'Passed dflux_dhornnet_constants has wrong amount of pages')
    ERRORSTOP(size(dhornnet_constants_dinput, 3) /= n_in, 'Passed dhornnet_constants_dinput has wrong amount of pages')

    dqlknn_out_dinput = 0.
    do inp = 1, n_in
      do outp = 1, n_out
        do ii = 1, n_hornet_constants
          dqlknn_out_dinput(outp, :, inp) = dqlknn_out_dinput(outp, :, inp) +  dflux_dhornnet_constants(outp, :, ii) * dhornnet_constants_dinput(ii, :, inp)
        enddo
      enddo
    enddo

    allocate(is_nonzero(n_rho))
    if (n_out > 4) then
      ! Not merging modes
      call is_not_close(dqlknn_out_dinput(1, :, 3), 0._qlknn_dp, is_nonzero)
      write(error_msg, *) 'output 1 (ETG) depends directly on special variable!'
      ERRORSTOP(any(is_nonzero), error_msg)
      dqlknn_out_dinput(1, :, 3) = dflux_dinput(1, :, 3)
      do outp = 2, 4, 2
        call is_not_close(dqlknn_out_dinput(outp, :, 2), 0._qlknn_dp, is_nonzero)
        ERRORSTOP(any(is_nonzero), 'output 2 or 4 (ITG) depends directly on special variable!')
        dqlknn_out_dinput(outp, :, 2) = dflux_dinput(outp, :, 2)
      enddo

      do outp =  3, 5, 2
        call is_not_close(dqlknn_out_dinput(outp, :, 3),  0._qlknn_dp, is_nonzero)
        ERRORSTOP(any(is_nonzero), 'output 3 or 5 (TEM) depends directly on special variable!')
        dqlknn_out_dinput(outp, :, 3) = dflux_dinput(outp, :, 3)
      enddo
    else
      call is_not_close(dqlknn_out_dinput(2, :, 3),  0._qlknn_dp, is_nonzero)
      write(error_msg, *) 'output 2 (ETG) depends directly on special variable!'
      ERRORSTOP(any(is_nonzero), error_msg)
      dqlknn_out_dinput(2, :, 3) = dqlknn_out_dinput(2, :, 3) + dflux_dinput(2, :, 3)
    endif
  end subroutine hornnet_multiply_jacobians

  subroutine hornnet_multiplier(heaviside_function_times, clip_by_value, hornnet_constants, sepflux_out, outp, pow_idx, block_idx, slope_idx, f, g, h, drelu_dhornnet_constants, drelu_dinput, &
         dclip_by_value_dhornnet_constants, dclip_by_value_dinput, df_dhornnet_constants, df_dinput, dg_dhornnet_constants, dg_dinput, dh_dhornnet_constants)
    real(qlknn_dp), dimension(:,:), intent(in) :: heaviside_function_times
    real(qlknn_dp), dimension(:,:), intent(in) :: clip_by_value
    real(qlknn_dp), dimension(:,:), intent(in) :: hornnet_constants
    real(qlknn_dp), dimension(:,:,:), intent(in), optional :: drelu_dhornnet_constants
    real(qlknn_dp), dimension(:,:,:), intent(in), optional :: drelu_dinput
    real(qlknn_dp), dimension(:,:,:), intent(in), optional :: dclip_by_value_dhornnet_constants
    real(qlknn_dp), dimension(:,:,:), intent(in), optional :: dclip_by_value_dinput
    integer(lli), intent(in) :: outp, pow_idx, block_idx, slope_idx
    real(qlknn_dp), dimension(:,:), intent(inout) :: f, g, h

    real(qlknn_dp), dimension(:,:), intent(inout) :: sepflux_out
    real(qlknn_dp), dimension(:,:,:), intent(inout), optional :: df_dhornnet_constants, dg_dhornnet_constants, dh_dhornnet_constants
    real(qlknn_dp), dimension(:,:,:), intent(inout), optional :: df_dinput, dg_dinput

    integer(lli) ::n_rho, n_sep_out
    logical :: calcder

    if(present(drelu_dhornnet_constants)) then
      calcder = .true.
    else
      calcder = .false.
    end if

    n_rho = int(size(sepflux_out, 1), li)
    n_sep_out = int(size(sepflux_out, 2), li)
    f(:, outp) = heaviside_function_times(:, block_idx)
    g(:, outp) = clip_by_value(:, block_idx)**max(hornnet_constants(:, pow_idx), 0._qlknn_dp)
    h(:, outp) = hornnet_constants(:, slope_idx)
    sepflux_out(:, outp) = f(:, outp) * g(:, outp) * h(:, outp)

    if (calcder) then
      df_dhornnet_constants(outp, :, :) = drelu_dhornnet_constants(outp, :, :)
      df_dinput(outp, :, :) = drelu_dinput(block_idx, : , :)

      where(hornnet_constants(:, pow_idx) > 0)
        ! g(u, z) = u(x,z) ^ z -> dg/dx = du/dx(x) * z * u(x, z) ^ (z - 1)
        dg_dhornnet_constants(outp, :, block_idx) = dclip_by_value_dhornnet_constants(outp, :, block_idx) * &
             hornnet_constants(:, pow_idx) * clip_by_value(:, block_idx) ** (hornnet_constants(:, pow_idx) - 1)
        dg_dinput(outp, :, 2) = dclip_by_value_dinput(block_idx, :, 2) * &
             hornnet_constants(:, pow_idx) * clip_by_value(:, block_idx) ** (hornnet_constants(:, pow_idx) - 1)
        dg_dinput(outp, :, 3) = dclip_by_value_dinput(block_idx, :, 3) * &
             hornnet_constants(:, pow_idx) * clip_by_value(:, block_idx) ** (hornnet_constants(:, pow_idx) - 1)

        ! g(u, z) = u(x,z) ^ z -> dg/dz = u(x, z) ^ (z) * [log(u(x, z)) + z * du/dz(x,z) / u(x,z)]
        dg_dhornnet_constants(outp, :, pow_idx) = clip_by_value(:, block_idx)**max(hornnet_constants(:, pow_idx), 0._qlknn_dp) * &
             (log(clip_by_value(:, block_idx)) + max(hornnet_constants(:, pow_idx), 0._qlknn_dp) * dclip_by_value_dhornnet_constants(block_idx, :, pow_idx) / clip_by_value(:, block_idx))
      endwhere

      dh_dhornnet_constants(outp, :, slope_idx) = 1.
    endif
  end subroutine hornnet_multiplier


  subroutine evaluate_hornnet_constants(input, blocks, qlknn_out, verbosityin, optsin, qlknn_normsin, dqlknn_out_dinput)
    !! Calculate the C* constants for HornNet
    real(qlknn_dp), dimension(:,:), intent(in) :: input
    !! Global input to the NN. Same as [[evaluate_QLKNN_10D]]
    real(qlknn_dp), dimension(:,:), allocatable :: input_clipped
    integer(lli), optional, intent(in) :: verbosityin
    type(block_collection), intent(in) :: blocks
    !! Blocks of NN layers to evaluate.
    !! Usually loaded with [[load_hornnet_nets_from_disk]]
    type(qlknn_options), optional, intent(in) :: optsin
    !! Options to be used while evaluating the nets
    !! Usually initialized with [[default_qlknn_hornnet_options]]
    type(qlknn_normpars), optional, intent(in) :: qlknn_normsin
    !! Normalizations needed for the Victor rule, see [[scale_with_victor]]

    real(qlknn_dp), dimension(:,:), intent(out) :: qlknn_out
    !! Output of the C* constants. Columns are (in order):
    !!
    !! - 1-3: \( c_{1, ETG}, c_{1, ITG}, c_{1, TEM} \)
    !! - 4-8: \( c_{2, q_{e,ETG}} c_{2, q_{e,ITG}}, c_{2,q_{e, TEM}}, c_{2, q_{i,ITG}}, c_{2, q_{i,TEM}} \)
    !! - 9-13: \( c_{3, q_{e,ETG}}, c_{3, q_{e, ITG}}, c_{3, q_{e, TEM}}, c_{3, q_{i,ITG}}, c_{3, q_{i, TEM}} \)
    !! - 14-15: \(c_{\Gamma_{e, ITG}}, c_{\Gamma_{e, TEM}} \)
    real(qlknn_dp), dimension(:,:,:), optional, intent(out) :: dqlknn_out_dinput
    !! Jacobians of qlknn_out to input

    type(qlknn_normpars) :: qlknn_norms

    integer(lli) :: ii, rho, verbosity, outp, n_common_out, n_common_in, inp, jj
    integer(lli) :: n_rho, n_outputs, n_total_inputs, n_hidden_in, n_hidden_out, n_output_out, n_hidden_layers, n_general_in
    integer(lli) :: n_concat_in, n_concat_out
    integer(li), parameter :: n_nets = 20
    real(qlknn_dp), dimension(:), allocatable :: res
    real(qlknn_dp), dimension(:,:), allocatable :: net_result
    real(qlknn_dp), dimension(:,:), allocatable :: hidden_result
    real(qlknn_dp), dimension(:,:), allocatable :: output_result
    real(qlknn_dp), dimension(:,:,:), allocatable :: hidden_results_cs
    real(qlknn_dp), dimension(:,:,:), allocatable :: hidden_results_pfes
    real(qlknn_dp), dimension(:,:,:), allocatable :: pfe_hidden_input_layers
    real(qlknn_dp), dimension(:,:,:), allocatable :: common_in
    real(qlknn_dp), dimension(:,:,:), allocatable :: common_in_resc
    real(qlknn_dp), dimension(:,:), allocatable :: common_in_layers
    real(qlknn_dp), dimension(:,:,:), allocatable :: concat_layers
    real(qlknn_dp), dimension(:,:,:), allocatable :: common_out

    ! Jacobians!
    real(qlknn_dp), dimension(:,:), allocatable :: dqlknn_out_dinput_tmp
    real(qlknn_dp), dimension(:,:,:), allocatable :: dqlknn_out_dcommon_in_resc
    real(qlknn_dp), dimension(:,:,:), allocatable :: dqlknn_out_dgeneral_in_resc
    real(qlknn_dp), dimension(:), allocatable :: dqlknn_out_dcommon_in_resc_tmp
    real(qlknn_dp), dimension(:,:,:,:), allocatable :: dhidden_result_cs_dcommon_in_resc
    real(qlknn_dp), dimension(:,:,:,:), allocatable :: dcommon_out_dcommon_in_resc
    real(qlknn_dp), dimension(:,:,:,:), allocatable :: dconcat_layers_dgeneral_in_resc
    real(qlknn_dp), dimension(:,:,:,:), allocatable :: dcommon_in_resc_dcommon_in
    real(qlknn_dp), dimension(:), allocatable :: dcommon_in_resc_dcommon_in_tmp
    real(qlknn_dp), dimension(:,:,:,:), allocatable :: dpfe_hidden_input_layers_dgeneral_in_resc
    real(qlknn_dp), dimension(:,:,:,:), allocatable :: dpfe_hidden_input_layers_dconcat_layers
    real(qlknn_dp), dimension(:,:,:), allocatable :: doutput_result_dhidden_results
    logical, dimension(:,:), allocatable :: jacobian_clipmask
    type(qlknn_options) :: opts
    logical :: calcder
    !character(len=100) :: fmt_tmp
    integer(lli), dimension(15) :: input_map
    integer(lli), dimension(8) :: this_input_map
    integer(lli), dimension(15) :: late_fuse_var_map
    integer(lli), dimension(8,3) :: common_input_map

    common_input_map = reshape( (/ &
         1, 2, 4, 5,  6,  7,  8,  9, & ! ETG
         1, 3, 4, 5,  6,  7,  8,  9, & ! ITG
         1, 2, 4, 5,  6,  7,  8,  9  & ! TEM
         /), (/ 8, 3 /))

    late_fuse_var_map = (/ 3, 2, 3, 3, 2, 3, 2, 3, 3, 2, 3, 2, 3, 2, 3 /)

    input_map = (/ 1, 2, 3, 1, 2, 3, 2, 3, 1, 2, 3, 2, 3, 2, 3 /)

    ! zeff ati  ate   an         q      smag         x  ti_te logNustar
    !1.0   2.000000  5.0  2.0  0.660156  0.399902  0.449951    1.0      0.001
    !1.0  13.000000  5.0  2.0  0.660156  0.399902  0.449951    1.0      0.001
    if(present(verbosityin)) then
       verbosity=verbosityin
    else
       verbosity = 0
    end if

    if(present(dqlknn_out_dinput)) then
      calcder = .true.
    else
      calcder = .false.
    end if

    n_total_inputs = int(size(input, 1), li)
    n_rho = int(size(input, 2), li)
    n_outputs = int(size(qlknn_out, 2), li)
    allocate(net_result(n_rho, n_nets))

    allocate(res(n_rho)) !Debug

    if (verbosity >= 1) then
      write(*, '(A,I2,A,I3,A,I3,A,I3)') 'Calculating c* constants from input with n_hornet_constants=', 15, ', n_total_inputs=', n_total_inputs, ', n_outputs=', n_outputs, ', n_rho=', n_rho
    endif
    if (.NOT. (n_rho == size(qlknn_out, 1))) then
       write(stderr,*) 'size(qlknn_out, 1)=', size(qlknn_out, 1), ', nrho=', n_rho

       ERRORSTOP(.true., 'Rows of qlknn_out should be equal to number of radial points!')
    end if
    if (15 /= n_outputs) then
       write(stderr,*) 'size(qlknn_out, 2)=', size(qlknn_out, 2)

       ERRORSTOP(.true., 'Columns of qlknn_out should be 15!')
    end if

    if (calcder) then
      if (15 /= size(dqlknn_out_dinput, 1)) then
        write(stderr,*) 'size(dqlknn_out_dinput, 1)=', size(dqlknn_out_dinput, 1)
        ERRORSTOP(.true., 'Rows of dqlknn_out_dinput should be equal to 15!')
      endif
      if (n_rho /= size(dqlknn_out_dinput, 2)) then
        write(stderr,*) 'size(dqlknn_out_dinput, 2)=', size(dqlknn_out_dinput, 2), ', nrho=', n_rho
        ERRORSTOP(.true., 'Columns of dqlknn_out_dinput should be equal to number of radial points!')
      endif
      if (n_total_inputs /= size(dqlknn_out_dinput, 3)) then
        write(stderr,*) 'size(dqlknn_out_dinput, 3)=', size(dqlknn_out_dinput, 3), ', n_total_inputs=', n_total_inputs
        ERRORSTOP(.true., 'Pages of dqlknn_out_dinput should be equal to number of inputs!')
      endif
    endif

    ! set options according to optsin if present from calling program. Otherwise set default
    if(present(optsin)) then
       opts=optsin
    else
       CALL default_qlknn_hornnet_options(opts)
    end if

    if (verbosity >= 1) then
       call print_qlknn_options(opts)
       write(*,*) 'input, n_rho=', n_rho
       do rho = 1, n_rho
          WRITE(*,'(11(F7.2, 1X))') (input(ii, rho), ii=1,n_total_inputs)
       end do
    end if

    if (.NOT. (n_outputs == size(qlknn_out, 2))) then
       write(stderr,*) 'size(qlknn_out, 2)=', size(qlknn_out, 2),', n_outputs=', n_outputs
       ERRORSTOP(.true., 'Columns of qlknn_out should be equal to number of outputs!')
    endif

    if (opts%apply_victor_rule .AND. .NOT. present(qlknn_normsin)) then
       ERRORSTOP(.true., 'Need to pass qlknn_normsin when applying Victor rule')
    else if (present(qlknn_normsin)) then
       qlknn_norms = qlknn_normsin
    end if



    ! Impose input constraints
    if (calcder) then
      call impose_input_constraints(input, input_clipped, opts, verbosity, jacobian_clipmask)
    else
      call impose_input_constraints(input, input_clipped, opts, verbosity)
    endif

    n_common_in = int(size(blocks%input_blocks(1)%weights_input, 2), lli) ! Assume all modes have same shaped input layer
    allocate(common_in(n_common_in, n_rho, 3))
    if (calcder) then
      n_hidden_layers = size(blocks%output_blocks(1)%biases_hidden)
      n_hidden_out = int(size(blocks%output_blocks(1)%biases_hidden(n_hidden_layers)%bias_layer), li)
      allocate(dhidden_result_cs_dcommon_in_resc(n_hidden_out, n_rho, n_common_in, 13))
      dhidden_result_cs_dcommon_in_resc = 0
    else
      allocate(dhidden_result_cs_dcommon_in_resc(0,0,0,0))
    endif
    do ii = 1, 3
      common_in(:, :, ii) = input_clipped(common_input_map(:, ii), :)
    enddo

    ! Scale common input
    ! If calcder, also calculate dcommon_in_resc_dcommon_in. We will need this at the end
    allocate(common_in_resc(n_common_in, n_rho, 3))
    allocate(dcommon_in_resc_dcommon_in(n_outputs, n_rho, n_common_in, 3))
    do rho = 1, n_rho
      do ii = 1, 3
        common_in_resc(:, rho, ii) = blocks%input_blocks(ii)%feature_prescale_factor(common_input_map(:, ii)) * common_in(:, rho, ii) + &
             blocks%input_blocks(ii)%feature_prescale_bias(common_input_map(:, ii))
        if (calcder) then
          do outp = 1, n_outputs
            dcommon_in_resc_dcommon_in(outp, rho,:, ii) = blocks%input_blocks(ii)%feature_prescale_factor(common_input_map(:, ii))
          enddo
        endif
      enddo
    enddo

    if (verbosity >= 3) then
      write(*,*) 'common_in_resc ETG'
      do rho = 1, n_rho
        write(*,'(8(f7.2, 1x))') common_in_resc(:, rho, 1)
      enddo
      write(*,*) 'common_in_resc ITG'
      do rho = 1, n_rho
        write(*,'(8(f7.2, 1x))') common_in_resc(:, rho, 2)
      enddo
    endif

    ! Caclulate common_out, the output of the common input layers
    ! If calcder, also calculate dcommon_out_dcommon_in_resc. This will be updated one-by-one, and will finally store
    ! the Jacobian output of the common output vs the scaled input of the common layers.
    n_common_out = int(size(blocks%input_blocks(1)%weights_input, 1), lli) ! Assume all modes have same shaped input layer. (ie. 64)
    allocate(common_out(n_common_out, n_rho, 3))
    ! Evaluate common input layers
    if (calcder) then
      allocate(dcommon_out_dcommon_in_resc(n_common_out, n_rho, n_common_in, 3)) ! ie. 64 x 24 x 8
      do ii = 1, 3
        call evaluate_layer(common_in_resc(:, :, ii), blocks%input_blocks(ii)%weights_input, blocks%input_blocks(ii)%biases_input, 'tanh', common_out(:, :, ii), verbosity, dcommon_out_dcommon_in_resc(:,:,:,ii))
      enddo
    else
      allocate(dcommon_out_dcommon_in_resc(0,0,0,0))
      do ii = 1, 3
        call evaluate_layer(common_in_resc(:, :, ii), blocks%input_blocks(ii)%weights_input, blocks%input_blocks(ii)%biases_input, 'tanh', common_out(:, :, ii), verbosity)
      enddo
    endif

    if (verbosity >= 3) then
      write(*,*) 'common_out ETG(:10, :)'
      do rho = 1, n_rho
        write(*,'(10(f7.2, 1x))') common_out(:10, rho, 1)
      enddo
      write(*,*) 'common_out ITG(:10, :)'
      do rho = 1, n_rho
        write(*,'(10(f7.2, 1x))') common_out(:10, rho, 2)
      enddo
      if (calcder) then
        write(*,*) 'dcommon_out_dcommon_in_resc ITG(:10, :, 1)'
        do rho = 1, n_rho
          write(*,'(10(f7.2, 1x))') dcommon_out_dcommon_in_resc(:10, rho, 1, 2)
        enddo
      endif
    endif

    ! Evaluate pfe concat layer
    ! This is equivalent to the 'input layer' of regular nets, as this one is differently shaped
    ! From all the other layers
    n_concat_in = int(size(blocks%input_blocks(4)%weights_input, 2), li) ! Assume all modes have same shaped input layer
    n_concat_out = int(size(blocks%input_blocks(4)%weights_input, 1), li) ! Assume all modes have same shaped input layer
    allocate(concat_layers(n_concat_in, n_rho, 3)) ! eg. 65 x 24 x 3
    allocate(pfe_hidden_input_layers(n_concat_out, n_rho, 3))
    concat_layers(:, :, 1) = 0
    pfe_hidden_input_layers(:, :, 1) = 0
    ! Concat input. The last input will be the special input
    concat_layers(:size(concat_layers, 1) - 1, :, 2) = common_out(:, :, input_map(14))
    concat_layers(size(concat_layers, 1), :, 2) = blocks%input_blocks(1)%feature_prescale_factor(2) * &
       input_clipped(2, :) + blocks%input_blocks(1)%feature_prescale_bias(2) ! ITG needs Ati
    concat_layers(:size(concat_layers, 1) - 1, :, 3) = common_out(:, :, input_map(15))
    concat_layers(size(concat_layers, 1), :, 3) = blocks%input_blocks(1)%feature_prescale_factor(3) * &
       input_clipped(3, :) + blocks%input_blocks(1)%feature_prescale_bias(3) ! TEM needs Ate
    n_general_in = 9
    if (calcder) then
      allocate(dconcat_layers_dgeneral_in_resc(n_concat_in, n_rho, n_general_in, 3)) ! eg. 65 x 24 x 9
      dconcat_layers_dgeneral_in_resc(:n_concat_in - 1, :, :n_general_in - 1, 2) = dcommon_out_dcommon_in_resc(:, :, :, input_map(14))
      dconcat_layers_dgeneral_in_resc(:n_concat_in - 1, :, n_general_in, 2) = 0.
      dconcat_layers_dgeneral_in_resc(n_concat_in, :, :n_general_in - 1, 2) = 0. ! Last output only depends on itself
      dconcat_layers_dgeneral_in_resc(n_concat_in, :, n_general_in, 2) = 1. ! Last output only depends on itself

      dconcat_layers_dgeneral_in_resc(:n_concat_in - 1, :, :n_general_in - 1, 3) = dcommon_out_dcommon_in_resc(:, :, :, input_map(15))
      dconcat_layers_dgeneral_in_resc(:n_concat_in - 1, :, n_general_in, 3) = 0.
      dconcat_layers_dgeneral_in_resc(n_concat_in, :, :n_general_in - 1, 3) = 0. ! Last output only depends on itself
      dconcat_layers_dgeneral_in_resc(n_concat_in, :, n_general_in, 3) = 1. ! Last output only depends on itself
    else
      allocate(dconcat_layers_dgeneral_in_resc(0,0,0,0))
    endif

    if (verbosity >= 3) then
      write(*,*) 'concat_layer_pfeITG_GB(:10, :)'
      do rho = 1, n_rho
        write(*,'(11(f7.3, 1x))') concat_layers(:10, rho, 2), concat_layers(size(concat_layers, 1), rho, 2)
      enddo
    endif

    ! Evaluate pfe input layers
    if (calcder) then
      allocate(dpfe_hidden_input_layers_dconcat_layers(n_concat_out, n_rho, n_concat_in, 3))
      allocate(dpfe_hidden_input_layers_dgeneral_in_resc(n_concat_out, n_rho, n_general_in, 3)) ! 64 x 24 x 9 x 3
      dpfe_hidden_input_layers_dgeneral_in_resc(:, :, :, 1) = 0.
      dpfe_hidden_input_layers_dconcat_layers(:, :, :, 1) = 0.
      allocate(dqlknn_out_dinput_tmp(n_concat_out, n_general_in))
      ! Calculate dpfe_hidden_input_layers_dconcat_layers, the Jacobian of the
      ! Hidden input layers vs the concat input layers. E.g. 64 x 24 x 65
      call evaluate_layer(concat_layers(:, :, 2), blocks%input_blocks(4)%weights_input, &
         blocks%input_blocks(4)%biases_input, 'tanh', pfe_hidden_input_layers(:, :, 2), verbosity, &
         dpfe_hidden_input_layers_dconcat_layers(:, :, :, 2))
      call evaluate_layer(concat_layers(:, :, 3), blocks%input_blocks(5)%weights_input, &
         blocks%input_blocks(5)%biases_input, 'tanh', pfe_hidden_input_layers(:, :, 3), verbosity, &
         dpfe_hidden_input_layers_dconcat_layers(:, :, :, 3))
      do rho = 1, n_rho
        call dgemm('N', 'N', n_concat_out, n_general_in, n_concat_in, 1._qlknn_dp, dpfe_hidden_input_layers_dconcat_layers(:, rho, :, 2), n_concat_out, &
             dconcat_layers_dgeneral_in_resc(:, rho, :, 2), n_concat_in, 0._qlknn_dp, dqlknn_out_dinput_tmp(:,:), n_concat_out)
        dpfe_hidden_input_layers_dgeneral_in_resc(:, rho, :, 2) = dqlknn_out_dinput_tmp
        call dgemm('N', 'N', n_concat_out, n_general_in, n_concat_in, 1._qlknn_dp, dpfe_hidden_input_layers_dconcat_layers(:, rho, :, 3), n_concat_out, &
             dconcat_layers_dgeneral_in_resc(:, rho, :, 3), n_concat_in, 0._qlknn_dp, dqlknn_out_dinput_tmp(:,:), n_concat_out)
        dpfe_hidden_input_layers_dgeneral_in_resc(:, rho, :, 3) = dqlknn_out_dinput_tmp
      enddo
      deallocate(dqlknn_out_dinput_tmp)
    else
      allocate(dpfe_hidden_input_layers_dgeneral_in_resc(0,0,0,0))
      call evaluate_layer(concat_layers(:, :, 2), blocks%input_blocks(4)%weights_input, &
         blocks%input_blocks(4)%biases_input, 'tanh', pfe_hidden_input_layers(:, :, 2), verbosity)
      call evaluate_layer(concat_layers(:, :, 3), blocks%input_blocks(5)%weights_input, &
         blocks%input_blocks(5)%biases_input, 'tanh', pfe_hidden_input_layers(:, :, 3), verbosity)
    endif

    if (verbosity >= 3) then
      write(*,*) '1.hidden_layer_pfeITG_GB((:10 -1), :)'
      do rho = 1, n_rho
        write(*,'(11(f7.3, 1x))') pfe_hidden_input_layers(:10, rho, 2), pfe_hidden_input_layers(size(pfe_hidden_input_layers, 1), rho, 2)
      enddo
      write(*,*) '1.hidden_layer_pfeTEM_GB((:10 -1), :)'
      do rho = 1, n_rho
        write(*,'(11(f7.3, 1x))') pfe_hidden_input_layers(:10, rho, 3), pfe_hidden_input_layers(size(pfe_hidden_input_layers, 1), rho, 3)
      enddo
      if (calcder) then
        write(*,*) 'dpfeITG_dpfe_hidden_input_layers_resc(:10, :, 4)'
        do rho = 1, n_rho
          write(*,'(10(f7.3, 1x))') dpfe_hidden_input_layers_dgeneral_in_resc(:10, rho, 4, 2)
        enddo
      endif
    endif

    ! This assumes all hidden layers have the same output shape
    n_hidden_layers = size(blocks%output_blocks(1)%biases_hidden)
    n_hidden_in = int(size(blocks%output_blocks(1)%weights_hidden(n_hidden_layers)%weight_layer, 2), li)
    n_hidden_out = int(size(blocks%output_blocks(1)%biases_hidden(n_hidden_layers)%bias_layer), li)
    allocate(common_in_layers(n_hidden_in, n_rho))
    allocate(hidden_result(n_hidden_out, n_rho))
    allocate(hidden_results_cs(n_hidden_out, n_rho, 13))
    if (calcder) then
      if (n_hidden_in /= n_common_out) then
        write(stderr,*) 'Warning! n_hidden_in /= n_common_out. unexpected'
      endif
      if (n_hidden_out /= n_common_out) then
        write(stderr,*) 'Warning! n_hidden_out /= n_common_out. unexpected'
      endif
    endif
    ! Evaluate the hidden layers of c*, do not evaluate pfe layers!
    ! evaluate_layers will internally auto-multiply, so we get dhidden_result_cs_dcommon_in_resc directly
    do ii = 1, 13
      common_in_layers = common_out(:, :, input_map(ii))
      if (calcder) then
        dhidden_result_cs_dcommon_in_resc(:,:,:, ii) = dcommon_out_dcommon_in_resc(:,:,:, input_map(ii))
        call evaluate_layers(common_in_layers, blocks%output_blocks(ii)%weights_hidden, &
             blocks%output_blocks(ii)%biases_hidden, blocks%output_blocks(ii)%hidden_activation, &
             hidden_result, verbosity, dhidden_result_cs_dcommon_in_resc(:,:,:, ii))
      else
        call evaluate_layers(common_in_layers, blocks%output_blocks(ii)%weights_hidden, &
             blocks%output_blocks(ii)%biases_hidden, blocks%output_blocks(ii)%hidden_activation, &
             hidden_result, verbosity)
      endif
      hidden_results_cs(:,:,ii) = hidden_result
    enddo
    deallocate(hidden_result)
    deallocate(common_in_layers)

    ! Evaluate pfe layers
    ! This assumes all hidden layers have the same output shape
    ! dpfe_hidden_input_layers_dconcat_layers e.g. 64 x 24 x 65 x 3
    ! pfe_hidden_input_layers e.g. 64 x 24 x 3
    n_hidden_in = int(size(blocks%output_blocks(14)%weights_hidden(1)%weight_layer, 2), li)
    n_hidden_layers = size(blocks%output_blocks(14)%biases_hidden)
    n_hidden_out = int(size(blocks%output_blocks(14)%biases_hidden(n_hidden_layers)%bias_layer), li) !64
    allocate(hidden_results_pfes(n_hidden_out, n_rho, 3))
    hidden_results_pfes(:, :, 1) = 0
    if (calcder) then
      call evaluate_layers(pfe_hidden_input_layers(:, :, 2), blocks%output_blocks(14)%weights_hidden, &
           blocks%output_blocks(14)%biases_hidden, blocks%output_blocks(14)%hidden_activation, &
           hidden_results_pfes(:, :, 2), verbosity, dpfe_hidden_input_layers_dgeneral_in_resc(:,:,:,2))
      call evaluate_layers(pfe_hidden_input_layers(:, :, 3), blocks%output_blocks(15)%weights_hidden, &
           blocks%output_blocks(15)%biases_hidden, blocks%output_blocks(15)%hidden_activation, &
           hidden_results_pfes(:, :, 3), verbosity, dpfe_hidden_input_layers_dgeneral_in_resc(:,:,:,3))
    else
      call evaluate_layers(pfe_hidden_input_layers(:, :, 2), blocks%output_blocks(14)%weights_hidden, &
           blocks%output_blocks(14)%biases_hidden, blocks%output_blocks(14)%hidden_activation, &
           hidden_results_pfes(:, :, 2), verbosity)
      call evaluate_layers(pfe_hidden_input_layers(:, :, 3), blocks%output_blocks(15)%weights_hidden, &
           blocks%output_blocks(15)%biases_hidden, blocks%output_blocks(15)%hidden_activation, &
           hidden_results_pfes(:, :, 3), verbosity)
    endif

    if (verbosity >= 3) then
      write(*,*) 'hidden_out c1_etg(:10)'
      do rho = 1, n_rho
        write(*,'(10(f7.3, 1x))') hidden_results_cs(:10, rho, 1)
      enddo
      write(*,*) 'hidden_out c2_efeitg(:10)'
      do rho = 1, n_rho
        write(*,'(10(f7.3, 1x))') hidden_results_cs(:10, rho, 5)
      enddo
      if (calcder) then
        write(*,*) 'hidden_out dc2_efeitg_dcommon_in(:10, :, 1)'
        do rho = 1, n_rho
          write(*,'(10(f7.3, 1x))') dhidden_result_cs_dcommon_in_resc(:10, rho, 1, 5)
        enddo
        write(*,*) 'dpfeITG_dpfe_hidden_layers_resc(:10, :, 4)'
        do rho = 1, n_rho
          write(*,'(10(f7.3, 1x))') dpfe_hidden_input_layers_dgeneral_in_resc(:10, rho, 4, 2)
        enddo
      endif
      write(*,*) 'hidden_out pfeitg(:10)'
      do rho = 1, n_rho
        write(*,'(10(f7.3, 1x))') hidden_results_pfes(:10, rho, 2)
      enddo
      write(*,*) 'hidden_out pfetem(:10)'
      do rho = 1, n_rho
        write(*,'(10(f7.3, 1x))') hidden_results_pfes(:10, rho, 3)
      enddo
    endif

    ! Apply c* output layer
    n_hidden_layers = size(blocks%output_blocks(1)%biases_hidden)
    n_hidden_out = int(size(blocks%output_blocks(1)%biases_hidden(n_hidden_layers)%bias_layer), li)
    n_output_out = int(size(blocks%output_blocks(1)%weights_output, 1), li)
    ERRORSTOP(n_output_out /= 1, 'Expected 1D output from c* layers')
    allocate(output_result(1, n_rho))
    if (calcder) then
      allocate(doutput_result_dhidden_results(n_output_out, n_rho, n_hidden_out)) ! e.g. 1 x 24 x 64
      allocate(dqlknn_out_dinput_tmp(n_output_out, n_common_in)) ! 1 x 8
      allocate(dqlknn_out_dcommon_in_resc(13, n_rho, n_common_in)) ! 13 x 24 x 8
    else
      allocate(dqlknn_out_dcommon_in_resc(0,0,0))
    endif
    if (n_output_out /= 1) then
      write(stderr, *) 'shape output block is ', n_output_out
      ERRORSTOP(.true., 'ND output block. Expected 1D')
    endif
    do ii = 1, 13
      if (calcder) then
        call evaluate_layer(hidden_results_cs(:, :, ii), blocks%output_blocks(ii)%weights_output, &
             blocks%output_blocks(ii)%biases_output, 'none', &
             output_result, verbosity, doutput_result_dhidden_results)
        do rho = 1, n_rho
          ! Gives us doutput_result_dcommon_in_resc ~= dqlknn_out_dinput (still need to clip)
          ! e.g. dhidden_result_cs_dcommon_in_resc 64 x 24 x 8 x 15
          call dgemm('N', 'N', n_output_out, n_common_in, n_hidden_out, 1._qlknn_dp, doutput_result_dhidden_results(:, rho, :), n_output_out, &
               dhidden_result_cs_dcommon_in_resc(:, rho, :, ii), n_hidden_out, 0._qlknn_dp, dqlknn_out_dinput_tmp(:,:), n_output_out)

          ! dqlknn_out_dinput_tmp is general here: It could be ND. We want it to be 1D (for now)
          ERRORSTOP(size(dqlknn_out_dinput_tmp, 1) /= 1, 'Output of hidden layer is not 1D')
          dqlknn_out_dcommon_in_resc(ii, rho, :) = dqlknn_out_dinput_tmp(1, :)
        enddo
      else
        call evaluate_layer(hidden_results_cs(:, :, ii), blocks%output_blocks(ii)%weights_output, &
             blocks%output_blocks(ii)%biases_output, 'none', &
             output_result, verbosity)
      endif
      qlknn_out(:, ii) = output_result(1, :)
    enddo

    ! Apply pfe output layer
    n_hidden_layers = size(blocks%output_blocks(14)%biases_hidden)
    n_hidden_out = int(size(blocks%output_blocks(14)%biases_hidden(n_hidden_layers)%bias_layer), li)
    n_output_out = int(size(blocks%output_blocks(14)%weights_output, 1), li)
    ERRORSTOP(n_output_out /= 1, 'Expected 1D output from pfe layers')
    if (calcder) then
      deallocate(dqlknn_out_dinput_tmp)
      allocate(dqlknn_out_dinput_tmp(n_output_out, n_general_in)) ! 1 x 9
      allocate(dqlknn_out_dgeneral_in_resc(3, n_rho, n_general_in)) ! 3 x 24 x 9
      do jj = 14, 15
        ii = jj - 12
        call evaluate_layer(hidden_results_pfes(:, :, ii), blocks%output_blocks(jj)%weights_output, &
             blocks%output_blocks(jj)%biases_output, 'none', &
             output_result, verbosity, doutput_result_dhidden_results)
        do rho = 1, n_rho
          ! dpfe_hidden_input_layers_dgeneral_in e.g. 64 x 24 x 9 x 3
          call dgemm('N', 'N', n_output_out, n_general_in, n_hidden_out, 1._qlknn_dp, doutput_result_dhidden_results(:, rho, :), n_output_out, &
               dpfe_hidden_input_layers_dgeneral_in_resc(:, rho, :, ii), n_hidden_out, 0._qlknn_dp, dqlknn_out_dinput_tmp(:,:), n_output_out)

          ! dqlknn_out_dinput_tmp is general here: It could be ND. We want it to be 1D (for now)
          ERRORSTOP(size(output_result, 1) /= 1, 'Output of hidden layer is not 1D')
          ERRORSTOP(size(dqlknn_out_dinput_tmp, 1) /= 1, 'Output of hidden layer is not 1D')
          dqlknn_out_dgeneral_in_resc(ii, rho, :) = dqlknn_out_dinput_tmp(1, :)
          qlknn_out(:, jj) = output_result(1, :)
        enddo
      enddo
    else
      allocate(dqlknn_out_dgeneral_in_resc(0,0,0))
      call evaluate_layer(hidden_results_pfes(:, :, 2), blocks%output_blocks(14)%weights_output, &
           blocks%output_blocks(14)%biases_output, 'none', &
           output_result, verbosity)

      qlknn_out(:, 14) = output_result(1, :)
      call evaluate_layer(hidden_results_pfes(:, :, 3), blocks%output_blocks(15)%weights_output, &
           blocks%output_blocks(15)%biases_output, 'none', &
           output_result, verbosity)
      qlknn_out(:, 15) = output_result(1, :)
    endif

    if (verbosity >= 3) then
      write(*,*) 'c* output layers out'
      do rho = 1, n_rho
        write(*,'(15(f7.3, 1x))') qlknn_out(rho, :)
      enddo
    endif
    ! c* does not depend on the special input, nor the victorrule inputs
    ! dcommon_in_resc_dcommon_in: 15 x 24 x 9 x 3
    if (calcder) then
      allocate(dcommon_in_resc_dcommon_in_tmp(n_total_inputs))
      allocate(dqlknn_out_dcommon_in_resc_tmp(n_total_inputs))
      do rho = 1, n_rho
        do outp = 1, 13
          this_input_map = common_input_map(:, input_map(outp))
          dcommon_in_resc_dcommon_in_tmp = 0.
          dcommon_in_resc_dcommon_in_tmp(this_input_map) = dcommon_in_resc_dcommon_in(outp, rho, :, input_map(outp))
          dqlknn_out_dcommon_in_resc_tmp = 0.
          dqlknn_out_dcommon_in_resc_tmp(this_input_map) = dqlknn_out_dcommon_in_resc(outp, rho, 1:8)
          call vdmul(n_total_inputs, dqlknn_out_dcommon_in_resc_tmp, dcommon_in_resc_dcommon_in_tmp, dqlknn_out_dinput(outp, rho, :))
        enddo
        do outp = 14, 15
          ! pfe DOES depend on special input
          ! input_map = (/ 1, 2, 3, 1, 2, 3, 2, 3, 1, 2, 3, 2, 3, 2, 3 /)
          ! common_input_map(:, 2) = 1, 3, 4, 5,  6,  7,  8,  9
          ! late_fuse_var_map = (/ 3, 2, 3, 3, 2, 3, 2, 3, 3, 2, 3, 2, 3, 2, 3 /)
          ii = outp - 12
          this_input_map = common_input_map(:, input_map(outp))
          dcommon_in_resc_dcommon_in_tmp = 0.
          dcommon_in_resc_dcommon_in_tmp(this_input_map) = dcommon_in_resc_dcommon_in(outp, rho, :, input_map(outp))
          dcommon_in_resc_dcommon_in_tmp(late_fuse_var_map(outp)) = dcommon_in_resc_dcommon_in(outp, rho, late_fuse_var_map(outp), input_map(outp))
          dqlknn_out_dcommon_in_resc_tmp = 0.
          dqlknn_out_dcommon_in_resc_tmp(this_input_map) = dqlknn_out_dgeneral_in_resc(ii, rho, 1:8) ! The first 8 vars are in the input map
          dqlknn_out_dcommon_in_resc_tmp(late_fuse_var_map(outp)) = dqlknn_out_dgeneral_in_resc(ii, rho, n_general_in) ! The 9th var is the special input
          call vdmul(n_total_inputs, dqlknn_out_dcommon_in_resc_tmp, dcommon_in_resc_dcommon_in_tmp, dqlknn_out_dinput(outp, rho, :))
        enddo
      enddo
    endif


    ! c2 neuron has a rectifier as activation function
    if (calcder) then
      do inp = 1, n_total_inputs
        do outp = 4, 8
          where (qlknn_out(:, outp) < 0.)
            dqlknn_out_dinput(outp, :, inp) = 0
          end where
        end do
      end do
    endif
    do outp = 4, 8
      qlknn_out(:, outp) = max(qlknn_out(:, outp), 0._qlknn_dp)
    enddo

    if (verbosity >= 1) then
      write(*,*) 'c* outputs:'
      do rho = 1, n_rho
        write(*,'(15(f7.3, 1x))') qlknn_out(rho, :)
      enddo
    endif
    if (verbosity >= 2) then
      if (calcder) then
        write(*,*) 'dc*_dinput (:, :, 2)'
        do rho = 1, n_rho
          write(*,'(15(f7.3, 1x))') dqlknn_out_dinput(:, rho, 2)
        enddo
        write(*,*) 'dc*_dinput (:, :, 3)'
        do rho = 1, n_rho
          write(*,'(15(f7.3, 1x))') dqlknn_out_dinput(:, rho, 3)
        enddo
      endif
    endif


  end subroutine evaluate_hornnet_constants

  subroutine evaluate_multinet(net_input, nets, net_evaluate, net_result, verbosityin, dnet_out_dnet_in)
    real(qlknn_dp), dimension(:,:), intent(in) :: net_input
    type(net_collection), intent(in) :: nets
    logical, dimension(:), intent(in) :: net_evaluate
    integer(lli), intent(in), optional :: verbosityin

    real(qlknn_dp), dimension(:,:), intent(out) :: net_result
    real(qlknn_dp), dimension(:,:,:), intent(out), optional :: dnet_out_dnet_in

    integer(li) :: job, n_in
    integer(lli) ii, jj, verbosity
    integer(lli), dimension(:), allocatable :: myjobs, joblist
    logical :: calcder
    !integer(lli), parameter :: max_nets = 23*10
    !integer(lli), dimension(max_nets), parameter :: potential_net_joblist = (/(ii, ii=1,max_nets)/)
#if (defined(LLI) && defined(__INTEL_COMPILER)) || defined(MEXING)
    integer(lli) :: my_world_rank, myjobs_length
#else
    integer(li) :: my_world_rank, myjobs_length
#endif
#ifdef MPI
    integer(li) :: n_rho
    integer(li), dimension(:), allocatable :: their_jobs, to_gather_jobs
    real(qlknn_dp), dimension(:), allocatable :: rec_buffer
    real(qlknn_dp), dimension(:,:), allocatable :: rec_buffer_jac
    integer(li) recv_status(MPI_STATUS_SIZE)
    logical :: master_is_no_worker
#if (defined(LLI) && defined(__INTEL_COMPILER)) || defined(MEXING)
    integer(lli) :: mpi_ierr, world_size, their_world_rank, their_jobs_length
#else
    integer(li) :: mpi_ierr, world_size, their_world_rank, their_jobs_length
#endif
#endif

    if(present(verbosityin)) then
       verbosity=verbosityin
    else
       verbosity = 0
    end if

#ifdef MPI
    call MPI_COMM_SIZE(MPI_COMM_WORLD, world_size, mpi_ierr)
    call MPI_COMM_RANK(MPI_COMM_WORLD, my_world_rank, mpi_ierr)
    if (my_world_rank == 0) then
      if (verbosity >= 2) write(*,*) 'World size in evaluate_multinet is ', world_size
    end if
    if (verbosity >= 2) write(*,*) 'Hello world from evaluate_multinet rank ', my_world_rank
    n_rho = int(size(net_input, 2), li)
#else
    my_world_rank = 0
#endif

    if(present(verbosityin)) then
      verbosity=verbosityin
    else
      verbosity = 0
    end if

    if(present(dnet_out_dnet_in)) then
      calcder = .true.
    else
      calcder = .false.
    end if

    !ERRORSTOP(size(net_evaluate) > max_nets, 'Number of nets to evaluate bigger than max_nets!')

    n_in = int(size(net_input, 1), li)

    allocate(joblist(COUNT(net_evaluate)))
    ! TODO Somhow this is making fullflux nets crash, suspicious!
    !joblist(1:COUNT(net_evaluate)) = PACK(potential_net_joblist, net_evaluate)
    jj = 1
    do ii = 1, SIZE(net_evaluate)
      if (net_evaluate(ii)) then
        joblist(jj) = ii
        jj = jj + 1
      endif
    enddo
    ERRORSTOP(maxval(joblist) > size(nets%nets), 'joblist contains index larger than amount of nets!')
    net_result = 0.
#ifdef MPI
    master_is_no_worker = .false.
    if (master_is_no_worker .and. world_size > 1) then
      if (my_world_rank /= 0) then
        CALL calc_length(world_size - my_world_rank, size(joblist), world_size - 1, myjobs_length)
        allocate(myjobs(myjobs_length))
        myjobs = joblist(world_size - my_world_rank:size(joblist):world_size - 1)
      else
        allocate(myjobs(0))
      end if
    else
      CALL calc_length(world_size - my_world_rank, size(joblist), world_size, myjobs_length)
      allocate(myjobs(myjobs_length))
      myjobs = joblist(world_size - my_world_rank:size(joblist):world_size)
    end if
#else
    myjobs_length = INT(size(joblist), li)
    allocate(myjobs(myjobs_length))
    myjobs = joblist
#endif
    do ii = 1,size(myjobs)
      job = INT(myjobs(ii), li)
      if (net_evaluate(job)) then
        if (verbosity >= 2) write(*,*) 'rank ', my_world_rank, 'doing job ', job
        if (calcder) then
          call evaluate_network(net_input, nets%nets(job), net_result(:, job), verbosity, dnet_out_dnet_in(job, :, :))
        else
          call evaluate_network(net_input, nets%nets(job), net_result(:, job), verbosity)
        endif
      end if
    end do
#ifdef MPI
    if (verbosity >= 2) write(*,*) 'rank ', my_world_rank, 'done with working'
    call mpi_barrier(MPI_COMM_WORLD, mpi_ierr)
    is_zero_rank: if (my_world_rank /= 0) then
      do ii =1,size(myjobs)
        job = INT(myjobs(ii), li)
        if (net_evaluate(job)) then
          if (verbosity >= 2) write(*,*) 'rank ', my_world_rank, 'sending job ', job, 'len ', size(net_result(:,job))
          call mpi_send(net_result(:,job), n_rho, MPI_DOUBLE_PRECISION, INT(0, li), job, MPI_COMM_WORLD, mpi_ierr)
          if (calcder) then
            call mpi_send(dnet_out_dnet_in(job, :, :), INT(n_rho * n_in, li), MPI_DOUBLE_PRECISION, INT(0, li), job, MPI_COMM_WORLD, mpi_ierr)
          end if
        end if
      end do
    else is_zero_rank
      allocate(to_gather_jobs(INT(size(joblist), li)))
      to_gather_jobs = INT(joblist, li)
      do ii = 1, size(myjobs)
        where(to_gather_jobs == myjobs(ii))
          to_gather_jobs = 0
        endwhere
      end do

      allocate(rec_buffer(n_rho))
      if (calcder) then
        allocate(rec_buffer_jac(n_rho, n_in))
      else
        allocate(rec_buffer_jac(0, 0))
      end if
      gathering: do while (.not. all(to_gather_jobs == 0))
        gather_jobs: do ii =1,size(to_gather_jobs)
          job = to_gather_jobs(ii)
          have_to_gather: if (job /= 0) then
#if (defined(LLI) && defined(__INTEL_COMPILER)) || defined(MEXING)
            do their_world_rank=1_lli, world_size-1_lli
#else
            do their_world_rank=1_li, world_size-1_li
#endif
              if (master_is_no_worker) then
                CALL calc_length(world_size - their_world_rank, size(joblist), world_size - 1_li, their_jobs_length)
                allocate(their_jobs(their_jobs_length))
                their_jobs = INT(joblist(world_size - their_world_rank:size(joblist):world_size - 1), li)
              else
                CALL calc_length(world_size - their_world_rank, size(joblist), world_size, their_jobs_length)
                allocate(their_jobs(their_jobs_length))
                their_jobs = INT(joblist(world_size - their_world_rank:INT(size(joblist), li):world_size), li)
              end if
              if (any(job == their_jobs)) then
                if (verbosity >= 2) write(*,*) 'rank ', my_world_rank, 'trying to receive job ', job, 'from rank ', their_world_rank
                call mpi_recv(rec_buffer, n_rho, MPI_DOUBLE_PRECISION, MPI_ANY_SOURCE, job, MPI_COMM_WORLD, recv_status, mpi_ierr)
                net_result(:,job) = rec_buffer
                if (calcder) then
                  call mpi_recv(rec_buffer_jac, INT(n_rho * n_in, li), MPI_DOUBLE_PRECISION, MPI_ANY_SOURCE, job, MPI_COMM_WORLD, recv_status, mpi_ierr)
                  dnet_out_dnet_in(job, :, :) = rec_buffer_jac
                end if
                where(to_gather_jobs == job)
                  to_gather_jobs = 0
                endwhere
              end if
              deallocate(their_jobs)
            end do
          end if have_to_gather
        end do gather_jobs
      end do gathering
    end if is_zero_rank
    call mpi_barrier(MPI_COMM_WORLD, mpi_ierr)

    if (my_world_rank /= 0) then
      if (verbosity >= 2) write(*,*) 'rank ', my_world_rank, 'returning'
      return
    else
      if (verbosity >= 2) write(*,*) 'rank ', my_world_rank, 'continuing'
    endif
#endif
  end subroutine evaluate_multinet

end module qlknn_evaluate_nets
