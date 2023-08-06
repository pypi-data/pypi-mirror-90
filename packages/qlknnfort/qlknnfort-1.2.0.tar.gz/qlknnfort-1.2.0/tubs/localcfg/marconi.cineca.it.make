# vim:filetype=make

# This is for the Marconi CINECA cluster
ifeq ($(TUBS_CONFIG_PHASE),1)
  undefine FC # Marconi's intel environment does not set FC correctly
else
  ifneq ($(TUBS_CONFIG_PHASE),2)
    $(error Unknown TUBS_CONFIG_PHASE $(TUBS_CONFIG_PHASE))
  endif
  # Use MPI?
  $(info $$TUBSCFG_MPI is [$(TUBSCFG_MPI)] for MODEL)

  ifeq ($(TUBSCFG_MPI),1)
    ifeq ($(TOOLCHAIN),gcc)
      FC = mpifort
      LINK = mpifort
    endif
    ifeq ($(TOOLCHAIN),intel)
      FC = mpiifort
      LINK = mpiifort
    endif
  endif # ~ TUBSCFG_MPI

  LOCALCFG_ACTIVE := marconi.cineca.it
endif

#EOF
