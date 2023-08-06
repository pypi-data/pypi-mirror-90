# util-clean.make
#
# Helpers: cleanup

define UTIL_clean_file =
	$(call UTIL_msg_clean,$(notdir $1),,$3)
	$(V_)-rm $1 2>/dev/null ; true
endef
define UTIL_clean_files =
	$(call UTIL_msg_clean,$(words $1),$2,$3)
	$(V_)-rm $1 2>/dev/null ; true
endef
define UTIL_clean_dir =
	$(call UTIL_msg_rmdir,.../$(subst $(TCI_MAKE_ROOT)/,,$1),$2)
	$(V_)-rmdir $1 2>/dev/null ; true
endef

#EOF vim:syntax=make:foldmethod=marker:ts=4:noexpandtab:
