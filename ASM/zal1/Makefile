all: fpc

fpc: np po mo floatingpoint.c
	gcc -g -o fpc numberpartition.o plusop.o minusop.o floatingpoint.c

np: numberpartition.asm
	nasm -g -f elf64 numberpartition.asm

po: plusop.asm
	nasm -g -f elf64 plusop.asm

mo: minusop.asm
	nasm -g -f elf64 minusop.asm

clean:
	rm -f *.o fpc

##EOF
