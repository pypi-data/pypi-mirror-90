TCI_MAKE_HERE     := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))
TCI_MAKE_ROOT     := $(abspath $(dir $(TCI_MAKE_HERE)))

# Make and spaces is weird.
# See http://stackoverflow.com/a/4735256
TCI_MAKE_NULL     := 
TCI_MAKE_SPACE     = ${TCI_MAKE_NULL} ${TCI_MAKE_NULL}
${TCI_MAKE_SPACE}  = ${TCI_MAKE_SPACE} 

# Setup: build variables and machine configuration.
include $(TCI_MAKE_HERE)/setup-defaults.make
include $(TCI_MAKE_HERE)/setup-variant.make
include $(TCI_MAKE_HERE)/setup-bake.make

# Utilities
include $(TCI_MAKE_HERE)/util-colors.make
include $(TCI_MAKE_HERE)/util-messages.make
include $(TCI_MAKE_HERE)/util-names.make
include $(TCI_MAKE_HERE)/util-moddep.make
include $(TCI_MAKE_HERE)/util-srcdep.make
include $(TCI_MAKE_HERE)/util-extraflag.make
include $(TCI_MAKE_HERE)/util-build.make
include $(TCI_MAKE_HERE)/util-clean.make

# Project stuff
include $(TCI_MAKE_HERE)/project-main.make
include $(TCI_MAKE_HERE)/project-subproj.make
include $(TCI_MAKE_HERE)/project-dirs.make
include $(TCI_MAKE_HERE)/project-meta.make

# Done.
TCI_MAIN_MAKE_DONE := 1

#EOF vim:syntax=make:foldmethod=marker:ts=4:noexpandtab:
