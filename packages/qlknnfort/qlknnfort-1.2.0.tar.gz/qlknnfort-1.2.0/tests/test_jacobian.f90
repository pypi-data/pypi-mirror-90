! This file is part of QLKNN-fortran
! You should have received the QLKNN-fortran LICENSE in the root of the project
module test_jacobian
#include "../src/core/preprocessor.inc"
  use qlknn_types

  real(qlknn_dp), dimension(5), parameter :: max_err_hyper = (/ 1e-5, 1e-6, 1e-8, 1., 1e-1 /)
  real(qlknn_dp), parameter :: stepsize_hyper = 1e-3

  real(qlknn_dp), dimension(6), parameter :: max_err_hornnet = (/ 1e-10, 1e-9, 1e-5, 2e-5 , 1e-1, 1e-2/)
  real(qlknn_dp), parameter :: stepsize_hornnet = 1e-4

contains
  function calc_error(dprofa,dprofn,prof0) result(error)
    use qlknn_primitives, only: is_not_close
    !! generic function to calculate calculate relative numerical vs analytical error in Jacobian
    !! err = ||numerical-analytical||/||analytical||
    real(qlknn_dp), dimension(:), intent(in):: dprofa, dprofn, prof0
    real(qlknn_dp), dimension(size(dprofa)) :: error
    real(qlknn_dp) :: near_zero

    real(qlknn_dp), dimension(:), allocatable :: difference

    logical, dimension(:), allocatable :: is_zeron
    logical, dimension(:), allocatable :: is_zeroa
    logical, dimension(:), allocatable :: is_zero0

    allocate(is_zeroa(size(dprofa, 1)))
    allocate(is_zeron(size(dprofn, 1)))
    allocate(is_zero0(size(prof0, 1)))

    near_zero = 10*epsilon(error)
    call is_not_close(dprofa, 0._qlknn_dp, is_zeroa)
    is_zeroa = .not. is_zeroa

    call is_not_close(dprofn, 0._qlknn_dp, is_zeron)
    is_zeron = .not. is_zeron

    call is_not_close(prof0, 0._qlknn_dp, is_zero0)
    is_zero0 = .not. is_zero0

    if ((all(is_zeron)) .and. (all(is_zeroa))) then
      write(stderr, *) 'Warning! No dependence'
      error = 0 !zero error because no dependence
    elseif (all(is_zero0)) then
      ERRORSTOP(.true., 'Normalization profile is 0.')
    elseif (all(is_zeron) .and.  .not. all(is_zeroa)) then
      write(stderr, *)'Numerical profile is zero while analytical profile is non-zero!'
    elseif (.not. all(is_zeron) .and.  all(is_zeroa)) then
      ERRORSTOP(.true., 'Analytical profile is zero while numerical profile is non-zero!')
    elseif ((norm2(dprofn)/norm2(prof0) < near_zero) .or. &
            (norm2(dprofa)/norm2(prof0) < near_zero) .or. &
            (norm2(dprofn) < near_zero) .or. &
            (norm2(dprofa) < near_zero)) then
      error = 0 ! zero because relative change is too small (but nonzero)
    else
      ! Workaround temp array for PGI compiler bug
      ! https://forums.developer.nvidia.com/t/fortran-expression-in-norm2-not-allowed/136385
      allocate(difference(size(dprofa, 1)))
      difference = dprofa - dprofn
      error = difference / (prof0 + epsilon(error))
    endif
  end function calc_error

  subroutine jacobian_hyper_multi(casenum, input, stepsize, net, err_out, verbosityin)
    use qlknn_evaluate_nets
    use qlknn_disk_io
    implicit none

    integer, intent(in) :: casenum
    real(qlknn_dp), dimension(:,:), intent(in):: input
    real(qlknn_dp), intent(in) :: stepsize
    integer(lli), intent(in) :: net
    integer(lli), intent(in), optional :: verbosityin
    real(qlknn_dp), dimension(:,:,:), allocatable, intent(out) :: err_out

    integer(lli) :: verbosity, n_rho=24, n_input_layer_out, rho, n_hidden_layers, n_hidden_layers_out
    integer :: inp, outp, n_out, n_in
    type (qlknn_options) :: opts
    type (qlknn_normpars) :: qlknn_norms
    real(qlknn_dp), dimension(:,:), allocatable :: input_min_half, input_plus_half
    !real(qlknn_dp) :: start, finish
    real(qlknn_dp), dimension(:,:), allocatable :: qlknn_out
    real(qlknn_dp), dimension(:,:), allocatable :: qlknn_out_min_half, qlknn_out_plus_half
    real(qlknn_dp), dimension(:,:), allocatable :: qlknn_out_tmp, qlknn_input_layer_out, qlknn_input_layer_out_min_half, qlknn_input_layer_out_plus_half
    real(qlknn_dp), dimension(:,:,:), allocatable :: dqlknn_input_layer_out_dinput
    real(qlknn_dp), dimension(:,:), allocatable :: qlknn_hidden_out, qlknn_hidden_out_plus, qlknn_hidden_out_min
    real(qlknn_dp), dimension(:,:), allocatable :: qlknn_out_min_half_tmp, qlknn_out_plus_half_tmp
    real(qlknn_dp), dimension(:,:,:), allocatable :: dqlknn_out_dinput
    real(qlknn_dp), dimension(:,:,:), allocatable :: dqlknn_out_dinput_tmp
    real(qlknn_dp), dimension(:,:), allocatable :: dinput_numerical, dout_numerical
    real(qlknn_dp), dimension(:), allocatable :: err, dana, dnum
    logical, dimension(:), allocatable :: err_okay
    !character(len=2) :: testcase_str
    !integer(lli) :: num_args, inp, n_inputs, outp, n_out, rho, testcase, n_in
    !integer(li) :: stat, length
    !real(qlknn_dp) :: stepsize, err, max_err
    !real(qlknn_dp), dimension(:,:), allocatable :: din

    if(present(verbosityin)) then
       verbosity=verbosityin
    else
       verbosity = 0
    end if

    n_in = size(input, 1)

    call default_qlknn_hyper_options(opts)

    ! Set default options
    opts%constrain_inputs = .false.
    opts%constrain_outputs = .false.
    opts%force_evaluate_all = .true.

    ! Set specific options, and allocated arrays that change shape between tests
    ! Each test should have at least:
    ! n_out: The amount of outputs of the outermost function
    ! n_in: The amount of inputs of the innermost function
    ! n_rho: The amount of radial points
    ! This defines the following quantities:
    ! dqlknn_out_dinput: The Jacobian of the outermost function with respect
    !    to the innermost input (n_out, n_rho, n_in)
    ! qlknn_out: The output of the outermost function
    ! qlknn_out_min_half: The output of the outermost function with input
    !    modified by -step
    ! qlknn_out_min_half: The output of the outermost function with input
    !    modified by +step
    select case (casenum)
    case(1)
      ! Test a single (input) layer
      opts%merge_modes = .false.
      n_out = size(nets%nets(1)%biases_input)
      ! First layer only depends on the first 9 dimensions, fill rest with 0s and
      ! define temporary variable to store the layers Jacobian in
      allocate(dqlknn_out_dinput(n_out, n_rho, n_in))
      allocate(err_out(n_out, n_rho, 9))
      allocate(dqlknn_out_dinput_tmp(n_out, n_rho, 9))
      dqlknn_out_dinput = 0
      ! The Jacobians of the layers are transposed as compared to the final
      ! outputted Jacobians. Allocate temporary arrays to save this transposed array
      allocate(qlknn_out_tmp(n_out, n_rho))
      allocate(qlknn_out_min_half_tmp(n_out, n_rho))
      allocate(qlknn_out_plus_half_tmp(n_out, n_rho))
    case(2)
      ! Test input layer + a single hidden layer
      n_out = size(nets%nets(1)%biases_hidden(1)%bias_layer)
      n_input_layer_out = size(nets%nets(1)%biases_input)
      ! First layer only depends on the first 9 dimensions, fill rest with 0s and
      ! define temporary variable to store the layers Jacobian in
      allocate(dqlknn_out_dinput(n_out, n_rho, 9))
      allocate(err_out(n_out, n_rho, 9))
      allocate(dqlknn_out_dinput_tmp(n_out, n_rho, n_input_layer_out))
      dqlknn_out_dinput = 0
      ! The Jacobians of the layers are transposed as compared to the final
      ! outputted Jacobians. Allocate temporary arrays to save this transposed array
      allocate(qlknn_out_tmp(n_out, n_rho))
      allocate(qlknn_out_min_half_tmp(n_out, n_rho))
      allocate(qlknn_out_plus_half_tmp(n_out, n_rho))
      ! We need to manually calculate the final combined Jacobian of the two layers
      allocate(dqlknn_input_layer_out_dinput(n_input_layer_out, n_rho, 9))
      allocate(qlknn_input_layer_out(n_input_layer_out, n_rho))
      allocate(qlknn_input_layer_out_plus_half(n_input_layer_out, n_rho))
      allocate(qlknn_input_layer_out_min_half(n_input_layer_out, n_rho))
      opts%merge_modes = .false.
    case(3)
      ! Test evaluate_net
      n_out = 1
      opts%merge_modes = .false.
      allocate(dqlknn_out_dinput(n_out, n_rho, 9))
      allocate(err_out(n_out, n_rho, 9))
    case(4)
      ! Test input layer + a all hidden layers with evaluate_nets
      n_hidden_layers = size(nets%nets(net)%biases_hidden)
      n_out = size(nets%nets(net)%biases_hidden(n_hidden_layers)%bias_layer)
      n_input_layer_out = size(nets%nets(net)%biases_input)
      ! First layer only depends on the first 9 dimensions, fill rest with 0s and
      ! define temporary variable to store the layers Jacobian in
      allocate(dqlknn_out_dinput(n_out, n_rho, 9))
      allocate(err_out(n_out, n_rho, 9))
      allocate(dqlknn_out_dinput_tmp(n_out, n_rho, n_input_layer_out))
      dqlknn_out_dinput = 0
      ! The Jacobians of the layers are transposed as compared to the final
      ! outputted Jacobians. Allocate temporary arrays to save this transposed array
      allocate(qlknn_out_tmp(n_out, n_rho))
      allocate(qlknn_out_min_half_tmp(n_out, n_rho))
      allocate(qlknn_out_plus_half_tmp(n_out, n_rho))
      ! We need to manually calculate the final combined Jacobian of the two layers
      allocate(dqlknn_input_layer_out_dinput(n_input_layer_out, n_rho, 9))
      allocate(qlknn_input_layer_out(n_input_layer_out, n_rho))
      allocate(qlknn_input_layer_out_plus_half(n_input_layer_out, n_rho))
      allocate(qlknn_input_layer_out_min_half(n_input_layer_out, n_rho))
      opts%merge_modes = .false.
    case(5)
      ! Test input layer + a all hidden layers with evaluate_nets
      n_hidden_layers = size(nets%nets(net)%biases_hidden)
      n_out = size(nets%nets(net)%biases_output)
      n_input_layer_out = size(nets%nets(net)%biases_input)
      n_hidden_layers_out = size(nets%nets(net)%biases_hidden(n_hidden_layers)%bias_layer)
      ! First layer only depends on the first 9 dimensions, fill rest with 0s and
      ! define temporary variable to store the layers Jacobian in
      allocate(dqlknn_out_dinput(n_out, n_rho, 9))
      allocate(err_out(n_out, n_rho, 9))
      allocate(dqlknn_out_dinput_tmp(n_out, n_rho, n_hidden_layers_out))
      dqlknn_out_dinput = 0
      !

      allocate(qlknn_hidden_out(n_hidden_layers_out, n_rho))
      allocate(qlknn_hidden_out_plus(n_hidden_layers_out, n_rho))
      allocate(qlknn_hidden_out_min(n_hidden_layers_out, n_rho))
      ! The Jacobians of the layers are transposed as compared to the final
      ! outputted Jacobians. Allocate temporary arrays to save this transposed array
      allocate(qlknn_out_tmp(n_out, n_rho))
      allocate(qlknn_out_min_half_tmp(n_out, n_rho))
      allocate(qlknn_out_plus_half_tmp(n_out, n_rho))
      ! We need to manually calculate the final combined Jacobian of the two layers
      allocate(dqlknn_input_layer_out_dinput(n_input_layer_out, n_rho, 9))
      allocate(qlknn_input_layer_out(n_input_layer_out, n_rho))
      allocate(qlknn_input_layer_out_plus_half(n_input_layer_out, n_rho))
      allocate(qlknn_input_layer_out_min_half(n_input_layer_out, n_rho))
      opts%merge_modes = .false.
    case default
      ERRORSTOP(.true., 'Given case number not implemented')
    endselect

    ! To store the results of evaluating at x, x-h and x+h
    allocate(qlknn_out(n_rho, n_out))
    allocate(qlknn_out_min_half(n_rho, n_out))
    allocate(qlknn_out_plus_half(n_rho, n_out))

    ! To store  x-h and x+h
    allocate(input_min_half(n_in, n_rho))
    allocate(input_plus_half(n_in, n_rho))

    ! To store profile data of the error
    allocate(err(n_rho))
    allocate(dana(n_rho))
    allocate(dnum(n_rho))
    allocate(err_okay(n_rho))

    ! To store f(x+h) - f(x-h)
    allocate(dout_numerical(n_rho, n_out))
    ! To store x+h - x - h (aka 2h)
    allocate(dinput_numerical(n_in, n_rho))

    ! Variables for Victor rule
    allocate(qlknn_norms%a1(n_rho))
    qlknn_norms%A1 = 2.
    qlknn_norms%R0 = 3.
    qlknn_norms%a = 1.

    do inp = 1, n_in - 2
      input_min_half(:, :) = input
      input_plus_half(:, :) = input
      input_min_half(inp, :) = input(inp, :) - 0.5 * stepsize
      input_plus_half(inp, :) = input(inp, :) + 0.5 * stepsize
      select case (casenum)
      case(1)
        call evaluate_layer(input(1:9, :), &
             nets%nets(net)%weights_input, nets%nets(1)%biases_input, 'tanh', &
             qlknn_out_tmp, verbosity - 1, dqlknn_out_dinput_tmp)
        call evaluate_layer(input_plus_half(1:9, :), &
             nets%nets(net)%weights_input, nets%nets(1)%biases_input, 'tanh', &
             qlknn_out_plus_half_tmp, verbosity - 1)
        call evaluate_layer(input_min_half(1:9, :), &
             nets%nets(net)%weights_input, nets%nets(1)%biases_input, 'tanh', &
             qlknn_out_min_half_tmp, verbosity - 1)

        qlknn_out_plus_half = transpose(qlknn_out_plus_half_tmp)
        qlknn_out_min_half = transpose(qlknn_out_min_half_tmp)
        qlknn_out = transpose(qlknn_out_tmp)
        dqlknn_out_dinput(:, :, 1:9) = dqlknn_out_dinput_tmp
      case(2)
        call evaluate_layer(input(1:9, :), &
             nets%nets(net)%weights_input, nets%nets(net)%biases_input, 'tanh', &
             qlknn_input_layer_out, verbosity - 1, dqlknn_input_layer_out_dinput)
        call evaluate_layer(input_plus_half(1:9, :), &
             nets%nets(net)%weights_input, nets%nets(net)%biases_input, 'tanh', &
             qlknn_input_layer_out_plus_half, verbosity - 1)
        call evaluate_layer(input_min_half(1:9, :), &
             nets%nets(net)%weights_input, nets%nets(net)%biases_input, 'tanh', &
             qlknn_input_layer_out_min_half, verbosity - 1)

        call evaluate_layer(qlknn_input_layer_out, &
             nets%nets(net)%weights_hidden(1)%weight_layer, nets%nets(net)%biases_hidden(1)%bias_layer, 'tanh', &
             qlknn_out_tmp, verbosity - 1, dqlknn_out_dinput_tmp)
        call evaluate_layer(qlknn_input_layer_out_plus_half, &
             nets%nets(net)%weights_hidden(1)%weight_layer, nets%nets(net)%biases_hidden(1)%bias_layer, 'tanh', &
             qlknn_out_plus_half_tmp, verbosity - 1)
        call evaluate_layer(qlknn_input_layer_out_min_half, &
             nets%nets(net)%weights_hidden(1)%weight_layer, nets%nets(net)%biases_hidden(1)%bias_layer, 'tanh', &
             qlknn_out_min_half_tmp, verbosity - 1)

        ! Copied from evaulate_net on 98b641de6e72a601c699e22c1234c8b1090bd85c
        do rho = 1, n_rho
          call dgemm('N', 'N', int(n_out, lli), 9_lli, n_input_layer_out, 1._qlknn_dp, dqlknn_out_dinput_tmp(:, rho, :), n_input_layer_out, &
               dqlknn_input_layer_out_dinput(:, rho, :), int(n_out, lli), 0._qlknn_dp,  dqlknn_out_dinput(:, rho, :), int(n_out, lli))
        enddo

        qlknn_out_plus_half = transpose(qlknn_out_plus_half_tmp)
        qlknn_out_min_half = transpose(qlknn_out_min_half_tmp)
        qlknn_out = transpose(qlknn_out_tmp)
      case(3)
        call evaluate_network(input(1:9, :), &
             nets%nets(1), qlknn_out(:, 1), &
             verbosity - 1, dqlknn_out_dinput(1, :, :))
        call evaluate_network(input_plus_half(1:9, :), &
             nets%nets(1), qlknn_out_plus_half(:, 1), &
             verbosity - 1)
        call evaluate_network(input_min_half(1:9, :), &
             nets%nets(1), qlknn_out_min_half(:, 1), &
             verbosity - 1)
      case(4)
        call evaluate_layer(input(1:9, :), &
             nets%nets(net)%weights_input, nets%nets(net)%biases_input, 'tanh', &
             qlknn_input_layer_out, verbosity - 1, dqlknn_input_layer_out_dinput)
        call evaluate_layer(input_plus_half(1:9, :), &
             nets%nets(net)%weights_input, nets%nets(net)%biases_input, 'tanh', &
             qlknn_input_layer_out_plus_half, verbosity - 1)
        call evaluate_layer(input_min_half(1:9, :), &
             nets%nets(net)%weights_input, nets%nets(net)%biases_input, 'tanh', &
             qlknn_input_layer_out_min_half, verbosity - 1)

        call evaluate_layers(qlknn_input_layer_out, &
             nets%nets(net)%weights_hidden, nets%nets(net)%biases_hidden, nets%nets(net)%hidden_activation, &
             qlknn_out_tmp, verbosity - 1, dqlknn_input_layer_out_dinput)
        call evaluate_layers(qlknn_input_layer_out_plus_half, &
             nets%nets(net)%weights_hidden, nets%nets(net)%biases_hidden, nets%nets(net)%hidden_activation, &
             qlknn_out_plus_half_tmp, verbosity - 1)
        call evaluate_layers(qlknn_input_layer_out_min_half, &
             nets%nets(net)%weights_hidden, nets%nets(net)%biases_hidden, nets%nets(net)%hidden_activation, &
             qlknn_out_min_half_tmp, verbosity - 1)

        dqlknn_out_dinput = dqlknn_input_layer_out_dinput
        qlknn_out_plus_half = transpose(qlknn_out_plus_half_tmp)
        qlknn_out_min_half = transpose(qlknn_out_min_half_tmp)
        qlknn_out = transpose(qlknn_out_tmp)
      case(5)
        call evaluate_layer(input(1:9, :), &
             nets%nets(net)%weights_input, nets%nets(net)%biases_input, 'tanh', &
             qlknn_input_layer_out, verbosity - 1, dqlknn_input_layer_out_dinput)
        call evaluate_layer(input_plus_half(1:9, :), &
             nets%nets(net)%weights_input, nets%nets(net)%biases_input, 'tanh', &
             qlknn_input_layer_out_plus_half, verbosity - 1)
        call evaluate_layer(input_min_half(1:9, :), &
             nets%nets(net)%weights_input, nets%nets(net)%biases_input, 'tanh', &
             qlknn_input_layer_out_min_half, verbosity - 1)

        call evaluate_layers(qlknn_input_layer_out, &
             nets%nets(net)%weights_hidden, nets%nets(net)%biases_hidden, nets%nets(net)%hidden_activation, &
             qlknn_hidden_out, verbosity - 1, dqlknn_input_layer_out_dinput)
        call evaluate_layers(qlknn_input_layer_out_plus_half, &
             nets%nets(net)%weights_hidden, nets%nets(net)%biases_hidden, nets%nets(net)%hidden_activation, &
             qlknn_hidden_out_plus, verbosity - 1)
        call evaluate_layers(qlknn_input_layer_out_min_half, &
             nets%nets(net)%weights_hidden, nets%nets(net)%biases_hidden, nets%nets(net)%hidden_activation, &
             qlknn_hidden_out_min, verbosity - 1)

        call evaluate_layer(qlknn_hidden_out, &
             nets%nets(net)%weights_output, nets%nets(net)%biases_output, 'tanh', &
             qlknn_out_tmp, verbosity - 1, dqlknn_out_dinput_tmp)
        call evaluate_layer(qlknn_hidden_out_plus, &
             nets%nets(net)%weights_output, nets%nets(net)%biases_output, 'tanh', &
             qlknn_out_plus_half_tmp, verbosity - 1)
        call evaluate_layer(qlknn_hidden_out_min, &
             nets%nets(net)%weights_output, nets%nets(net)%biases_output, 'tanh', &
             qlknn_out_min_half_tmp, verbosity - 1)

        do rho = 1, n_rho
          call dgemm('N', 'N', int(n_out, lli), 9_lli, n_hidden_layers_out, 1._qlknn_dp, dqlknn_out_dinput_tmp(:, rho, :), int(n_out, lli), &
               dqlknn_input_layer_out_dinput(:, rho, :), int(n_hidden_layers_out, lli), 0._qlknn_dp,  dqlknn_out_dinput(:, rho, :), int(n_out, lli))
        enddo

        qlknn_out_plus_half = transpose(qlknn_out_plus_half_tmp)
        qlknn_out_min_half = transpose(qlknn_out_min_half_tmp)
      end select

      dout_numerical = qlknn_out_plus_half - qlknn_out_min_half
      dinput_numerical = input_plus_half - input_min_half

      do outp = 1, n_out
        dana = dqlknn_out_dinput(outp, :, inp) * dinput_numerical(inp, :)
        dnum = qlknn_out_plus_half(:, outp) - qlknn_out_min_half(:, outp)
        if (verbosity >= 1) then
          write(*, *)
          write(*, *)'---------------------------'
          write(*, '(A,I4,A,I4)') 'outp=', outp, ', inp=', inp
          write(*, *)'---------------------------'
          write(*, *)'danalytical'
          write(*, *) dana
          write(*, *)
          write(*, *)'dnumerical'
          write(*, *) dnum
          write(*, *)
          write(*, *)'danalytical - dnumerical'
          write(*, *) dana - dnum
          write(*, *)
        endif

        err(:) = calc_error(dana, dnum, qlknn_out_min_half(:, outp))

        if (verbosity >= 1) then
          write(*, *)'err(:)'
          write(*, *) err(:)
        endif
        err_out(outp, :, inp) = err
      enddo
    enddo
  end subroutine jacobian_hyper_multi

  subroutine jacobian_hornnet_multi(casenum, input, stepsize, err_out, verbosityin)
    use qlknn_evaluate_nets
    use qlknn_disk_io
    implicit none

    integer, intent(in) :: casenum
    real(qlknn_dp), dimension(:,:), intent(in):: input
    real(qlknn_dp), intent(in) :: stepsize
    integer(lli), intent(in), optional :: verbosityin
    real(qlknn_dp), dimension(:,:,:), allocatable, intent(out) :: err_out

    !integer(lli), dimension(8) :: etg_map = (/ 1, 2, 4, 5,  6,  7,  8,  9 /)
    integer(lli), dimension(8) :: itg_map = (/ 1, 3, 4, 5,  6,  7,  8,  9 /)
    integer(lli), dimension(8) :: tem_map = (/ 1, 2, 4, 5,  6,  7,  8,  9 /)

    !integer(lli), dimension(1) :: c_etg_outp_map = (/ 1 /)
    !integer(lli), dimension(7) :: c_itg_outp_map = (/ 2, 4, 6, 8, 10, 12, 14 /)
    !integer(lli), dimension(7) :: c_tem_outp_map = (/ 3, 5, 7, 9, 11, 13, 15 /)

    integer(lli) :: verbosity, n_in, n_out, n_rho=24, outp, inp
    type (qlknn_options) :: opts
    type (qlknn_normpars) :: qlknn_norms
    real(qlknn_dp), dimension(:,:), allocatable :: input_min_half, input_plus_half
    real(qlknn_dp), dimension(:,:), allocatable :: qlknn_out
    real(qlknn_dp), dimension(:,:), allocatable :: qlknn_out_min_half, qlknn_out_plus_half
    real(qlknn_dp), dimension(:,:), allocatable :: qlknn_out_min_half_tmp, qlknn_out_plus_half_tmp
    real(qlknn_dp), dimension(:,:), allocatable :: hornnet_constants
    real(qlknn_dp), dimension(:,:), allocatable :: hornnet_constants_min_half, hornnet_constants_plus_half
    real(qlknn_dp), dimension(:,:), allocatable :: qlknn_out_tmp
    real(qlknn_dp), dimension(:,:,:), allocatable :: dqlknn_out_dinput
    real(qlknn_dp), dimension(:,:,:), allocatable :: dqlknn_out_dinput_tmp
    real(qlknn_dp), dimension(:,:,:), allocatable :: dflux_dhornnet_constants, dhornnet_constants_dinput, dflux_dinput
    real(qlknn_dp), dimension(:,:), allocatable :: dinput_numerical, dout_numerical
    real(qlknn_dp), dimension(:), allocatable :: err, dana, dnum
    logical, dimension(:), allocatable :: err_okay

    if(present(verbosityin)) then
       verbosity=verbosityin
    else
       verbosity = 0
    end if

    n_in = size(input, 1)

    call default_qlknn_hornnet_options(opts)

    ! Set default options
    opts%constrain_inputs = .false.
    opts%constrain_outputs = .false.
    opts%force_evaluate_all = .true.
    opts%apply_victor_rule = .false.

    ! Set specific options, and allocated arrays that change shape between tests
    ! Each test should have at least:
    ! n_out: The amount of outputs of the outermost function
    ! n_in: The amount of inputs of the innermost function
    ! n_rho: The amount of radial points
    ! This defines the following quantities:
    ! dqlknn_out_dinput: The Jacobian of the outermost function with respect
    !    to the innermost input (n_out, n_rho, n_in)
    ! qlknn_out: The output of the outermost function
    ! qlknn_out_min_half: The output of the outermost function with input
    !    modified by -step
    ! qlknn_out_min_half: The output of the outermost function with input
    !    modified by +step
    select case (casenum)
    case(1)
      ! Test a single (input) layer
      n_out = size(blocks%input_blocks(2)%biases_input)
      ! Common layer only depends on the first 8 dimensions, fill rest with 0s and
      ! define temporary variable to store the layers Jacobian in
      allocate(dqlknn_out_dinput(n_out, n_rho, n_in))
      allocate(err_out(n_out, n_rho, 9))
      allocate(dqlknn_out_dinput_tmp(n_out, n_rho, 8))
      dqlknn_out_dinput = 0
      ! The Jacobians of the layers are transposed as compared to the final
      ! outputted Jacobians. Allocate temporary arrays to save this transposed array
      allocate(qlknn_out_tmp(n_out, n_rho))
      allocate(qlknn_out_min_half_tmp(n_out, n_rho))
      allocate(qlknn_out_plus_half_tmp(n_out, n_rho))
    case(2)
      ! Test getting the c* constants
      n_out = 15
      allocate(dqlknn_out_dinput(n_out, n_rho, n_in))
      allocate(err_out(n_out, n_rho, n_in))
    case(3)
      ! Test getting the non-pfe fluxes
      opts%merge_modes = .false.
      n_out = 7
      allocate(hornnet_constants(n_rho, 15))
      allocate(hornnet_constants_min_half(n_rho, 15))
      allocate(hornnet_constants_plus_half(n_rho, 15))

      allocate(dhornnet_constants_dinput(15, n_rho, n_in))
      allocate(dflux_dhornnet_constants(n_out, n_rho, 15))
      allocate(dflux_dinput(n_out, n_rho, n_in))

      allocate(dqlknn_out_dinput(n_out, n_rho, n_in))
      allocate(err_out(n_out, n_rho, n_in))
    case(4)
      ! Test getting the c_pfe constants on the threshold dim
      n_out = 15
      allocate(dqlknn_out_dinput(n_out, n_rho, n_in))
      allocate(err_out(n_out, n_rho, n_in))
    case(5)
      ! Test getting the pfe fluxes
      opts%merge_modes = .false.
      n_out = 7
      allocate(hornnet_constants(n_rho, 15))
      allocate(hornnet_constants_min_half(n_rho, 15))
      allocate(hornnet_constants_plus_half(n_rho, 15))

      allocate(dhornnet_constants_dinput(15, n_rho, n_in))
      allocate(dflux_dhornnet_constants(n_out, n_rho, 15))
      allocate(dflux_dinput(n_out, n_rho, n_in))

      allocate(dqlknn_out_dinput(n_out, n_rho, n_in))
      allocate(err_out(n_out, n_rho, n_in))
    case(6)
      ! Test getting merged fluxes
      opts%merge_modes = .true.
      n_out = 4
      allocate(hornnet_constants(n_rho, 15))
      allocate(hornnet_constants_min_half(n_rho, 15))
      allocate(hornnet_constants_plus_half(n_rho, 15))

      allocate(dhornnet_constants_dinput(15, n_rho, n_in))
      allocate(dflux_dhornnet_constants(n_out, n_rho, 15))
      allocate(dflux_dinput(n_out, n_rho, n_in))

      allocate(dqlknn_out_dinput(n_out, n_rho, n_in))
      allocate(err_out(n_out, n_rho, n_in))
    case default
      ERRORSTOP(.true., 'Given case number not implemented')
    endselect

    ! To store the results of evaluating at x, x-h and x+h
    allocate(qlknn_out(n_rho, n_out))
    allocate(qlknn_out_min_half(n_rho, n_out))
    allocate(qlknn_out_plus_half(n_rho, n_out))
    allocate(dout_numerical(n_rho, n_out))

    ! To store  x-h and x+h
    allocate(input_min_half(n_in, n_rho))
    allocate(input_plus_half(n_in, n_rho))
    allocate(dinput_numerical(n_in, n_rho))

    ! To store profile data of the error
    allocate(err(n_rho))
    allocate(dana(n_rho))
    allocate(dnum(n_rho))
    allocate(err_okay(n_rho))

    ! Variables for Victor rule
    allocate(qlknn_norms%a1(n_rho))
    qlknn_norms%A1 = 2.
    qlknn_norms%R0 = 3.
    qlknn_norms%a = 1.

    select case (casenum)
    case(2,3,4,5,6)
      err_out(:, :, 10:11) = 0.
    endselect
    do inp = 1, n_in - 2
      input_min_half(:, :) = input
      input_plus_half(:, :) = input
      input_min_half(inp, :) = input(inp, :) - stepsize
      input_plus_half(inp, :) = input(inp, :) + stepsize
      select case (casenum)
      case(1)
        if (.not. any(itg_map == inp)) then
          err_out(:, :, inp) = 0.
          cycle
        endif
        call evaluate_layer(input(itg_map, :), &
             blocks%input_blocks(2)%weights_input, blocks%input_blocks(2)%biases_input, 'tanh', &
             qlknn_out_tmp, verbosity - 1, dqlknn_out_dinput_tmp)
        call evaluate_layer(input_plus_half(itg_map, :), &
             blocks%input_blocks(2)%weights_input, blocks%input_blocks(2)%biases_input, 'tanh', &
             qlknn_out_plus_half_tmp, verbosity - 1)
        call evaluate_layer(input_min_half(itg_map, :), &
             blocks%input_blocks(2)%weights_input, blocks%input_blocks(2)%biases_input, 'tanh', &
             qlknn_out_min_half_tmp, verbosity - 1)
        qlknn_out_plus_half = transpose(qlknn_out_plus_half_tmp)
        qlknn_out_min_half = transpose(qlknn_out_min_half_tmp)
        qlknn_out = transpose(qlknn_out_tmp)
        dqlknn_out_dinput(:, :, itg_map) = dqlknn_out_dinput_tmp
      case(2)
        call evaluate_hornnet_constants(input, blocks, qlknn_out, verbosity - 1, opts, qlknn_norms, dqlknn_out_dinput)
        call evaluate_hornnet_constants(input_min_half, blocks, qlknn_out_min_half, verbosity - 1, opts, qlknn_norms)
        call evaluate_hornnet_constants(input_plus_half, blocks, qlknn_out_plus_half, verbosity - 1, opts, qlknn_norms)
      case(3)
        call evaluate_hornnet_constants(input, blocks, hornnet_constants, verbosity - 1, opts, qlknn_norms, dhornnet_constants_dinput)
        call evaluate_hornnet_constants(input_min_half, blocks, hornnet_constants_min_half, verbosity - 1, opts, qlknn_norms)
        call evaluate_hornnet_constants(input_plus_half, blocks, hornnet_constants_plus_half, verbosity - 1, opts, qlknn_norms)

        call hornnet_flux_from_constants(input, blocks, hornnet_constants, qlknn_out, verbosity - 1, opts, qlknn_norms, dflux_dhornnet_constants, dflux_dinput)
        call hornnet_flux_from_constants(input_min_half, blocks, hornnet_constants_min_half, qlknn_out_min_half, verbosity - 1, opts, qlknn_norms)
        call hornnet_flux_from_constants(input_plus_half, blocks, hornnet_constants_plus_half, qlknn_out_plus_half, verbosity - 1, opts, qlknn_norms)

        call hornnet_multiply_jacobians(dhornnet_constants_dinput, dflux_dhornnet_constants, dflux_dinput, dqlknn_out_dinput)
      case(4)
        call evaluate_hornnet_constants(input, blocks, qlknn_out, verbosity - 1, opts, qlknn_norms, dqlknn_out_dinput)
        call evaluate_hornnet_constants(input_min_half, blocks, qlknn_out_min_half, verbosity - 1, opts, qlknn_norms)
        call evaluate_hornnet_constants(input_plus_half, blocks, qlknn_out_plus_half, verbosity - 1, opts, qlknn_norms)
      case(5)
        call evaluate_hornnet_constants(input, blocks, hornnet_constants, verbosity - 1, opts, qlknn_norms, dhornnet_constants_dinput)
        call evaluate_hornnet_constants(input_min_half, blocks, hornnet_constants_min_half, verbosity - 1, opts, qlknn_norms)
        call evaluate_hornnet_constants(input_plus_half, blocks, hornnet_constants_plus_half, verbosity - 1, opts, qlknn_norms)

        call hornnet_flux_from_constants(input, blocks, hornnet_constants, qlknn_out, verbosity - 1, opts, qlknn_norms, dflux_dhornnet_constants, dflux_dinput)
        call hornnet_flux_from_constants(input_min_half, blocks, hornnet_constants_min_half, qlknn_out_min_half, verbosity - 1, opts, qlknn_norms)
        call hornnet_flux_from_constants(input_plus_half, blocks, hornnet_constants_plus_half, qlknn_out_plus_half, verbosity - 1, opts, qlknn_norms)

        call hornnet_multiply_jacobians(dhornnet_constants_dinput, dflux_dhornnet_constants, dflux_dinput, dqlknn_out_dinput)
      case(6)
        call evaluate_hornnet_constants(input, blocks, hornnet_constants, verbosity - 1, opts, qlknn_norms, dhornnet_constants_dinput)
        call evaluate_hornnet_constants(input_min_half, blocks, hornnet_constants_min_half, verbosity - 1, opts, qlknn_norms)
        call evaluate_hornnet_constants(input_plus_half, blocks, hornnet_constants_plus_half, verbosity - 1, opts, qlknn_norms)

        call hornnet_flux_from_constants(input, blocks, hornnet_constants, qlknn_out, verbosity - 1, opts, qlknn_norms, dflux_dhornnet_constants, dflux_dinput)
        call hornnet_flux_from_constants(input_min_half, blocks, hornnet_constants_min_half, qlknn_out_min_half, verbosity - 1, opts, qlknn_norms)
        call hornnet_flux_from_constants(input_plus_half, blocks, hornnet_constants_plus_half, qlknn_out_plus_half, verbosity - 1, opts, qlknn_norms)

        call hornnet_multiply_jacobians(dhornnet_constants_dinput, dflux_dhornnet_constants, dflux_dinput, dqlknn_out_dinput)
      end select

      dout_numerical = qlknn_out_plus_half - qlknn_out_min_half
      dinput_numerical = input_plus_half - input_min_half

      do outp = 1, n_out
        select case (casenum)
        case(2)
          ! Some outputs (the bendy guys) are hard to check. Ignore for now
          if (any(outp == (/ 5, 8 /))) then
            err_out(outp, :, inp) = 0.
            cycle
          endif
          ! Skip the threshold dimension for c_pfe. Test those separately
          if (outp == 14 .and. .not. any(inp == itg_map) .or. &
              outp == 15 .and. .not. any(inp == tem_map)) then
            err_out(outp, :, inp) = 0.
            cycle
          endif
        case(3)
          ! Skip pfe
          if (any(outp == (/ 6, 7 /))) then
            err_out(outp, :, inp) = 0.
            cycle
          endif
        case(4)
          ! Check the threshold dimension for c_pfe.
          if (.not. (outp == 14 .and. .not. any(inp == itg_map)) .and. &
              .not. (outp == 15 .and. .not. any(inp == tem_map))) then
            err_out(outp, :, inp) = 0.
            cycle
          endif
        case(5)
          ! Check pfe
          if (.not. any(outp == (/ 6, 7 /))) then
            err_out(outp, :, inp) = 0.
            cycle
          endif
        endselect
        dana = dqlknn_out_dinput(outp, :, inp) * dinput_numerical(inp, :)
        dnum = qlknn_out_plus_half(:, outp) - qlknn_out_min_half(:, outp)
        if (verbosity >= 1) then
          write(*, *)
          write(*, *)'---------------------------'
          write(*, '(A,I4,A,I4)') 'outp=', outp, ', inp=', inp
          write(*, *)'---------------------------'
          write(*, *)'danalytical'
          write(*, *) dana
          write(*, *)
          write(*, *)'dnumerical'
          write(*, *) dnum
          write(*, *)
          write(*, *)'danalytical - dnumerical'
          write(*, *) dana - dnum
          write(*, *)
        endif

        err(:) = calc_error(dana, dnum, qlknn_out_min_half(:, outp))

        if (verbosity >= 1) then
          write(*, *)'err(:)'
          write(*, *) err(:)
          write(*, *)'max(abs(err(:)))', maxval(abs(err))
        endif
        err_out(outp, :, inp) = err
      enddo
    enddo
  end subroutine jacobian_hornnet_multi

  subroutine passed_test(err, max_err, err_okay, verbosityin)
    use qlknn_primitives, only: is_not_close

    real(qlknn_dp), dimension(:,:,:), intent(in) :: err
    real(qlknn_dp), intent(in) :: max_err
    logical, dimension(:,:,:), allocatable, intent(out) :: err_okay
    integer(lli), intent(in), optional :: verbosityin

    real(qlknn_dp), dimension(:), allocatable :: this_err
    logical, dimension(:), allocatable :: this_err_okay
    integer(lli) :: inp, outp, verbosity

    logical, dimension(:), allocatable :: is_nonzero

    if(present(verbosityin)) then
       verbosity=verbosityin
    else
       verbosity = 0
    end if
    if (verbosity >= 1) then
      write(*,"(A,E9.2)")"Checking against error ", max_err
    endif

    allocate(err_okay(size(err, 1), size(err, 2), size(err, 3)))
    allocate(this_err(size(err, 2)))
    allocate(this_err_okay(size(err, 2)))
    allocate(is_nonzero(size(err, 2)))

    err_okay = abs(err) < max_err
    if (verbosity >= 1) then
      do inp = 1, size(err, 3)
        do outp = 1, size(err, 1)
          this_err = err(outp, :, inp)
          this_err_okay = err_okay(outp, :, inp)
          call is_not_close(this_err, 0._qlknn_dp, is_nonzero)
          if (.not. any(is_nonzero) .and. verbosity <= 4) then
            ! Skip zero errors
            cycle
          endif

          if (verbosity >= 2) then
            write(*,*)
            write(*,'(A, I3, A, I3)')'inp=', inp, ', outp=', outp
          endif
          if (verbosity >= 3) then
            write(*,'(A, I3, A, I3, A, *(E9.2, 1X))')'abs(err(', outp, ', :, ', inp, ')) = ', abs(this_err)
          endif
          if (verbosity >= 2) then
            write(*,'(A, I3, A, I3, A, *(E9.2, 1X))')'max(abs(err(', outp, ', :, ', inp, '))) = ', maxval(abs(this_err))
            write(*, '(A, *(L1, 1X))')'err_okay(outp, :, inp) ', err_okay(outp, :, inp)
          endif
          if (verbosity >= 1 .and. .not. all(this_err_okay)) then
            write(*,'(A, I3, A, I3, A, E9.2)')'Failed! max(abs(err(', outp, ', :, ', inp, '))) = ', maxval(abs(this_err))
          endif
        enddo
      enddo
    endif
  end subroutine passed_test

end module test_jacobian
