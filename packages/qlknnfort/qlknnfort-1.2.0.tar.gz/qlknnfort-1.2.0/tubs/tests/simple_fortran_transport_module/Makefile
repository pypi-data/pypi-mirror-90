# Boilerplate: include the make definitions
ROOT_ := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))
$(info $(ROOT_))

# Include all tubs definitions
TCI_MAKE_ROOT := $(ROOT_)
include $(ROOT_)/../../main.make

# Boilerplate: if invoked directly (and not via the root Makefile), generate
# the neccessary standard rules
ifeq ($(TCI_MAIN_MAKE_FIRST),1)
$(call PROJECT_setup)
endif

# Boilerplate: if invoked directly (and not via the root Makefile), generate
# the neccessary standard rules
ifeq ($(TCI_MAIN_MAKE_FIRST),1)
$(call PROJECT_setup)
endif

$(call SUBPROJECT_open,karel,staticlib)
include $(ROOT_)/transport_module_mpi.make
$(call SUBPROJECT_close)

$(call SUBPROJECT_open,karel_standalone,app)
include $(ROOT_)/karel_standalone.make
$(call SUBPROJECT_close)

# Boilerplate: if invoked directly (and not via the root Makefile), generate
# the build rules here
ifeq ($(TCI_MAIN_MAKE_FIRST),1)
$(call PROJECT_finalize)
endif

# Dump all variables
# Based on https://www.cmcrossroads.com/article/dumping-every-makefile-variable
# Basically, for every defined variable the expanded and defined values are
# are printed out. Some variables are skipped, as on expansion they actually
# run functions.
.PHONY: printvars
ignore_printvar=PROJECT_finalize PROJECT_setup SUBPROJECT_close SUBPROJECT_close_impl_ SUBPROJECT_open SUBPROJECT_close_impl_ SUBPROJECT_open_impl_ UTIL_build UTIL_link UTIL_target_of
printvars:
	@$(foreach V,$(sort $(.VARIABLES)), $(if $(filter-out .VARIABLES $(ignore_printvar) $      (filter-out environment% default automatic,$(origin $V)), $V),$(info $V=$($V) ($(value $V      )))))
	@$(foreach V,$(ignore_printvar), $(info Ignored $V))
