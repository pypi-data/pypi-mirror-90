ifeq ($(TUBS_CONFIG_PHASE),2)
  # Use MPI?
  $(info $$TUBSCFG_MPI is [$(TUBSCFG_MPI)] for MODEL)

  ifeq ($(TUBSCFG_MPI),1)
    ifeq ($(TOOLCHAIN),gcc)
      FC = mpifort
    endif
    ifeq ($(TOOLCHAIN),intel)
      $(warning Build not working yet! Open an issue on gitlab.com/tci-dev/tubs if you need this or got it to work)
      FC = OMPI_FC=ifort mpifort
    endif
  endif # ~ TUBSCFG_MPI
  LINK = $(FC)

  LOCALCFG_ACTIVE := nersc.gov
endif

#EOF
