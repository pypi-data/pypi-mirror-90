# util-extraflag.make
#
# Helpers for dealing with per-target extra build flags. These rely on the
# actual build rules checking for extra flags via `TARGET_get_extra_flags`!

# Function: TARGET_add_extra_flags
#
# Add extra flags for the specified target.
#
# Arguments: target (full path), extra flags
define TARGET_add_extra_flags =
$(eval TARGET_EXTRAFLAGS_$(strip $1) += $2)
endef

# FUNCTION: TARGET_get_extra_flags
#
# Retrieve extra flags for the specified target.
#
# Arguments: target (full path)
define TARGET_get_extra_flags =
$(TARGET_EXTRAFLAGS_$(strip $1))
endef

#EOF vim:syntax=make:foldmethod=marker:ts=4:noexpandtab:
