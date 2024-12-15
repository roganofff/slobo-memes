#!/bin/bash

directories=`echo */`
echo $directories

for directory in $directories 
do
	cd $directory
	flake8
	cd ..
done
