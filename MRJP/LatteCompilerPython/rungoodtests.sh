#!/bin/bash          
echo Running tests!
for i in $( ls  good/*.lat); do
	echo item: $i
	python lattemain.py $i
done
