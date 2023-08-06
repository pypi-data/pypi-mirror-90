ifeq ($(TUBS_CONFIG_PHASE),1)
  ifeq ($(BUILD),release)
    ifeq ($(TOOLCHAIN),pgi)
      # -Mvect forces -O2, do not use
      TUBSFFLAGS_OPT ?= -Mflushz -Mcache_align
    endif
  endif
else
  # Use MPI?
  ifeq ($(TUBSCFG_MPI),1)
    ifeq ($(TOOLCHAIN),gcc)
      FC = mpif90
      LINK = mpif90 - lnag_nag
    endif
    ifeq ($(TOOLCHAIN),intel)
      FC = mpif90
      LINK = mpif90
    endif
    ifeq ($(TOOLCHAIN),pgi)
      FC = mpif90
      LINK = mpif90
    endif
  endif # ~ TUBSCFG_MPI

  LOCALCFG_ACTIVE := hpc.l
endif

#EOF
