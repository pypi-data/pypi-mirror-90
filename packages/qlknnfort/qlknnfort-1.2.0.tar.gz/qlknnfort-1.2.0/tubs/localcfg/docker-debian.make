# vim:filetype=make

# Main use case is in the QuaLiKiz Docker container
ifeq ($(TUBS_CONFIG_PHASE),1)
  # Check if we are compiling with MPI
  ifeq ($(TUBSCFG_MPI),1)
    $(info Detected MPI compilation, TUBSCFG_MPI=$(TUBSCFG_MPI))
    ifeq ($(TOOLCHAIN),gcc)
      $(info Detected TOOLCHAIN=$(TOOLCHAIN))
      ifeq ($(origin FC), $(filter $(origin FC),default undefined))
        FC:=mpifort # Use OpenMPI for gfortran
      endif
    else ifeq ($(TOOLCHAIN),intel)
      $(info Detected TOOLCHAIN=$(TOOLCHAIN))
      ifeq ($(origin FC), $(filter $(origin FC),default undefined))
        FC:=mpiifort # Use Intel MPI for ifort
      endif
    else ifeq ($(TOOLCHAIN),pgi)
      $(info Detected TOOLCHAIN=$(TOOLCHAIN))
      ifeq ($(origin FC), $(filter $(origin FC),default undefined))
        FC:=mpifort.pgi # Use specific OpenMPI binary for NVIDIA compiler
      endif
    else
      $(error Unknown TOOLCHAIN=$(TOOLCHAIN))
    endif
  else ifeq ($(TUBSCFG_MPI),0)
    $(info Serial compilation, TUBSCFG_MKL=$(TUBSCFG_MKL))
  endif
else ifeq ($(TUBS_CONFIG_PHASE),2)
  ifeq ($(origin LINK), $(filter $(origin LINK),default undefined file))
    LINK:=$(FC)
  endif

  # Check if we are compiling with MKL
  ifeq ($(TUBSCFG_MKL),1)
    $(info Detected MKL compilation, TUBSCFG_MKL=$(TUBSCFG_MKL))
    MKLROOT?=/opt/intel/mkl
    F95ROOT?=$(MKLROOT)
    # Flags generated with the Intel Math Kernel Library Link Line Advisor
    # https://software.intel.com/en-us/articles/intel-mkl-link-line-advisor
    # Link to the int64 (lli) version of MKL for MATLAB compatibility
    ifeq ($(TOOLCHAIN),gcc)
      $(info Detected TOOLCHAIN=$(TOOLCHAIN))
      F95ROOT=$(MKLROOT)
      TUBS_FFLAGS+=-fdefault-integer-8 -I${F95ROOT}/include/intel64/ilp64 -m64 -I${MKLROOT}/include
      MKL_LDFLAGS+=${F95ROOT}/lib/intel64/libmkl_blas95_ilp64.a
      MKL_LDFLAGS+=${F95ROOT}/lib/intel64/libmkl_lapack95_ilp64.a
      MKL_LDFLAGS+=-Wl,--start-group ${MKLROOT}/lib/intel64/libmkl_gf_ilp64.a ${MKLROOT}/lib/intel64/libmkl_sequential.a ${MKLROOT}/lib/intel64/libmkl_core.a -Wl,--end-group -lpthread -lm -ldl
    else ifeq ($(TOOLCHAIN),intel)
      $(info Detected TOOLCHAIN=$(TOOLCHAIN))
      TUBS_FFLAGS+=-i8 -I${MKLROOT}/include/intel64/ilp64 -I${MKLROOT}/include
      MKL_LDFLAGS+=-i8 # Needed for MPI linking with INTEL MPI to go correctly
      MKL_LDFLAGS+=${MKLROOT}/lib/intel64/libmkl_blas95_ilp64.a
      MKL_LDFLAGS+=${MKLROOT}/lib/intel64/libmkl_lapack95_ilp64.a
      MKL_LDFLAGS += -Wl,--start-group ${MKLROOT}/lib/intel64/libmkl_intel_ilp64.a ${MKLROOT}/lib/intel64/libmkl_sequential.a ${MKLROOT}/lib/intel64/libmkl_core.a -Wl,--end-group -lpthread -lm -ldl
    else ifeq ($(TOOLCHAIN),pgi)
      $(info Detected TOOLCHAIN=$(TOOLCHAIN))
      TUBS_FFLAGS+=-i8 -I${MKLROOT}/include
      MKL_LDFLAGS+=${F95ROOT}/lib/intel64/libmkl_blas95_ilp64.a
      MKL_LDFLAGS+=${F95ROOT}/lib/intel64/libmkl_lapack95_ilp64.a
      MKL_LDFLAGS+=-Wl,--start-group ${MKLROOT}/lib/intel64/libmkl_intel_ilp64.a ${MKLROOT}/lib/intel64/libmkl_sequential.a ${MKLROOT}/lib/intel64/libmkl_core.a -Wl,--end-group -lpthread -lm -ldl
    else
      $(error Unknown TOOLCHAIN=$(TOOLCHAIN))
    endif
  else ifeq ($(TUBSCFG_MKL),0)
    $(info Not compiling with MKL, TUBSCFG_MKL=$(TUBSCFG_MKL))
  else
    $(info Unknown TUBSCFG_MKL $(TUBSCFG_MKL))
  endif

  LOCALCFG_ACTIVE:= docker-debian
else
  $(error Unknown TUBS_CONFIG_PHASE $(TUBS_CONFIG_PHASE))
endif
