import subprocess
import os
for file in os.listdir("../pockets/pockets_2_5A_mol2/"):
    fname = file[0:-4]
    cmd = ['/bin/zsh', '-i', '-c', f"pymol -c convMol2.pml -- {fname}"]
    result = subprocess.run(cmd, text = True, capture_output = True)
