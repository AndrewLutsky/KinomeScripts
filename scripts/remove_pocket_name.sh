#!/bin/bash

cd $1

files=`ls -A1`
for file in $files
do
	awk 'NR == 3 {print substr($0, 8)} NR != 3' "$file" > "$file"_temp
	mv "$file"_temp "$file"
done
