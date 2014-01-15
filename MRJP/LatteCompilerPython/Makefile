SDIR=src
PDIR=plylib
TDIR=lattetests
COMPNAME=latc
COMPNAME_ASM=latc_x86_64
CWD = $(shell pwd)

latcmake:
	sed "s|srcpath|$(CWD)|g" $(SDIR)/bashscript.sh > $(COMPNAME) && chmod +x $(COMPNAME) && python -m compileall . \
	&& javac lib/Runtime.java \
	&& sed "s|srcpath|$(CWD)|g" $(SDIR)/bashscript_asm.sh > $(COMPNAME_ASM) && chmod +x $(COMPNAME_ASM) \
	&& gcc -c -o lib/runtime.o lib/runtime.c

clean:
	rm -f -r $(COMPNAME) $(COMPNAME_ASM) $(TDIR)/good/output/ $(TDIR)/bad/output/ && find . -name \*.pyc -delete \
	&& find . -name \*.class -delete && find . -name \*.j -delete && find . -name \*.as, -delete && find . -name \*.s -delete
