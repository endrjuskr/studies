#!/bin/bash          
echo Running $1 tests!
mkdir $1/output
for i in $( cd $1 && ls *.lat); do
	echo item: $i
	./../latc $1/$i 2> $1/output/$i.err
done
