! This file is part of QLKNN-fortran
! You should have received the QLKNN-fortran LICENSE in the root of the project
module qlknn_victor_rule
    use qlknn_types
    use qlknn_primitives

    implicit none
    real(qlknn_dp), parameter :: c_1 = 0.13, c_2 = 0.41, c_3 = 0.09, c_4 = 1.65
    real(qlknn_dp), parameter :: gamma0_lower_bound = 1e-4; !Clip, gamma0 can't be negative! Avoid infinities for now
    real(qlknn_dp), parameter :: victor_Te_norm = 1e-4;

    !! Documentation regarding Victor Rule linear GENE run reference parameters (not needed here in code but written for reference)
    !real(qlknn_dp), parameter :: Te_ref_vic = 1.98 !keV
    !real(qlknn_dp), parameter :: n_ref_vic = 2.7 !10^-19 m-3
    !real(qlknn_dp), parameter :: B_ref_vic = 3.35 !T
    !real(qlknn_dp), parameter :: L_ref_vic = 2.947 !m
    !real(qlknn_dp), parameter :: A_ref_vic = 2 !au

contains
    subroutine get_f_victorthesis(input, nets, f_victorthesis, dthesis_dinput)
        real(qlknn_dp), dimension(:,:), intent(in):: input
        type(net_collection), intent(in) :: nets

        real(qlknn_dp), dimension(:), intent(out) :: f_victorthesis
        real(qlknn_dp), dimension(:,:), optional :: dthesis_dinput

        real(qlknn_dp) :: epsLCFS_nn

        epsLCFS_nn = nets%a / nets%R_0
        f_victorthesis = c_1 * input(nets%q_ind, :) + &
            c_2 * input(nets%smag_ind, :) + &
            c_3 / (epsLCFS_nn * input(nets%x_ind, :)) - &
            c_4

       if (present(dthesis_dinput)) then
         dthesis_dinput = 0
         dthesis_dinput(:, nets%q_ind) = c_1
         dthesis_dinput(:, nets%smag_ind) = c_2
         dthesis_dinput(:, nets%x_ind) = -c_3 / (epsLCFS_nn * input(nets%x_ind, :)**2)
       endif
    end subroutine

    subroutine get_f_vic(input, nets, qlknn_norms, f_vic, verbosity, df_vic_dinput)
        real(qlknn_dp), dimension(:,:), intent(in):: input
        type(net_collection), intent(in) :: nets
        type(qlknn_normpars), intent(in):: qlknn_norms
        integer(lli), optional, intent(in) :: verbosity

        real(qlknn_dp), dimension(:), intent(out) :: f_vic
        real(qlknn_dp), dimension(:,:), optional, intent(out) :: df_vic_dinput

        integer(lli) :: n_rho, n_inputs, inp
        !gammaE below is targeted to be QLK GB units [csou/a] with csou=sqrt(Te/mi)
        real(qlknn_dp), dimension(:), allocatable :: f_victorthesis, gamma0, dvperp_dr, c_sou, gammaE, c_c_sou
        real(qlknn_dp), dimension(:,:), allocatable :: dthesis_dinput, dgamma0_dinput
        real(qlknn_dp), dimension(:), allocatable :: dvperp_dr_dgammaE_inp, dc_sou_dTe, dgammaE_dgammaE_inp, dgammaE_dTe
        real(qlknn_dp), dimension(:), allocatable :: temp_vec
        real(qlknn_dp), dimension(:,:), allocatable :: temp_matr
        logical, dimension(:), allocatable :: gamma0_clipped, f_vic_clipped
        character(len=512) :: line
        logical :: calcder

        n_rho = size(input, 2)
        n_inputs = size(input, 1)
        if (present(df_vic_dinput)) then
          calcder = .true.
        else
          calcder = .false.
        endif

        allocate(gamma0(n_rho))
        if (calcder) then
          allocate(dgamma0_dinput(n_rho, 9))
          call evaluate_network(input(1:9, :), nets%nets(20), gamma0, verbosity, dgamma0_dinput)
        else
          call evaluate_network(input(1:9, :), nets%nets(20), gamma0, verbosity)
        endif
        if (verbosity >= 3) then
            write(*,*) 'gamma0 pre-clip'
            write(*,'(F7.2)') gamma0
        end if

        !gamma0 in QLK GB units [csou/Rmin] where csou = sqrt(Te/mi)
        gamma0 = MAX(gamma0, gamma0_lower_bound)
        if (verbosity >= 3) then
            write(*,*) 'gamma0 post-clip'
            write(*,'(F7.2)') gamma0
        end if

        allocate(f_victorthesis(n_rho))
        allocate(dvperp_dr(n_rho))
        allocate(c_sou(n_rho))
        allocate(c_c_sou(n_rho))
        allocate(gammaE(n_rho))
        if (calcder) then
          allocate(dthesis_dinput(n_rho, n_inputs))
          allocate(gamma0_clipped(n_rho))
          allocate(dvperp_dr_dgammaE_inp(n_rho))
          allocate(dc_sou_dTe(n_rho))
          allocate(dgammaE_dgammaE_inp(n_rho))
          allocate(dgammaE_dTe(n_rho))
          allocate(temp_vec(n_rho))
          allocate(temp_matr(n_rho, 9))
          call is_not_close(gamma0, gamma0_lower_bound, gamma0_clipped)
          gamma0_clipped = .not. gamma0_clipped
        else
          allocate(dthesis_dinput(0,0))
          allocate(gamma0_clipped(0))
          allocate(dvperp_dr_dgammaE_inp(0))
          allocate(dc_sou_dTe(0))
          allocate(dgammaE_dgammaE_inp(0))
          allocate(dgammaE_dTe(0))
          allocate(temp_vec(0))
          allocate(temp_matr(0,0))
        endif

        !assumes gammaE input is in QLK cref/R0 normalisation
        dvperp_dr = input(nets%gammaE_ind, :) * c_qlk_ref / qlknn_norms%R0
        c_c_sou = (qe * 1e3) / (qlknn_norms%A1 * mp)
        c_sou = sqrt(c_c_sou * input(nets%Te_ind, :))
        gammaE = dvperp_dr * qlknn_norms%a / c_sou
        if (verbosity >= 3) then
            write(*,*) 'gammaE'
            write(*,'(F7.2)') gammaE
        end if
        if (calcder) then
          dvperp_dr_dgammaE_inp = c_qlk_ref / qlknn_norms%R0
          dc_sou_dTe = c_c_sou / (2 * c_sou)
          dgammaE_dgammaE_inp = qlknn_norms%a / c_sou * dvperp_dr_dgammaE_inp
          dgammaE_dTe = -dvperp_dr * qlknn_norms%a * dc_sou_dTe / c_sou**2
          call get_f_victorthesis(input, nets, f_victorthesis, dthesis_dinput)
        else
          call get_f_victorthesis(input, nets, f_victorthesis)
        endif
        if (verbosity >= 3) then
            write(*,*) 'f_victorthesis'
            write(*,'(F7.2)') f_victorthesis
        end if
        ! f = 1 + f_victorthesis(9D) * gammaE(gammaE_QLK) / gamma0(9D)
        !f_vic = MAX(1 + f_victorthesis * abs(gammaE) / gamma0, 2._qlknn_dp)
        f_vic = 1 + f_victorthesis * abs(gammaE) / gamma0
        if (calcder) then
          where (gamma0_clipped) f_vic = 0
          do inp = 1, n_inputs
            where (gamma0_clipped) df_vic_dinput(:, inp) = 0
          enddo
          ! df_vic/d9D = gammaE(gammaE_in)/ {dgamma0(9D)/d9D}**2 * (df_victorthesis(9D)/d9D * gamma0(9D) - dgamma0(9D)/d9D * f_victorthesis(9D))
          call matr_vec_mult_elemwise(n_rho * 9_li, dthesis_dinput(:, 1:9), gamma0, df_vic_dinput(:, 1:9))
          call matr_vec_mult_elemwise(n_rho * 9_li, dgamma0_dinput, f_victorthesis, temp_matr)
          df_vic_dinput(:, 1:9) =  df_vic_dinput(:, 1:9) - temp_matr
          call matr_vec_mult_elemwise(n_rho * 9_li, df_vic_dinput(:, 1:9), abs(gammaE)/gamma0**2, df_vic_dinput(:, 1:9))
          ! df_vic/dgammaE_in = f_victorthesis / gamma0 * dgammaE/dgammaE_in
          df_vic_dinput(:, nets%gammaE_ind) = f_victorthesis / (gamma0 + epsilon(gamma0)) * dgammaE_dgammaE_inp * gammaE/abs(gammaE + epsilon(gammaE))
          write(line,*) 'getting ', nets%Te_ind
          df_vic_dinput(:, nets%Te_ind) = f_victorthesis / gamma0 * dgammaE_dTe * gammaE/abs(gammaE + epsilon(gammaE))

          allocate(f_vic_clipped(n_rho))
          call is_not_close(f_vic, 0._qlknn_dp, f_vic_clipped)
          f_vic_clipped = .not. f_vic_clipped
          do inp = 1, n_inputs
            where (f_vic_clipped) df_vic_dinput(:, inp) = 0
          enddo
        endif
        if (verbosity >= 3) then
            write(*,*) 'f_vic'
            write(*,'(F7.2)') f_vic
        end if
        ! Not sure if this is needed, pending deletion
        !where (gamma0 .le. gamma0_lower_bound) f_vic = 0

    end subroutine get_f_vic

    subroutine scale_with_victor(leading_map, input, nets, qlknn_norms, net_result, verbosity, dnet_out_dinput)
        integer(lli), dimension(:,:), intent(in) :: leading_map
        real(qlknn_dp), dimension(:,:), intent(in):: input
        type(net_collection), intent(in) :: nets
        type(qlknn_normpars), intent(in):: qlknn_norms
        integer(lli), optional, intent(in) :: verbosity

        real(qlknn_dp), dimension(:,:), intent(inout) :: net_result
        real(qlknn_dp), dimension(:,:,:), optional, intent(inout) :: dnet_out_dinput
        real(qlknn_dp), dimension(:,:), allocatable :: df_vic_dinput

        integer(lli) :: n_rho, ii, idx, n_inputs, inp, leading_ITG, leading_TEM
        real(qlknn_dp), dimension(:), allocatable :: f_vic
        logical :: calcder
        character(len=512) :: line
        leading_TEM = leading_map(1, 2)
        leading_ITG = leading_map(1, 3)

        n_rho = size(input, 2)
        if (present(dnet_out_dinput)) then
          calcder = .true.
        else
          calcder = .false.
        endif

        allocate(f_vic(n_rho))
        if (calcder) then
          n_inputs = size(input, 1)
          allocate(df_vic_dinput(n_rho, n_inputs))
          write(line,*) 'size=', n_rho, 'x', n_inputs
          call get_f_vic(input, nets, qlknn_norms, f_vic, verbosity, df_vic_dinput)
        else
          call get_f_vic(input, nets, qlknn_norms, f_vic, verbosity)
        endif

        if (calcder) then
          do inp = 1, n_inputs
            !df_vic_dinput nRho x nInputs
            !net_result nRho x nOutp
            !f_vic nRho
            !dnet_out_dinput nOutp x nRho x nInp
            dnet_out_dinput(leading_ITG, :, inp) = df_vic_dinput(:, inp) * net_result(:, leading_ITG) + f_vic * dnet_out_dinput(leading_ITG,:,inp)
            do ii = 2, size(leading_map,1)
                idx = leading_map(ii, 3)
                if (idx == 0) then
                    cycle
                endif
                dnet_out_dinput(idx, :, inp) = df_vic_dinput(:, inp) * net_result(:, idx) + f_vic * dnet_out_dinput(idx,:,inp)
            enddo

            dnet_out_dinput(leading_TEM, :, inp) = df_vic_dinput(:, inp) * net_result(:, leading_TEM) + f_vic * dnet_out_dinput(leading_TEM,:,inp)
            do ii = 2, size(leading_map,1)
                idx = leading_map(ii, 2)
                if (idx == 0) then
                    cycle
                endif
                dnet_out_dinput(idx, :, inp) = df_vic_dinput(:, inp) * net_result(:, idx) + f_vic * dnet_out_dinput(idx,:,inp)
            enddo
          enddo
        endif

        net_result(:, leading_ITG) = f_vic * net_result(:, leading_ITG)
        do ii = 2, size(leading_map,1)
            idx = leading_map(ii, 3)
            if (idx == 0) then
                cycle
            endif
            net_result(:, idx) = f_vic * net_result(:, idx)
        end do

        net_result(:, leading_TEM) = f_vic * net_result(:, leading_TEM)
        do ii = 2, size(leading_map,1)
            idx = leading_map(ii, 2)
            if (idx == 0) then
                cycle
            endif
            net_result(:, idx) = f_vic * net_result(:, idx)
        end do

    end subroutine scale_with_victor

end module qlknn_victor_rule
