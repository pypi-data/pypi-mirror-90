# This file is part of QLKNN-fortran
# You should have received the QLKNN-fortran LICENSE in the root of the project
$(call SUBPROJECT_depend, QLKNN qlknn_test)

$(call SUBPROJECT_reset_local)
$(call SUBPROJECT_set_local_dir_here)

# lto gives trouble with fruit
ifeq ($(TOOLCHAIN),gcc)
  QLKNN_EXTRA_FFLAGS+=-fno-lto -Wno-error
endif
$(eval include $(QLKNNROOT_)/flags.make)
#
#$(call SUBPROJECT_set_linkflags, gcc, \
#	$(QLKNN_EXTRA_LFLAGS) \
#)

$(call LOCAL_add, \
	lib/src/fruit/src/fruit.f90 \
)

ifeq ($(TUBSCFG_MPI),1)
  $(call LOCAL_add, \
    lib/src/fruit/src/fruit_mpi.f90 \
  )
  $(call LOCAL_mod_dep, tests/test_jacobian_hyper.f90, fruit_mpi.mod fruit.mod fruit_util.mod setup_mpi.mod teardown_mpi.mod qlknn_types.mod qlknn_evaluate_nets.mod qlknn_disk_io.mod test_jacobian.mod )
  $(call LOCAL_mod_dep, tests/test_jacobian_hornnet.f90, fruit_mpi.mod fruit.mod fruit_util.mod setup_mpi.mod teardown_mpi.mod qlknn_types.mod qlknn_evaluate_nets.mod qlknn_disk_io.mod test_jacobian.mod )
  $(call LOCAL_mod_dep, tests/test_regression_hyper.f90, fruit_mpi.mod fruit.mod fruit_util.mod setup_mpi.mod teardown_mpi.mod qlknn_types.mod qlknn_evaluate_nets.mod qlknn_disk_io.mod test_regression.mod )
  $(call LOCAL_mod_dep, tests/test_imas.f90, fruit.mod fruit_util.mod qlknn_types.mod qlknn_evaluate_nets.mod qlknn_disk_io.mod )
else
  $(call LOCAL_mod_dep, tests/test_jacobian_hyper.f90, fruit.mod fruit_util.mod qlknn_types.mod qlknn_evaluate_nets.mod qlknn_disk_io.mod test_jacobian.mod )
  $(call LOCAL_mod_dep, tests/test_jacobian_hornnet.f90, fruit.mod fruit_util.mod qlknn_types.mod qlknn_evaluate_nets.mod qlknn_disk_io.mod test_jacobian.mod )
  $(call LOCAL_mod_dep, tests/test_regression_hyper.f90, fruit.mod fruit_util.mod qlknn_types.mod qlknn_evaluate_nets.mod qlknn_disk_io.mod test_regression.mod )
  $(call LOCAL_mod_dep, tests/test_regression_hyper.f90, fruit.mod fruit_util.mod qlknn_types.mod qlknn_evaluate_nets.mod qlknn_disk_io.mod )
endif

# Add new regression tests here
$(call LOCAL_add, \
	tests/test_dummy.f90 \
	tests/test_jacobian_hyper.f90 \
	tests/test_jacobian_hornnet.f90 \
	tests/test_regression_hyper.f90 \
	tests/test_imas.f90 \
	tests/setup_mpi.f90 \
	tests/teardown_mpi.f90 \
)
