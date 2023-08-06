# This file is part of QLKNN-fortran
# You should have received the QLKNN-fortran LICENSE in the root of the project
$(call SUBPROJECT_depend, QLKNN CLAF90)

$(call SUBPROJECT_reset_local)
$(call SUBPROJECT_set_local_dir_here)

$(eval include $(QLKNNROOT_)/flags.make)

$(call LOCAL_add,\
	src/qlknn_hyper_standalone.f90 \
)

$(call LOCAL_mod_dep, src/qlknn_hyper_standalone.f90, kinds.mod )
