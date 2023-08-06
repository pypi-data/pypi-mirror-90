# vim:filetype=make

# Main use case is the Heimdall cluster
# Heimdall uses OpenMPI wrappers for all compilers
ifeq ($(TUBS_CONFIG_PHASE),1)
  # Use same optimization for mixed-architecture Heimdall/Freia nodes. See discussion on !3
  $(info Filter ',haswell-64' from FFLAGS)
  FFLAGS := $(FFLAGS:,haswell-64=)
  ifeq ($(TOOLCHAIN),pgi)
    ifeq ($(BUILD),release)
      # -Mvect forces -O2, do not use
      TUBSCFG_OPT += -Mnoframe -Mcache_align -Mflushz -Mpre
    endif
  endif
else ifeq ($(TUBS_CONFIG_PHASE),2)
  # Check if we are compiling with MPI
  ifeq ($(TUBSCFG_MPI),1)
    $(info Detected MPI compilation, TUBSCFG_MPI=$(TUBSCFG_MPI))
    ifeq ($(TOOLCHAIN),gcc)
      $(info Detected TOOLCHAIN=$(TOOLCHAIN))
      # Tested with `module unload pgi; module load gfortran/4.8 openmpi/1.8.2`
      FC = mpifort
      LINK = mpifort
    else ifeq ($(TOOLCHAIN),intel)
      $(info Detected TOOLCHAIN=$(TOOLCHAIN))
      # Tested with `module unload pgi openmpi; module load ifort/12.0 openmpi-ifort-12.0/2.1.0`
      FC = mpifort
      LINK = mpifort
    else ifeq ($(TOOLCHAIN),pgi)
      $(info Detected TOOLCHAIN=$(TOOLCHAIN))
      # Tested with `module load pgi/14.4 openmpi/1.8.2`
      FC = mpifort
      LINK = mpifort
      TUBS_FFLAGS += -m64 -tp=sandybridge
    else
      $(error Unknown TOOLCHAIN=$(TOOLCHAIN))
    endif
  else ifeq ($(TUBSCFG_MPI),0)
    $(info Serial compilation, TUBSCFG_MKL=$(TUBSCFG_MKL))
  endif

  # Check if we are compiling with MKL
  ifeq ($(TUBSCFG_MKL),1)
    $(info Detected MKL compilation, TUBSCFG_MKL=$(TUBSCFG_MKL))
    # If we compile with MKL
    MKLROOT ?= /usr/local/depot/INTEL2018/intel/compilers_and_libraries_2018.2.199/linux/mkl/
    F95ROOT ?= $(MKLROOT)
    # Flags generated with the Intel Math Kernal Library Link Line Advisor
    # https://software.intel.com/en-us/articles/intel-mkl-link-line-advisor
    # Link to the int64 (lli) version of MKL for MATLAB compatibility
    ifeq ($(TOOLCHAIN),gcc)
      $(info Detected TOOLCHAIN=$(TOOLCHAIN))
      F95ROOT = $(MKLROOT)
      TUBS_FFLAGS += -fdefault-integer-8 -I${F95ROOT}/include/intel64/ilp64 -m64 -I${MKLROOT}/include
      MKL_LDFLAGS += ${F95ROOT}/lib/intel64/libmkl_blas95_ilp64.a
      MKL_LDFLAGS += ${F95ROOT}/lib/intel64/libmkl_lapack95_ilp64.a
      MKL_LDFLAGS += -Wl,--start-group ${MKLROOT}/lib/intel64/libmkl_gf_ilp64.a ${MKLROOT}/lib/intel64/libmkl_sequential.a ${MKLROOT}/lib/intel64/libmkl_core.a -Wl,--end-group -lpthread -lm -ldl
    else ifeq ($(TOOLCHAIN),intel)
      $(info Detected TOOLCHAIN=$(TOOLCHAIN))
      TUBS_FFLAGS += -i8 -I${MKLROOT}/include/intel64/ilp64 -I${MKLROOT}/include
      MKL_LDFLAGS += -i8 # Needed for MPI linking with INTEL MPI to go correctly
      MKL_LDFLAGS += ${MKLROOT}/lib/intel64/libmkl_blas95_ilp64.a
      MKL_LDFLAGS += ${MKLROOT}/lib/intel64/libmkl_lapack95_ilp64.a
      MKL_LDFLAGS += -Wl,--start-group ${MKLROOT}/lib/intel64/libmkl_intel_ilp64.a ${MKLROOT}/lib/intel64/libmkl_sequential.a ${MKLROOT}/lib/intel64/libmkl_core.a -Wl,--end-group -lpthread -lm -ldl
    else ifeq ($(TOOLCHAIN),pgi)
      $(info Detected TOOLCHAIN=$(TOOLCHAIN))
      TUBS_FFLAGS += -i8 -I${MKLROOT}/include
      MKL_LDFLAGS += ${F95ROOT}/lib/intel64/libmkl_blas95_ilp64.a
      MKL_LDFLAGS += ${F95ROOT}/lib/intel64/libmkl_lapack95_ilp64.a
      MKL_LDFLAGS += -Wl,--start-group ${MKLROOT}/lib/intel64/libmkl_intel_ilp64.a ${MKLROOT}/lib/intel64/libmkl_sequential.a ${MKLROOT}/lib/intel64/libmkl_core.a -Wl,--end-group -lpthread -lm -ldl
    else
      $(error Unknown TOOLCHAIN=$(TOOLCHAIN))
    endif
  else ifeq ($(TUBSCFG_MKL),0)
    $(info Not compiling with MKL, TUBSCFG_MKL=$(TUBSCFG_MKL))
  else
    $(info Unknown TUBSCFG_MKL $(TUBSCFG_MKL))
  endif

  LOCALCFG_ACTIVE := jet.uk
else
  $(error Unknown TUBS_CONFIG_PHASE $(TUBS_CONFIG_PHASE))
endif

