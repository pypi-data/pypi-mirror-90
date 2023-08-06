# This file is part of QLKNN-fortran
# You should have received the QLKNN-fortran LICENSE in the root of the project
# When standalone, overwrite TUBS, we are can go higher than the default
ifneq ($(QLKNN_FIRST_FLAGS_CALL),0)
  ifeq ($(BUILD),release)
    ifeq ($(TOOLCHAIN),gcc)
      # O4 and Ofast work, but seem to give no speed increase
      QLKNN_EXTRA_FFLAGS += -O3
      QLKNN_EXTRA_LFLAGS += -O3
    endif
    ifeq ($(TOOLCHAIN),intel)
      QLKNN_EXTRA_FFLAGS += -O2
      # O3 and Ofast work, but seem to give no speed increase
      # Add this if you compile with fast (implies static)
      #ifeq ($(TUBSCFG_MPI),1)
      #  #TUBSCFG_OPT = -static_mpi
      #endif
      QLKNN_EXTRA_LFLAGS += -O2
    endif
    ifeq ($(TOOLCHAIN),pgi)
      # O3 and Ofast work, but seem to give no speed increase. O4 seems slower
      QLKNN_EXTRA_FFLAGS += -O2
      QLKNN_EXTRA_LFLAGS += -O2
    endif
  endif
  QLKNN_FIRST_FLAGS_CALL=0
endif

$(call SUBPROJECT_set_local_fflags, gcc, \
	-ffree-line-length-256 \
	-Werror \
	-Wall \
	-cpp \
	-std=f2008 \
	$(QLKNN_EXTRA_FFLAGS) \
)

$(call SUBPROJECT_set_local_fflags, intel, \
	-fpp \
	$(QLKNN_EXTRA_FFLAGS) \
)
$(call SUBPROJECT_set_local_fflags, pgi, \
	-Mpreprocess \
	$(QLKNN_EXTRA_FFLAGS) \
)

$(call SUBPROJECT_set_linkflags, gcc, \
	$(QLKNN_EXTRA_LFLAGS) \
)

$(call SUBPROJECT_set_linkflags, intel, \
	$(QLKNN_EXTRA_LFLAGS) \
)

$(call SUBPROJECT_set_linkflags, pgi, \
	$(QLKNN_EXTRA_LFLAGS) \
)
