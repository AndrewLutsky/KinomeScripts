import os
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import numpy as np
from sklearn.neighbors import NearestNeighbors
import plotly.express as px
import pandas as pd

def read_inv(file_path):
    with open(file_path, 'r') as file:
    
        length = int(file.readline().strip())
        
        vector = []
        
        for _ in range(length):
            line = file.readline().strip()  
            element = float(line)  
            vector.append(element) 
    
    return vector

def distance(vector1, vector2):
    if len(vector1) != len(vector2):
        raise ValueError("Vectors must be of the same length")
    
    squared_diff_sum = sum((a - b) ** 2 for a, b in zip(vector1, vector2))
    
    euclidean_distance = squared_diff_sum ** 0.5
    
    return euclidean_distance

def read_all_inv(input_dir):
    vectors = []
    ids = []
    # Iterate through all files in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith(".inv"):
            input_file_path = os.path.join(input_dir, filename)
            vector = read_inv(input_file_path)
            vectors.append(vector)
            id = filename[:6]
            ids.append(id)
            #print(id)
    return vectors, ids

def generate_dist_matrix(vectors):
    # Initialize a matrix of zeros with the appropriate dimensions
    n = len(vectors)
    dist_matrix = [[0 for _ in range(n)] for _ in range(n)]
    
    # Compute the distance between each pair of vectors
    for i in range(n):
        for j in range(i, n):  # No need to calculate when j < i, matrix is symmetric
            if i == j:
                # The distance between a vector and itself is 0
                dist_matrix[i][j] = 0
            else:
                # Use the distance function you have for vectors i and j
                d = distance(vectors[i], vectors[j])
                dist_matrix[i][j] = dist_matrix[j][i] = d
                
    return dist_matrix

def cluster(dist_matrix):
    dbscan = DBSCAN(eps=2.5, min_samples=3, metric='precomputed')
    clusters = dbscan.fit_predict(dist_matrix)
    return clusters

def plotly_vis(vectors, clusters, pdb_ids):
    df = pd.DataFrame(vectors, columns=[f'feature_{i}' for i in range(121)])
    df['pdb_id'] = pdb_ids  # Adding PDB IDs
    df['cluster'] = clusters  # Adding cluster labels

    # Perform PCA
    pca = PCA()
    components = pca.fit_transform(df.iloc[:, :-2])  # Exclude the last two columns (pdb_id and cluster)

    # Create labels for the PCA components
    labels = {
        str(i): f"PC {i+1} ({var:.1f}%)"
        for i, var in enumerate(pca.explained_variance_ratio_ * 100)
    }

    # Since plotting all components can be overwhelming, focus on the first few for visualization
    dimensions = range(4)  # Adjust based on how many PCs you want to visualize

    # Plotting the PCA components
    fig = px.scatter_matrix(
        components,
        labels=labels,
        dimensions=dimensions,
        color=df["cluster"].astype(str)  # Using cluster labels for coloring
    )
    fig.update_traces(diagonal_visible=False)
    if not os.path.exists("plots"):
        os.mkdir("plots")
    fig.write_image("plots/DBSCAN_eps_2-5_min_3.png")
    fig.show()
    


vectors, ids = read_all_inv("pocket_3dzds")

dist_matrix = generate_dist_matrix(vectors)
#print(dist_matrix)

clusters = cluster(dist_matrix)

plotly_vis(vectors, clusters, ids)