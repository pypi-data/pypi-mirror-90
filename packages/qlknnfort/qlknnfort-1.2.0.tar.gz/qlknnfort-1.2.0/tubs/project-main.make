# project-main.make
#
# Setup/finalize a project. These are function generate global make rules and
# must only be called once per make-invocation. In particular, `PROJECT_setup`
# should be called before any other make rules are defined. `PROJECT_finalize`
# should be called after all subproject definitions have been processed.
# 

# Internal: all functions appended to the PROJECTimpl_FINALIZE_ACTS variable
# will be called by `PROJECT_finalize`.
PROJECTimpl_FINALIZE_ACTS := PROJECT_finalize_impl_

# FUNCTION: PROJECT_setup
#
# Setup global make targets/rules. This includes the entry points "all",
# "clean" and "help". `PROJECT_setup` should be called *before* any make rules
# are defined, and before defining any subprojects. `PROJECT_setup` may only be
# called once.
#
# "realclean" is just an alias to "clean". "realclean" was used in the original
# makefiles.
#
# Arguments: (none)
define PROJECT_setup =
$(eval $(call PROJECT_setup_impl_))
endef
define PROJECT_setup_impl_ = 
PROJECT_TARGETS := 

all : meta-print meta-build-all

clean : meta-clean-all

realclean : meta-clean-all

help : meta-print-help

overview : meta-print-overview

endef

# FUNCTION: PROJECT_finalize
#
# Generate rules that invoke subprojects. `PROJECT_finalize` must be called
# after all subprojects are defined. `PROJECT_finalize` may only be called
# once.
#
# Arguments: (none)
define PROJECT_finalize = 
$(foreach fin,$(PROJECTimpl_FINALIZE_ACTS),$(eval $(call $(fin))))
endef
define PROJECT_finalize_impl_ =
$(call TOOL_additional_cleanup)

meta-print : meta-print-shortcfg meta-print-messages

meta-build-all : $$(foreach tgt,$$(PROJECT_TARGETS),meta-build-$$(tgt))

meta-clean-all : $$(foreach tgt,$$(PROJECT_TARGETS),meta-clean-$$(tgt)) $$(TOOL_ADDITIONAL_CLEANUP) meta-clean-dirs

endef

#EOF vim:syntax=make:foldmethod=marker:ts=4:noexpandtab:
