$(call SUBPROJECT_depend, karel)

$(call SUBPROJECT_reset_local)
$(call SUBPROJECT_set_local_dir_here)

$(call LOCAL_add,\
	src/karel_standalone.f90 \
)

$(call LOCAL_mod_dep, src/karel_standalone.f90, karel_types.mod )
