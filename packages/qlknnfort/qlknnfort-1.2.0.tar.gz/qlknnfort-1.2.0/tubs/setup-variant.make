# setup-variant.make
# 
# Include "user" definitions. 

# Start TUBS config phase 1
TUBS_CONFIG_PHASE := 1

# Look for a usercfg. If it exists and defines multiple tubs
# phases, load it here for phase one. If not, warn the user and
# do not load anything
# User-overrides may be created by placing a `usercfg.make` in the top-level
# directory. This file *SHOULD NEVER* be checked in!
USERCFG_FILE := $(strip $(wildcard $(TCI_MAKE_ROOT)/usercfg.make))
ifeq ($(USERCFG_FILE),)
  USERCFG_ACTIVE = inactive
else
  USERCFG_PHASE_SPECIFICATION := $(shell grep TUBS_CONFIG_PHASE $(USERCFG_FILE))
  ifeq ($(USERCFG_PHASE_SPECIFICATION),)
    $(warning Warning! TUBS_CONFIG_PHASE not found in usercfg.make. Only loading once.)
  else
    include $(TCI_MAKE_ROOT)/usercfg.make
  endif
endif

# Apply 'local' settings (i.e., overrides for the current machine)
# Local settings are optional
include $(TCI_MAKE_HERE)/setup-localcfg.make

# Load the settings for the selected variant (toolchain + build). This
# must exist.
# 
# Note: $(SYS) was used in the original makefiles. We'll use the same name for
# now.
SYS := $(TOOLCHAIN)-$(BUILD)-$(TARGET_ENV)
ifeq ($(TUBSCFG_MPI),1)
  SYS := $(SYS)-mpi
endif
ifeq ($(TUBSCFG_MKL),1)
  SYS := $(SYS)-mkl
endif

include $(TCI_MAKE_HERE)/variants/$(TOOLCHAIN)-$(BUILD).make

# Start TUBS config phase two
TUBS_CONFIG_PHASE := 2
# Load local settings for phase two. Each localcfg should define both phase one
# and phase two if it exists
include $(TCI_MAKE_HERE)/setup-localcfg.make

# Then check if there are any special environment settings. Currently not autodetected
-include $(TCI_MAKE_HERE)/environments/$(TARGET_ENV).make

# Finally, load the usercdf again, for phase two if it defined phases, or just
# normally if it did not.
ifneq ($(USERCFG_FILE),)
  include $(TCI_MAKE_ROOT)/usercfg.make
  USERCFG_ACTIVE = active
endif

#EOF vim:syntax=make:foldmethod=marker:ts=4:noexpandtab:
