import os
import subprocess
import shutil
from Bio.PDB import PDBParser, Superimposer, PDBList, PDBIO, Select

def read_pdbs_from_file(file_path):
    pdbs = []
    pdb_sidechain = {}
    pdb_conforms = {}
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if parts[9] == "NA" or parts[9] == "10_PDB_validation":
                continue
            pdb = parts[9]
            pdbs.append(pdb)
            pdb_sidechain[pdb[0:4]] = pdb[4]
            pdb_id = pdb[0:4] + "_" + pdb[4]
            pdb_conforms[pdb_id] = parts[10]
    return pdbs, pdb_sidechain, pdb_conforms

def download_pdb_files(pdb_ids, output_folder='pdb_files'):
    """
    Downloads PDB files for the given list of PDB IDs into the specified folder.

    :param pdb_ids: List of PDB IDs to download.
    :param output_folder: Folder to save the PDB files. Defaults to 'pdb_files'.
    """
    pdbl = PDBList()

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Download each PDB file
    for pdb_id in pdb_ids:
        print(f"Downloading PDB file for: {pdb_id}")
        file_path = pdbl.retrieve_pdb_file(pdb_id, file_format='pdb', pdir=output_folder, overwrite=True)

        # Rename the file to have a .pdb extension
        pdb_file_name = os.path.join(output_folder, pdb_id.lower() + ".pdb")
        shutil.move(file_path, pdb_file_name)

    print("All requested PDB files have been downloaded.")



class ChainSelect(Select):
    def __init__(self, chain_id):
        self.chain_id = chain_id

    def accept_chain(self, chain):
        return chain.get_id() == self.chain_id

def extract_and_save_chain(pdb_filename, chain_id, output_filename):
    parser = PDBParser()
    structure = parser.get_structure("protein_structure", pdb_filename)

    # Create a PDBIO object
    io = PDBIO()

    # Set the structure to the PDBIO object
    io.set_structure(structure)

    # Use a lambda function as a select rule: it returns True only for the desired chain
    io.save(output_filename, select=ChainSelect(chain_id))

def get_all_chains(folder_path, chain_dict, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Process each PDB file in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdb"):
            pdb_id = filename.split('.')[0]  # Extract PDB ID from the filename
            chain_id = chain_dict.get(pdb_id)

            if chain_id:
                pdb_path = os.path.join(folder_path, filename)
                output_filename = os.path.join(output_folder, f"{pdb_id}_{chain_id}.pdb")
                extract_and_save_chain(pdb_path, chain_id, output_filename)
                print(f"Extracted chain {chain_id} from {pdb_id} to {output_filename}")
            else:
                print(f"No chain information for {pdb_id}")

def run_tm_align(pdb_file1, pdb_file2, output_file):
    # Construct the TM-align command
    cmd = ['TMalign', pdb_file1, pdb_file2, '-o', output_file]

    # Run TM-align
    result = subprocess.run(cmd, capture_output=True, text=True)

    # Check if TM-align ran successfully
    if result.returncode != 0:
        print("Error in running TM-align: ", result.stderr)
    else:
        print("TM-align ran successfully. Output saved to:", output_file)


"This calls single_align.pml to align two proteins and save it in a new folder"
def align(pdb_file1, pdb_file2, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # For each pdb name align to 3E5A 
    
    #Construct the command
    cmd = ['/bin/zsh','-i','-c', f"pymol -c single_align.pml -- {pdb_file1}"]
    #print(cmd)
    result = subprocess.run(cmd, text = True, capture_output=True, executable='/bin/zsh')

    #Check return code
    
    if result.returncode != 0:
        print(result.stderr)
        #raise RuntimeError("single_align.pml failed to run")
        # If RMSD exceeds some threshold -> we manually examine
        # Write to folder
    

    return
# Example usage
#run_tm_align('protein1.pdb', 'protein2.pdb', 'tm_align_output.txt')


pdbs, pdb_sidechain, pdb_conforms = read_pdbs_from_file("paper_data.txt")
pdb_ids = list(pdb_sidechain.keys())

print(pdb_conforms)

#pdb_folder = "pdb_structs"
#output_folder = "pdb_chains"

#get_all_chains(pdb_folder, pdb_sidechain, output_folder)


'''
for pdb in pdbs:
    align(pdb[0:4] + "_" + pdb[4:5], "0000", "pdb_aligned")
'''


# Initialize PDB parser and PDB list
#parser = PDBParser()
#pdb_list = PDBList()

'''
# Create the directory for aligned structures if it doesn't exist
output_dir1 = 'aligned_structs'
if not os.path.exists(output_dir1):
    os.makedirs(output_dir1)

# Fetch and parse the reference PDB (3E5A)
pdb_list.retrieve_pdb_file('3E5A', pdir='.', file_format='pdb')
ref_structure = parser.get_structure('3E5A', 'pdb3e5a.ent')

# Extract all atoms from the A chain of the reference structure
ref_atoms = [atom for atom in ref_structure[0]['A'].get_atoms()]
'''


