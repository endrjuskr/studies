all:
	spin -a prot.pml
	gcc -O2 -w -o pan pan.c
	./pan -m100000000 -a -f

multi:
	spin -a prot.pml
	gcc -O2 -w -o pan pan.c

extended:
	spin -a prot-ext.pml
	gcc -O2 -DCOLLAPSE -w -o pan pan.c
	./pan -m100000000 -a -f

dbfs:
	spin -a prot-ext.pml
	gcc -O2 -DBFS -w -o pan pan.c
	./pan -m100000000

multi-ext:
	spin -a prot.pml
	gcc -O2 -w -o pan pan.c

clean:
	rm -f pan* prot.pml.trail _spin_nvr.tmp