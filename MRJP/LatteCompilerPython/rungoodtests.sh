#!/bin/bash          
echo Running good tests!
for i in $( cd lattetests/good && ls *.lat); do
	./latc lattetests/good/$i 2> test.err > test.out
	if [[ "OK" != $(head -n 1 "test.err") ]]; then
        echo error in $i
    fi
    echo "" >> lattetests/good/"${i%%.*}".input
    java -classpath "lattetests/good/:lib/" "${i%%.*}" < lattetests/good/"${i%%.*}".input > lattetests/good/"${i%%.*}".test.output
    # To see error code add - ; echo $?
    diff lattetests/good/"${i%%.*}".output lattetests/good/"${i%%.*}".test.output
    rm *.err
    rm *.out
    rm lattetests/good/*.test.output
    rm lattetests/good/*.j
    rm lattetests/good/*.class
done
echo Done!
