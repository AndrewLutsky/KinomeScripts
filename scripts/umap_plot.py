import sklearn
import numpy as np
import umap.umap_ as umap
from sklearn import manifold
import matplotlib.pyplot as plt
import create_dist_mat as cdm
import seaborn as sb


dist_mat = cdm.get_dist_mat('../FuzCav/scores.txt', True)
print(dist_mat)
#labels = ['kinome'] * 10 + ['estrogen'] * 14

#dict_labels = {'kinome': "yellow", 'estrogen': "blue"}

#labels = [dict_labels[label] for label in labels]
# Create a umap given a distance matrix. 

reducer = umap.UMAP(metric='precomputed')
    
# Fit the model to your distance matrix and transform it into a 2D embedding

embedding = reducer.fit_transform(dist_mat)


#for label in np.unique(labels):
#        indices = [i for i, x in enumerate(labels) if x == label]
#        plt.scatter(embedding[indices, 0], embedding[indices, 1], label=label)
# Plotting the result
plt.scatter(embedding[:, 0], embedding[:, 1])

plt.title('UMAP projection of the dataset')
plt.xlabel('UMAP 1')
plt.ylabel('UMAP 2')
plt.legend()
plt.show()
 
