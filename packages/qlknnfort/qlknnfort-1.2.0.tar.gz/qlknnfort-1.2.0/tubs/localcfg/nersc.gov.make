ifeq ($(TUBS_CONFIG_PHASE),2)
  # Use MPI?
  $(info $$TUBSCFG_MPI is [$(TUBSCFG_MPI)] for MODEL)

  ifeq ($(TUBSCFG_MPI),1)
    ifeq ($(TOOLCHAIN),gcc)
      # Run `module load PrgEnv-gnu openmpi` first
      $(warning Build not working yet! Open an issue on gitlab.com/tci-dev/tubs if you need this or got it to work)
      FC = mpifort
    endif
    ifeq ($(TOOLCHAIN),intel)
      # Run `module load PrgEnv-intel openmpi` first
      FC = mpifort
    endif
  endif # ~ TUBSCFG_MPI
  LINK = $(FC)

  LOCALCFG_ACTIVE := nersc.gov
endif

#EOF
