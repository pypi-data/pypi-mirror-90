# project-meta.make
# 
# Additional misc. global targets.

PROJECTimpl_FINALIZE_ACTS += PROJECTimpl_meta_print PROJECTimpl_meta_targets
PROJECTimpl_META_MESSAGES := 

# FUNCTION: PROJ_message
# 
# Output messages at the beginning of the build.
# 
# Arguments: string
define PROJ_message =
$(eval PROJECTimpl_META_MESSAGES += $(1)\\n)
endef

define PROJimpl_overview_ = 
$(patsubst /%,%,$(subst $(TCI_MAKE_ROOT),,$(MAKEFILE_LIST)))
endef

define PROJECTimpl_meta_print =
meta-print-shortcfg :
	@$(ECHO) "$(TCIfmtBLD)TCI | Summary:$(TCIfmtRST)"
	@$(ECHO) "  - toolchain: $(TCIfmtYEL)$(TOOLCHAIN)$(TCIfmtRST)"
	@$(ECHO) "  - config: $(TCIfmtYEL)$(BUILD)$(TCIfmtRST)"
	@$(ECHO) "  - on $(TCIfmtYEL)$(HOSTFULL)$(TCIfmtRST) with localcfg $(TCIfmtYEL)$(LOCALCFG_ACTIVE)$(TCIfmtRST)"
	@$(ECHO) "  - with environment $(TCIfmtYEL)$(TARGET_ENV)$(TCIfmtRST)"
	@$(ECHO) "  - and usercfg $(TCIfmtYEL)$(USERCFG_ACTIVE)$(TCIfmtRST)"
	@$(ECHO) "  - selected subprojects: $(TCIfmtGRY)$(SUBPROJECTS)$(TCIfmtRST)"
	@$(ECHO) "  - config: $(TCIfmtYEL)TUBSCFG_MPI$(TCIfmtRST)=$(TCIfmtBLD)$(TUBSCFG_MPI)$(TCIfmtRST)"
	@$(ECHO) "            $(TCIfmtYEL)TUBSCFG_MKL$(TCIfmtRST)=$(TCIfmtBLD)$(TUBSCFG_MKL)$(TCIfmtRST)"
	@$(ECHO) ""

meta-print-messages : | meta-print-shortcfg
	@$(ECHO) "$(TCIfmtBLD)TCI | Messages:$(TCIfmtRST)"
	@$(ECHO) "$(PROJECTimpl_META_MESSAGES)"

meta-print-help : 
	@$(ECHO) "Synopsis: make [-jN] [-f Makefile] [TOOLCHAIN=<tc>] [BUILD=<bld>] [...]"
	@$(ECHO) ""
	@$(ECHO) "The toolchain <tc> and the build configuration <bld> together determine"
	@$(ECHO) "the build variant. Each build variant is defined in 'defs/variants/'."
	@$(ECHO) "The default values are TOOLCHAIN=gcc and BUILD=debug. Common alternatives"
	@$(ECHO) "include BUILD=release, which enables optimizations, and TOOLCHAIN=intel"
	@$(ECHO) "which uses the Intel compiler tools (ifort et al.)."
	@$(ECHO) ""
	@$(ECHO) "Other common options include:"
	@$(ECHO) "  - VERBOSE=1       : print executed commands fully"
	@$(ECHO) "  - NOCOLOR=1       : do not colorize output"
	@$(ECHO) ""
	@$(ECHO) "The following build time options are available"
	@$(ECHO) "  - TUBSCFG_MPI=0  : Don't include MPI codes"
	@$(ECHO) "(Warning: 'make clean' first when changing build-time options)"
	@$(ECHO) ""
	@$(ECHO) "Special targets (via 'make <target>'):"
	@$(ECHO) "   help      : print this message"
	@$(ECHO) "   overview  : generate an overview of included subprojects/makefiles"
	@$(ECHO) ""
	@$(ECHO) "For additional information, please read 'defs/readme.md'."

meta-print-overview : 
	@$(ECHO) "$(call PROJimpl_overview_)" | $(TCI_MAKE_HERE)/overview.sh $(NOCOLOR)

endef


define PROJECTimpl_meta_targets =
meta-tool-setup : meta-build-dirs | meta-print

meta-build-dirs : $(BAKEDBUILDDIR) $(BAKEDMODDEST) $(LIBDEST) $(BINDEST)

meta-clean-dirs :
	$(call UTIL_clean_dir,$(BAKEDBUILDDIR),<$(SYS)>)
	$(call UTIL_clean_dir,$(BAKEDMODDEST),<$(SYS)>)
	$(call UTIL_clean_dir,$(BUILDDIR),_)
	$(call UTIL_clean_dir,$(MODDEST),_)
	$(call UTIL_clean_dir,$(LIBDEST),_)
	$(call UTIL_clean_dir,$(BINDEST),_)
endef

#EOF vim:syntax=make:foldmethod=marker:ts=4:noexpandtab:
