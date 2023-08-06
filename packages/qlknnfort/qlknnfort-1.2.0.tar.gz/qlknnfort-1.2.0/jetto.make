# This file is part of QLKNN-fortran
# You should have received the QLKNN-fortran LICENSE in the root of the project
# Import main JETTO build include file
include $(JSRCPATH)/include.mk

## Set the local environment
## ------------------------------------
# Overwrite JETTO pattern rules.
%.mod %.o: %.f90
	# Keep this line WITH the tab

# Import 'transport folder' build include file
include $(QLKNNROOT_)/../include.mk

.PHONY: $(LIBNAME)

$(LIBNAME): $(PROJECT_SUB_QLKNN_TGT) $(PROJECT_SUB_QLKNN_OBJS)
	@echo Building $(LIBNAME)
	@echo The objects were contained in $(PROJECT_SUB_QLKNN_TGT)
	@echo Namely $(PROJECT_SUB_QLKNN_OBJS)
	ar vr $(LIBNAME) $(PROJECT_SUB_QLKNN_OBJS)
