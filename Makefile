.PHONY: info
info ::
	@echo "make clean"
.PHONY: clean
clean ::
	@/bin/rm -f *~
	@for d in * ; do \
	    if [ -d $${d} ] ; then \
	        ( cd $${d} && /bin/rm -f *~ ) \
	    ; fi \
	; done
