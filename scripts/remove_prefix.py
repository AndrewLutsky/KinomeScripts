import os

# Specify the directory containing the files
folder_path = '../pockets/pockets_2_5A_mol2'

# List all files in the directory
files = os.listdir(folder_path)

for filename in files:
    # Check if the filename length is greater than 7 to avoid error
    if len(filename) > 7:
        # Construct the old file path
        old_file_path = os.path.join(folder_path, filename)
        
        # Construct the new file name by removing the first seven characters
        new_filename = filename[7:]
        
        # Construct the new file path
        new_file_path = os.path.join(folder_path, new_filename)
        
        # Rename the file
        os.rename(old_file_path, new_file_path)
        print(f"Renamed '{old_file_path}' to '{new_file_path}'")

print("Renaming complete.")
