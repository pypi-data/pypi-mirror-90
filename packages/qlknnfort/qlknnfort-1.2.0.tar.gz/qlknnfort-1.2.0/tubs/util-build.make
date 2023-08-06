# util-build.make
#
# Helpers for building sources.

# FUNCTION: UTIL_build
#
# Build the specified source file.
#
# Arguments: source file (full path), optional informational subproject name
define UTIL_build =
$(or $(call UTIL_build_$(suffix $1),$1,$(call TARGET_get_extra_flags,$1),$2),$(error "$(notdir $1) $2": do not know how to build $(suffix $1)-files))
endef

# $1: Source file (full path)
# $2: Extra flags of source file
# $3: Subproject name
define UTIL_build_.f90 =
$(call UTIL_mod_of,$1) : $(call UTIL_obj_of,$1)
$(call TOOL_invoke_fort,$1,$(call UTIL_obj_of,$1),$2,$(call MOD_depend_get,$1)  $(call SRC_depend_get,$1),$3)
endef
define UTIL_build_.F90 =
$(call UTIL_mod_of,$1) : $(call UTIL_obj_of,$1)
$(call TOOL_invoke_fort,$1,$(call UTIL_obj_of,$1),$2,$(call MOD_depend_get,$1)  $(call SRC_depend_get,$1),$3)
endef
define UTIL_build_.f =
$(call UTIL_mod_of,$1) : $(call UTIL_obj_of,$1)
$(call TOOL_invoke_fort,$1,$(call UTIL_obj_of,$1),$2,$(call MOD_depend_get,$1) $(call SRC_depend_get,$1),$3)
endef


# FUNCTION: UTIL_link
#
# Link the specified target from the specified source files/objects.
#
# Arguments: target kind, target full path, source object full paths, extra
# dependencies (any valid make target), optional informational subproject name
define UTIL_link =
$(or $(call UTIL_link_$1,$2,$3,$(filter-out -l%,$4),$(filter -l%,$4) $(call TARGET_get_extra_flags,$2),$5),$(error "$(notdir $2) $5": do not know how to link a $1))
endef

define UTIL_link_staticlib =
$(call TOOL_invoke_ar,$1,$2,$5)
endef
define UTIL_link_app =
$(call TOOL_invoke_link,$1,$2,$3,$4,$5)
endef

#EOF vim:syntax=make:foldmethod=marker:ts=4:noexpandtab:
