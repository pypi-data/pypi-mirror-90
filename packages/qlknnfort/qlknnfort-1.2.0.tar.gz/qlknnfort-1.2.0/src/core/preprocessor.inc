! This file is part of QLKNN-fortran
! You should have received the QLKNN-fortran LICENSE in the root of the project
#if defined MEXING
#define ERRORSTOP(cond, msg) if(cond) then; call mexErrMsgIdAndTxt('MATLAB:qlknn:critical', msg); endif;
#elif defined __PGI
#define ERRORSTOP(cond, msg) if(cond) then; write(stderr,*) msg; STOP 1; endif;
#elif defined __INTEL_COMPILER
#define ERRORSTOP(cond, msg) if(cond) then; write(stderr,*) msg; STOP 1; endif;
#else
#define ERRORSTOP(cond, msg) if(cond) then; write(stderr,*) msg; ERROR STOP; endif;
#endif

#define INTNAN -99999
