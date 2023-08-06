# project-dirs.make
#
# Rules to create required directories.

PROJECTimpl_FINALIZE_ACTS += PROJECTimpl_make_dirs

define PROJECTimpl_make_dirs =
$(BAKEDBUILDDIR) : | meta-print
	$(call UTIL_msg_mkdir,$$(subst $(TCI_MAKE_ROOT),,...$$@), <$(SYS)>)
	$(V_)mkdir -p $$@


$(BAKEDMODDEST) : | meta-print
	$(call UTIL_msg_mkdir,$$(subst $(TCI_MAKE_ROOT),,...$$@), <$(SYS)>)
	$(V_)mkdir -p $$@

$(LIBDEST) : | meta-print
	$(call UTIL_msg_mkdir,$$(subst $(TCI_MAKE_ROOT),,...$$@), _)
	$(V_)mkdir -p $$@

$(BINDEST) : | meta-print
	$(call UTIL_msg_mkdir,$$(subst $(TCI_MAKE_ROOT),,...$$@), _)
	$(V_)mkdir -p $$@

endef

#EOF vim:syntax=make:foldmethod=marker:ts=4:noexpandtab:
