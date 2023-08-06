ifeq ($(origin FC), default)
  FC       := pgfortran
endif

FSTD_DEF   :=
FSTD_95    := -stand f95
FSTD_03    := -stand f03
FSTD_08    :=             # error: standard not found :-(


LINK       ?= pgfortran

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
BAKEDFFLAGS  := $$(BAKEDFSTD) $(TUBS_FFLAGS) $(FFLAGS) $(MODULE_FLAG) $$(BAKEDMODDEST) $$(BAKEDFDEFS) $$(BAKEDFPATH)
endef
define TOOL_bake_ar =

endef
define TOOL_bake_link =
BAKEDLPATH   := -L$$(LIBDEST) $(foreach p,$(LNKPATH),-L$p)
BAKEDLFLAGS  := $$(BAKEDFSTD) $$(TUBS_LDFLAGS) $$(LDFLAGS) $$(BAKEDLPATH) $(foreach l,$(LNKLIBS),-l$l)
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
