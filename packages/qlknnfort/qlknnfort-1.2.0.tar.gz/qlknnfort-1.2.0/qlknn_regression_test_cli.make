# This file is part of QLKNN-fortran
# You should have received the QLKNN-fortran LICENSE in the root of the project
$(call SUBPROJECT_depend, QLKNN qlknn_test CLAF90)

$(call SUBPROJECT_reset_local)
$(call SUBPROJECT_set_local_dir_here)

$(eval include $(QLKNNROOT_)/flags.make)

$(call LOCAL_add,\
	src/test_regression_cli.f90 \
)

$(call LOCAL_mod_dep, src/test_regression_cli.f90, cla.mod kinds.mod qlknn_types.mod qlknn_disk_io.mod test_regression.mod )
