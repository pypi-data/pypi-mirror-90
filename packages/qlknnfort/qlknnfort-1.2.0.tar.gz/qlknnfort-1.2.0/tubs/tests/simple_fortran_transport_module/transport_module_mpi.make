$(call SUBPROJECT_reset_local)
$(call SUBPROJECT_set_local_dir_here)

ifeq ($(origin ROOT_), undefined)
  ROOT_ := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))
endif

$(call LOCAL_add, \
	src/karel_types.f90 \
	src/karel_model.f90 \
	src/daan_correction.f90 \
)

# The .mod dependencies must match the .mod filename that was generated
$(call LOCAL_mod_dep, src/karel_model.f90, karel_types.mod )
$(call LOCAL_mod_dep, src/karel_model.f90, daan_correction.mod )
