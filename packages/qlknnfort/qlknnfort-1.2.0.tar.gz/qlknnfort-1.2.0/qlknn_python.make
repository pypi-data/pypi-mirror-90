# This file is part of QLKNN-fortran
# You should have received the QLKNN-fortran LICENSE in the root of the project
# Python rules
KIND_MAP=$(QLKNNROOT_)/src/qlknn_python_kind_map
F90WRAP_MODULE?=qlknn_f90wrap

f90wrap_files: $(PROJECT_SUB_QLKNN_OBJS) $(KIND_MAP)
	$(info PROJECT_SUB_QLKNN_SRCS=$(PROJECT_SUB_QLKNN_SRCS))
	$(info BAKEDMODDEST=$(BAKEDMODDEST))
	$(info BAKEDBUILDDIR=$(BAKEDBUILDDIR))
	$(info PROJECT_SUB_QLKNN_OBJS=$(PROJECT_SUB_QLKNN_OBJS))
	# Indentation error with f90wrap v0.2.3
	f90wrap --py-max-line-length 90 -m $(F90WRAP_MODULE) $(PROJECT_SUB_QLKNN_SRCS) -k $(KIND_MAP)
	mv f90wrap_*.f90 $(F90WRAP_MODULE).py qlknnfort/

f2py_f90wrap:
	f2py-f90wrap  --include-paths $(BAKEDMODDEST) -I$(BAKEDMODDEST) -c -m _$(F90WRAP_MODULE) $(PROJECT_SUB_QLKNN_OBJS) $(BAKEDBUILDDIR)/f90wrap_*.f90 
	mv $(F90WRAP_MODULE).py _$(F90WRAP_MODULE)* .f2py_f2cmap $(BAKEDBUILDDIR)
