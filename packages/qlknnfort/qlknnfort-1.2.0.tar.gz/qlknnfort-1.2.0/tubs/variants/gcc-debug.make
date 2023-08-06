# Debug build with GCC/gfortran
#
# Includes run-time checks via (-fcheck=all and -ffpe-trap=invalid,zero,overflow)

TUBS_FFLAGS     ?= -march=native -g -Wall -fPIC -fopenmp -fcheck=all

# Formerly this included -ffpe-trap=invalid,zero,overflow. But TGLF relies on
# non-trapping behaviour; disabling this flag at a later time is tricky
# (currently, there's no -fno-fpe-trap, and a later -ffpe-trap= doesn't
# disable previously enabled flags.)

TUBS_LDFLAGS  ?= -fPIC -fopenmp

include $(TCI_MAKE_HERE)/variants/gcc_common.make

#EOF vim:syntax=make:foldmethod=marker:ts=4:noexpandtab:
