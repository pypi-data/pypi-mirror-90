# util-srcdep.make
#
# See util-moddep.make for longwinded stuff. This tracks raw dependencies. This
# is useful to deal with #include/INCLUDE chains.
#
# SRC_depend_add requires abslute paths.
#
# TODO: merge this with moddep.make
define SRC_depend_add =
$(eval SRC_DEPEND_$(strip $1) += $(foreach d,$2,$(strip $d)))
endef
define SRC_depend_get =
$(SRC_DEPEND_$(strip $1))
endef

#EOF vim:syntax=make:foldmethod=marker:ts=4:noexpandtab:
