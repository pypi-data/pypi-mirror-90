# This file is part of QLKNN-fortran
# You should have received the QLKNN-fortran LICENSE in the root of the project
# Boilerplate: include the make definitions
QLKNNROOT_ := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))

# Include all tubs definitions
include $(QLKNNROOT_)/tubs/main.make

# Boilerplate: if invoked directly (and not via the root Makefile), generate
# the neccessary standard rules
ifeq ($(TCI_MAIN_MAKE_FIRST),1)
$(call PROJECT_setup)
endif

ifeq ($(TUBSCFG_MPI),1)
  QLKNN_EXTRA_FFLAGS += -DMPI
endif

ifeq ($(TUBSCFG_MKL),1)
  QLKNN_EXTRA_FFLAGS += -DUSE_MKL -DLLI
endif

ifeq ($(QLKNN_10D_SOURCE_NET),1)
  QLKNN_EXTRA_FFLAGS += -DQLKNN_10D_SOURCE_NET
endif

# Boilerplate: if invoked directly (and not via the root Makefile), generate
# the neccessary standard rules
ifeq ($(TCI_MAIN_MAKE_FIRST),1)
$(call PROJECT_setup)
endif

$(call SUBPROJECT_open,QLKNN,staticlib)
include $(QLKNNROOT_)/transport_module_mpi.make
$(call SUBPROJECT_close)

$(call SUBPROJECT_open,qlknn_test,staticlib)
include $(QLKNNROOT_)/qlknn_test.make
$(call SUBPROJECT_close)

$(call SUBPROJECT_open,CLAF90,staticlib)
include $(QLKNNROOT_)/claf90.make
$(call SUBPROJECT_close)

$(call SUBPROJECT_open,fruit,staticlib)
include $(QLKNNROOT_)/fruit.make
$(call SUBPROJECT_close)

ifneq ($(TUBSCFG_MPI),1)
  include $(QLKNNROOT_)/qlknn_mex.make
  include $(QLKNNROOT_)/qlknn_python.make
endif

$(call SUBPROJECT_open,qlknn_regression_test_cli,app)
include $(QLKNNROOT_)/qlknn_regression_test_cli.make
$(call SUBPROJECT_close)

$(call SUBPROJECT_open,qlknn_jacobian_test_cli,app)
include $(QLKNNROOT_)/qlknn_jacobian_test_cli.make
$(call SUBPROJECT_close)

$(call SUBPROJECT_open,qlknn_hyper,app)
include $(QLKNNROOT_)/qlknn_hyper_standalone.make
$(call SUBPROJECT_close)

$(call SUBPROJECT_open,qlknn_fullflux,app)
include $(QLKNNROOT_)/qlknn_fullflux_standalone.make
$(call SUBPROJECT_close)

$(call SUBPROJECT_open,qlknn_jetexp,app)
include $(QLKNNROOT_)/qlknn_jetexp_standalone.make
$(call SUBPROJECT_close)

$(call SUBPROJECT_open,qlknn_hornnet,app)
include $(QLKNNROOT_)/qlknn_hornnet_standalone.make
$(call SUBPROJECT_close)

# Set up post-tubs JETTO-specific overwrites
ifeq ($(TARGET_ENV),jetto)
  $(info JETTO build detected, loading JETTO settings)
  include jetto.make
endif

# Boilerplate: if invoked directly (and not via the root Makefile), generate
# the build rules here
ifeq ($(TCI_MAIN_MAKE_FIRST),1)
$(call PROJECT_finalize)
endif

# Recipes for fruitsh
QLKNN_TEST_LIBS := $(PROJECT_SUB_QLKNN_TGT) $(PROJECT_SUB_qlknn_test_TGT) $(PROJECT_SUB_fruit_TGT)
QLKNN_TEST_OBJS := $(PROJECT_SUB_fruit_OBJS)

# Original TUBS recipe for gcc $(V_)$$(FC) $$(BAKEDFFLAGS) $3 -c $$< -o $$@
# $3 = Extra flags
# gfortran  -march=native -O2 -Wall -fPIC -fopenmp -flto  -J /home/karel/working/QLKNN-fortran/include/gcc-release-default   -ffree-line-length-1024 -cpp   -c /home/karel/working/QLKNN-fortran/tests/qlknn_test.f90 -o /home/karel/working/QLKNN-fortran/build/gcc-release-default/tests_-_qlknn_test.f90.o
test%.f90.o: test%.f90
	$(V_)$(FC) $(BAKEDFFLAGS) $(SUB_LOCALFLAGS_$(TOOLCHAIN)_.f90) -c $< -o $@

# Original TUBS recipe for gcc $(V_)$$(LINK) $$(BAKEDLFLAGS) -o $$@ $2 $$(LNKGRPBEG) $4 $$(patsubst lib%.a,-l%,$$(notdir $3)) $$(LNKGRPEND) $$(MKL_LDFLAGS)
# $2 = Object files matching recipe target
# $3 = Path to archives to link to
# $4 = Extra link flags
test%: test%.f90.o $(QLKNN_TEST_LIBS)
	$(V_)$(LINK) $(BAKEDLFLAGS) -o $@ $< $(LNKGRPBEG) $(PROJECT_SUB_EXTRALNK_$(TOOLCHAIN)) $(patsubst lib%.a,-l%,$(notdir $(QLKNN_TEST_LIBS))) $(LNKGRPEND) $(MKL_LDFLAGS)
