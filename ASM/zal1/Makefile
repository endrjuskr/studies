all: fpc

fpc: fpasm floatingpoint.c
	gcc -g -o fpc floatingpoint.o floatingpoint.c

fpasm: floatingpoint.asm
	/usr/local/bin/nasm -g -f macho64 floatingpoint.asm
	##ld -dynamic-linker /lib64/ld-linux-x86-64.so.2 -o fpasm -lc fpoint.o

clean:
	rm -f *.o fpasm fpc

##EOF
