ifneq (3.82,$(firstword $(sort $(MAKE_VERSION) 3.82)))
  $(error Detected make version $(MAKE_VERSION), need at least 3.82)
endif
TCI_MAIN_MAKE_HERE := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))

# Include all definitions, but only if this wasn't already done. `all.make`
# signales its inclusion by setting `TCI_MAIN_MAKE_DONE` at its end.
#
# Further, the flag `TCI_MAIN_MAKE_FIRST` informs the user if this was the
# first inclusion of `main.make`. This may be used to conditional call the
# functions `PROJECT_setup` and `PROJECT_finalize` from non-toplevel Makefiles.
ifndef TCI_MAIN_MAKE_DONE
TCI_MAIN_MAKE_FIRST := 1
include $(TCI_MAIN_MAKE_HERE)/all.make
else
TCI_MAIN_MAKE_FIRST := 0
endif

#EOF vim:syntax=make:foldmethod=marker:ts=4:noexpandtab:
