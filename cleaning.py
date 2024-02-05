import prody as pd
import os
import gemmi

def extract_hetero_resnames(pdb_folder, output_file):
    """
    Iterates through all PDB files in the specified folder, identifies heteroatom
    residue names, and appends them to a single output file.
    
    Parameters:
    - pdb_folder: Path to the folder containing PDB files.
    - output_file: Path to the output file where heteroatom residue names will be listed.
    """
    # Ensure output directory exists (if specified with a directory path)
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w') as outfile:
        outfile.write("PDB File\tResidue Name\n")
        
        for pdb_file in os.listdir(pdb_folder):
            if pdb_file.endswith('.pdb'):
                # Load the PDB file
                structure = pd.parsePDB(os.path.join(pdb_folder, pdb_file))
                
                # Select heteroatoms
                heteroatoms = structure.select('hetero')
                
                # Extract unique residue names from the selection
                if heteroatoms is not None:
                    unique_resnames = set(heteroatoms.getResnames())
                    for resname in unique_resnames:
                        outfile.write(f"{pdb_file}\t{resname}\n")



def create_resname_to_formula_dict(cif_path):
    doc = gemmi.cif.read_file(cif_path)  # Read the CIF file
    resname_to_formula = {}

    for block in doc:
        # Look for the _chem_comp.id and _chem_comp.formula in each block
        comp_id = block.find_value('_chem_comp.id')
        formula = block.find_value('_chem_comp.formula')
        if comp_id and formula:  # Ensure both ID and formula are present
            # Clean up the formula string if necessary
            cleaned_formula = formula.strip()
            resname_to_formula[comp_id] = cleaned_formula
        elif comp_id:  # Found comp_id but no formula
            print(f"Formula not found for {comp_id}.")

    return resname_to_formula

def contains_phosphorous(formula):
    return 'P' in formula

def extract_hetatms_with_phosphorous(pdb_files_dir, resname_to_formula_dict, output_pdb_path):
    hetatms_with_p = []  # List to hold HETATM lines for output

    for filename in os.listdir(pdb_files_dir):
        if filename.endswith(".pdb"):
            file_path = os.path.join(pdb_files_dir, filename)
            with open(file_path, 'r') as pdb_file:
                for line in pdb_file:
                    if line.startswith("HETATM"):
                        parts = line.split()
                        res_name = parts[3]
                        #res_name = line[17:20].strip()
                        formula = resname_to_formula_dict.get(res_name, "")
                        if contains_phosphorous(formula):
                            hetatms_with_p.append(line)

    # Write the collected HETATM lines to the output PDB file
    with open(output_pdb_path, 'w') as output_file:
        for hetatm_line in hetatms_with_p:
            output_file.write(hetatm_line)

def extract_all_hetatms(pdb_files_dir, output_pdb_path):
    hetatms = []  # List to hold HETATM lines for output

    for filename in os.listdir(pdb_files_dir):
        if filename.endswith(".pdb"):
            file_path = os.path.join(pdb_files_dir, filename)
            with open(file_path, 'r') as pdb_file:
                for line in pdb_file:
                    if line.startswith("HETATM"):
                        hetatms.append(line)

    # Write the collected HETATM lines to the output PDB file
    with open(output_pdb_path, 'w') as output_file:
        for hetatm_line in hetatms:
            output_file.write(hetatm_line)

def isolate_proteins(input_dir, output_dir):
    # Create the output directory if it does not exist
    os.makedirs(output_dir, exist_ok=True)

    # Iterate through all files in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith(".pdb"):
            input_file_path = os.path.join(input_dir, filename)
            output_file_path = os.path.join(output_dir, filename)

            with open(input_file_path, 'r') as input_file, open(output_file_path, 'w') as output_file:
                for line in input_file:
                    if not line.startswith("HETATM"):
                        output_file.write(line)

'''
## Run this to isolate protiens
input_dir = 'pdb_aligned'
output_dir = 'pdb_aligned_protein'
isolate_proteins(input_dir, output_dir)
'''

## Run this to extract all hetero atoms to one merged pdb
pdb_files_dir = 'pdb_aligned' 
output_pdb_path = 'hetatms_all.pdb'  
extract_all_hetatms(pdb_files_dir, output_pdb_path)





'''
## Run this to output pdb with all hetatms containing phosphorus
cif_path = 'components.cif'
pdb_files_dir = 'pdb_aligned'  # Directory containing PDB files
output_pdb_path = 'hetatms_with_p.pdb'  # Path for the output PDB file

# Generate the dictionary mapping residue names to chemical formulas 
resname_to_formula_dict = create_resname_to_formula_dict(cif_path)
#print(resname_to_formula_dict["PTR"])

# Extract HETATMs and write to a single PDB file
extract_hetatms_with_phosphorous(pdb_files_dir, resname_to_formula_dict, output_pdb_path)

'''
