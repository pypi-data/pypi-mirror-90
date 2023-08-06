ifeq ($(TUBS_CONFIG_PHASE),2)
  # Use MPI?
  ifeq ($(TUBSCFG_MPI),1)
    ifeq ($(TOOLCHAIN),gcc)
      TUBS_FFLAGS     += $(shell mpifort -showme:compile)
      TUBS_LDFLAGS  += $(shell mpifort -showme:link)
    endif
  endif # ~ TUBSCFG_MPI

  LOCALCFG_ACTIVE := glyph
endif

#EOF
