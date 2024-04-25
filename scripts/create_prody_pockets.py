import prody as pd
import os
import numpy as np  # Ensure numpy is imported for array operations
from scipy.spatial.distance import cdist
# Path to the ligands PDB file
ligands_pdb_path = 'ligands.pdb'
# Directory containing the protein PDB files
protein_pdb_dir = 'pdb_aligned_protein/'
# Directory to save the pocket PDB files
pocket_pdb_dir = "prody_pockets_1A"

# Create the prody_pockets directory if it doesn't exist
if not os.path.exists(pocket_pdb_dir):
    os.makedirs(pocket_pdb_dir)

# Parse the ligands PDB
ligands = pd.parsePDB(ligands_pdb_path)

# Iterate over each protein PDB file in the directory
for protein_pdb in os.listdir(protein_pdb_dir):
    if protein_pdb.endswith(".pdb"):
        protein_path = os.path.join(protein_pdb_dir, protein_pdb)
        
        # Parse the protein PDB
        protein = pd.parsePDB(protein_path)
        
        # Calculate the distance between each atom in the protein and the ligand atom cloud
        #dist_matrix = pd.calcDistance(ligands, protein)

        ligand_coords = ligands.getCoords()
        protein_coords = protein.getCoords()

        # Calculate distance matrix
        dist_matrix = cdist(ligand_coords, protein_coords)
        
        # Find indices of atoms in the protein that are within 3 angstroms of the ligand
        close_atoms_indices = np.where(dist_matrix < 1)[1]
        
        # Get unique residue numbers for these atoms
        close_residues = np.unique(protein.getResnums()[close_atoms_indices])
        
        # Select residues that are close to the ligands
        pocket = protein.select('resnum ' + ' '.join(map(str, close_residues)))
        
        if pocket is not None:
            # Define the path for saving the pocket PDB within the prody_pockets directory
            pocket_pdb_path = os.path.join(pocket_pdb_dir, 'pocket_' + protein_pdb)
            pd.writePDB(pocket_pdb_path, pocket)
            print(f"Pocket PDB generated for {protein_pdb}: {pocket_pdb_path}")
        else:
            print(f"No close residues found for {protein_pdb}")
