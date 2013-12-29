PROGS=mm-test mm-nasm mm-test_org

all: $(PROGS)

mm-test: mm-test.o mm-nasm
	gcc -g -o mm-test mm-nasm.o mm-test.c

mm-test_org: mm-test_org.o 
	gcc -o mm-test_org mm-test_org.o


mm-nasm: mm-nasm.asm
	nasm -f elf64 -g -F dwarf -o mm-nasm.o mm-nasm.asm

clean:
	rm *.o $(PROGS)

##EOF
