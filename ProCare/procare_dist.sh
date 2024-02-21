#!/bin/bash

cd pockets_5_mol2
pockets1=`ls -A1`
pockets2=`ls -A1`



for i in $pockets1:
do
	for j in $pockets2:
	do
		echo "Comparing $i with $j"
		python ../../ProCare/utils/procare_rescoring.py -s $i -t $j -o output.tsv
	done
done

cat output.tsv >> procare_dist.txt
mv procare_dist.txt ../
rm output.txt

cd ..
