SDIR=src
PDIR=plylib
TDIR=lattetests
COMPNAME=latc
CWD = $(shell pwd)

latcmake:
	sed "s|srcpath|$(CWD)|g" $(SDIR)/bashscript.sh > $(COMPNAME) && chmod +x $(COMPNAME) && python -m compileall .

clean:
	rm -f -r $(COMPNAME) $(TDIR)/good/output/ $(TDIR)/bad/output/ && find . -name \*.pyc -delete 
