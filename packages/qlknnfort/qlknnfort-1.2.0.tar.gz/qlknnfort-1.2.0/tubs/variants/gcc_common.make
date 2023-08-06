# Debug build with GCC/gfortran
#
# Includes run-time checks via (-fcheck=all and -ffpe-trap=invalid,zero,overflow)

ifeq ($(origin FC), default)
  FC       := gfortran
endif

# Formerly this included -ffpe-trap=invalid,zero,overflow. But TGLF relies on
# non-trapping behaviour; disabling this flag at a later time is tricky
# (currently, there's no -fno-fpe-trap, and a later -ffpe-trap= doesn't
# disable previously enabled flags.)

FSTD_DEF   :=
FSTD_95    := -std=f95
FSTD_03    := -std=f2003
FSTD_08    := -std=f2008

LINK       ?= gfortran

LNKGRPBEG  ?= -Wl,-\(
LNKGRPEND  ?= -Wl,-\)
MODULE_FLAG := -J


# Use gcc-ar in case we want to do LTO
ifeq ($(origin AR), default)
  AR := gcc-ar rcu
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
BAKEDLFLAGS  := $$(BAKEDFSTD) $$(TUBS_LDFLAGS) $$(LDFLAGS) $$(BAKEDLPATH) $(foreach l,$(LNKLIBS),-l$l)
endef

# $1: Source file (full path)
# $2: Object file
# $3: Extra flags of source file
# $4: List of Module dependencies + SRC depedencies
# $5: Subproject name
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
