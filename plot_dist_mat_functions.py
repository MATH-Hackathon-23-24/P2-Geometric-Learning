import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

from sklearn.manifold import MDS
from scipy.cluster.hierarchy import dendrogram
from sklearn.cluster import AgglomerativeClustering

def plot_diffusion_maps(distance_mat, labels, eps='auto', alpha=.5):
    if eps=='auto': eps = np.mean(distance_mat ** 2)
    L = np.exp(- distance_mat ** 2 / eps)
    D = np.diag(np.sum(L, axis=0))
    L_alpha = np.linalg.inv(D ** alpha) @ L @ np.linalg.inv(D ** alpha)
    D_alpha = np.diag(np.sum(L_alpha, axis=0))
    M = np.linalg.inv(D_alpha) @ L_alpha
    l, e = np.linalg.eigh(M.transpose())
    print(l)
    embedding = e[:, -2:]

    fig = plt.figure(figsize=(15, 15))
    plt.plot(embedding[:, 0], embedding[:, 1], 'ko')
    plt.axis('equal')
    plt.axis('off')
    
    for (i, coo) in enumerate(embedding): plt.text(coo[0], coo[1]+.05, labels[i])
    
def plot_dendrogram(model, **kwargs):
    # Create linkage matrix and then plot the dendrogram

    # create the counts of samples under each node
    counts = np.zeros(model.children_.shape[0])
    n_samples = len(model.labels_)
    for i, merge in enumerate(model.children_):
        current_count = 0
        for child_idx in merge:
            if child_idx < n_samples:
                current_count += 1  # leaf node
            else:
                current_count += counts[child_idx - n_samples]
        counts[i] = current_count

    linkage_matrix = np.column_stack(
        [model.children_, model.distances_, counts]
    ).astype(float)

    dendrogram(linkage_matrix, **kwargs)

def plot_hierachical_clustering(distance_mat, labels):
    clustering = AgglomerativeClustering(metric='precomputed', linkage='complete', compute_distances=True).fit(distance_mat)
    fig = plt.figure(figsize=(15, 10))
    plot_dendrogram(clustering, truncate_mode="level", color_threshold=0, labels=labels, above_threshold_color='k')
    
def plot_mds(distance_mat, labels):
    multidimensional_scaling = MDS(n_components=2, dissimilarity='precomputed', normalized_stress=False)
    embedding = multidimensional_scaling.fit_transform(distance_mat)
    embedding = embedding / np.max(embedding)

    fig = plt.figure(figsize=(15, 15))
    plt.plot(embedding[:, 0], embedding[:, 1], 'ko')
    plt.axis('equal')
    plt.axis('off')
    
    for (i, coo) in enumerate(embedding): plt.text(coo[0], coo[1]+.05, labels[i])