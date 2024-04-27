import os
from scipy.spatial.distance import cdist
from sklearn import metrics
import matplotlib.pyplot as plt
import numpy as np
import math


def read_tough_m1():
    neg_list_path = "tough-m1/TOUGH-M1_negative.list"
    pos_list_path = "tough-m1/TOUGH-M1_positive.list"

    tough_labels = {}

    with open(neg_list_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            pair = (parts[0], parts[1])
            tough_labels[pair] = 1

    with open(pos_list_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            pair = (parts[0], parts[1])
            tough_labels[pair] = 0
    
    return tough_labels




def read_conforms():
    kin_data_path = "paper_data/paper_data.txt"
    est_data_path = "paper_data/er_labels.csv"
    pdbs = []
    pdb_sidechain = {}
    pdb_conforms = {}
    with open(kin_data_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if parts[9] == "NA" or parts[9] == "10_PDB_validation":
                continue
            pdb = parts[9]
            pdbs.append(pdb)
            pdb_sidechain[pdb[0:4]] = pdb[4]
            pdb_id = pdb[0:4].lower() + pdb[4]
            if parts[10] == "NA":
                pdb_conforms[pdb_id] = "kin_na"
            else:
                pdb_conforms[pdb_id] = parts[10]
    with open(est_data_path, 'r') as file:
        for i, line in enumerate(file):
            if i < 2:
                continue
            parts = line.strip().split(sep=',')
            id = parts[1]
            #print(id)
            #print(parts[-2])
            if parts[-2] == 'Alpha':
                pdb_conforms[id] = 'Alpha'
            elif parts[-2] == 'Beta':
                pdb_conforms[id] = 'Beta'
            else:
                pdb_conforms[id] = 'est_na'
    #print(pdb_conforms)
    
    return pdbs, pdb_sidechain, pdb_conforms


def read_fuzcav(input_path, kinome=True):

    if kinome: 
        kinase_vectors = {}
        est_vectors = {}
        all_vectors = {}

        with open(input_path, 'r') as file:
            for line in file: 
                parts = line.strip().split(sep = ':')
                filename = parts[0].strip()
                str_vector = parts[1].strip().split(sep=';')
                vector = [float(item) for item in str_vector]
                if filename.endswith('pocket'):
                    pdb = filename[0:6]
                    chain = pdb[-1]
                    id = pdb[0:4].lower() + chain

                    kinase_vectors[id] = vector
                    all_vectors[id] = vector
                else:
                    id = filename.lower()
                    est_vectors[id] = vector
                    all_vectors[id] = vector
        return kinase_vectors, est_vectors, all_vectors
    else:
        fuz_tough_vectors = {}
        with open(input_path, 'r') as file:
            for line in file: 
                parts = line.strip().split(sep = ':')
                filename = parts[0].strip()
                str_vector = parts[1].strip().split(sep=';')
                vector = [float(item) for item in str_vector]

                id = filename[0:5]
                fuz_tough_vectors[id] = vector
        return fuz_tough_vectors
                
def read_tm(file_path):
    names = []
    mat = []

    with open(file_path, 'r') as file:
        for i, line in enumerate(file):
            if i == 0:
                continue
            parts = line.strip().split()
            id = parts[0]
            if '_' in id:
                chain = id[-1]
                names.append(id[0:4].lower() + chain)
            else:
                names.append(id)
            dists = parts[1:]
            row = [float(item) for item in dists]
            mat.append(row)
    return names, mat

def read_inv(file_path):
    with open(file_path, 'r') as file:
    
        length = int(file.readline().strip())
        
        vector = []
        
        for _ in range(length):
            line = file.readline().strip()  
            element = float(line)  
            vector.append(element)
    
    return vector

def manhattan_distance(pocket1, pocket2):
    if len(pocket1) != len(pocket2):
        raise ValueError("Both vectors must have the same length")
    
    return sum(abs(a - b) for a, b in zip(pocket1, pocket2))

def euclidean_distance(list1, list2):
    if len(list1) != len(list2):
        raise ValueError("Both lists must have the same length")
    
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(list1, list2)))

def read_3dzds(input_dir):
    kinase_vectors = {}
    est_vectors = {}
    all_vectors = {}
    
    for filename in sorted(os.listdir(input_dir)):
        if filename.endswith("pocket.inv"):
            input_file_path = os.path.join(input_dir, filename)
            vector = read_inv(input_file_path)
    
            pdb = filename[0:6]
            chain = pdb[-1]
            id = pdb[0:4].lower() + chain

            kinase_vectors[id] = vector
            all_vectors[id] = vector
        else:
            input_file_path = os.path.join(input_dir, filename)
            vector = read_inv(input_file_path)
            id = filename[0:4].lower()

            est_vectors[id] = vector
            all_vectors[id] = vector
           
    return kinase_vectors, est_vectors, all_vectors

def read_tough_zd(input_dir):
    tough_vectors = {}

    for filename in sorted(os.listdir(input_dir)):
        input_file_path = os.path.join(input_dir, filename)
        vector = read_inv(input_file_path)

        id = filename[0:5]

        tough_vectors[id] = vector
    
    return tough_vectors


def tough_m1_roc_plot():
    tough_labels = read_tough_m1()
    print("read in tough labels")

    tough_zd_path = "tough-m1/tough_zd"
    fuz_path = "tough-m1/fcav_tough_vectors.txt"

    tough_zds = read_tough_zd(tough_zd_path)
    print("read in tough zds")

    tough_fcs = read_fuzcav(fuz_path, kinome=False)
    print("read in tough fcs")

    labels = []
    zd_dists = []
    fc_dists = []
    i = 1
    total = len(list(tough_labels.keys()))
    for pair, label in tough_labels.items():
        pocket1 = pair[0]
        pocket2 = pair[1]
        percent = round((i*100)/total, 2)
        print(f"calculating dist for key {i}, {percent} complete")
        i += 1
        if (pocket1 in tough_fcs) and (pocket2 in tough_fcs):
            dist_zd = manhattan_distance(tough_zds[pocket1], tough_zds[pocket2])
            #dist_zd = euclidean_distance(tough_zds[pocket1], tough_zds[pocket2])
            dist_fc = manhattan_distance(tough_fcs[pocket1], tough_fcs[pocket2])
            labels.append(label)
            zd_dists.append(dist_zd)
            fc_dists.append(dist_fc)
    
    print("calculated distances")
    all_dists = [zd_dists, fc_dists]
    #all_dists = [zd_dists]

    dist_labels = ["Zernike", "FuzCav"]
    #dist_labels = ["Zernike"]

    labels_arr = np.array(labels)
    
    plt.figure(figsize=(10, 8))
    
    for i, dist_list in enumerate(all_dists):
        dist_label = dist_labels[i]
        fpr, tpr, _ = metrics.roc_curve(labels_arr, dist_list)
        roc_auc = metrics.auc(fpr, tpr)
        legend_label = ""
        if dist_label.startswith('Z'):
            legend_label = "Zernike "  + "(AUC = %0.2f)" % roc_auc
        elif dist_label.startswith('F'):
            fpr, tpr, _ = metrics.roc_curve(1-labels_arr, dist_list)
            roc_auc = metrics.auc(fpr, tpr)
            legend_label = "FuzCav "  + "(AUC = %0.2f)" % roc_auc
        else:
            legend_label = "TMAlign " + "(AUC = %0.2f)" % roc_auc
        print(f"plotting {dist_label}")
        plt.plot(fpr, tpr, lw=2, label=legend_label)
    
    plt.plot([0, 1], [0, 1], color='navy', linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Tough M1 ROC')
    plt.legend(loc="lower right")
    plt.savefig('plots/tough_m1_roc_plot.png', dpi=300)
    plt.show()
    





def all_roc_plot(conform=True):
    #tough_labels = read_tough_m1()
    #print(tough_labels)

    _,_, pdb_conforms = read_conforms()

    zd_3A_path = "Zernike/3A_3dzds"
    zd_5A_path = "Zernike/5A_3dzds"
    zd_7A_path = "Zernike/7A_3dzds"
    zd_9A_path = "Zernike/9A_3dzds"

    fc_3A_path = "FuzCav/tyler_scores/3A_scores.txt"
    fc_5A_path = "FuzCav/tyler_scores/5A_scores.txt"
    fc_7A_path = "FuzCav/tyler_scores/7A_scores.txt"
    fc_9A_path = "FuzCav/tyler_scores/9A_scores.txt"

    tm_3A_path = "TMAlign/tm_3A.txt"
    tm_5A_path = "TMAlign/tm_5A.txt"
    tm_7A_path = "TMAlign/tm_7A.txt"
    tm_9A_path = "TMAlign/tm_9A.txt"

    names_3A, tm_3A_mat = read_tm(tm_3A_path)
    names_5A, tm_5A_mat = read_tm(tm_5A_path)
    names_7A, tm_7A_mat = read_tm(tm_7A_path)
    names_9A, tm_9A_mat = read_tm(tm_9A_path)


    kin_zds_3A, est_zds_3A, all_zds_3A = read_3dzds(zd_3A_path)
    kin_zds_5A, est_zds_5A, all_zds_5A = read_3dzds(zd_5A_path)
    kin_zds_7A, est_zds_7A, all_zds_7A = read_3dzds(zd_7A_path)
    kin_zds_9A, est_zds_9A, all_zds_9A = read_3dzds(zd_9A_path)

    kin_fc_3A, est_fc_3A, all_fc_3A = read_fuzcav(fc_3A_path)
    kin_fc_5A, est_fc_5A, all_fc_5A = read_fuzcav(fc_5A_path)
    kin_fc_7A, est_fc_7A, all_fc_7A = read_fuzcav(fc_7A_path)
    kin_fc_9A, est_fc_9A, all_fc_9A = read_fuzcav(fc_9A_path)

    all_sets = [set(all_zds_3A), set(all_zds_5A), set(all_zds_7A), set(all_zds_9A), set(all_fc_3A), set(all_fc_5A), set(all_fc_7A), set(all_fc_9A)]
    kin_sets = [set(kin_zds_3A), set(kin_zds_5A), set(kin_zds_7A), set(kin_zds_9A), set(kin_fc_3A), set(kin_fc_5A), set(kin_fc_7A), set(kin_fc_9A)]
    est_sets = [set(kin_zds_3A), set(est_zds_5A), set(est_zds_7A), set(est_zds_9A), set(est_fc_3A), set(est_fc_5A), set(est_fc_7A), set(est_fc_9A)]

    all_labels = []
    all_pockets = list(set.intersection(*all_sets))
    all_kin = list(set.intersection(*kin_sets))
    all_est = list(set.intersection(*est_sets))

    zd_all_dists_3A = []
    zd_all_dists_5A = []
    zd_all_dists_7A = []
    zd_all_dists_9A = []

    fc_all_dists_3A = []
    fc_all_dists_5A = []
    fc_all_dists_7A = []
    fc_all_dists_9A = []

    tm_all_dists_3A = []
    tm_all_dists_5A = []
    tm_all_dists_7A = []
    tm_all_dists_9A = []
   
   

    for pocket1 in all_pockets:
        for pocket2 in all_pockets:
            
            zd_dist_3A = manhattan_distance(all_zds_3A[pocket1], all_zds_3A[pocket2])
            zd_dist_5A = manhattan_distance(all_zds_5A[pocket1], all_zds_5A[pocket2])
            zd_dist_7A = manhattan_distance(all_zds_7A[pocket1], all_zds_7A[pocket2])
            zd_dist_9A = manhattan_distance(all_zds_9A[pocket1], all_zds_9A[pocket2])

            fc_dist_3A = manhattan_distance(all_fc_3A[pocket1], all_fc_3A[pocket2])
            fc_dist_5A = manhattan_distance(all_fc_5A[pocket1], all_fc_5A[pocket2])
            fc_dist_7A = manhattan_distance(all_fc_7A[pocket1], all_fc_7A[pocket2])
            fc_dist_9A = manhattan_distance(all_fc_9A[pocket1], all_fc_9A[pocket2])

            zd_all_dists_3A.append(zd_dist_3A)
            zd_all_dists_5A.append(zd_dist_5A)
            zd_all_dists_7A.append(zd_dist_7A)
            zd_all_dists_9A.append(zd_dist_9A)

            fc_all_dists_3A.append(fc_dist_3A)
            fc_all_dists_5A.append(fc_dist_5A)
            fc_all_dists_7A.append(fc_dist_7A)
            fc_all_dists_9A.append(fc_dist_9A)

            tm_all_dists_3A.append(tm_3A_mat[names_3A.index(pocket1)][names_3A.index(pocket2)])
            tm_all_dists_5A.append(tm_5A_mat[names_5A.index(pocket1)][names_5A.index(pocket2)])
            tm_all_dists_7A.append(tm_7A_mat[names_7A.index(pocket1)][names_7A.index(pocket2)])
            tm_all_dists_9A.append(tm_9A_mat[names_9A.index(pocket1)][names_9A.index(pocket2)])

            if conform:
                if pdb_conforms[pocket1] == pdb_conforms[pocket2]:
                    all_labels.append(0)
                else:
                    all_labels.append(1)
            else:
                if (pocket1 in all_kin and pocket2 in all_kin) or (pocket1 in all_est and pocket2 in all_est):
                    all_labels.append(0)
                else:
                    all_labels.append(1)

    all_dists = [zd_all_dists_3A, zd_all_dists_5A, zd_all_dists_7A, zd_all_dists_9A, fc_all_dists_3A, fc_all_dists_5A, fc_all_dists_7A, fc_all_dists_9A, tm_all_dists_3A, tm_all_dists_5A, tm_all_dists_7A, tm_all_dists_9A]

    dist_labels = ['zd_all_dists_3A', 'zd_all_dists_5A', 'zd_all_dists_7A', 'zd_all_dists_9A', 'fc_all_dists_3A', 'fc_all_dists_5A', 'fc_all_dists_7A', 'fc_all_dists_9A', 'tm_all_dists_3A', 'tm_all_dists_5A', 'tm_all_dists_7A', 'tm_all_dists_9A']

    '''
    for pair, label in tough_labels.items():
        if pair[0] in zds and pair[1] in zds:
            dist = cdist(pair[0], pair[1], metric='cityblock')  
            all_labels.append(label)
            all_dists.append(dist)
    '''


    plt.figure(figsize=(10, 8))
    
    for i, dist_list in enumerate(all_dists):
        dist_label = dist_labels[i]
        angs = dist_label[-2]
        fpr, tpr, _ = metrics.roc_curve(all_labels, dist_list)
        roc_auc = metrics.auc(fpr, tpr)
        legend_label = ""
        if dist_label.startswith('z'):
            legend_label = "Zernike " + str(angs) + "A (AUC = %0.2f)" % roc_auc
        elif dist_label.startswith('f'):
            #labels_arr = np.array(all_labels)
            #fpr, tpr, _ = metrics.roc_curve(1-labels_arr, dist_list)
            #roc_auc = metrics.auc(fpr, tpr)
            legend_label = "FuzCav " + str(angs) + "A (AUC = %0.2f)" % roc_auc
        else:
            legend_label = "TMAlign " + str(angs) + "A (AUC = %0.2f)" % roc_auc
        plt.plot(fpr, tpr, lw=2, label=legend_label)
    
    plt.plot([0, 1], [0, 1], color='navy', linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Kinase v. ER Receptor ROC')
    plt.legend(loc="lower right")
    plt.savefig('plots/all_roc_plot.png', dpi=300)
    plt.show()


#all_roc_plot(conform=False)

tough_m1_roc_plot()



            

