
# Change directories
cd ../pockets/pockets_2_5A_mol2/


# First argument variable
arg = sys.argv[1]
# Open the first argument
cmd.load(str(arg) + ".pdb")

cmd.save(str(arg) + ".mol2")
cd ..
cmd.quit()


