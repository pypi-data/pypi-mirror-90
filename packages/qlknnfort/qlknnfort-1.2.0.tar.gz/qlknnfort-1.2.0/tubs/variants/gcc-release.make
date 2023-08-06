ifneq ($(USERCFG_OPT),1)
  TUBSCFG_OPT += -O2
endif
TUBS_FFLAGS     ?= -march=native $(TUBSCFG_OPT) -Wall -fPIC -fopenmp -flto

# -flto : LTO seems to induce some crashes... ?

TUBS_LDFLAGS  ?= -march=native $(TUBSCFG_OPT) -fPIC -fopenmp -flto

include $(TCI_MAKE_HERE)/variants/gcc_common.make

#EOF vim:syntax=make:foldmethod=marker:ts=4:noexpandtab:
