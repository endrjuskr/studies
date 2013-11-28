all: fpc

fpc: np po mo to floatingpoint.c
	gcc -g -o fpc numberpartition.o plusop.o minusop.o timesop.o floatingpoint.c

np: numberpartition.asm
	nasm -g -f elf64 numberpartition.asm

po: plusop.asm
	nasm -g -f elf64 plusop.asm

mo: minusop.asm
	nasm -g -f elf64 minusop.asm

to: timesop.asm
	nasm -g -f elf64 timesop.asm

clean:
	rm -f *.o fpc

##EOF
