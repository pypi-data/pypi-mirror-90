! This file is part of QLKNN-fortran
! You should have received the QLKNN-fortran LICENSE in the root of the project
#include "fintrf.h"

subroutine mexFunction(nlhs, plhs, nrhs, prhs)
  use qlknn_evaluate_nets
  use qlknn_disk_io
  use qlknn_types

  implicit none
  mwPointer :: plhs(*), prhs(*)
  integer :: nlhs, nrhs

  integer(lli) :: n_rho, n_out, n_raptor, n_merged_outputs, total_n_in, n_nets, nn_type
  integer(lli) :: n_members ! Specific for committee NN

  real(qlknn_dp), dimension(:,:), allocatable :: input, qlknn_out, qlknn_out_raptor, qlknn_eb
  real(qlknn_dp), dimension(:,:,:), allocatable :: dqlknn_out_dinput, dqlknn_out_dinput_raptor
  !logical(qlknn_bool), dimension(:,:), allocatable :: qlknn_validity, qlknn_validity_raptor
  logical, dimension(:,:), allocatable :: qlknn_validity, qlknn_validity_raptor
  integer(lli) :: verbosity, path_ix, input_ix, verbosity_ix, opts_ix, norms_ix, nntype_ix
  integer(lli) :: dout_din_ix, validity_ix
  integer :: double_id
  integer :: matlab_int
  type (qlknn_options) :: opts
  type(qlknn_normpars) :: norms

  logical, save :: nets_loaded=.false.
  logical :: has_verbosity, has_dout_din, has_validity, has_opts, has_norms, has_nntype

#if MX_HAS_INTERLEAVED_COMPLEX
  mwPointer mxGetDoubles
#else
  mwPointer mxGetPr
#endif

  mwPointer mxCreateDoubleMatrix
  mwPointer mxCreateNumericArray
  integer mxIsNumeric, mxIsChar, mxIsStruct
  integer mxClassIDFromClassName
  mwPointer mxGetM, mxGetN

  !     Pointers to input/output mxArrays:
  mwPointer inp_ptr, verb_ptr, nntype_ptr, outp_ptr, dout_din_ptr, opts_ptr, norms_ptr

  !     Array information:
  mwPointer ncols_in
  mwSize size_in, size_out
  mwSize din_dout_shape(3)

  integer status
  mwPointer mxGetString

  !     Arguments for computational routine:
  real*8 verbosityin, nntypein
  real*8 mxGetScalar
  ! Maximum string size = maxbuf
  mwSize  maxbuf
  parameter(maxbuf = 2048)
  character*2048 qlknn_path

  mwPointer  arrlen

  !-----------------------------------------------------------------------
  !     Check for proper number of arguments. 
  ! Validate inputs
  path_ix = 1
  input_ix = 2
  verbosity_ix = 3
  opts_ix = 4
  norms_ix = 5
  nntype_ix = 6
  dout_din_ix = 2
  validity_ix = 3
  ! Amount of in/outputs checking
  if (nrhs < 2) then
    call mexErrMsgIdAndTxt ('MATLAB:qlknn:nInput', &
         'At least two inputs required.')
  elseif (nlhs > 3) then
    call mexErrMsgIdAndTxt ('MATLAB:qlknn:nOutput', &
         'Too many output arguments.')
  ! Input typechecks
  elseif (mxIsChar(prhs(path_ix)) .ne. 1) then
    call mexErrMsgIdAndTxt ('MATLAB:qlknn:NonString', &
         'Input must be a string.')
    ! The input must be a row vector.
  elseif (mxGetM(prhs(path_ix)) .ne. 1) then
    call mexErrMsgIdAndTxt ('MATLAB:qlknn:NonRowVector', &
         'Input must be a row vector.')
  elseif (mxIsNumeric(prhs(input_ix)) .eq. 0) then
    call mexErrMsgIdAndTxt ('MATLAB:qlknn:NonNumeric', &
         'input array must be numeric.')
  elseif (nrhs >= verbosity_ix) then
    if (mxIsNumeric(prhs(verbosity_ix)) == 0) then
      call mexErrMsgIdAndTxt ('MATLAB:qlknn:NonNumeric', &
           'verbosity must be a number.')
    endif
  elseif (nrhs >= opts_ix) then
    if (mxIsStruct(prhs(opts_ix)) == 0) then
      call mexErrMsgIdAndTxt ('MATLAB:qlknn:NonStruct', &
         'Input opts must be a struct.')
    endif
  elseif (nrhs >= norms_ix) then
    if (mxIsStruct(prhs(norms_ix)) == 0) then
      call mexErrMsgIdAndTxt ('MATLAB:qlknn:NonStruct', &
         'Input norms must be a struct.')
    endif
  elseif (nrhs >= nntype_ix) then
    if (mxIsNumeric(prhs(nntype_ix)) == 0) then
      call mexErrMsgIdAndTxt ('MATLAB:qlknn:NonNumeric', &
         'Input NN type must be a number.')
    endif
  endif

  if (nlhs >= dout_din_ix) then
    has_dout_din = .true.
  else
    has_dout_din = .false.
  endif
  if (nlhs >= validity_ix) then
    has_validity = .true.
  else
    has_validity = .false.
  endif
  if (nrhs >= verbosity_ix) then
    has_verbosity = .true.
  else
    has_verbosity = .false.
  endif
  if (nrhs >= opts_ix) then
    has_opts = .true.
  else
    has_opts = .false.
  endif
  if (nrhs >= norms_ix) then
    has_norms = .true.
  else
    has_norms = .false.
  endif
  if (nrhs >= nntype_ix) then
    has_nntype = .true.
  else
    has_nntype = .false.
  endif

  !------------------
  ! Prepare verbosity
  if (has_verbosity) then
    arrlen = mxGetM(prhs(verbosity_ix))*mxGetN(prhs(verbosity_ix))
    if (arrlen .gt. 1) then
      call mexErrMsgIdAndTxt('MATLAB:qlknn:verbosity_in', &
           'Verbosity should be a single number.')
    endif
#if MX_HAS_INTERLEAVED_COMPLEX
    verb_ptr = mxGetInt32s(prhs(verbosity_ix))
#else
    verb_ptr = mxGetPr(prhs(verbosity_ix))
#endif
    verbosityin = mxGetScalar(prhs(verbosity_ix))
    verbosity = INT(verbosityin, li)
  else
    verbosity = 0
  endif

  !------------------
  ! Prepare path to qlknn
  ! Get the length of the input string.
  arrlen = mxGetM(prhs(path_ix))*mxGetN(prhs(path_ix))
  if (arrlen .gt. maxbuf) then
    call mexErrMsgIdAndTxt ('MATLAB:revord:maxbuf', &
         'Max string length 2048.')
  endif

  status = mxGetString(prhs(path_ix), qlknn_path, maxbuf)
  ! Check if mxGetString is successful.
  if (status .ne. 0) then
    call mexErrMsgIdAndTxt ('MATLAB:revord:readError', &
         'Error reading string.')
  endif

  !-------------
  ! Prepare network type selection
  if (has_nntype) then
    arrlen = mxGetM(prhs(nntype_ix))*mxGetN(prhs(nntype_ix))
    if (arrlen .gt. 1) then
      call mexErrMsgIdAndTxt('MATLAB:qlknn:nntype_in', &
           'NN type should be a single number.')
    endif
#if MX_HAS_INTERLEAVED_COMPLEX
    nntype_ptr = mxGetInt32s(prhs(nntype_ix))
#else
    nntype_ptr = mxGetPr(prhs(nntype_ix))
#endif
    nntypein = mxGetScalar(prhs(nntype_ix))
    nn_type = INT(nntypein, li)
  else
    nn_type = 0
  endif

  !-------------
  ! Set network specific array sizes and options
  select case (nn_type)
  case (2)
    total_n_in = 14
    n_merged_outputs = 13
    n_nets = 25
    n_members = 10
    call default_qlknn_jetexp_options(opts)
  case default   ! also represents nn_type == 0
    total_n_in = 11
    n_merged_outputs = 10
    n_nets = 20
    n_members = 1
    call default_qlknn_hyper_options(opts)
  end select

  !-------------
  ! Prepare opts struct
  if (has_opts) then
#if MX_HAS_INTERLEAVED_COMPLEX
    opts_ptr = should raise error on compile
#else
    opts_ptr = prhs(opts_ix) ! Pointer to the option mxArray
#endif
    call matlabify_opts(opts_ptr, opts, verbosity)
  endif

  if (opts%merge_modes) then
    n_out = n_merged_outputs
    n_raptor = 7
  else
    n_out = n_nets
    n_raptor = n_nets
  end if

  !------------------
  ! Prepare input array
  ! Get the size of the input array, total_n_in depends on selected network type
  n_rho = INT(mxGetM(prhs(input_ix)), li)
  ncols_in = mxGetN(prhs(input_ix))
  size_in = n_rho * ncols_in

  if (ncols_in /= total_n_in) then
    call mexErrMsgIdAndTxt ('MATLAB:qlknn:input_in', &
         'Input array should have the right number of columns')
  endif

  ! Create Fortran array from the input argument.
#if MX_HAS_INTERLEAVED_COMPLEX
  inp_ptr = mxGetDoubles(prhs(input_ix))
#else
  inp_ptr = mxGetPr(prhs(input_ix))
#endif
  allocate(input(total_n_in, n_rho))
  call mxCopyPtrToReal8(inp_ptr,TRANSPOSE(input),size_in)

  if (has_norms) then
#if MX_HAS_INTERLEAVED_COMPLEX
    norms_ptr =
#else
    norms_ptr = prhs(norms_ix) ! Pointer to the option mxArray
#endif
    allocate(norms%A1(n_rho))
    call matlabify_norms(norms_ptr, norms, verbosity)
  endif

  !------------------
  ! Loads networks before
  if (.NOT. nets_loaded) then
    if (verbosity >= 1) then
      call mexPrintf('Loading NNs from path = ')
      call mexPrintf(qlknn_path)
      call mexPrintf(achar(10))
    endif
    select case (nn_type)
    case (2)
      call load_jetexp_nets_from_disk(trim(qlknn_path), verbosity)
    case default   ! also represents nn_type == 0
      call load_qlknn_hyper_nets_from_disk(trim(qlknn_path), verbosity)
    end select
    nets_loaded=.true.
  end if

  !------------------
  ! Prepare output matrix
  ! Create matrix for the return argument, [n_outputs, n_nets, n_out, n_raptor] all depend on selected network type
  plhs(1) = mxCreateDoubleMatrix(INT(n_rho, KIND(matlab_int)), INT(n_raptor, KIND(matlab_int)),0)
#if MX_HAS_INTERLEAVED_COMPLEX
  outp_ptr = mxGetDoubles(plhs(1))
#else
  outp_ptr = mxGetPr(plhs(1))
#endif
  allocate(qlknn_out(n_rho, n_out))

  if (has_dout_din) then
    double_id = mxClassIDFromClassName('double')
    din_dout_shape = (/n_rho, n_raptor, total_n_in/)
    plhs(dout_din_ix) = mxCreateNumericArray(3, din_dout_shape, double_id, 0)
#if MX_HAS_INTERLEAVED_COMPLEX
    dout_din_ptr = mxGetDoubles(plhs(dout_din_ix))
#else
    dout_din_ptr = mxGetPr(plhs(dout_din_ix))
#endif
    allocate(dqlknn_out_dinput(n_out, n_rho, total_n_in))
  endif

  !------------------
  ! Neural networks evaluated at lower verbosity level than calling model
  verbosity = verbosity - 1_li
  open(unit=stderr,file='qlknn_stderr.txt',status='unknown')

  !------------------
  ! Adapt function call and output treatment based on selected network type
  select case (nn_type)
  case (2)

    if (has_validity) then
      plhs(validity_ix) = mxCreateDoubleMatrix(n_rho, n_raptor, 0)
      allocate(qlknn_validity(n_rho, n_out))
    endif

    if (has_dout_din .and. has_validity) then
      CALL evaluate_jetexp_net(input, nets, n_members, qlknn_out, qlknn_eb, verbosity, opts, dqlknn_out_dinput=dqlknn_out_dinput, qlknn_validity=qlknn_validity)
    elseif (has_dout_din .and. .not. has_validity) then
      CALL evaluate_jetexp_net(input, nets, n_members, qlknn_out, qlknn_eb, verbosity, opts, dqlknn_out_dinput=dqlknn_out_dinput)
    elseif (.not. has_dout_din .and. has_validity) then
      CALL evaluate_jetexp_net(input, nets, n_members, qlknn_out, qlknn_eb, verbosity, opts, qlknn_validity=qlknn_validity)
    elseif (.not. has_dout_din .and. .not. has_validity) then
      CALL evaluate_jetexp_net(input, nets, n_members, qlknn_out, qlknn_eb, verbosity, opts)
    endif
  
    if (opts%merge_modes) then
      allocate(qlknn_out_raptor(n_rho, n_raptor))
      qlknn_out_raptor(:, 1) = qlknn_out(:, 1) !qe
      qlknn_out_raptor(:, 2) = qlknn_out(:, 3) !qi
      qlknn_out_raptor(:, 3) = qlknn_out(:, 4) !Gamma_e
      qlknn_out_raptor(:, 4) = qlknn_out(:, 7) !De
      qlknn_out_raptor(:, 5) = qlknn_out(:, 8) + qlknn_out(:, 9) !Ve
      qlknn_out_raptor(:, 6) = qlknn_out(:, 10) !Di
      qlknn_out_raptor(:, 7) = qlknn_out(:, 11) + qlknn_out(:, 12) + qlknn_out(:,13) !Vi
      if (has_dout_din) then
        allocate(dqlknn_out_dinput_raptor(n_raptor, n_rho, total_n_in))
        dqlknn_out_dinput_raptor(1, :, :) = dqlknn_out_dinput(1, :, :) !qe
        dqlknn_out_dinput_raptor(2, :, :) = dqlknn_out_dinput(3, :, :) !qi
        dqlknn_out_dinput_raptor(3, :, :) = dqlknn_out_dinput(4, :, :) !Gamma_e
        dqlknn_out_dinput_raptor(4, :, :) = dqlknn_out_dinput(7, :, :) !De
        dqlknn_out_dinput_raptor(5, :, :) = dqlknn_out_dinput(8, :, :) + dqlknn_out_dinput(9, :, :) !Ve
        dqlknn_out_dinput_raptor(6, :, :) = dqlknn_out_dinput(10, :, :) !Di
        dqlknn_out_dinput_raptor(7, :, :) = dqlknn_out_dinput(11, :, :) + dqlknn_out_dinput(12, :, :) + dqlknn_out_dinput(13, :, :) !Vi
      endif
      if (has_validity) then
        allocate(qlknn_validity_raptor(n_rho, n_raptor))
        qlknn_validity_raptor(:, 1) = qlknn_validity(:, 1)
        qlknn_validity_raptor(:, 2) = qlknn_validity(:, 3) !qi
        qlknn_validity_raptor(:, 3) = qlknn_validity(:, 4) !Gamma_e
        qlknn_validity_raptor(:, 4) = qlknn_validity(:, 7) !De
        qlknn_validity_raptor(:, 5) = qlknn_validity(:, 8) .and. qlknn_validity(:, 9) !Ve
        qlknn_validity_raptor(:, 6) = qlknn_validity(:, 10) !Di
        qlknn_validity_raptor(:, 7) = qlknn_validity(:, 11) .and. qlknn_validity(:, 12) .and. qlknn_validity(:,13) !Vi
      endif
    else
      qlknn_out_raptor = qlknn_out
      if (has_dout_din) then
        dqlknn_out_dinput_raptor = dqlknn_out_dinput
      endif
      if (has_validity) then
        qlknn_validity_raptor = qlknn_validity
      endif
    endif

  case default  ! also represents nn_type == 0 

    if (.not. has_norms .and. opts%apply_victor_rule) then
      call mexErrMsgIdAndTxt ('MATLAB:qlknn:inputError', &
           'norms need to be provided when applying victor rule')
    endif

    if (has_dout_din .and. opts%apply_victor_rule) then
      CALL evaluate_QLKNN_10D(input, nets, qlknn_out, verbosity, opts, qlknn_normsin=norms, dqlknn_out_dinput=dqlknn_out_dinput)
    elseif (has_dout_din .and. .not. opts%apply_victor_rule) then
      CALL evaluate_QLKNN_10D(input, nets, qlknn_out, verbosity, opts, dqlknn_out_dinput=dqlknn_out_dinput)
    elseif (.not. has_dout_din .and. opts%apply_victor_rule) then
      CALL evaluate_QLKNN_10D(input, nets, qlknn_out, verbosity, opts, qlknn_normsin=norms)
    elseif (.not. has_dout_din .and. .not. opts%apply_victor_rule) then
      CALL evaluate_QLKNN_10D(input, nets, qlknn_out, verbosity, opts)
    endif
  
    if (opts%merge_modes) then
      allocate(qlknn_out_raptor(n_rho, n_raptor))
      qlknn_out_raptor(:, 1) = qlknn_out(:, 1) !qe
      qlknn_out_raptor(:, 2) = qlknn_out(:, 3) !qi
      qlknn_out_raptor(:, 3) = qlknn_out(:, 4) !Gamma_e
      qlknn_out_raptor(:, 4) = qlknn_out(:, 5) !De
      qlknn_out_raptor(:, 5) = qlknn_out(:, 6) + qlknn_out(:, 7)!Ve
      qlknn_out_raptor(:, 6) = qlknn_out(:, 8) !Di
      qlknn_out_raptor(:, 7) = qlknn_out(:, 9) + qlknn_out(:, 10) !Vi
      if (has_dout_din) then
        allocate(dqlknn_out_dinput_raptor(n_raptor, n_rho, total_n_in))
        dqlknn_out_dinput_raptor(1, :, :) = dqlknn_out_dinput(1, :, :) !qe
        dqlknn_out_dinput_raptor(2, :, :) = dqlknn_out_dinput(3, :, :) !qi
        dqlknn_out_dinput_raptor(3, :, :) = dqlknn_out_dinput(4, :, :) !Gamma_e
        dqlknn_out_dinput_raptor(4, :, :) = dqlknn_out_dinput(5, :, :) !De
        dqlknn_out_dinput_raptor(5, :, :) = dqlknn_out_dinput(6, :, :) + dqlknn_out_dinput(7, :, :)!Ve
        dqlknn_out_dinput_raptor(6, :, :) = dqlknn_out_dinput(8, :, :) !Di
        dqlknn_out_dinput_raptor(7, :, :) = dqlknn_out_dinput(9, :, :) + dqlknn_out_dinput(10, :, :) !Vi
      endif
    else
      qlknn_out_raptor = qlknn_out
      if (has_dout_din) then
        dqlknn_out_dinput_raptor = dqlknn_out_dinput
      endif
    endif
  
  end select

  !     Call the computational subroutine.
  !call timestwo(y_output, input)

  ! Load the data into y_ptr, which is the output to MATLAB.
  size_out = n_rho * n_raptor
  call mxCopyReal8ToPtr(qlknn_out_raptor,outp_ptr,size_out)
  if (has_dout_din) then
    call mxCopyReal8ToPtr(reshape(dqlknn_out_dinput_raptor, din_dout_shape, order=(/ 2, 1, 3 /)), dout_din_ptr, product(din_dout_shape))
  end if
  if (has_validity) then
    !call mxCopyReal8ToPtr(qlknn_validity_raptor, plhs(validity_ix), size_out)
  end if

  return
end

  !-----------------------------------------------------------------------
  !     Computational routine

  subroutine timestwo(y_output, x_input)
    real*8 x_input, y_output

    y_output = 2.0 * x_input
    return
  end

  subroutine matlabify_norms(norms_ptr, norms, verbosity)
    use qlknn_types
    use qlknn_mex_struct
    integer(lli), intent(in) :: verbosity
    mwPointer, intent(in) :: norms_ptr
    type (qlknn_normpars), intent(inout) :: norms
  !  character(len=512) :: line

    call set_real_struct(norms_ptr, 'a', norms%a, verbosity)
    call set_real_struct(norms_ptr, 'R0', norms%R0, verbosity)
    call set_real_array_struct(norms_ptr, 'A1', norms%A1, verbosity)

  end subroutine matlabify_norms

  subroutine matlabify_opts(opts_ptr, opts, verbosity)
    use qlknn_types
    use qlknn_mex_struct
    integer(lli), intent(in) :: verbosity
    mwPointer, intent(in) :: opts_ptr
    type (qlknn_options), intent(inout) :: opts

    call set_logical_struct(opts_ptr, 'use_ion_diffusivity_networks', opts%use_ion_diffusivity_networks, verbosity)
    call set_logical_struct(opts_ptr, 'apply_victor_rule', opts%apply_victor_rule, verbosity)
    call set_logical_struct(opts_ptr, 'use_effective_diffusivity', opts%use_effective_diffusivity, verbosity)
    call set_logical_struct(opts_ptr, 'calc_heat_transport', opts%calc_heat_transport, verbosity)
    call set_logical_struct(opts_ptr, 'calc_part_transport', opts%calc_part_transport, verbosity)
    call set_logical_struct(opts_ptr, 'use_ETG', opts%use_ETG, verbosity)
    call set_logical_struct(opts_ptr, 'use_ITG', opts%use_ITG, verbosity)
    call set_logical_struct(opts_ptr, 'use_TEM', opts%use_TEM, verbosity)
    call set_logical_struct(opts_ptr, 'apply_stability_clipping', opts%apply_stability_clipping, verbosity)
    call set_logical_struct(opts_ptr, 'merge_modes', opts%merge_modes, verbosity)
    call set_logical_struct(opts_ptr, 'force_evaluate_all', opts%force_evaluate_all, verbosity)

    call set_logical_array_struct(opts_ptr, 'constrain_inputs', opts%constrain_inputs, verbosity)
    call set_logical_array_struct(opts_ptr, 'constrain_outputs', opts%constrain_outputs, verbosity)

    call set_real_array_struct(opts_ptr, 'min_input', opts%min_input, verbosity)
    call set_real_array_struct(opts_ptr, 'max_input', opts%max_input, verbosity)
    call set_real_array_struct(opts_ptr, 'margin_input', opts%margin_input, verbosity)
    call set_real_array_struct(opts_ptr, 'min_output', opts%min_output, verbosity)
    call set_real_array_struct(opts_ptr, 'max_output', opts%max_output, verbosity)
    call set_real_array_struct(opts_ptr, 'margin_output', opts%margin_output, verbosity)
end subroutine matlabify_opts

