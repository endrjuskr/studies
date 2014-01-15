#!/bin/bash          
echo Running good tests!
for i in $( cd lattetests/good && ls *.lat); do
	./latc_x86_64 lattetests/good/$i 2> test.err > test.out
	if [[ "OK" != $(head -n 1 "test.err") ]]; then
        echo error in $i
        cat test.err
    fi
    echo "" >> lattetests/good/"${i%%.*}".input
    ./a.out < lattetests/good/"${i%%.*}".input > lattetests/good/"${i%%.*}".test.output

    # To see error code add - ; echo $?
    echo $i
    diff lattetests/good/"${i%%.*}".output lattetests/good/"${i%%.*}".test.output
    rm -f *.err
    rm -f lattetests/good/*.test.output
    rm -f lattetests/good/*.s
    rm -f lattetests/good/*.asm
    rm -f lattetests/good/*.o
    rm -f lattetests/good/*.out
done
echo Done!