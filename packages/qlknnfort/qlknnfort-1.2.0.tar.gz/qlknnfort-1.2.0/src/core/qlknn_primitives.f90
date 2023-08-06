! This file is part of QLKNN-fortran
! You should have received the QLKNN-fortran LICENSE in the root of the project
module qlknn_primitives
#include "preprocessor.inc"
  use qlknn_types

  implicit none

  interface calc_length
     module procedure &
          calc_length_li, &
          calc_length_lli, &
          calc_length_mixed1, &
          calc_length_mixed2
  end interface

  interface is_not_close
     module procedure &
          double_2d_2d_is_not_close, &
          double_1d_1d_is_not_close, &
          double_1d_0d_is_not_close
  end interface
! Removing this seems to not matter. Dependent on linking? Keeping them around just to be sure
!#ifdef USE_MKL
  !include "mkl_vml.fi"
  !include "mkl_blas.fi"
!#endif

contains
  subroutine evaluate_network(input, net, output_1d, verbosityin, dnet_out1d_dinput)
    !! Evaluate a single feed-forward neural network. Assumes the output of the network is 1D.
    real(qlknn_dp), dimension(:,:), intent(in) :: input
    !! Input array fed to the network
    type(networktype), intent(in) :: net
    !! A 1D network to be evaluated
    integer(lli), optional, intent(in) :: verbosityin
    !! Verbosity of this function
    integer(lli):: verbosity
    real(qlknn_dp), dimension(:,:), allocatable :: output
    real(qlknn_dp), dimension(:), intent(out) :: output_1d
    !! Output of the network cast to a 1D array
    real(qlknn_dp), dimension(:,:), optional, intent(out) :: dnet_out1d_dinput
    !! Jacobian of the network cast to a 2D array

    integer(lli) :: rho, outp, inp, ii, lay, n_inputs_layer
    integer(lli) :: n_hidden_layers, n_hidden_nodes, n_inputs, n_outputs, n_rho
    real(qlknn_dp), dimension(:,:), allocatable :: inp_resc
    real(qlknn_dp), dimension(:,:,:), allocatable :: dnet_out_dinput, dthis_dprev, dlayers_dnorm
    real(qlknn_dp), dimension(:,:), allocatable :: dlayers_dnorm_tmp
    logical :: calcder
    character(len=200) :: error_msg
    real(qlknn_dp), dimension(:,:), allocatable :: outp_resc

    if(present(verbosityin)) then
      verbosity=verbosityin
    else
      verbosity = 0
    end if

    if(present(dnet_out1d_dinput)) then
      calcder = .true.
    else
      calcder = .false.
    end if

    n_hidden_layers = net%n_hidden_layers
    n_hidden_nodes = net%n_max_nodes
    n_inputs = size(net%weights_input, 2)
    n_outputs = size(net%weights_output, 1)
    n_rho = size(input, 2)
    write(error_msg, *) 'Expected 1D output from network, not', n_outputs, 'D'
    ERRORSTOP(n_outputs > 1, error_msg)
    ERRORSTOP(.NOT. size(output_1d) == n_rho, 'Passed output_1d has wrong shape!')
    if (.NOT. n_inputs == size(input, 1)) then
      write(stderr,*) 'Passed input has wrong number of inputs! size(input, 1)=', size(input, 1), ', needed n_inputs=', n_inputs
      ERRORSTOP(.true., '')
    end if

    allocate(inp_resc(n_inputs, n_rho))
    allocate(outp_resc(n_hidden_nodes, n_rho))
    allocate(output(n_outputs, n_rho))
    if (calcder) then
      allocate(dthis_dprev(n_hidden_nodes, n_rho, n_hidden_nodes))
      allocate(dlayers_dnorm(n_hidden_nodes, n_rho, n_inputs))
      allocate(dnet_out_dinput(n_outputs, n_rho, n_inputs))
#ifdef USE_MKL
      allocate(dlayers_dnorm_tmp(n_hidden_nodes, n_inputs))
#else
      allocate(dlayers_dnorm_tmp(0, 0))
#endif
    else
      allocate(dthis_dprev(0, 0, 0))
      allocate(dlayers_dnorm(0, 0, 0))
      allocate(dnet_out_dinput(0, 0, 0))
      allocate(dlayers_dnorm_tmp(0, 0))
    endif
    inp_resc = 0
    outp_resc = 0

    if (verbosity >= 4) then
      write(*, *) 'n_hidden_layers', n_hidden_layers
      write(*, *) 'n_hidden_nodes', n_hidden_nodes
      write(*, *) 'n_inputs', n_inputs
      write(*, *) 'n_outputs', n_outputs
      write(*, *) 'n_rho', n_rho
      write(*,*) 'input'
      do rho = 1, n_rho
        write(*,'(11(f7.2, 1X))') input(:, rho)
      end do
    end if
    if (verbosity >= 4) write(*,*) 'evaluating network'
    if (verbosity >= 4) write(*,*) 'inp_resc'
    do rho = 1, n_rho
      inp_resc(:,rho) = net%feature_prescale_factor * input(:,rho) + &
           net%feature_prescale_bias
      if (calcder) then
        do outp = 1, n_outputs
          dnet_out_dinput(outp, rho, :) = net%feature_prescale_factor
        end do
      end if
      if (verbosity >= 4) write(*,'(11(f7.2, 1X))') inp_resc(:, rho)
    end do

    !----------------------------
    ! Apply input layer
    if (calcder) then
      call evaluate_layer(inp_resc, net%weights_input, net%biases_input, net%hidden_activation(1), &
         outp_resc, verbosity, dlayers_dnorm)
    else
      call evaluate_layer(inp_resc, net%weights_input, net%biases_input, net%hidden_activation(1), &
         outp_resc, verbosity)
    endif
    if (verbosity >= 4) then
      write(*,*) 'input_layer post_tanh. (1:12, 1:12)'
      do ii = 1, 12
        write(*,'(12(f7.2, 1x))') outp_resc(ii, 1:12)
      end do
    end if

    !----------------------------
    ! Apply hidden layers
    do lay = 1, n_hidden_layers - 1
      n_inputs_layer = size(net%weights_hidden(lay)%weight_layer, 2)
      if (calcder) then
        call evaluate_layer(outp_resc(:n_inputs_layer, :), net%weights_hidden(lay)%weight_layer, net%biases_hidden(lay)%bias_layer, net%hidden_activation(lay+1), &
           outp_resc, verbosity, dthis_dprev)
        do rho = 1, n_rho
#ifdef USE_MKL
          ! MKL with GCC actually faster with explicit temp variable
          dlayers_dnorm_tmp = dlayers_dnorm(:, rho, :)
          call dgemm('N', 'N', n_hidden_nodes, n_inputs, n_hidden_nodes, 1._qlknn_dp, dthis_dprev(:, rho, :), n_hidden_nodes, &
             dlayers_dnorm_tmp, n_hidden_nodes, 0._qlknn_dp, dlayers_dnorm(:, rho, :), n_hidden_nodes)
#else
          call dgemm('N', 'N', n_hidden_nodes, n_inputs, n_hidden_nodes, 1._qlknn_dp, dthis_dprev(:, rho, :), n_hidden_nodes, &
             dlayers_dnorm(:, rho, :), n_hidden_nodes, 0._qlknn_dp, dlayers_dnorm(:, rho, :), n_hidden_nodes)
#endif
        end do
      else
        call evaluate_layer(outp_resc(:n_inputs_layer, :), net%weights_hidden(lay)%weight_layer, net%biases_hidden(lay)%bias_layer, net%hidden_activation(lay+1), &
           outp_resc, verbosity)
      endif
      if (verbosity >= 5) then
        write(*,*) 'layer ', lay, ' weights. (1:12, 1:12)'
        do ii = 1, 12
          write(*,'(12(f7.2, 1X))') net%weights_hidden(lay)%weight_layer(ii, 1:12)
        end do
        write(*,*) 'layer ', lay, ' biases. (1:12)'
        write(*,'(12(f7.2, 1X))') net%biases_hidden(lay)%bias_layer(1:12)
        write(*,*) 'layer ', lay, ' act.'
        write(*, '(A)') net%hidden_activation(lay)
      end if
      if (verbosity >= 4) then
        write(*,*) 'layer ', lay, ' post_act. (1:12, 1:12)'
        do ii = 1, 12
          write(*,'(12(f7.2, 1X))') outp_resc(ii, 1:12)
        end do
      end if
    end do

    !---------------------
    ! Apply output layer
    n_inputs_layer = size(net%weights_output, 2)
    if (calcder) then
      call evaluate_layer(outp_resc(:n_inputs_layer, :), net%weights_output, net%biases_output, 'none', &
         outp_resc, verbosity, dthis_dprev)
      do rho = 1, n_rho
#ifdef USE_MKL
        ! MKL with GCC actually faster with explicit temp variable
        dlayers_dnorm_tmp = dlayers_dnorm(:, rho, :)
        call dgemm('N', 'N', n_hidden_nodes, n_inputs, n_hidden_nodes, 1._qlknn_dp, dthis_dprev(:, rho, :), n_hidden_nodes, &
             dlayers_dnorm_tmp, n_hidden_nodes, 0._qlknn_dp, dlayers_dnorm(:, rho, :), n_hidden_nodes)
#else
        call dgemm('N', 'N', n_hidden_nodes, n_inputs, n_hidden_nodes, 1._qlknn_dp, dthis_dprev(:, rho, :), n_hidden_nodes, &
             dlayers_dnorm(:, rho, :), n_hidden_nodes, 0._qlknn_dp, dlayers_dnorm(:, rho, :), n_hidden_nodes)
#endif
      end do
    else
      call evaluate_layer(outp_resc(:n_inputs_layer, :), net%weights_output, net%biases_output, 'none', &
         outp_resc, verbosity)
    endif
    output = outp_resc(:n_outputs, :)
    if (verbosity >= 4) write(*,*) 'output_layer'
    if (verbosity >= 4) write(*,'(20(f7.2, 1x))') output

    !------------------------
    ! Denormalize output
    do rho = 1, n_rho
      output(:, rho) = dot_product(1/net%target_prescale_factor(:), output(:, rho) - &
           net%target_prescale_bias)
    end do
    if (calcder) then
      do rho = 1, n_rho
        do inp = 1, n_inputs
          call vdmul(n_outputs, 1/net%target_prescale_factor(:), dnet_out_dinput(:, rho, inp), dnet_out_dinput(:, rho, inp))
          call vdmul(n_outputs, dnet_out_dinput(:, rho, inp), dlayers_dnorm(:n_outputs, rho, inp),  dnet_out_dinput(:, rho, inp))
        end do
      end do
    end if
    if (verbosity >= 4) write(*,*) 'output_descaled'
    if (verbosity >= 4) write(*,'(20(f7.2, 1x))') output

    output_1d(:) = output(1, :)
    if (calcder) then
      dnet_out1d_dinput = dnet_out_dinput(1, :, :)
    end if
    !WRITE(*,'(*(F7.2 X))'), (output(1, ii), ii=1,n_rho)
    !deallocate(inp_resc)
    !deallocate(B_hidden)
    !deallocate(B_output)
    !deallocate(dthis_dprev)
    !deallocate(dlayers_dnorm_tmp)
    !deallocate(dnet_out_dinput_tmp)
    !deallocate(outp_resc)
  end subroutine evaluate_network

  subroutine evaluate_layers(input, weights, biases, activation, outp_resc, verbosityin, doutput_dnorm)
    !! Evaluate multiple (hidden) layers, layer shapes handled by ragged arrays
    real(qlknn_dp), dimension(:,:), intent(in) :: input
    !! Input array fed to the layers (n_in x n_rho)
    type(ragged_weights_array), dimension(:), intent(in) :: weights
    !! Weights of the layers (n_layers % (n_out x n_in))
    type(ragged_biases_array), dimension(:), intent(in) :: biases
    !! Biases of the layer (n_layers % (n_out))
    character(len=4), dimension(:), intent(in) :: activation
    !! Activation functions of the layer
    integer(lli), optional, intent(in) :: verbosityin
    !! Verbosity of this function
    integer(lli):: verbosity
    real(qlknn_dp), dimension(:,:), intent(out) :: outp_resc
    !! Output of the layers
    real(qlknn_dp), dimension(:,:,:), intent(inout), optional :: doutput_dnorm
    !! Already existing Jacobian to start with (n_out x n_rho x n_norm_in)

    integer(lli) rho, lay, ii
    integer(lli) :: n_layers, n_inputs, n_outputs, n_rho, n_inputs_layer, n_norm_inputs
    logical :: calcder
    real(qlknn_dp), dimension(:,:), allocatable :: output_prev
    real(qlknn_dp), dimension(:,:,:), allocatable :: dthis_dprev
#ifdef USE_MKL
    real(qlknn_dp), dimension(:,:), allocatable :: doutput_dnorm_tmp
#endif


    if(present(verbosityin)) then
      verbosity=verbosityin
    else
      verbosity = 0
    end if

    if (verbosity >= 3) then
      write(*,*) 'evaluate_layers'
    endif

    if(present(doutput_dnorm)) then
      calcder = .true.
    else
      calcder = .false.
    end if

    n_layers = size(weights)
    n_inputs = size(biases(1)%bias_layer)
    n_outputs = size(weights(n_layers)%weight_layer, 2)
    n_rho = size(input, 2)

    !write(*,*) 'n_layers=', n_layers, 'n_inputs=', n_inputs, 'n_outputs', n_outputs, 'n_rho=', n_rho

    allocate(output_prev(n_outputs, n_rho))
    if (calcder) then
      allocate(dthis_dprev(n_outputs, n_rho, n_outputs))
      n_norm_inputs = size(doutput_dnorm, 3)
    else
      allocate(dthis_dprev(0, 0, 0))
    endif

#ifdef USE_MKL
    if (calcder) then
      allocate(doutput_dnorm_tmp(n_outputs, n_outputs))
    else
      allocate(doutput_dnorm_tmp(0, 0))
    endif
#endif

    !----------------------------
    ! Apply hidden layers
    outp_resc = input
    do lay = 1, n_layers
      n_inputs_layer = size(weights(lay)%weight_layer, 2)
      if (calcder) then
        call evaluate_layer(outp_resc(:n_inputs_layer, :), weights(lay)%weight_layer, biases(lay)%bias_layer, activation(lay), &
           outp_resc, verbosity, dthis_dprev)
        if (verbosity >= 5) then
          write(*,'(A,I2,A,I2,A)') 'layer ', lay, ' dthis_dprev from evaluate_layer. (1:12, ', floor(real(n_rho)/2.), ', 1:12)'
          do ii = 1, 12
            write(*,'(12(f7.2, 1X))') dthis_dprev(ii, floor(real(n_rho)/2.), 1:12)
          end do
        endif
        do rho = 1, n_rho
#ifdef USE_MKL
          ! MKL with GCC actually faster with explicit temp variable
          doutput_dnorm_tmp = doutput_dnorm(:, rho, :)
          call dgemm('N', 'N', n_outputs, n_norm_inputs, n_outputs, 1._qlknn_dp, dthis_dprev(:, rho, :), n_outputs, &
             doutput_dnorm_tmp, n_outputs, 0._qlknn_dp, doutput_dnorm(:, rho, :), n_outputs)
#else
          call dgemm('N', 'N', n_outputs, n_norm_inputs, n_outputs, 1._qlknn_dp, dthis_dprev(:, rho, :), n_outputs, &
               doutput_dnorm(:, rho, :), n_outputs, 0._qlknn_dp, doutput_dnorm(:, rho, :), n_outputs)
#endif
        end do
        if (verbosity >= 5) then
          write(*,'(A,I2,A,I2,A,I2,A)') 'layer ', lay, ' doutput_dnorm from evaluate_layer. (1:12, ', floor(real(n_rho)/2.), ', 1:', n_norm_inputs, ')'
          do ii = 1, 12
            write(*,'(12(f7.2, 1X))') doutput_dnorm(ii, floor(real(n_rho)/2.), 1:n_norm_inputs)
          end do
        endif
      else
        call evaluate_layer(outp_resc(:n_inputs_layer, :), weights(lay)%weight_layer, biases(lay)%bias_layer, activation(lay), &
           outp_resc, verbosity)
      endif
      if (verbosity >= 5) then
        write(*,*) 'layer ', lay, ' weights. (1:12, 1:12)'
        do ii = 1, 12
          write(*,'(12(f7.2, 1X))') weights(lay)%weight_layer(ii, 1:12)
        end do
        write(*,*) 'layer ', lay, ' biases. (1:12)'
        write(*,'(12(f7.2, 1X))') biases(lay)%bias_layer(1:12)
        write(*,*) 'layer ', lay, ' act.'
        write(*, '(A)') activation(lay)
      end if
      if (verbosity >= 4) then
        write(*,*) 'layer ', lay, ' post_act. (1:12, 1:12)'
        do ii = 1, 12
          write(*,'(12(f7.2, 1X))') outp_resc(ii, 1:12)
        end do
      end if
    end do

  end subroutine evaluate_layers

  subroutine evaluate_layer(input, weights, biases, activation_func, output, verbosityin, doutput_dinput)
    !! Evaluate a single layer
    real(qlknn_dp), dimension(:,:), intent(in) :: input
    !! Input array fed to the layer (n_in x n_rho)
    real(qlknn_dp), dimension(:,:), intent(in) :: weights
    !! Weights of the layer (n_out x n_in)
    real(qlknn_dp), dimension(:), intent(in) :: biases
    !! Biases of the layer (n_out)
    character(len=4), intent(in) :: activation_func
    !! Activation function of the layer. 0: tanh, 1: linear
    integer(lli), optional, intent(in) :: verbosityin
    !! Verbosity of this function
    integer(lli):: verbosity
    real(qlknn_dp), dimension(:,:), intent(out) :: output
    !! Output of the layer
    real(qlknn_dp), dimension(:,:,:), optional, intent(out) :: doutput_dinput
    !! Jacobian of the layer

    integer(lli) rho, inp
    integer(lli) :: n_inputs, n_outputs, n_rho
    real(qlknn_dp), dimension(:,:), allocatable :: output_shaped
    logical :: calcder
    integer(lli), parameter :: n_plot_outputs_max = 24
    integer(lli) :: n_plot_outputs

    if(present(verbosityin)) then
      verbosity=verbosityin
    else
      verbosity = 0
    end if

    if(present(doutput_dinput)) then
      calcder = .true.
    else
      calcder = .false.
    end if
    n_inputs = size(weights, 2)
    n_outputs = size(weights, 1)
    n_rho = size(input, 2)

    allocate(output_shaped(n_outputs, n_rho))

    if (verbosity >= 3) then
      write(*, '(A,I2,A,I3,A,I3)') 'Evaluate layer with n_inputs=', n_inputs, ', n_outputs=', n_outputs, ', n_rho=', n_rho
      write(*, '(A,I4,A,I4,A)') 'Results in output_shaped(', size(output_shaped, 1), ',', size(output_shaped, 2), ')'
    endif

    if (size(output, 1) < n_outputs .or. size(output, 2) < n_rho) then
      write(*,'(A,I4,A,I4,A,I4,A,I4,A,I4,A,I4,A)') 'weights(', n_outputs, ', ', n_inputs, ') x input(',  size(input, 1), ', ', &
           n_rho, ') /= output(', size(output, 1), ',', size(output, 2), ')'
      ERRORSTOP(size(output, 1) < n_outputs, 'Passed output has wrong amount of rows!')
      ERRORSTOP(size(output, 2) < n_rho, 'Passed output has wrong amount of columns!')
    endif
    if (calcder) then
      if (size(doutput_dinput, 1) < n_outputs .or. size(doutput_dinput, 2) < n_rho .or. size(doutput_dinput, 3) < n_inputs) then
        write(*,'(A,I4,A,I4,A,I4,A,I4,A,I4,A,I4,A,I4,A)') 'for nrho=', n_rho, ' do output_tmp(', n_outputs, ', ', n_rho, ', ', n_inputs, &
             ') x doutput_dinput(', size(doutput_dinput, 1), ', ', size(doutput_dinput, 2), ', ', size(doutput_dinput, 3), ')'
        ERRORSTOP(size(doutput_dinput, 1) < n_outputs, 'Passed output Jacobian has wrong amount of rows!')
        ERRORSTOP(size(doutput_dinput, 2) < n_rho, 'Passed output Jacobian has wrong amount of columns!')
        ERRORSTOP(size(doutput_dinput, 3) < n_inputs, 'Passed output Jacobian has wrong amount of pages!')
      endif
    endif

    do rho = 1, n_rho
      output_shaped(:, rho) = biases
    end do
    ! dgemm(transa, transb, m, n, k, alpha, a, lda, b, ldb, beta, c, ldc)
    ! lda = m, ldb=k, ldc=m
    call dgemm('N', 'N', n_outputs, n_rho, n_inputs, 1._qlknn_dp, weights, n_outputs, input, &
          n_inputs, 1._qlknn_dp, &
          output_shaped, n_outputs)
    if (activation_func == 'tanh') then
      call vdtanh(n_rho * n_outputs, output_shaped(:, :), output_shaped) !Does not work without colons
    endif
    output(:n_outputs, :) = output_shaped
    if (n_outputs < size(output, 1)) output(n_outputs+1:, :) = 0

    if (calcder) then
      ! Df/Dx = f'(W * in_0 + b) .* W
      do inp = 1, n_inputs
        doutput_dinput(:, :, inp) = output !dactivation_dx == f'(W * in_0 + b)
      end do
      if (n_inputs < size(doutput_dinput, 3)) doutput_dinput(:, :, n_inputs+1:) = 0
      if (activation_func == 'tanh') then
        doutput_dinput(:n_outputs, :, :n_inputs) = 1 - doutput_dinput(:n_outputs, :, :n_inputs) ** 2
        do rho = 1, n_rho
          call matr_mult_elemwise(n_outputs * n_inputs, doutput_dinput(:n_outputs, rho, :n_inputs), weights, doutput_dinput(:n_outputs, rho, :n_inputs))
        end do
      else if (activation_func == 'none') then
        do rho = 1, n_rho
          doutput_dinput(:n_outputs, rho, :n_inputs) = weights
        end do
      endif
    endif

    if (verbosity >= 4) then
      if (n_outputs > n_plot_outputs_max) then
        n_plot_outputs = n_plot_outputs_max
        write(*, '(A,I4,A)') 'layer out(:, :', n_plot_outputs, ')'
      else
        n_plot_outputs = n_outputs
        write(*, '(A)') 'layer out(:,:)'
      endif
      do rho = 1, n_rho
        WRITE(*,'(*(F7.2, 1X))') output(:n_plot_outputs, rho)
      enddo
    endif
  end subroutine evaluate_layer

  subroutine impose_output_constraints(output, opts, verbosity, dnet_out_dinput, output_eb)
    !! Clip given network output array to [min, mix, margin]_output given in opts.
    !!
    !! Using a maximum of \( c_{max} \), minimum of \( c_{min} \), margin of \( c_{margin} \)
    !! and value \( y \), the value x will be clipped in place to
    !! $$ y_{min} = c_{min} + (1-c_{margin}) * abs(c_{min}) $$
    !! $$ y_{max} = c_{max} - (1-c_{margin}) * abs(c_{max}) $$
    real(qlknn_dp), dimension(:,:), intent(inout) :: output
    !! To-be clipped output (n_rho x n_outputs)
    type (qlknn_options), intent(in) :: opts
    !! Options containing [min, mix, margin]_output
    integer(lli), intent(in) :: verbosity
    !! Verbosity of this function
    real(qlknn_dp), dimension(:,:,:), optional, intent(inout) :: dnet_out_dinput
    !! Jacobian of clipped output
    real(qlknn_dp), dimension(:,:), optional, intent(inout) :: output_eb
    !! Error bounds of clipped output

    integer(lli) :: ii, rho, n_rho, n_inp, inp, n_outputs
    real(qlknn_dp), dimension(:), allocatable :: output_min, output_max
    logical :: calcder, calceb
    character(200) :: fmt_str

    n_rho = size(output, 1)
    n_outputs = size(output, 2)
    if(present(dnet_out_dinput)) then
      calcder = .true.
      n_inp = size(dnet_out_dinput, 3)
    else
      calcder = .false.
      n_inp = -1
    endif
    if (present(output_eb)) then
      calceb = .true.
      ERRORSTOP(.not. all(shape(output_eb) == shape(output)),'Clipped errorbound array should be the same shape as out array')
    else
      calceb = .false.
    endif

    ERRORSTOP(size(opts%min_output) /= n_outputs, 'min_output not same size as number of outputs')
    ERRORSTOP(size(opts%max_output) /= n_outputs, 'max_output not same size as number of outputs')
    ERRORSTOP(size(opts%margin_output) /= n_outputs, 'margin_output not same size as number of outputs')

    allocate(output_min(n_outputs))
    allocate(output_max(n_outputs))

    output_min = opts%min_output + (1-opts%margin_output) * abs(opts%min_output)
    output_max = opts%max_output - (1-opts%margin_output) * abs(opts%max_output)
    if (calcder) then
      do inp = 1, n_inp
        do rho = 1, n_rho
          where (output(rho, :) < output_min .AND. opts%constrain_outputs)
            dnet_out_dinput(:, rho, inp) = 0
          end where
        end do
      end do
      do inp = 1, n_inp
        do rho = 1, n_rho
          where (output(rho, :) > output_max .AND. opts%constrain_outputs)
            dnet_out_dinput(:, rho, inp) = 0
          end where
        end do
      end do
    endif
    do rho = 1, n_rho
      if (calceb) then
        where ((output(rho, :) < output_min) .AND. opts%constrain_outputs)
          output_eb(rho, :) = output_eb(rho, :) + abs(output_min - output(rho, :))
        elsewhere ((output(rho, :) > output_max) .AND. opts%constrain_outputs)
          output_eb(rho, :) = output_eb(rho, :) + abs(output(rho, :) - output_max)
        endwhere
      endif
      where ((output(rho, :) < output_min) .AND. opts%constrain_outputs)
        output(rho, :) = output_min
      elsewhere ((output(rho, :) > output_max) .AND. opts%constrain_outputs)
        output(rho, :) = output_max
      endwhere
    end do

    if (verbosity >= 3) then
      write(*,*) 'output clipped, n_rho=', n_rho
      do rho = 1, n_rho
        write(fmt_str, '(A, I0, A)') '(', n_outputs, '(F7.2, 1X))'
        WRITE(*, fmt_str) (output(rho, ii), ii=1,n_outputs)
      end do
    end if
  end subroutine impose_output_constraints

  subroutine impose_input_constraints(input, input_clipped, opts, verbosity, jacobian_clipmask)
    !! Clip given network input array to [min, mix, margin]_input given in opts.
    !!
    !! Using a maximum of \( c_{max} \), minimum of \( c_{min} \), margin of \( c_{margin} \)
    !! and value \( x \), the value x will be copied and clipped to
    !! $$ x_{min} = c_{min} + (1-c_{margin}) * abs(c_{min}) $$
    !! $$ x_{max} = c_{max} - (1-c_{margin}) * abs(c_{max}) $$
    real(qlknn_dp), dimension(:,:), intent(in) :: input
    !! Network input
    type (qlknn_options), intent(in) :: opts
    !! Options containing [min, mix, margin]_input
    integer(lli), intent(in) :: verbosity
    !! Verbosity of this function
    real(qlknn_dp), dimension(:,:), allocatable, intent(out) :: input_clipped
    !! Clipped network input array
    logical, dimension(:,:), allocatable, intent(out), optional :: jacobian_clipmask
    !! Mask containing true for input elements that were clipped

    integer(lli) :: ii, rho, n_rho, n_inp
    real(qlknn_dp), dimension(:), allocatable :: input_min, input_max
    logical :: calcder
    character(200) :: fmt_str

    n_rho = size(input, 2)
    n_inp = size(input, 1)
    allocate(input_min(n_inp))
    allocate(input_max(n_inp))

    if(present(jacobian_clipmask)) then
      calcder = .true.
      allocate(jacobian_clipmask(n_inp, n_rho))
    else
      calcder = .false.
    endif

    input_min = opts%min_input + (1-opts%margin_input) * abs(opts%min_input)
    input_max = opts%max_input - (1-opts%margin_input) * abs(opts%max_input)
#if (defined(__PGI) && __PGIC__ < 15) || (defined(__INTEL_COMPILER) && !defined(USE_MKL))
    allocate(input_clipped(lbound(input,1):ubound(input,1), lbound(input,2):ubound(input,2)))
#else
    allocate(input_clipped(n_inp, n_rho))
#endif
    input_clipped = input
    do rho = 1, n_rho
      where ((input_clipped(:, rho) < input_min) .AND. opts%constrain_inputs)
        input_clipped(:, rho) = input_min
      endwhere
      where ((input_clipped(:, rho) > input_max) .AND. opts%constrain_inputs)
        input_clipped(:, rho) = input_max
      endwhere
    end do
    if (calcder) then
      call is_not_close(input_clipped, input, jacobian_clipmask)
    endif

    if (verbosity >= 3) then
      write(*,*) 'input clipped, n_rho=', n_rho
      do rho = 1, n_rho
        write(fmt_str, '(A, I0, A)') '(', n_inp, '(F7.2, 1X))'
        WRITE(*, fmt_str) (input_clipped(ii, rho), ii=1,n_inp)
      end do
    end if
    end subroutine impose_input_constraints

  subroutine apply_stability_clipping(leading_map, net_result, verbosity)
      !! Clip in-place columns that are [ETG,TEM,ITG] stable to 0
      integer(lli), dimension(:,:), intent(in) :: leading_map
      !! Map with 3 columns representing ETG, TEM, and ITG. The first row
      !! contains the indices of net_result containing the leading flux and
      !! the other rows containing non-leading flux indices padded with 0's
      real(qlknn_dp), dimension(:,:), intent(inout):: net_result
      !! The leading flux stable points clipped to 0
      integer(lli), intent(in) :: verbosity
      !! Verbosity of this function
      integer(lli) :: ii, idx, leading_ETG, leading_TEM, leading_ITG

      leading_ETG = leading_map(1, 1)
      leading_TEM = leading_map(1, 2)
      leading_ITG = leading_map(1, 3)
      ! Clip leading fluxes to 0
      if (verbosity >= 3) then
        write(*,*) net_result(:, (/leading_ETG, leading_ITG, leading_TEM/)).le.0
      end if
      where (net_result(:, (/leading_ETG, leading_ITG, leading_TEM/)).le.0)
        net_result(:, (/leading_ETG, leading_ITG, leading_TEM/)) = 0
      endwhere
      do ii = 2, size(leading_map,1)
        idx = leading_map(ii, 3)
        if (idx == 0) then
          cycle
        endif
        where (net_result(:, leading_ITG).le.0)
          net_result(:, idx) = 0
        endwhere
      enddo
      do ii = 2, size(leading_map,1)
        idx = leading_map(ii, 2)
        if (idx == 0) then
          cycle
        endif
        where (net_result(:, leading_TEM).le.0)
          net_result(:, idx) = 0
        endwhere
      enddo
    end subroutine apply_stability_clipping

    subroutine impose_leading_flux_constraints(leading_map, net_result, verbosity, dnet_out_dnet_in, net_eb)
      !! Clip in-place leading-flux columns that are [ETG,TEM,ITG] stable to 0
      integer(lli), dimension(:,:), intent(in) :: leading_map
      !! Map with 3 columns representing ETG, TEM, and ITG. The first row
      !! contains the indices of net_result containing the leading flux
      real(qlknn_dp), dimension(:,:), intent(inout):: net_result
      !! The original data (in) and stable leading fluxes clipped to 0 (out)
      real(qlknn_dp), dimension(:,:,:), optional, intent(inout):: dnet_out_dnet_in
      !! The Jacobian of net_result to the input
      real(qlknn_dp), dimension(:,:), optional, intent(inout):: net_eb
      !! The error bounds of net_result. Will be set to 0 for stable points
      integer(lli), intent(in) :: verbosity
      !! Verbosity of this function
      integer(lli) :: n_inp, n_rho, inp, rho

      ! Clip leading fluxes to 0
      if (verbosity >= 3) then
        write(*,*) net_result(:, leading_map(1, :)).le.0
      end if
      where (net_result(:, leading_map(1, :)).le.0)
        net_result(:, leading_map(1, :)) = 0
      endwhere
      if (present(net_eb)) then
        where (net_eb(:, leading_map(1, :)).le.0)
          net_eb(:, leading_map(1, :)) = 0
        endwhere
      endif
      if(present(dnet_out_dnet_in)) then
        n_inp = size(dnet_out_dnet_in, 3)
        n_rho = size(dnet_out_dnet_in, 2)
        do rho = 1, n_rho
          do inp = 1, n_inp
            where (net_result(rho, leading_map(1, :)).le.0)
              dnet_out_dnet_in(leading_map(1, :), rho, inp) = 0
            endwhere
          enddo
        enddo
      endif
    end subroutine impose_leading_flux_constraints

    subroutine multiply_div_networks(leading_map, net_result, verbosity, dqlknn_out_dinput, net_eb)
      !! Multiply div networks with their leading flux in-place.

      !! The net_result (and dqlknn_out_dinput and net_eb) array(s) will be
      !! re-used to store the result. The result is stored in the columns where
      !! the div network was in before. For error bounds we assume the variables
      !! are uncorrelated and normal distributed with \( \mu_1, \sigma_1 \) and
      !! \( \mu_2, \sigma_2 \), resulting in a result \( \mu_r, \sigma_r \) of:
      !! $$ \mu_r = \mu_1 \times \mu_2 $$
      !! $$ \sigma_r = \sqrt{\mu_1^2 \sigma_2^2 + \mu_2^2 \sigma_1^2} $$
      integer(lli), dimension(:,:), intent(in) :: leading_map
      !! Map with 3 columns representing ETG, TEM, and ITG. The first row
      !! contains the indices of net_result containing the leading flux and
      !! the other rows containing non-leading flux indices padded with 0's
      real(qlknn_dp), dimension(:,:), intent(inout):: net_result
      !! The original data (in) and multiplied data (out)
      real(qlknn_dp), dimension(:,:,:), optional, intent(out) :: dqlknn_out_dinput
      !! The original Jacobian (in) and multiplied Jacobian (out)
      real(qlknn_dp), dimension(:,:), optional, intent(inout):: net_eb
      !! The original error bounds (in) and multiplied error bounds (out)
      real(qlknn_dp), dimension(:), allocatable :: temp_eb
      real(qlknn_dp), dimension(:,:,:), allocatable :: jaco_tmp
      integer(lli), intent(in) :: verbosity
      !! Verbosity of this function
      integer(lli) :: ii, idx, n_rho, n_inp, n_out, leading_ITG, leading_TEM
      logical :: calceb

      if (verbosity >= 3) then
        write(*,*) 'Multiplying div nets'
      endif

      leading_TEM = leading_map(1, 2)
      leading_ITG = leading_map(1, 3)
      n_rho = size(net_result, 1)
      if (present(dqlknn_out_dinput)) then
        n_inp = size(dqlknn_out_dinput, 3)
        n_out = size(dqlknn_out_dinput, 1)
        allocate(jaco_tmp(n_out, n_rho, n_inp))
        jaco_tmp = -99999
      else
        allocate(jaco_tmp(0, 0, 0))
        n_inp = -1
      endif
      if (present(net_eb)) then
        calceb = .true.
        ERRORSTOP(.not. all(shape(net_eb) == shape(net_result)),'Multiplied errorbound array should be the same shape as out array')
        allocate(temp_eb(n_rho))
      else
        calceb = .false.
        allocate(temp_eb(0))
      endif

      do ii = 2, size(leading_map,1)
        idx = leading_map(ii, 3)
        if (idx == 0) then
          cycle
        endif
        if (calceb) then
          CALL vdmul(n_rho, net_result(:, idx)**2, net_eb(:, leading_ITG)**2, temp_eb)
          CALL vdmul(n_rho, net_eb(:, idx)**2, net_result(:, leading_ITG)**2, net_eb(:, idx))
          net_eb(:, idx) = sqrt(net_eb(:, idx) + temp_eb)
        endif
        if (present(dqlknn_out_dinput)) then
          CALL matr_vec_mult_elemwise(n_rho * n_inp, dqlknn_out_dinput(idx, :, :), net_result(:, leading_ITG), dqlknn_out_dinput(idx, :, :))
          CALL matr_vec_mult_elemwise(n_rho * n_inp, dqlknn_out_dinput(leading_ITG, :, :), net_result(:, idx), jaco_tmp(idx, :, :))
          dqlknn_out_dinput(idx, :, :) = dqlknn_out_dinput(idx, :, :) + jaco_tmp(idx, :, :)
        endif
        CALL vdmul(n_rho, net_result(:, idx), net_result(:, leading_ITG), net_result(:, idx))
      enddo
      do ii = 2, size(leading_map,1)
        idx = leading_map(ii, 2)
        if (idx == 0) then
          cycle
        endif
        if (present(dqlknn_out_dinput)) then
          CALL matr_vec_mult_elemwise(n_rho * n_inp, dqlknn_out_dinput(idx, :, :), net_result(:, leading_TEM), dqlknn_out_dinput(idx, :, :))
          CALL matr_vec_mult_elemwise(n_rho * n_inp, dqlknn_out_dinput(leading_TEM, :, :), net_result(:, idx), jaco_tmp(idx, :, :))
          dqlknn_out_dinput(idx, :, :) = dqlknn_out_dinput(idx, :, :) + jaco_tmp(idx, :, :)
        endif
        CALL vdmul(n_rho, net_result(:, idx), net_result(:, leading_TEM), net_result(:, idx))
      enddo
    end subroutine multiply_div_networks

    subroutine merge_modes(merge_map, net_result, merged_net_result, verbosity, dqlknn_out_dinput, dqlknn_out_merged_dinput, net_eb, merged_net_eb)
      !! Sum columns of the same variable and same mode together

      !! For error bounds we assume the variables are uncorrolated and normal distributed
      !! with \( \mu_i, \sigma_i \) resulting in a result \( \mu_r, \sigma_r \) of:
      !! $$ \mu_r = \sum_i \mu_i $$
      !! $$ \sigma_r = \sqrt{\left(\sum_i \sigma_i^2\right)} $$

      integer(lli), dimension(:,:), intent(in) :: merge_map
      !! Map with the columns to be merged together. Each column of the map
      !! represents the column of merged_net_result the result will be stored
      !! in. Each index in the column, padded with 0's, will be merged together
      real(qlknn_dp), dimension(:,:), intent(in):: net_result
      !! The original to-be-merged data
      real(qlknn_dp), dimension(:,:), intent(out) :: merged_net_result
      !! The merged togethed data
      integer(lli), intent(in) :: verbosity
      real(qlknn_dp), dimension(:,:,:), optional, intent(in) :: dqlknn_out_dinput
      !! The jacobian of the to-be-merged data
      real(qlknn_dp), dimension(:,:,:), optional, intent(inout) :: dqlknn_out_merged_dinput
      !! The merged together jacobians of the data
      real(qlknn_dp), dimension(:,:), optional, intent(in) :: net_eb
      !! The error bounds of the original to-be-merged data
      real(qlknn_dp), dimension(:,:), optional, intent(out) :: merged_net_eb
      !! The merged together error bounds of the data
      integer(lli) :: n_rho, n_inputs, n_outputs, n_merged_out, ii, jj
      integer(lli), dimension(:), allocatable :: map
      logical :: calcder, calceb
      !character(len=200) :: error_msg

      if (verbosity >= 3) then
        write(*,*) 'Merging modes'
      endif

      ERRORSTOP(.not. size(merge_map, 1) == size(merged_net_result, 2),'Merge map different amount of rows than amount of merged result columns')
      if (present(merged_net_eb)) then
        calceb = .true.
        ERRORSTOP(.not. all(shape(merged_net_result) == shape(merged_net_eb)),'Merged committee errorbound array should be the same shape as out array')
        ERRORSTOP(.not. all(shape(net_result) == shape(net_eb)),'Net result given to merge modes should be same shape as error bound array')
      else
        calceb = .false.
      endif

      n_rho = size(net_result, 1)
      n_merged_out = size(merged_net_result, 2)
      if (present(dqlknn_out_dinput)) then
        if (present(dqlknn_out_merged_dinput)) then
          calcder = .true.
          n_outputs = size(dqlknn_out_dinput, 1)
          n_inputs = size(dqlknn_out_dinput, 3)
          !allocate(dqlknn_out_merged_dinput(n_outputs, n_rho, n_inputs))
        else
          ERRORSTOP(.true., 'Also provide dqlknn_out_merged_dinput if dqlknn_out_dinput is provided')
          calcder = .false.
        endif
      else
        calcder = .false.
      endif
      do ii = 1, n_rho
        do jj = 1, n_merged_out
          allocate(map(count(merge_map(jj, :) /= 0)))
          map = pack(merge_map(jj, :), merge_map(jj, :) /= 0)
          merged_net_result(ii, jj) = sum(net_result(ii, map))
          if (calceb) then
            merged_net_eb(ii, jj) = sqrt(sum(net_eb(ii, map)**2))
          endif
          if (calcder) then
            dqlknn_out_merged_dinput(jj, ii, :) = sum(dqlknn_out_dinput(map, ii, :), 1)
          endif
          deallocate(map)
        enddo
      enddo
    end subroutine merge_modes

    subroutine merge_committee(net_result, n_members, merged_net_result, merged_net_eb, verbosity, dqlknn_out_dinput, dqlknn_out_merged_dinput)
      !! Combine predictions of committee members

      !! We assume the committee results are stored in consecutive columns and
      !! each variable has the same amount of members per committee. We use the
      !! uncorrected sample standard deviation as error bound, e.g. for samples
      !! \( x_i \) with mean
      !! $$ \mu = \frac{1}{N} \sum^N_{i=1} x_i $$
      !! We get error bound \(  \text{EB} \)
      !! $$ \text{EB} = \sigma = \sqrt{\left[ \frac{1}{N} \sum^N_{i=1} \left( x_i - \mu \right)^2 \right]} $$
      real(qlknn_dp), dimension(:,:), intent(in):: net_result
      !! The separate member predictions
      integer(lli), intent(in) :: n_members
      !! The number of members per committee
      real(qlknn_dp), dimension(:,:), intent(out) :: merged_net_result
      !! The prediction of the full committee
      real(qlknn_dp), dimension(:,:), intent(out) :: merged_net_eb
      !! The error bound on the prediction of the full committee
      integer(lli), intent(in) :: verbosity
      !! Verbosity of this function
      real(qlknn_dp), dimension(:,:,:), optional, intent(in) :: dqlknn_out_dinput
      !! The Jacobian of the separate member predictions
      real(qlknn_dp), dimension(:,:,:), optional, intent(inout) :: dqlknn_out_merged_dinput
      !! The Jacobian of the full committee
      integer(lli) :: n_rho, n_inputs, n_outputs, ii, jj, start, n_post_committee_outputs
      logical :: calcder
      !character(len=200) :: error_msg

      if (verbosity >= 3) then
        write(*,*) 'Merging committee members'
      endif

      ERRORSTOP(.not. all(shape(merged_net_result) == shape(merged_net_eb)), 'Merged committee errorbound array should be the same size as out array')

      n_outputs = int(size(net_result, 2), li)
      n_post_committee_outputs = int(size(merged_net_result, 2), li)
      ERRORSTOP(mod(n_outputs, n_members) /= 0, 'Nets cannot be equally split between committee members')
      ERRORSTOP(n_outputs / n_members /= n_post_committee_outputs, 'Outputs divided by members not the same as passed output array')
      n_rho = size(net_result, 1)
      if (present(dqlknn_out_dinput)) then
        if (present(dqlknn_out_merged_dinput)) then
          calcder = .true.
          ERRORSTOP(n_outputs /= size(dqlknn_out_dinput, 1), 'Jacobian array has different shape from output array!')
          n_inputs = size(dqlknn_out_dinput, 3)
          !allocate(dqlknn_out_merged_dinput(n_outputs, n_rho, n_inputs))
        else
          ERRORSTOP(.true., 'Also provide dqlknn_out_merged_dinput if dqlknn_out_dinput is provided')
          calcder = .false.
        endif
      else
        calcder = .false.
      endif
      ! Assume committee members are next to each other in the arrays
      do ii = 1, n_rho
        do jj = 1, n_post_committee_outputs
          start = n_members * (jj - 1) + 1
          !print *, jj, start, start + n_members - 1
          !print *, net_result(ii, start:start + n_members - 1)
          merged_net_result(ii, jj) = sum(net_result(ii, start:start + n_members - 1)) / n_members
          ! Assuming merged_net_result contains the mean
          ! Use uncorrected sample standard deviation as error bound
          merged_net_eb(ii, jj) = sqrt(sum((net_result(ii, start:start + n_members - 1) - merged_net_result(ii, jj))**2)/n_members)
          if (calcder) then
            dqlknn_out_merged_dinput(jj, ii, :) = sum(dqlknn_out_dinput(start:start + n_members - 1, ii, :)) / n_members
          endif
        enddo
      enddo
    end subroutine merge_committee

    subroutine matr_mult_elemwise(n, a, b, y)
      !! Multiply two matrices element wise
      integer(lli), intent(in) :: n
      real(qlknn_dp), dimension(:,:), intent(in) :: a, b
      real(qlknn_dp), dimension(:,:), intent(out) :: y
      integer(lli) :: i, n_vec
      ERRORSTOP((size(a, 1) /= size(b, 1)) .or. (size(a, 2) /= size(b, 2)), 'a and b different shapes')
      n_vec = n / size(a, 2)
      do i = 1, size(a, 2)
        call vdmul(n_vec, a(:, i), b(:, i), y(:, i))
      end do
    end subroutine matr_mult_elemwise

    subroutine matr_vec_mult_elemwise(n, a, b, y)
      !! Multiply a vector with a matrix element wise
      integer(lli), intent(in) :: n
      real(qlknn_dp), dimension(:,:), intent(in) :: a
      real(qlknn_dp), dimension(:), intent(in) :: b
      real(qlknn_dp), dimension(:,:), intent(out) :: y
      integer(lli) :: i, n_vec
      ERRORSTOP((size(a, 1) /= size(b)), 'a and b different shapes')
      n_vec = n / size(a, 2)
      do i = 1, size(a, 2)
        call vdmul(n_vec, a(:, i), b(:), y(:, i))
      end do
    end subroutine matr_vec_mult_elemwise
#ifndef USE_MKL
    subroutine vdmul(n, a, b, y)
      !! Multiply a vector with a vector element wise
      !!
      !! Drop-in replacement for Intel's https://software.intel.com/en-us/mkl-developer-reference-fortran-v-mul
      integer(lli), intent(in) :: n
      real(qlknn_dp), dimension(:), intent(in) :: a, b
      real(qlknn_dp), dimension(:), intent(out) :: y
      if (size(a) /= n) then
        write(stderr,*) 'Warning! Argument a in vdmul has different size than n'
      endif
      y = a * b
    end subroutine vdmul

    subroutine dgemm(transa, transb, m, n, k, alpha, a, lda, b, ldb, beta, c, ldc)
      !! Perform \( A B + C \) in-place
      !!
      !! Drop-in replacement for Intel's https://software.intel.com/en-us/mkl-developer-reference-fortran-gemm
      character(len=1), intent(in) :: transa, transb
      integer(lli), intent(in) :: m, n, k, lda, ldb, ldc
      real(qlknn_dp), intent(in) :: alpha, beta
      real(qlknn_dp), dimension(:,:), intent(in) :: a, b
      real(qlknn_dp), dimension(:,:), intent(inout) :: c
      real(qlknn_dp), dimension(:,:), allocatable :: c_tmp
      if ((size(a, 1) /= m) .or. (size(a, 2) /= k)) then
        write(stderr,*) 'Warning! Argument a in dgemm is not m x k'
        write(stderr,'(A,2I3,A,I3,A,I3,A)') 'shape(a) =', shape(a), ', m=', m, ', k=', k, &
             ', callsig(transa, transb, m, n, k, alpha, a, lda, b, ldb, beta, c, ldc)'
      endif
      if (size(a, 1) /= lda) then
        write(stderr,*) 'Warning! Argument a in dgemm does not have lda rows'
        write(stderr,'(A,I3,A,I3)') 'rows(a) =', size(a, 1), ', lda=', lda
      endif
      if ((size(b, 1) /= k) .or. (size(b, 2) /= n)) then
        write(stderr,*) 'Warning! Argument b in dgemm is not k x n'
        write(stderr,'(A,2I3,A,I3,A,I3,A)') 'shape(b) =', shape(b), ', k=', k, ', n=', n, &
             ', callsig(transa, transb, m, n, k, alpha, a, lda, b, ldb, beta, c, ldc)'
      endif
      if (size(b, 1) /= ldb) then
        write(stderr,*) 'Warning! Argument b in dgemm does not have ldb rows'
        write(stderr,'(A,I3,A,I3)') 'rows(b) =', size(b, 1), ', ldb=', ldb
      endif
      if ((size(c, 1) /= m) .or. (size(c, 2) /= n)) then
        write(stderr,*) 'Warning! Argument c in dgemm is not m x n'
        write(stderr,'(A,2I3,A,I3,A,I3,A)') 'shape(c) =', shape(c), ', m=', m, ', n=', n, &
             ', callsig(transa, transb, m, n, k, alpha, a, lda, b, ldb, beta, c, ldc)'
      endif
      if (size(c, 1) /= ldc) then
        write(stderr,*) 'Warning! Argument c in dgemm does not have ldc rows'
        write(stderr,'(A,I3,A,I3)') 'rows(c) =', size(c, 1), ', ldc=', ldc
      endif
      ERRORSTOP((transa /= 'N') .or. (transb /= 'N'), 'trans /= N not implemented yet')
      allocate(c_tmp(size(c,1), size(c,2)))
      c_tmp = alpha * matmul(a, b)
      c = c_tmp + beta * c
      deallocate(c_tmp)
    end subroutine

    subroutine vdtanh(n, a, y)
      !! Calculate the tanh on each vector element
      !!
      !! Drop-in replacement for Intel's https://software.intel.com/en-us/mkl-developer-reference-fortran-v-tanh
      integer(lli), intent(in) :: n
      real(qlknn_dp), dimension(:,:), intent(in) :: a
      real(qlknn_dp), dimension(:,:), intent(out) :: y
      if (size(a) /= n) then
        write(stderr,*) 'Warning! Argument a in vdtanh has different size than n'
      endif
      y = tanh(a)
    end subroutine
#endif
    subroutine relu(n, a, y)
      integer(lli), intent(in) :: n
      real(qlknn_dp), dimension(:), intent(in) :: a
      real(qlknn_dp), dimension(:), intent(out) :: y
      if (size(a) /= n) then
        write(stderr,*) 'Warning! Argument a in relu has different size than n'
      endif
      y = a
      where (a < 0)
        y = 0
      endwhere
    end subroutine

    subroutine calc_length_lli(start, end, step, length)
      !! Calculate the length of a job array
      integer(lli), intent(in) :: start, end, step
      integer(lli), intent(out) :: length
      real(qlknn_dp) :: length_rl
      length_rl = (end - start - 0) / real(step, qlknn_dp) + 1
      length = int(floor(length_rl), li)
    end subroutine

    subroutine calc_length_li(start, end, step, length)
      !! Calculate the length of a job array
      integer(li), intent(in) :: start, end, step
      integer(li), intent(out) :: length
      real(qlknn_dp) :: length_rl
      length_rl = (end - start - 0) / real(step, qlknn_dp) + 1
      length = int(floor(length_rl), li)
    end subroutine

    subroutine calc_length_mixed1(start, end, step, length)
      !! Calculate the length of a job array
      integer(li), intent(in) :: start, step
      integer(lli), intent(in) :: end
      integer(li), intent(out) :: length
      real(qlknn_dp) :: length_rl
      length_rl = (end - start - 0) / real(step, qlknn_dp) + 1
      length = int(floor(length_rl), li)
    end subroutine

    subroutine calc_length_mixed2(start, end, step, length)
      !! Calculate the length of a job array
      integer(li), intent(in) :: start
      integer(lli), intent(in) :: step, end
      integer(li), intent(out) :: length
      real(qlknn_dp) :: length_rl
      length_rl = (end - start - 0) / real(step, qlknn_dp) + 1
      length = int(floor(length_rl), li)
    end subroutine

    subroutine double_1d_0d_is_not_close(arr1, arr2, is_not_close, boundin)
      real(qlknn_dp), dimension(:), intent(in) :: arr1
      real(qlknn_dp), intent(in) :: arr2
      real(qlknn_dp), intent(in), optional :: boundin
      logical, dimension(:), intent(out) :: is_not_close

      real(qlknn_dp) :: bound

      if (present(boundin)) then
        bound = boundin
      else
        bound = 10*epsilon(arr2)
      endif
      is_not_close = arr1 < arr2 - bound .or. arr1 > arr2 + bound
    end subroutine double_1d_0d_is_not_close


    subroutine double_1d_1d_is_not_close(arr1, arr2, is_not_close, boundin)
      real(qlknn_dp), dimension(:), intent(in) :: arr1
      real(qlknn_dp), dimension(:), intent(in) :: arr2
      real(qlknn_dp), intent(in), optional :: boundin
      logical, dimension(:), intent(out) :: is_not_close

      real(qlknn_dp) :: bound

      if (present(boundin)) then
        bound = boundin
      else
        bound = 10*epsilon(arr2)
      endif
      is_not_close = arr1 < arr2 - bound .or. arr1 > arr2 + bound
    end subroutine double_1d_1d_is_not_close

    subroutine double_2d_2d_is_not_close(arr1, arr2, is_not_close, boundin)
      real(qlknn_dp), dimension(:,:), intent(in) :: arr1
      real(qlknn_dp), dimension(:,:), intent(in) :: arr2
      real(qlknn_dp), intent(in), optional :: boundin
      logical, dimension(:,:), intent(out) :: is_not_close

      real(qlknn_dp) :: bound

      if (present(boundin)) then
        bound = boundin
      else
        bound = 10*epsilon(arr2)
      endif
      is_not_close = arr1 < arr2 - bound .or. arr1 > arr2 + bound
    end subroutine double_2d_2d_is_not_close
  end module qlknn_primitives
