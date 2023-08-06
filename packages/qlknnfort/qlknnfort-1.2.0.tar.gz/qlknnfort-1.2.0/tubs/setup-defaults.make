# setup-defaults.make
#
# Setup default settings for various options.

# Default target information
BUILD         ?= release
TOOLCHAIN     ?= intel

# Build options
TUBSCFG_MPI  ?= 1
TUBSCFG_MKL  ?= 0

# Make output control
VERBOSE       ?= 
NOCOLOR       ?= 

# Directories
LIBDEST       ?= $(TCI_MAKE_ROOT)/lib
BINDEST       ?= $(TCI_MAKE_ROOT)/bin
MODDEST       ?= $(TCI_MAKE_ROOT)/include

BUILDDIR      ?= $(TCI_MAKE_ROOT)/build


# Fortran compiler flags
# These are informational only; the settings for the selected TOOLCHAIN/BUILD
# are loaded in setup-variant.make!

#FC         ?=         # the fortran compiler
FSTD          ?= FSTD_DEF

#FFLAGS       ?=         # global fortran compiler flags

#FPATH        ?=         # list of include paths
#FDEFS        ?=         # list of predefined macros (.Fnn only, presumably)

FSTD_DEF      :=
FSTD_95       :=
FSTD_03       :=
FSTD_08       :=

# Linker flags
# Informational only; see above.

#LINK         ?= $(FC)

#LNKFLAGS     ?= 

#LNKPATH      ?= 
LNKLIBS       += dl

#LNKGRPBEG     ?=
#LNKGRPEND     ?=

#AR           ?= ar rcu

# Other tools
# Make sure that we use the proper `echo` and  `printf` instead of potential
# shell built-ins (*cough*zsh*cough). The built-ins may not support `-e` or
# the escape sequence \e.
ECHO          ?= $(shell which echo) -e
PRINTF        ?= $(shell which printf)

# Environment
HOSTNAME      := $(shell hostname)
ifeq ($(origin HOSTFULL), undefined)
HOSTFULL      := $(shell hostname -f)
else
$(warning Warning! HOSTFULL defined before TUBS! Using "$(HOSTFULL)")
endif

PLATFORM      := $(shell uname | tr '[:upper:]' '[:lower:]')
TARGET_ENV    ?= default

# Misc.
LOCALCFG_ACTIVE := (none)

#EOF vim:syntax=make:foldmethod=marker:ts=4:noexpandtab:
