ifeq ($(TUBS_CONFIG_PHASE),1)
else
  ifneq ($(TUBS_CONFIG_PHASE),2)
    $(error Unknown TUBS_CONFIG_PHASE $(TUBS_CONFIG_PHASE))
  endif
  # Use MPI?
  ifeq ($(TUBSCFG_MPI),1)
    ifeq ($(TOOLCHAIN),intel)
      FC = mpiifort
    endif
  endif # ~ TUBSCFG_MPI
  LINK = $(FC)
  LOCALCFG_ACTIVE := cobra
endif

#EOF
