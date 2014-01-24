PROGS=ppm_reader ppm_converter.o

all: $(PROGS)

mm-test: ppm_converter.o
	gcc -o ppm_reader ppm_converter.o ppm_reader.c

ppm_converter.o: ppm_converter.s
	gas -o ppm_converter.o ppm_converter.s

clean:
	rm $(PROGS) *.o

##EOF
