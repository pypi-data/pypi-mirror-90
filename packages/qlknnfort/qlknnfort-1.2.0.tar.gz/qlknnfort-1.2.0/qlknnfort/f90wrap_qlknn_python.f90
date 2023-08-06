! Module qlknn_python defined in file /builds/qualikiz-group/QLKNN-fortran/src/qlknn_python.f90

subroutine f90wrap_evaluate_qlknn_10d_direct(qlknn_path, input, qlknn_out, verbosityin, optsin, qlknn_normsin, n0, n1, &
    n2, n3)
    use qlknn_types, only: qlknn_options, qlknn_normpars
    use qlknn_python, only: evaluate_qlknn_10d_direct
    implicit none
    
    type qlknn_options_ptr_type
        type(qlknn_options), pointer :: p => NULL()
    end type qlknn_options_ptr_type
    type qlknn_normpars_ptr_type
        type(qlknn_normpars), pointer :: p => NULL()
    end type qlknn_normpars_ptr_type
    character(2048), intent(in) :: qlknn_path
    real(8), intent(in), dimension(n0,n1) :: input
    real(8), intent(inout), dimension(n2,n3) :: qlknn_out
    integer(8), optional, intent(in) :: verbosityin
    type(qlknn_options_ptr_type) :: optsin_ptr
    integer, optional, intent(in), dimension(2) :: optsin
    type(qlknn_normpars_ptr_type) :: qlknn_normsin_ptr
    integer, optional, intent(in), dimension(2) :: qlknn_normsin
    integer :: n0
    !f2py intent(hide), depend(input) :: n0 = shape(input,0)
    integer :: n1
    !f2py intent(hide), depend(input) :: n1 = shape(input,1)
    integer :: n2
    !f2py intent(hide), depend(qlknn_out) :: n2 = shape(qlknn_out,0)
    integer :: n3
    !f2py intent(hide), depend(qlknn_out) :: n3 = shape(qlknn_out,1)
    if (present(optsin)) then
        optsin_ptr = transfer(optsin, optsin_ptr)
    else
        optsin_ptr%p => null()
    end if
    if (present(qlknn_normsin)) then
        qlknn_normsin_ptr = transfer(qlknn_normsin, qlknn_normsin_ptr)
    else
        qlknn_normsin_ptr%p => null()
    end if
    call evaluate_qlknn_10d_direct(qlknn_path=qlknn_path, input=input, qlknn_out=qlknn_out, verbosityin=verbosityin, &
        optsin=optsin_ptr%p, qlknn_normsin=qlknn_normsin_ptr%p)
end subroutine f90wrap_evaluate_qlknn_10d_direct

subroutine f90wrap_finalize
    use qlknn_python, only: finalize
    implicit none
    
    call finalize()
end subroutine f90wrap_finalize

subroutine f90wrap_abort(msg)
    use qlknn_python, only: abort
    implicit none
    
    character(2048), intent(in) :: msg
    call abort(msg=msg)
end subroutine f90wrap_abort

! End of module qlknn_python defined in file /builds/qualikiz-group/QLKNN-fortran/src/qlknn_python.f90

