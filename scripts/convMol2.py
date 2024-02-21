import subprocess
import os
for file in os.listdir("./prody_pockets_5A/"):
    fname = file[0:-4]
    cmd = ['/bin/zsh', '-i', '-c', f"pymol -c convMol2.pml -- {fname}"]
    result = subprocess.run(cmd, text = True, capture_output = True)
