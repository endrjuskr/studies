PROGS=mm-test mm-nasm.o mm-test-org

all: $(PROGS)

mm-test: mm-test.o mm-nasm.o
	gcc -g -o mm-test mm-nasm.o mm-test.c

mm-test-org: mm-test-org.o 
	gcc -o mm-test-org mm-test-org.o

mm-nasm.o: mm-nasm.asm
	nasm -f elf64 -g -F dwarf -o mm-nasm.o mm-nasm.asm

clean:
	rm $(PROGS) *.o

##EOF
