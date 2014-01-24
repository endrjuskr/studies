PROGS=ppm_reader

all: $(PROGS)

ppm_reader: ppm_converter.o
	gcc -o ppm_reader ppm_converter.o ppm_reader.c

ppm_converter.o: ppm_converter.s
	as -o ppm_converter.o ppm_converter.s

clean:
	rm -f $(PROGS) *.o

##EOF
