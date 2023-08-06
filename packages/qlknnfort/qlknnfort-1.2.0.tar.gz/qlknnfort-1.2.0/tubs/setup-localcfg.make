# The following (rather inelegantly) looks for the full host name (e.g.,
# "r000u05g02.marconi.cineca.it"), then strips the first part up to four times.
# (so it will look for "marconi.cineca.it", then "cineca.it", then "it", and
# finally for nothing "" given the above full hostname).
LOCALCFG_ := $(HOSTFULL)
-include $(TCI_MAKE_HERE)/localcfg/$(LOCALCFG_).make

LOCALCFG_ := $(subst ${ },.,$(wordlist 2,255,$(subst .,${ },$(LOCALCFG_))))
-include $(TCI_MAKE_HERE)/localcfg/$(LOCALCFG_).make

LOCALCFG_ := $(subst ${ },.,$(wordlist 2,255,$(subst .,${ },$(LOCALCFG_))))
-include $(TCI_MAKE_HERE)/localcfg/$(LOCALCFG_).make

LOCALCFG_ := $(subst ${ },.,$(wordlist 2,255,$(subst .,${ },$(LOCALCFG_))))
-include $(TCI_MAKE_HERE)/localcfg/$(LOCALCFG_).make

LOCALCFG_ := $(subst ${ },.,$(wordlist 2,255,$(subst .,${ },$(LOCALCFG_))))
-include $(TCI_MAKE_HERE)/localcfg/$(LOCALCFG_).make
