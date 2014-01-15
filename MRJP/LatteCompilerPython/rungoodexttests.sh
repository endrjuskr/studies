#!/bin/bash          
echo Running good tests!
for i in $( cd lattetests/good && ls *.lat); do
	./latc_x86_64 lattetests/good/$i 2> test.err > test.out
	if [[ "OK" != $(head -n 1 "test.err") ]]; then
        echo error in $i
        cat test.err
    fi
    echo "" >> lattetests/good/"${i%%.*}".input
    cat test.err
    ./lattetests/good/a.out < lattetests/good/"${i%%.*}".input > lattetests/good/"${i%%.*}".test.output

    # To see error code add - ; echo $?
    echo $i
    diff lattetests/good/"${i%%.*}".output lattetests/good/"${i%%.*}".test.output
done
    rm -f *.err
    rm -f *.out
    rm -f lattetests/good/*.test.output
    rm -f lattetests/good/*.s
    rm -f lattetests/good/*.asm
    rm -f lattetests/good/*.o
    rm -f lattetests/good/*.out
echo Done!

echo Running extensions/arrays1 tests!
for i in $( cd lattetests/extensions/arrays1 && ls *.lat); do
	./latc_x86_64 lattetests/extensions/arrays1/$i 2> test.err > test.out
	if [[ "OK" != $(head -n 1 "test.err") ]]; then
        echo error in $i
        cat test.err
        cat test.out
    fi
    cat test.err
    echo "" >> lattetests/extensions/arrays1/"${i%%.*}".input
    ./lattetests/extensions/arrays1/a.out < lattetests/extensions/arrays1/"${i%%.*}".input > lattetests/extensions/arrays1/"${i%%.*}".test.output

    # To see error code add - ; echo $?
    diff lattetests/extensions/arrays1/"${i%%.*}".output lattetests/extensions/arrays1/"${i%%.*}".test.output
done
    rm -f *.err
    rm -f *.out
    rm -f lattetests/extensions/arrays1/*.test.output
    rm -f lattetests/extensions/arrays1/*.s
    rm -f lattetests/extensions/arrays1/*.asm
    rm -f lattetests/extensions/arrays1/*.o
    rm -f lattetests/extensions/arrays1/*.out
echo Done!