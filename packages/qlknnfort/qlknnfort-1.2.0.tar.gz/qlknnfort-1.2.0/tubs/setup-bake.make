# setup-bake.make
#
# Precompute commonly used values based on several configuration options. Also
# invoke the "callbacks" defined by the variants (see TOOL_bake_*).

BAKEDLIBDEST   := $(LIBDEST)/$(SYS)
BAKEDMODDEST   := $(MODDEST)/$(SYS)

BAKEDBUILDDIR  := $(BUILDDIR)/$(SYS)


$(eval $(call TOOL_bake_fort))
$(eval $(call TOOL_bake_ar))
$(eval $(call TOOL_bake_link))


# If VERBOSE is set, show the full commands that are executed. Make prints the
# commands by default; this may be suppressed by prefixing commands with "@".
# We use the variable V_, which evalutes to either nothing (commands will be
# printed) or to "@" (printing of commands suppressed). 
#
# Usage:
# foo : bar
# 	$(V_)somecommand -o $@ -i $<
ifdef VERBOSE
V_             := 
else
V_             := @
endif

#EOF vim:syntax=make:foldmethod=marker:ts=4:noexpandtab:
