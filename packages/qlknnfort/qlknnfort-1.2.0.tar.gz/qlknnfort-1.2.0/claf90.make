# This file is part of QLKNN-fortran
# You should have received the QLKNN-fortran LICENSE in the root of the project
$(call SUBPROJECT_reset_local)
$(call SUBPROJECT_set_local_dir_here)

ifeq ($(TOOLCHAIN),gcc)
  QLKNN_EXTRA_FFLAGS+=-Wno-error
endif
$(eval include $(QLKNNROOT_)/flags.make)

$(call LOCAL_add, \
	lib/src/CLAF90/kinds.f90 \
	lib/src/CLAF90/cla.f90 \
)

$(call LOCAL_mod_dep, lib/src/CLAF90/cla.f90, kinds.mod )
# ⋅⋅⋅lib/src/CLAF90/cla_test.g90
