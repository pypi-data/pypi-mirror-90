# This file is part of QLKNN-fortran
# You should have received the QLKNN-fortran LICENSE in the root of the project
$(call SUBPROJECT_reset_local)
$(call SUBPROJECT_set_local_dir_here)
ifeq ($(origin QLKNNROOT_), undefined)
QLKNNROOT_ := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))
endif

# Local QLKNN flags
include $(QLKNNROOT_)/flags.make

# Fortran files for QLKNN
$(call LOCAL_add, \
	src/core/qlknn_disk_io.f90 \
	src/core/qlknn_primitives.f90 \
	src/core/qlknn_types.f90 \
	src/core/qlknn_victor_rule.f90 \
	src/core/qlknn_error_filter.f90 \
	src/qlknn_python.f90 \
)
#src/qlknn_mpi_test.f90 \
#src/test_jacobian.f90 \

$(call LOCAL_add, \
	src/core/qlknn_evaluate_nets.f90 \
)

#	src/qlknn_mex.f90 \
#	src/qlknn_mex_struct.f90 \
#
# Set dependecies of python shared objects
# $(call LOCAL_mod_dep, qlknn_primitives.so: qlknn_types.mod
# $(call LOCAL_mod_dep, qlknn_disk_io.so: qlknn_types.mod
# $(call LOCAL_mod_dep, qlknn_evaluate_nets.so: qlknn_types.mod qlknn_primitives.mod
# $(call LOCAL_mod_dep, qlknn_python.so: qlknn_disk_io.mod qlknn_evaluate_nets.mod
# 
# $(call LOCAL_mod_dep, qlknn_primitives.mexa64.o: qlknn_types.mexa64.o
# $(call LOCAL_mod_dep, qlknn_disk_io.mexa64.o: qlknn_types.mexa64.o
# $(call LOCAL_mod_dep, qlknn_evaluate_nets.mexa64.o: qlknn_types.mexa64.o qlknn_primitives.mexa64.o qlknn_victor_rule.mexa64.o
# $(call LOCAL_mod_dep, qlknn_python.mexa64.o: qlknn_disk_io.mexa64.o qlknn_evaluate_nets.mexa64.o

$(call LOCAL_mod_dep, src/core/qlknn_primitives.f90, qlknn_types.mod )
$(call LOCAL_mod_dep, src/core/qlknn_disk_io.f90, qlknn_types.mod )
$(call LOCAL_mod_dep, src/core/qlknn_evaluate_nets.f90, qlknn_types.mod qlknn_primitives.mod qlknn_victor_rule.mod qlknn_error_filter.mod )
$(call LOCAL_mod_dep, src/qlknn_python.f90, qlknn_disk_io.mod qlknn_evaluate_nets.mod )
ifeq ($(QLKNN_10D_SOURCE_NET),1)
  $(call LOCAL_add, \
    lib/src/qlknn-hyper-sources/net_efeetg_gb.f90 \
    lib/src/qlknn-hyper-sources/net_efetem_gb.f90 \
    lib/src/qlknn-hyper-sources/net_efiitg_gb.f90 \
    lib/src/qlknn-hyper-sources/net_gam_leq_gb.f90 \
    lib/src/qlknn-hyper-sources/net_dfeitg_gb_div_efiitg_gb.f90 \
    lib/src/qlknn-hyper-sources/net_dfetem_gb_div_efetem_gb.f90 \
    lib/src/qlknn-hyper-sources/net_dfiitg_gb_div_efiitg_gb.f90 \
    lib/src/qlknn-hyper-sources/net_dfitem_gb_div_efetem_gb.f90 \
    lib/src/qlknn-hyper-sources/net_efeitg_gb_div_efiitg_gb.f90 \
    lib/src/qlknn-hyper-sources/net_efitem_gb_div_efetem_gb.f89 \
    lib/src/qlknn-hyper-sources/net_pfeitg_gb_div_efiitg_gb.f90 \
    lib/src/qlknn-hyper-sources/net_pfetem_gb_div_efetem_gb.f90 \
    lib/src/qlknn-hyper-sources/net_vceitg_gb_div_efiitg_gb.f90 \
    lib/src/qlknn-hyper-sources/net_vcetem_gb_div_efetem_gb.f90 \
    lib/src/qlknn-hyper-sources/net_vciitg_gb_div_efiitg_gb.f90 \
    lib/src/qlknn-hyper-sources/net_vcitem_gb_div_efetem_gb.f90 \
    lib/src/qlknn-hyper-sources/net_vteitg_gb_div_efiitg_gb.f90 \
    lib/src/qlknn-hyper-sources/net_vtetem_gb_div_efetem_gb.f90 \
    lib/src/qlknn-hyper-sources/net_vtiitg_gb_div_efiitg_gb.f90 \
    lib/src/qlknn-hyper-sources/net_vtitem_gb_div_efetem_gb.f90 \
    src/qlknn_10d_source_net.f90 \
  )
  $(call LOCAL_mod_dep, src/qlknn_10d_source_net.f90, \
    net_efeetg_gb.mod \
    net_efetem_gb.mod \
    net_efiitg_gb.mod \
    net_gam_leq_gb.mod \
    net_dfeitg_gb_div_efiitg_gb.mod \
    net_dfetem_gb_div_efetem_gb.mod \
    net_dfiitg_gb_div_efiitg_gb.mod \
    net_dfitem_gb_div_efetem_gb.mod \
    net_efeitg_gb_div_efiitg_gb.mod \
    net_efitem_gb_div_efetem_gb.mod \
    net_pfeitg_gb_div_efiitg_gb.mod \
    net_pfetem_gb_div_efetem_gb.mod \
    net_vceitg_gb_div_efiitg_gb.mod \
    net_vcetem_gb_div_efetem_gb.mod \
    net_vciitg_gb_div_efiitg_gb.mod \
    net_vcitem_gb_div_efetem_gb.mod \
    net_vteitg_gb_div_efiitg_gb.mod \
    net_vtetem_gb_div_efetem_gb.mod \
    net_vtiitg_gb_div_efiitg_gb.mod \
    net_vtitem_gb_div_efetem_gb.mod \
    )
endif

# Set dependencies to preprocessor file
#$(call LOCAL_src_dep, src/asymmetry.f90, preprocessor.inc)
#$(call LOCAL_src_dep, src/mod_fluidsol.f90, preprocessor.inc)
