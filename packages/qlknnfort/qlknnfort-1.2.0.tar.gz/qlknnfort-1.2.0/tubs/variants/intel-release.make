TUBSCFG_OPT += -O1
TUBS_FFLAGS ?= -fPIC $(TUBSCFG_OPT)
# When doing LTO, also put optimization flags in the link step
TUBS_LDFLAGS ?= -fPIC $(TUBSCFG_OPT)

include $(TCI_MAKE_HERE)/variants/intel_common.make


#EOF vim:syntax=make:foldmethod=marker:ts=4:noexpandtab:
