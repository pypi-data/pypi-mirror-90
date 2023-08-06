# util-messages.make
#
# Common messages printed during the build.

define UTIL_msg_fort =
	@$(ECHO) "$(TCIfmtMAG)FC $(TCIfmtRST) : $(TCIfmtGRY)$2$(TCIfmtRST) $1"
endef
define UTIL_msg_ar =
	@$(ECHO) "$(TCIfmtBLU)AR   $(TCIfmtRST) : $(TCIfmtGRY)$2$(TCIfmtRST) $(TCIfmtBLD)$1$(TCIfmtRST) from $3 object files"
endef
define UTIL_msg_link =
	@$(ECHO) "$(TCIfmtGRN)APP  $(TCIfmtRST) : $(TCIfmtGRY)$2$(TCIfmtRST) $(TCIfmtBLD)$1$(TCIfmtRST) from $3 object files"
endef
define UTIL_msg_mkdir =
	@$(ECHO) "$(TCIfmtGRY)DIR  $(TCIfmtRST) : $(TCIfmtGRY)$2$(TCIfmtRST) $1"
endef


define UTIL_msg_clean =
	@$(ECHO) "$(TCIfmtRED)CLEAN$(TCIfmtRST) : $(TCIfmtGRY)$3$(TCIfmtRST) $(TCIfmtBLD)$1$(TCIfmtRST) $2"
endef
define UTIL_msg_rmdir =
	@$(ECHO) "$(TCIfmtYEL)RMDIR$(TCIfmtRST) : $(TCIfmtGRY)$2$(TCIfmtRST) $1"
endef

#EOF vim:syntax=make:foldmethod=marker:ts=4:noexpandtab:
