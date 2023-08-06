# previous jet cluster with some issues on the mpi install
# pre Heimdall that machine was actually unnamed
# Now it is named 'Freia', 
ifeq ($(TUBS_CONFIG_PHASE),1)
  include $(TCI_MAKE_HERE)/localcfg/jet.uk.make
else
  ifeq ($(TUBS_CONFIG_PHASE),2)
    include $(TCI_MAKE_HERE)/localcfg/jet.uk.make
    $(warning Loaded "jet.uk" config as well)
    LOCALCFG_ACTIVE := hpc.l
  else
    $(error Unknown TUBS_CONFIG_PHASE $(TUBS_CONFIG_PHASE))
  endif
endif

#EOF vim:syntax=make:foldmethod=marker:ts=4:noexpandtab:
