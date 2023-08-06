! This file is part of QLKNN-fortran
! You should have received the QLKNN-fortran LICENSE in the root of the project
#include "fintrf.h"
module qlknn_mex_struct
  implicit none
  contains
    subroutine set_logical_struct(opts_ptr, field_name, opts_field, verbosity)
      use qlknn_types
      mwPointer, intent(in) :: opts_ptr ! Pointer to the option mxArray
      integer(lli), intent(in) :: verbosity
      character(len=*), intent(in) :: field_name
      logical, intent(inout) :: opts_field

      integer mxIsStruct, mxIsLogical, mxGetNumberOfElements
      mwPointer :: mxGetField
      mwPointer :: field_ptr !Pointer to mxArray in the specified field at the specified fieldname
      character(len=80) :: line
      real*8 :: struct_val, mxGetScalar

      if (mxIsStruct(opts_ptr) == 0) then
        call mexErrMsgIdAndTxt('MATLAB:qlknn:opts_ptr', &
             'Passed non-structure pointer to set_logical_struct!')
      endif

      field_ptr = mxGetField(opts_ptr, 1, field_name)
      not_has_field: if (field_ptr == 0) then
        call mexErrMsgIdAndTxt('MATLAB:qlknn:OptField', &
             'field ' // field_name // ' not in opts struct. Please supply.')
      else not_has_field
        if (field_ptr == 0) then
          call mexErrMsgIdAndTxt('MATLAB:qlknn:ReadField', &
               'problem reading field ' // field_name)
        elseif (mxIsLogical(field_ptr) == 0) then
          call mexErrMsgIdAndTxt('MATLAB:qlknn:LogicalField', &
               field_name // ' should be logical (true/false)')
        elseif (mxGetNumberOfElements(field_ptr) /= 1) then
          call mexErrMsgIdAndTxt('MATLAB:qlknn:LogicalScalar', &
               field_name // ' should be a single logical (true/false)')
        endif
        struct_val = mxGetScalar(field_ptr)
        if (verbosity >= 4) then
          write(line,*) "opt field = ", opts_field
          call mexPrintf(line // achar(10))
          write(line,*) "field_ptr = ", field_ptr
          call mexPrintf(line // achar(10))
          write(line,*) "data      = ", struct_val
          call mexPrintf(line // achar(10))
        endif
        if (struct_val == 0) then
          opts_field = .false.
        else
          opts_field = .true.
        endif
        if (verbosity >= 1) then
          write(line,*) 'set type opt ', field_name, ' to ', opts_field
          call mexPrintf(line // achar(10))
        endif
      endif not_has_field
    end subroutine set_logical_struct

    subroutine set_logical_array_struct(opts_ptr, field_name, opts_field, verbosity)
      use qlknn_types
      mwPointer, intent(in) :: opts_ptr ! Pointer to the option mxArray
      integer(lli), intent(in) :: verbosity
      character(len=*), intent(in) :: field_name
      logical, dimension(:), intent(inout) :: opts_field

      integer mxIsStruct, mxIsLogical, mxGetNumberOfElements
      mwPointer :: mxGetField
      mwPointer :: field_ptr !Pointer to mxArray in the specified field at the specified fieldname
      character(len=80) :: line
      real*8 :: struct_val, mxgetscalar

      if (mxIsStruct(opts_ptr) == 0) then
        call mexErrMsgIdAndTxt('MATLAB:qlknn:opts_ptr', &
             'Passed non-structure pointer to set_logical_struct!')
      endif

      field_ptr = mxGetField(opts_ptr, 1, field_name)
      not_has_field: if (field_ptr == 0) then
        call mexErrMsgIdAndTxt('MATLAB:qlknn:OptField', &
             'field ' // field_name // ' not in opts struct. Please supply.')
      else not_has_field
        if (field_ptr == 0) then
          call mexErrMsgIdAndTxt('MATLAB:qlknn:ReadField', &
               'problem reading field ' // field_name)
        elseif (mxIsLogical(field_ptr) == 0) then
          call mexErrMsgIdAndTxt('MATLAB:qlknn:LogicalField', &
               field_name // ' should be logical (true/false)')
        elseif (mxGetNumberOfElements(field_ptr) /= 1) then
          call mexErrMsgIdAndTxt('MATLAB:qlknn:LogicalScalar', &
               field_name // ' should be a single logical (true/false)')
        endif
        struct_val = mxGetScalar(field_ptr)

        if (verbosity >= 4) then
          write(line,*) "opt field = ", opts_field
          call mexPrintf(line // achar(10))
          write(line,*) "field_ptr = ", field_ptr
          call mexPrintf(line // achar(10))
          write(line,*) "data      = ", struct_val
          call mexPrintf(line // achar(10))
        endif
        if (struct_val == 0) then
          opts_field = .false.
        else
          opts_field = .true.
        endif
        if (verbosity >= 1) then
          write(line,*) 'set type opt ', field_name, ' to ', opts_field
          call mexPrintf(line // achar(10))
        endif
      endif not_has_field
    end subroutine set_logical_array_struct

    subroutine set_real_struct(opts_ptr, field_name, opts_field, verbosity)
      use qlknn_types
      mwPointer, intent(in) :: opts_ptr ! Pointer to the option mxArray
      integer(lli), intent(in) :: verbosity
      character(len=*), intent(in) :: field_name
      real(qlknn_dp), intent(inout) :: opts_field

      integer mxIsNumeric, mxIsStruct, mxGetNumberOfElements
      mwPointer :: mxGetField
      mwPointer :: field_ptr !Pointer to mxArray in the specified field at the specified fieldname
      character(len=80) :: line
      real*8 :: struct_val, mxGetScalar

      if (mxIsStruct(opts_ptr) == 0) then
        call mexErrMsgIdAndTxt('MATLAB:qlknn:opts_ptr', &
             'Passed non-structure pointer to set_real_struct!')
      endif

      field_ptr = mxGetField(opts_ptr, 1, field_name)
      not_has_field: if (field_ptr == 0) then
        call mexErrMsgIdAndTxt('MATLAB:qlknn:OptField', &
             'field ' // field_name // ' not in struct. Please supply.')
      else not_has_field
        if (field_ptr == 0) then
          call mexErrMsgIdAndTxt('MATLAB:qlknn:ReadField', &
               'problem reading field ' // field_name)
        elseif (mxIsNumeric(field_ptr) == 0) then
          call mexErrMsgIdAndTxt('MATLAB:qlknn:NumericField', &
               field_name // ' should be numeric')
        elseif (mxGetNumberOfElements(field_ptr) /= 1) then
          call mexErrMsgIdAndTxt('MATLAB:qlknn:NumericScalar', &
               field_name // ' should be a single number')
        endif
        struct_val = mxGetScalar(field_ptr)
        if (verbosity >= 4) then
          write(line,*) "opt field = ", opts_field
          call mexPrintf(line // achar(10))
          write(line,*) "field_ptr = ", field_ptr
          call mexPrintf(line // achar(10))
          write(line,*) "data      = ", struct_val
          call mexPrintf(line // achar(10))
        endif
        opts_field = struct_val
        if (verbosity >= 1) then
          write(line,*) 'set type opt ', field_name, ' to ', opts_field
          call mexPrintf(line // achar(10))
        endif
      endif not_has_field
    end subroutine set_real_struct

    subroutine set_real_array_struct(opts_ptr, field_name, opts_field, verbosity)
      use qlknn_types
      mwPointer, intent(in) :: opts_ptr ! Pointer to the option mxArray
      integer(lli), intent(in) :: verbosity
      character(len=*), intent(in) :: field_name
      real(qlknn_dp), dimension(:), intent(inout) :: opts_field

      integer mxIsNumeric, mxIsStruct, mxGetNumberOfElements, mxIsEmpty
      mwPointer :: mxGetField, mxGetPr
      mwPointer :: field_ptr !Pointer to mxArray in the specified field at the specified fieldname
      mwPointer :: data_ptr

      character(len=4096) :: line
      real*8, dimension(:), allocatable :: struct_vals

      if (mxIsStruct(opts_ptr) == 0) then
        call mexErrMsgIdAndTxt('MATLAB:qlknn:opts_ptr', &
             'Passed non-structure pointer to set_logical_struct!')
      endif

      field_ptr = mxGetField(opts_ptr, 1, field_name)
      not_has_field: if (field_ptr == 0) then
        call mexErrMsgIdAndTxt('MATLAB:qlknn:OptField', &
             'field ' // field_name // ' not in opts struct. Please supply.')
      else not_has_field
        if (field_ptr == 0) then
          call mexErrMsgIdAndTxt('MATLAB:qlknn:ReadField', &
               'problem reading field ' // field_name)
        elseif (mxIsNumeric(field_ptr) == 0) then
          call mexErrMsgIdAndTxt('MATLAB:qlknn:NumericField', &
               field_name // ' should be numeric')
        elseif (mxIsEmpty(field_ptr) /= 0) then
          call mexErrMsgIdAndTxt('MATLAB:qlknn:EmptyField', &
               field_name // ' should not be empty')
        elseif (mxGetNumberOfElements(field_ptr) /= 1 .AND. &
               mxGetNumberOfElements(field_ptr) /= SIZE(opts_field)) then
          write(line, '(A,A,A,A,I0,A,I0)') field_name , ' should be either a single number or have the same length as the default. len(', field_name, ')=', mxGetNumberOfElements(field_ptr), ', len(default)=', SIZE(opts_field)
          call mexErrMsgIdAndTxt('MATLAB:qlknn:LogicalScalar', line)
        endif
        data_ptr = mxGetPr(field_ptr)
        if (verbosity >= 4) then
          write(line, '(A,*(F7.2 X))') "opts field = ", opts_field
          call mexPrintf(trim(line) // achar(10))
          write(line,*) "field_ptr = ", field_ptr
          call mexPrintf(trim(line) // achar(10))
          write(line,*) "data_ptr = ", data_ptr
          call mexPrintf(trim(line) // achar(10))
        endif
        if (mxGetNumberOfElements(field_ptr) == 1) then
          allocate(struct_vals(1))
          call mxCopyPtrToReal8(data_ptr, struct_vals, 1)
          opts_field = struct_vals(1)
        else
          allocate(struct_vals(SIZE(opts_field)))
          call mxCopyPtrToReal8(data_ptr, struct_vals, SIZE(opts_field))
          opts_field = struct_vals
        endif
        if (verbosity >= 1) then
          write(line,'(A,A,A,*(F7.2 X))') 'set type opt ', field_name, ' to ', opts_field
          call mexPrintf(trim(line) // achar(10))
        endif
      endif not_has_field
    end subroutine set_real_array_struct
      end module qlknn_mex_struct
