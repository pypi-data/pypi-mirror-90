! This file is part of QLKNN-fortran
! You should have received the QLKNN-fortran LICENSE in the root of the project
module qlknn_error_filter
#include "preprocessor.inc"
    use qlknn_types
    use qlknn_primitives

    ! This file should contain the acceptable variance thresholds for committee NNs
    ! Also provides the function required to evaluate and return pass/fail
    implicit none

contains

    subroutine determine_validity_with_eb(abs_limits, rel_limits, net_out, net_eb, validity, verbosity, mask)
        !! This program is meant to accept direct outputs from committee NNs, without additional processing
        !! First dimension is radial points
        !! Second dimension is the individual networks
        real(qlknn_dp), dimension(:), intent(in) :: abs_limits, rel_limits
        real(qlknn_dp), dimension(:,:), intent(in) :: net_out, net_eb
        integer(lli), intent(in) :: verbosity
        !logical(qlknn_bool), dimension(:), optional, intent(in) :: mask
        logical, dimension(:), optional, intent(in) :: mask

        !logical(qlknn_bool), dimension(:,:), intent(out) :: validity
        logical, dimension(:,:), intent(out) :: validity

        integer(lli) :: n_rho, ii
        !logical(qlknn_bool), dimension(:), allocatable :: rel_result
        logical, dimension(:), allocatable :: rel_result
        logical, dimension(:), allocatable :: is_nonzero

        ERRORSTOP(.not. all(shape(net_out) .eq. shape(net_eb)), 'NN outputs not same size as NN errors')
        ERRORSTOP(size(abs_limits) .ne. size(net_eb, 2), 'NN absolute limits not same size as NN vector')
        ERRORSTOP(size(rel_limits) .ne. size(net_eb, 2), 'NN relative limits not same size as NN vector')
        if (present(mask)) then
            ERRORSTOP(size(mask) .ne. size(net_eb, 2), 'NN mask not same size as NN error vector')
        endif

        if (verbosity >= 3) then
            write(*,*) 'Determining validity of NN on input space'
        endif

        n_rho = size(net_eb, 1)
        allocate(rel_result(size(net_eb,2)))
        allocate(is_nonzero(size(net_eb,2)))
        validity = .true.
        do ii = 1, n_rho
            rel_result = .true.
            call is_not_close(net_out(ii,:), 0._qlknn_dp, is_nonzero)
            where (is_nonzero) rel_result = net_eb(ii,:) <= (rel_limits * net_out(ii,:))
            validity(ii,:) = (net_eb(ii,:) <= abs_limits) .or. rel_result
            if (present(mask)) then
                where (mask .eqv. .false.) validity(ii,:) = .true.
            end if
        enddo
        deallocate(rel_result)
    end subroutine determine_validity_with_eb


    subroutine determine_validity_multiplied_networks(leading_map, validity, verbosity)
      !! Determines validity of post-multiplication results by applying
      !! logical .and. to validity of pre-multiplication networks

      integer(lli), dimension(:,:), intent(in) :: leading_map
      !! Map with 3 columns representing ETG, TEM, and ITG. The first row
      !! contains the indices of net_result containing the leading flux and
      !! the other rows containing non-leading flux indices padded with 0's
      !logical(qlknn_bool), dimension(:,:), intent(inout):: validity
      logical, dimension(:,:), intent(inout):: validity
      integer(lli), intent(in) :: verbosity
      !! Verbosity of this function
      integer(lli) :: ii, jj, idx, n_rho, leading_ITG, leading_TEM

      if (verbosity >= 3) then
        write(*,*) 'Determining validity of multiplied div results'
      endif

      leading_TEM = leading_map(1, 2)
      leading_ITG = leading_map(1, 3)
      n_rho = size(validity, 1)
      do ii = 2, size(leading_map,1)
        idx = leading_map(ii, 3)
        if (idx == 0) then
          cycle
        endif
        do jj = 1, n_rho
          validity(jj,idx) = validity(jj,idx) .and. validity(jj,leading_ITG)
        enddo
      enddo
      do ii = 2, size(leading_map,1)
        idx = leading_map(ii, 2)
        if (idx == 0) then
          cycle
        endif
        do jj = 1, n_rho
          validity(jj,idx) = validity(jj,idx) .and. validity(jj,leading_TEM)
        enddo
      enddo
    end subroutine determine_validity_multiplied_networks


    subroutine determine_validity_merged_modes(merge_map, validity, merged_validity, verbosity)
      !! Determine validity after merging columns of the same variable and same mode together
      !! by applying logical .and. to the individual validity flags

      integer(lli), dimension(:,:), intent(in) :: merge_map
      !! Map with the columns to be merged together. Each column of the map
      !! represents the column of merged_net_result the result will be stored
      !! in. Each index in the column, padded with 0's, will be merged together
      !logical(qlknn_bool), dimension(:,:), intent(in):: validity
      logical, dimension(:,:), intent(in):: validity
      !! The original to-be-merged data
      !logical(qlknn_bool), dimension(:,:), intent(out) :: merged_validity
      logical, dimension(:,:), intent(out) :: merged_validity
      !! The merged togethed data
      integer(lli), intent(in) :: verbosity
      integer(lli) :: n_rho, n_merged_out, ii, jj
      integer(lli), dimension(:), allocatable :: map

      if (verbosity >= 3) then
        write(*,*) 'Determining validity of merged modes'
      endif

      ERRORSTOP(.not. size(merge_map, 1) == size(merged_validity, 2),'Merge map n_rows different than merged result n_cols')

      n_rho = size(validity, 1)
      n_merged_out = size(merged_validity, 2)
      do ii = 1, n_rho
        do jj = 1, n_merged_out
          allocate(map(count(merge_map(jj, :) /= 0)))
          map = pack(merge_map(jj, :), merge_map(jj, :) /= 0)
          merged_validity(ii, jj) = all(validity(ii, map))
          deallocate(map)
        enddo
      enddo
    end subroutine determine_validity_merged_modes

end module qlknn_error_filter
