import os


# Function that reads in a file and creates a dictionary that maps the distance between
# two pockets to a distance value.

def read_file(file):
    dist_dict = {}
    with open(file, 'r') as f:
        for line in f:
            line = line.split()
            key = line[0] + '_' + line[1]
            dist_dict[key] = float(line[2])
    return dist_dict



# Function that takes in a dictionary and writes index and key to a file.
def write_indices(dist_dict):
    with open('indices.txt', 'w') as f:
        idx = 0
        visited = set()
        for key in dist_dict.keys():
            i, _ = key.split('_')
            if i not in visited:
                f.write(str(idx) + ' ' + i + '\n')
                visited.add(i)
                idx += 1


# Function that takes in a dictionary and creates a distance matrix.
def create_dist_mat(dist_dict, rev, indices):
    # If rev is true we find 1-distance, else we find distance.
    # Create an n x n matrix where n is sqrt(number of keys).
    n = int(len(dist_dict)**0.5)
    dist_mat = [[0 for i in range(n+1)] for j in range(n+1)]
    for key in dist_dict.keys():
        i, j = key.split('_')
        i = indices[i]
        j = indices[j]
        if rev:
            dist_mat[i][j] = 1 - dist_dict[key]
        else:
            dist_mat[i][j] = dist_dict[key]
    return dist_mat


# Function that reads in indices.txt and turns it into a dictionary.
def read_indices():
    indices = {}
    with open('indices.txt', 'r') as f:
        for line in f:
            line = line.split()
            indices[line[1]] = int(line[0])
    return indices



# Function that returns the whole distance matrix given the file name.
def get_dist_mat(file, rev):
    dist_dict = read_file(file)
    write_indices(dist_dict)
    indices = read_indices()
    return create_dist_mat(dist_dict, rev, indices)



