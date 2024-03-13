import prody as pdy
import os
import pandas as pd

def remove_not_lig(filepath, ligname):
    for file in os.listdir(filepath):
        if file.endswith(".pdb"):
            structure = pdy.parsePDB(filepath + file)
            resname = ligname.get(file[:4], -1) #ligname[file[:4]]
            if resname != -1:
                structure = structure.select('protein or resname ' + resname)
                pdy.writePDB("../estrogen_pockets/" + file, structure)

def split_chains(filepath):
    for file in os.listdir(filepath):
        if file.endswith(".pdb"):
            structure = pdy.parsePDB(filepath + file)
            chids = structure.getChids()
            structure = structure.select("chain " + chids[0])
            pdy.writePDB("../estrogen_pockets/" + file, structure)

def map_pdb_lig(filepath) -> dict:
    # Read in excel file
    df = pd.read_excel(filepath, header = 1) 
    print(df)
    # Create dictionary
    map_lig = {}
    # Iterate through rows
    for index, row in df.iterrows():
        # Add to dictionary
        if not str(row['Ligand Name']).isnumeric() and not ("mer" in str(row['Ligand Name'])):
            map_lig[row['PDB code']] = row['Ligand Name']

    return map_lig

def create_pockets(filepath, threshold, ligname):
    # Define pockets as whole residues threshold distance away from the ligand.
    for file in os.listdir(filepath):
        if file.endswith(".pdb"):
            structure = pdy.parsePDB(filepath + file)
            ligand = structure.select('resname ' + ligname[file[:4]])
            pocket = structure.select('same residue as (not resname ' + ligname[file[:4]] + ' and within ' + str(threshold) + ' of resname ' + ligname[file[:4]] + ')')
            pdy.writePDB("../estrogen_pockets/" + file, pocket)

map_lig = map_pdb_lig("../EstrogenReceptors.xlsx")
print(map_lig)


remove_not_lig('../estrogen_receptors_pdbs/', map_lig)
split_chains('../estrogen_pockets/')
create_pockets('../estrogen_pockets/', 5, map_lig)
