all: fpc

fpc: np po mo to do floatingpoint.c
	gcc -o fpc numberpartition.o plusop.o minusop.o timesop.o divideop.o floatingpoint.c

np: numberpartition.asm
	nasm -g -f elf64 numberpartition.asm

po: plusop.asm
	nasm -g -f elf64 plusop.asm

mo: minusop.asm
	nasm -g -f elf64 minusop.asm

to: timesop.asm
	nasm -g -f elf64 timesop.asm

do: divideop.asm
	nasm -g -f elf64 divideop.asm

clean:
	rm -f *.o fpc

##EOF
