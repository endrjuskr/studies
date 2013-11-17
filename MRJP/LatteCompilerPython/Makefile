SDIR=src
TDIR=lattetests
COMPNAME=latc
CWD = $(shell pwd)

latcmake:
	sed "s|srcpath|$(CWD)|g" $(SDIR)/bashscript.sh > $(COMPNAME) && chmod +x $(COMPNAME)

clean:
	rm -f -r $(SDIR)/*.pyc $(COMPNAME) $(TDIR)/good/output/ $(TDIR)/bad/output/
