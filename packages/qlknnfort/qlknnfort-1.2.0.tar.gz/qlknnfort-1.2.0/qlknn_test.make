# This file is part of QLKNN-fortran
# You should have received the QLKNN-fortran LICENSE in the root of the project
$(call SUBPROJECT_depend, QLKNN)

$(call SUBPROJECT_reset_local)
$(call SUBPROJECT_set_local_dir_here)

$(eval include $(QLKNNROOT_)/flags.make)

$(call LOCAL_add, \
	tests/test_jacobian.f90 \
	tests/test_regression.f90 \
)

$(call LOCAL_mod_dep, tests/test_jacobian.f90, qlknn_types.mod qlknn_evaluate_nets.mod qlknn_disk_io.mod )
$(call LOCAL_mod_dep, tests/test_regression.f90, qlknn_types.mod qlknn_evaluate_nets.mod qlknn_disk_io.mod )
