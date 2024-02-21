# Load pocket cloud.
cmd.load("pocket_define3.pdb")

# Change directories
cd ./pdb_aligned_protein/

# First argument variable
arg = sys.argv[1]

# Open the first argument
cmd.load(str(arg) + ".pdb")


cmd.select("pocket", str(arg) + " near_to 3 of pocket_define3")

# select pocket
# cmd.select("pocket", "byres " + str(arg) + " and within 3 of pocket_define3")
# print("byres " + str(arg) + " within 1 of pocket_define3")

# Change directories
cd ../pockets/

# Write out Mobile to new folder
cmd.save(str(arg) + "_pocket.mol2", "pocket")

# Return to parent directory.
cd ..

exit
