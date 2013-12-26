PROGS=mm-test mm-nasm mm-test_org

all: $(PROGS)

mm-test: mm-test.o 
	gcc -o mm-test mm-test.o

mm-test_org: mm-test_org.o 
	gcc -o mm-test_org mm-test_org.o


mm-nasm: mm-nasm.asm
	nasm -f elf mm-nasm.asm

clean:
	rm *.o $(PROGS)

##EOF
