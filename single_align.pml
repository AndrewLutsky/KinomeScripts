# Open 3E5A
load 3E5A_A_aligned.pdb


# Change directories
cd ./pdb_chains


# First argument variable
set arg = sys.argv[1]
# Open the first argument
load str(arg) + ".pdb"


# Align mobile to target

select Mobile, arg

select Target, 3E5A

align Mobile, Target




# Change directories
cd ../pdb_aligned/

# Write out Mobile to new folder
save str(arg) + "_aligned.pdb", Mobile

