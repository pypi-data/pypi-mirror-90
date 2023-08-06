# This file is part of QLKNN-fortran
# You should have received the QLKNN-fortran LICENSE in the root of the project

# Mex rules
$(BAKEDBUILDDIR)/src_-_qlknn_types.mexa64.o: $(QLKNNROOT_)/src/core/qlknn_types.f90
$(BAKEDBUILDDIR)/src_-_qlknn_victor_rule.mexa64.o: $(QLKNNROOT_)/src/core/qlknn_victor_rule.f90
$(BAKEDBUILDDIR)/src_-_qlknn_mex_struct.mexa64.o: $(QLKNNROOT_)/src/qlknn_mex_struct.f90
$(BAKEDBUILDDIR)/src_-_qlknn_primitives.mexa64.o: $(QLKNNROOT_)/src/core/qlknn_primitives.f90 $(BAKEDBUILDDIR)/src_-_qlknn_types.mexa64.o $(QLKNNROOT_)/src/core/preprocessor.inc
$(BAKEDBUILDDIR)/src_-_qlknn_disk_io.mexa64.o: $(QLKNNROOT_)/src/core/qlknn_disk_io.f90 $(BAKEDBUILDDIR)/src_-_qlknn_types.mexa64.o $(QLKNNROOT_)/src/core/preprocessor.inc
$(BAKEDBUILDDIR)/src_-_qlknn_error_filter.mexa64.o: $(QLKNNROOT_)/src/core/qlknn_error_filter.f90 $(BAKEDBUILDDIR)/src_-_qlknn_types.mexa64.o
$(BAKEDBUILDDIR)/src_-_qlknn_evaluate_nets.mexa64.o: $(QLKNNROOT_)/src/core/qlknn_evaluate_nets.f90 $(BAKEDBUILDDIR)/src_-_qlknn_types.mexa64.o $(BAKEDBUILDDIR)/src_-_qlknn_primitives.mexa64.o $(BAKEDBUILDDIR)/src_-_qlknn_victor_rule.mexa64.o $(QLKNNROOT_)/src/core/preprocessor.inc $(BAKEDBUILDDIR)/src_-_qlknn_error_filter.mexa64.o

QLKNN_SRCS= \
  qlknn_primitives.f90 \
  qlknn_disk_io.f90 \
  qlknn_types.f90 \
  qlknn_python.f90 \
  qlknn_error_filter.f90 \
  qlknn_evaluate_nets.f90 \
  qlknn_victor_rule.f90
QLKNN_MEXOBJS = \
  $(BAKEDBUILDDIR)/src_-_qlknn_types.mexa64.o \
  $(BAKEDBUILDDIR)/src_-_qlknn_primitives.mexa64.o \
  $(BAKEDBUILDDIR)/src_-_qlknn_disk_io.mexa64.o \
  $(BAKEDBUILDDIR)/src_-_qlknn_evaluate_nets.mexa64.o \
  $(BAKEDBUILDDIR)/src_-_qlknn_error_filter.mexa64.o \
  $(BAKEDBUILDDIR)/src_-_qlknn_victor_rule.mexa64.o \
  $(BAKEDBUILDDIR)/src_-_qlknn_mex_struct.mexa64.o
#QLKNN_MEXOBJS:=$(QLKNN_SRCS:%f90=%mexa64) qlknn_mex_struct.mexa64
#QLKNN_MEXOBJS:=$(QLKNN_MEXOBJS:%=$(BAKEDBUILDDIR)/%)

$(eval include $(QLKNNROOT_)/flags.make)

MEX ?= mex
#
$(QLKNN_MEXOBJS):
	mkdir -p $(LIBDEST)
	mkdir -p $(BINDEST)
	mkdir -p $(BAKEDMODDEST)
	mkdir -p $(BAKEDBUILDDIR)
	# -output is ignored
	$(MEX) -c -v FOPTIMFLAGS="-O3" FFLAGS="-fPIC $(BAKEDFFLAGS) $(SUB_LOCALFLAGS_$(TOOLCHAIN)_.f90) -std=gnu" FC=$(FC) -DMEXING -outdir $(BAKEDBUILDDIR) $<
	$(eval generated_path=$(<:%.f90=%.o))
	mv $(BAKEDBUILDDIR)/$(notdir $(generated_path)) $@

# Detect gfortran version
GFORT_VERSION:=$(shell $(FC) --version 2> /dev/null | head -n 1 | cut -d' ' -f 4)
ifeq ($(GFORT_VERSION),)
  GFORT_VERSION=null
  GFORT_MAJOR_VERSION=null
else
  GFORT_MAJOR_VERSION:=$(shell echo $(GFORT_VERSION) 2> /dev/null | cut -d'.' -f 1)
endif
EXTRA_FLAGS=$(shell if [ $(GFORT_MAJOR_VERSION) -gt 9 ]; then echo -fallow-invalid-boz; else echo ''; fi)

#-
#space := $(null) #
#comma := ,
#MEX_COMMA='$(subst $(space),'$(comma)',$(QLKNN_MEXOBJS))'
#@$(foreach V,$(sort $(.VARIABLES)), $(if $(filter-out environment% default automatic, $(origin $V)),$(warning $V=$($V) ($(value $V)))))
matlab $(BINDEST)/qlknn_mex.mexa64: $(QLKNNROOT_)/src/qlknn_mex.f90 $(QLKNN_MEXOBJS)
	$(MEX) -v FOPTIMFLAGS="-O3" FFLAGS="-fPIC $(BAKEDFFLAGS) $(SUB_LOCALFLAGS_$(TOOLCHAIN)_.f90) -std=gnu $(EXTRA_FLAGS)" FC=$(FC) -DMEXING -outdir $(BINDEST) -output $@ $(QLKNN_MEXOBJS) $<
