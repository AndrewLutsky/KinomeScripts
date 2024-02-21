import os
import subprocess
import shutil
from Bio.PDB import PDBParser, Superimposer, PDBList, PDBIO, Select

# Function to read in each file name in a folder and return a list of file names
def read_files_in_folder(folder):
    files = []
    for file in os.listdir(folder):
        if file.endswith(".pdb"):
            files.append(file)
    return files


def create_pockets(pdb, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    #Construct the command
    cmd = ['/bin/zsh','-i','-c', f"pymol -c get_pocket.pml -- {pdb}"]
    #print(cmd)
    result = subprocess.run(cmd, text = True, capture_output=True, executable='/bin/zsh')
 
    if result.returncode != 0:
        print(result.stderr)

    return

# Function to cut off end off file extension given a file. E.g. 1a2b.pdb -> 1a2b
def cut_off_end(file):
    return file.split(".")[0]

pdbs = read_files_in_folder("pdb_aligned_protein")
for pdb in pdbs:
    pdb = cut_off_end(pdb)
    create_pockets(pdb, "pockets")
    print(f"Created pockets for {pdb}")
