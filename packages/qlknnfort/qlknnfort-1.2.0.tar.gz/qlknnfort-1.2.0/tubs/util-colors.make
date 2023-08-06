# util-colors.make
#
# Color defintions (via ANSI color sequences). Color output may be suppressed
# by defining NOCOLOR (e.g. NOCOLOR=1 on the command line).

ifndef NOCOLOR
	TCIfmtRST := \e[0m
	TCIfmtBLD := \e[1m

	TCIfmtRED := \e[31m
	TCIfmtGRN := \e[32m
	TCIfmtYEL := \e[33m
	TCIfmtBLU := \e[34m
	TCIfmtMAG := \e[35m
	TCIfmtCYA := \e[36m
	TCIfmtGRY := \e[37m
else
	TCIfmtRST :=
	TCIfmtBLD :=

	TCIfmtRED :=
	TCIfmtGRN :=
	TCIfmtYEL :=
	TCIfmtBLU :=
	TCIfmtMAG :=
	TCIfmtCYA :=
	TCIfmtGRY :=
endif

#EOF vim:syntax=make:foldmethod=marker:ts=4:noexpandtab: 
