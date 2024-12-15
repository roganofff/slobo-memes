#!/bin/bash

directories=`echo */`

for directory in $directories 
do
	cd $directory
	flake8
	cd ..
done
