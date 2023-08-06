# Figure out optimization flags for your architecture using pgfortran -help -fast
TUBSCFG_OPT += -O1 -Mlre -Mautoinline
TUBS_FFLAGS ?= $(TUBSCFG_OPT) -fPIC -mp

TUBS_LDFLAGS  ?= $(TUBSCFG_OPT) -fPIC -mp

include $(TCI_MAKE_HERE)/variants/pgi_common.make

#EOF vim:syntax=make:foldmethod=marker:ts=4:noexpandtab:
