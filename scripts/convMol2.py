import pymolPy3
import os
import sys


pm = pymolPy3.pymolPy3(0)

for file in os.listdir(sys.argv[1]):
    if file.endswith(".pdb"):
        pm("cd " + sys.argv[1])
        pm("load " + file)
        pm("save " + file.split(".")[0] + ".mol2")
        pm("delete all")
    else:
        continue
