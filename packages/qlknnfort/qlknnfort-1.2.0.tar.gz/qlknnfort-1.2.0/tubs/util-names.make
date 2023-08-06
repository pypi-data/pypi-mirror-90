# util-names.make
# 
# Helpers for (consistently) getting full names of output files.

# Function: UTIL_target_of
#
# Compute the full name of a subproject's target. For example, 
#   $(call UTIL_target_of, myLib, staticlib)
# would return the full path of the output libmyLib.a.
# 
# Arguments: name, kind
define UTIL_target_of =
$(if ${UTILimpl_target_of_$(2)},$(call UTILimpl_target_of_$(2),$(1)),$(error Subproject "$(1)": kind "$2" not supported))
endef

define UTILimpl_target_of_staticlib =
$(LIBDEST)/lib$(1)-$(SYS).a
endef
define UTILimpl_target_of_app =
$(BINDEST)/$(1)-$(SYS).exe
endef

# Function: UTIL_obj_of
#
# Compute the name of the object file generated from a source file.
#
# Arguments: one or more full source file paths
define UTIL_obj_of =
$(foreach s,$1,$(BAKEDBUILDDIR)/$(subst /,_-_,$(subst $(TCI_MAKE_ROOT)/,,$s)).o)
endef

# Function: UTIL_mod_of
#
# Returns the list of output modules of a fortran source file. Also see the
# functions in `util-moddep.make`.
# 
# Arguments: one or more full fortran source file paths
define UTIL_mod_of =
$(foreach s,$1,$(call MOD_output_get,$s))
endef

#EOF vim:syntax=make:foldmethod=marker:ts=4:noexpandtab:
