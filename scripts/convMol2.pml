
# Change directories
cd ./prody_pockets_5A/


# First argument variable
arg = sys.argv[1]
# Open the first argument
cmd.load(str(arg) + ".pdb")

cd ../pocketsMol2/
cmd.save(str(arg)[7:] + ".mol2")
cd ..
cmd.quit()


