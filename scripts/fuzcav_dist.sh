#!/bin/bash

# $1 is the input path to the folder, $2 is the output file placed in Fuzcav

# This script is used to calculate the distance between all the pockets in the ./pockets directory.
# The distance is calculated using the fuzcav program. The output is written to the file fuzcav_dist.txt.
cd $1
pockets1=`ls -A1`
pockets2=`ls -A1`

for i in $pockets1
do
	for j in $pockets2
	do 
		if [ $i != $j ] 
		then
			echo $i $j
			echo "Printing working directory"
			pwd
			cp $i ~/Downloads/FuzCav/pipeline
			cp $j ~/Downloads/FuzCav/pipeline
			cd ~/Downloads/FuzCav/pipeline
			echo "Running shell script"
			./fuzcav.sh $i $j >> ~/Desktop/School/CMU/Research/Kinome/FuzCav/$2
			rm ~/Downloads/FuzCav/pipeline/$i
			rm ~/Downloads/FuzCav/pipeline/$j
			cd $1
		fi
	done
done




