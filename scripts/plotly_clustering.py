import os
from sklearn.cluster import DBSCAN
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.metrics.pairwise import pairwise_distances
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import numpy as np
from sklearn.neighbors import NearestNeighbors
import plotly.express as px
import pandas as pd


def read_pdbs_from_file(file_path):
    pdbs = []
    pdb_sidechain = {}
    pdb_conforms = {}
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if parts[9] == "NA" or parts[9] == "10_PDB_validation":
                continue
            pdb = parts[9]
            pdbs.append(pdb)
            pdb_sidechain[pdb[0:4]] = pdb[4]
            pdb_id = pdb[0:4] + "_" + pdb[4]
            pdb_conforms[pdb_id] = parts[10]
    return pdbs, pdb_sidechain, pdb_conforms

def read_inv(file_path):
    with open(file_path, 'r') as file:
    
        length = int(file.readline().strip())
        
        vector = []
        
        for _ in range(length):
            line = file.readline().strip()  
            element = float(line)  
            vector.append(element) 
    
    return vector


def read_all_inv(input_dir):
    vectors = []
    ids = []
    # Iterate through all files in the input directory
    for filename in sorted(os.listdir(input_dir)):
        if filename.endswith(".inv"):
            input_file_path = os.path.join(input_dir, filename)
            vector = read_inv(input_file_path)
            vectors.append(vector)
            #id = filename[:6]
            id = filename[7:13]
            ids.append(id)
            #print(id)
    return vectors, ids




def k_means_clustering(vectors, k):
    # Initialize the KMeans model with the desired number of clusters
    kmeans = KMeans(n_clusters=k, random_state=42)
    
    # Fit the model on the data
    kmeans.fit(vectors)
    
    # Return the cluster labels for each data point
    return kmeans.labels_


def k_distance_plot(vectors, k):
    distance_matrix = pairwise_distances(vectors, metric='manhattan')

    # Sort the distances
    k_distances = np.sort(distance_matrix, axis=1)[:, k]

    # Sort the k distances
    sorted_k_distances = np.sort(k_distances)

    # Plot the k-distance plot
    plt.figure(figsize=(10, 6))
    plt.plot(sorted_k_distances)
    plt.xlabel('Data Points sorted by distance')
    plt.ylabel(f'Distance to {k}-th nearest neighbor')
    plt.title('k-Distance Plot')
    plt.grid(True)
    plt.show()



def dbscan_clustering(vectors, eps, min_samples):
   
    dbscan = DBSCAN(eps=eps, min_samples=min_samples, metric="manhattan")
    dbscan.fit(vectors)
    return dbscan.labels_

def agglomerative_clustering(vectors):
    clustering = AgglomerativeClustering(n_clusters=10, linkage="single", metric="manhattan").fit(vectors)
    return clustering.labels_

'''
plotly_vis takes as input a list of list called vectors, where each vector is a list of 121-element 3D Zernike Descriptor of a pocket.
It also takes as input a list of cluster labels corresponding to each pocket, a list of the PDB IDs, a list of their conformations, and a boolean flag
conform to indicate whether or not to color by conform. 
'''

def plotly_vis(vectors, clusters, pdb_ids, pdb_conforms, conform, hide_noise, recluster_noise=False, merge_clusters=False):
    df = pd.DataFrame(vectors, columns=[f'feature_{i}' for i in range(121)])
    df['pdb_id'] = pdb_ids  # Adding PDB IDs
    df['cluster'] = clusters  # Adding cluster labels
    df['conformation'] = df['pdb_id'].map(pdb_conforms)

    # Perform PCA
    pca = PCA()
    components = pca.fit_transform(df.drop(['pdb_id', 'cluster', 'conformation'], axis=1))

    pca_df = pd.DataFrame(components, columns=[f"PC {i+1}" for i in range(components.shape[1])])
    pca_df['pdb_id'] = df['pdb_id']  # Ensure pdb_id is correctly added as a column
    pca_df['conformation'] = df['conformation']
    pca_df['cluster'] = df['cluster']


    # Since plotting all components can be overwhelming, focus on the first few for visualization
    dimensions = [f"PC {i+1}" for i in range(4)]  
    labels = {
        f"PC {i+1}": f"PC {i+1} ({var:.1f}%)"
        for i, var in enumerate(pca.explained_variance_ratio_ * 100)
    }   
    
    
    ## re run DBSCAN on noise
    ## update clusters in noise_df to these clusters
    if recluster_noise:
        noise_indices = pca_df['cluster'] == -1
        noise_vectors = [vectors[i] for i in range(len(vectors)) if noise_indices.iloc[i]]
        noise_df = pca_df.loc[noise_indices].reset_index(drop=True).copy()
        if noise_vectors:  # Ensure there are noise points to cluster
            noise_labels = dbscan_clustering(noise_vectors, eps=2.75, min_samples=3)  # Adjust eps and min_samples as needed
            #noise_df = pca_df[noise_indices].reset_index(drop=True)
            noise_df['cluster'] = noise_labels  # Update cluster labels in noise_df
            
            new_cluster_offset = pca_df['cluster'].max() + 1
            noise_df['cluster'] = noise_df['cluster'].apply(lambda x: x + new_cluster_offset if x != -1 else x)

            for i, (is_noise, new_label) in enumerate(zip(noise_indices, noise_df['cluster'])):
                if is_noise:
                    pca_df.loc[pca_df.index[i], 'cluster'] = new_label

        else:
            noise_df = pd.DataFrame()  # No noise points to cluster

    if hide_noise:
        pca_df = pca_df[pca_df['cluster'] != -1]

    if merge_clusters:
        cluster_conformations = pca_df.groupby('cluster')['conformation'].unique()
        unique_conformation_clusters = {cluster: conformations[0] for cluster, conformations in cluster_conformations.items() if len(conformations) == 1}
        cluster_merge_map = {}
        new_cluster_id = max(pca_df['cluster']) + 1

        for cluster, conformation in unique_conformation_clusters.items():
            # If this conformation is not yet assigned a merge target, assign a new one
            if conformation not in cluster_merge_map.values():
                cluster_merge_map[cluster] = new_cluster_id
                new_cluster_id += 1
            else:
                # If this conformation already has a merge target, use the same target cluster ID
                target_cluster = [key for key, value in cluster_merge_map.items() if value == conformation][0]
                cluster_merge_map[cluster] = cluster_merge_map[target_cluster]
        pca_df['merged_cluster'] = pca_df['cluster']

        # Update the 'merged_cluster' column based on the merge map
        for original_cluster, new_cluster in cluster_merge_map.items():
            pca_df.loc[pca_df['cluster'] == original_cluster, 'merged_cluster'] = new_cluster

        
        

    if conform == False and not merge_clusters:
        fig = px.scatter_matrix(
        pca_df,
        labels=labels,
        dimensions=dimensions,
        #color=df["conformation"].astype(str),  
        color=pca_df["cluster"].astype(str), # Using cluster for coloring
        hover_data=["pdb_id", "cluster", "conformation"],
        color_discrete_sequence= px.colors.qualitative.G10
        )
    elif merge_clusters:
        fig = px.scatter_matrix(
        pca_df,
        labels=labels,
        dimensions=dimensions,
        #color=df["conformation"].astype(str),  
        color=pca_df["merged_cluster"].astype(str), # Using cluster for coloring
        hover_data=["pdb_id", "cluster", "conformation"],
        color_discrete_sequence= px.colors.qualitative.G10
        )

    else: 
        fig = px.scatter_matrix(
        pca_df,
        labels=labels,
        dimensions=dimensions,
        color=df["conformation"].astype(str),  # Using conformational state for coloring
        #color=pca_df["cluster"].astype(str),
        hover_data=["pdb_id", "cluster", "conformation"],
        color_discrete_sequence= px.colors.qualitative.Dark24
        
        )
    
    fig.update_traces(diagonal_visible=False)
    if not os.path.exists("plots"):
        os.mkdir("plots")

    width = 1920  
    height = 1080  
    scale = 2  

    #fig.write_image("plots/DBSCAN_2-5_min_3_color_clusters_2_5A_reclustered_2_75_min_3_no_noise.png", width=width, height=height, scale=scale)
    #fig.write_image("plots/KMeans_4_color_conforms_3A.png", width=width, height=height, scale=scale)
    #fig.write_image("plots/DBSCAN_2_5_min_3_2_5A_no_noise_merged_clusters.png", width=width, height= height, scale = scale)
    #fig.write_image("plots/DBSCAN_2-5_min_3_color_clusters_2_5A_manhattan.png", width=width, height=height, scale=scale)
    fig.show()
    

pdbs, pdb_sidechain, pdb_conforms = read_pdbs_from_file("paper_data.txt")

vectors, ids = read_all_inv("pocket_3dzds_2_5A")

#distance_matrix = pairwise_distances(vectors, metric='manhattan')
#mask = np.ones(distance_matrix.shape, dtype=bool)
#np.fill_diagonal(mask, 0)

#min_distance = np.min(distance_matrix[mask])
#print(f"Minimum non-zero distance: {min_distance}")

#max_distance = np.max(distance_matrix)
#print(f"Maximum distance: {max_distance}")

#print(distance_matrix)
#k_distance_plot(vectors, 4)

#clusters = dbscan_clustering(vectors, 21, 3)
#clusters = k_means_clustering(vectors, 4)
clusters = agglomerative_clustering(vectors)

#plotly_vis(vectors, clusters, ids, pdb_conforms, False, True)
plotly_vis(vectors, clusters, ids, pdb_conforms, conform =False, hide_noise = False, recluster_noise=False, merge_clusters=False)
#plotly_vis(vectors, clusters, ids, pdb_conforms, conform =False, hide_noise = False, recluster_noise=False, merge_clusters=False)
#plotly_vis(vectors, clusters, ids, pdb_conforms, conform =True, hide_noise = True, recluster_noise=False, merge_clusters=False)

'''
Leaderboard
- DBSCAN 2.5A e = 2.5, minpts = 3

'''