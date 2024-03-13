import pandas as pd
import prody as pdy
import os
# Write a function that given a filepath to an excel file it reads out the pdb files and returns a list of the pdb file
def read_excel(filepath) -> list:
    # Read the excel file
    df = pd.read_excel(filepath, header=1)
    # Extract the pdb files
    print(df)
    pdb_files = df['PDB code'].tolist()
    return pdb_files


def main():
    # Test the function
    filepath = "EstrogenReceptors.xlsx"
    pdb_files = read_excel(filepath)
    for pdb_id in pdb_files:
        get_protein(pdb_id, "estrogen_receptors_pdbs")
    return

def get_protein(idx, folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
    structure = pdy.fetchPDB(idx, compressed=False, path = folder + "/" + idx + ".pdb")
    
    # Save the structure to a file
    #pdy.writePDB(folder + "/" + idx + ".pdb", structure)


if __name__ == "__main__":
    main()
