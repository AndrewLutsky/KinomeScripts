with open("fuzcav_dist.txt","r") as f:
    lines = f.readlines()
    dict = {}
    for line in lines:
        line = line.split()
        dict[(line[0],line[1])] = float(line[2])

