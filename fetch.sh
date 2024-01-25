#!/bin/bash





# Read in program name,file name, column pdb id's are in, and output name as arguments.
progname=$0
file=$1
col=$2


# Hard code rcsb url.
url="https://files.rcsb.org/download"



# Read in csv pdb's. Pdb id must be second argument.
ids=`cat $1 | tail -n +2 | grep -v "NA" | cut -d "," -f $2`

# Create empty directory.
mkdir pdb_structs
cd pdb_structs

# Get wd.
out=`pwd`

# Range through pdb ids.
for id in $ids
do
	id="${id:0:4}"
	# Echo the id.
	echo $id

	
	pdb_out="$out/$id.pdb"

	# Echo the url
	echo $url/$id

	# Use curl
	curl -f "$url/$id.pdb" -o $pdb_out || echo "Failed to download $url/$id.pdb"
done


cd ..
echo "Download for all files completed."
