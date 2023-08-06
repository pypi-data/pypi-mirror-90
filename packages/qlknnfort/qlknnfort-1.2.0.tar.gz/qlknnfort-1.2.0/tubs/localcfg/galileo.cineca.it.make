# vim:filetype=make
#
# This is the EF Gateway (check `hostname -f`)
# Need to support both itmenv and imasenv
ifeq ($(TUBS_CONFIG_PHASE),2)
  # Use MPI?
  $(info $$TUBSCFG_MPI is [$(TUBSCFG_MPI)] for MODEL)

  ifeq ($(TUBSCFG_MPI),1)
    ifeq ($(TOOLCHAIN),gcc)
      FC = mpiifort
      LINK = mpiifort
    endif
    ifeq ($(TOOLCHAIN),intel)
      FC = mpiifort
      LINK = mpiifort
    endif
  endif # ~ TUBSCFG_MPI

  LOCALCFG_ACTIVE := galileo.cineca.it
endif

#EOF
