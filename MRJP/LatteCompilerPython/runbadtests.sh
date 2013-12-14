#!/bin/bash          
echo Running bad tests!
for i in $( cd lattetests/bad && ls *.lat); do
	latc lattetests/bad/$i 2> test.err > test.out
	if [[ "ERROR" != $(head -n 1 "test.err") ]]; then
        echo error in $i
    fi
    rm *.err
    rm *.out
done
echo Done!
