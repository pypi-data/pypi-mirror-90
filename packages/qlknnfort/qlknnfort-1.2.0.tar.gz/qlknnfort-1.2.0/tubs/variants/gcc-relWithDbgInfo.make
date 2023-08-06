FFLAGS_OPT += -O2
TUBS_FFLAGS     ?= -march=native -g $(FFLAGS_OPT) -Wall -fPIC -fopenmp -flto

TUBS_LDFLAGS  ?= -march=native -g $(FFLAGS_OPT) -fPIC -fopenmp -flto

include $(TCI_MAKE_HERE)/variants/gcc_common.make

#EOF vim:syntax=make:foldmethod=marker:ts=4:noexpandtab:
