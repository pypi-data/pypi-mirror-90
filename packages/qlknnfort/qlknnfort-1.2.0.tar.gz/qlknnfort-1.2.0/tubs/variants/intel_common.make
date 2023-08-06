ifeq ($(origin FC), $(filter $(origin FC),default undefined))
  FC       := ifort
endif

FSTD_DEF   :=
FSTD_95    := -stand f95
FSTD_03    := -stand f03
FSTD_08    := -stand f08


LINK       ?= ifort

# Detect ifort version
IFORT_VERSION := $(shell $(FC) --version 2> /dev/null | head -n 1 | cut -d' ' -f 3)
ifeq ($(IFORT_VERSION),)
  IFORT_VERSION = null
  IFORT_MAJOR_VERSION = null
else
  IFORT_MAJOR_VERSION := $(shell echo $(IFORT_VERSION) 2> /dev/null | cut -d'.' -f 1)
endif

ifeq ($(shell expr $(IFORT_MAJOR_VERSION) \>= 18), 1)
   TUBS_LDFLAGS += -qopenmp
   TUBS_FFLAGS += -qopenmp
else
   TUBS_LDFLAGS += -openmp
   TUBS_FFLAGS += -openmp
endif
#-fstack-protector-all -qopenmp -lssp

LNKGRPBEG  ?= -Wl,-\(
LNKGRPEND  ?= -Wl,-\)
MODULE_FLAG := -module

ifeq ($(origin AR), default)
  AR         := ar rcu
endif

define TOOL_bake_fort =
BAKEDFSTD    := $($(FSTD))
BAKEDFPATH   := $(foreach p,$(FPATH),-I$p)
BAKEDFDEFS   := $(foreach d,$(FDEFS),-D$p)
BAKEDFFLAGS  := $$(BAKEDFSTD) $(TUBS_FFLAGS) $(FFLAGS) $$(MODULE_FLAG) $$(BAKEDMODDEST) $$(BAKEDFDEFS) $$(BAKEDFPATH)
endef
define TOOL_bake_ar =

endef
define TOOL_bake_link =
BAKEDLPATH   := -L$$(LIBDEST) $(foreach p,$(LNKPATH),-L$p)
BAKEDLFLAGS  := $$(BAKEDFSTD) $$(TUBS_LDFLAGS) $$(LDFLAGS) $$(BAKEDLPATH)  $(foreach l,$(LNKLIBS),-l$l)
endef

define TOOL_invoke_fort =
$2 : $1 $4 | meta-tool-setup
	$$(call UTIL_msg_fort,$(notdir $1),$5)
	$(V_)$$(FC) $$(BAKEDFFLAGS) $3 -c $$< -o $$@
endef
define TOOL_invoke_ar =
$1 : $2 | meta-tool-setup
	$$(call UTIL_msg_ar,$(notdir $1),$3,$(words $2))
	$(V_)-rm $$@ 2>/dev/null; true
	$(V_)$$(AR) $$@ $$^
endef
define TOOL_invoke_link =
$1 : $2 $3 | meta-tool-setup
	$$(call UTIL_msg_link,$(notdir $1),$5,$(words $2))
	$(V_)$$(LINK) $$(BAKEDLFLAGS) -o $$@ $2 $$(LNKGRPBEG) $4 $$(patsubst lib%.a,-l%,$$(notdir $3)) $$(LNKGRPEND) $$(MKL_LDFLAGS)
endef

#EOF vim:syntax=make:foldmethod=marker:ts=4:noexpandtab:
