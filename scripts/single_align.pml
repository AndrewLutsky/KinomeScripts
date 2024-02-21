# Open 3E5A
load 3E5A_A_aligned.pdb


# Change directories
cd ./pdb_chains


# First argument variable
arg = sys.argv[1]
# Open the first argument
cmd.load(str(arg) + ".pdb")


# Align mobile to target

cmd.select("Mobile", arg)

select Target, 3E5A

align Mobile, Target




# Change directories
cd ../pdb_aligned/

# Write out Mobile to new folder
cmd.save(str(arg) + "_aligned.pdb", "Mobile")

# Return to parent directory.
cd ..
