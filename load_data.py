import networkx as nx
import numpy as np

def is_flake_of_stone(flake_id, stone_id) -> bool:
    return flake_id[:-2] == stone_id

def z_score_normalize(data):
    # normalize 1D data array
    mean = np.mean(data)
    std_dev = np.std(data)
    normalized_data = (data - mean) / std_dev
    return normalized_data

LETTERS = ['a', 'b', 'c', 'd', 'e', 'f',]

def create_graph(dataset, data_collection, stone_id):
    # create Graph for stone_id with node values from data_collection
    G = nx.DiGraph()
    data_index = 0
    for index, row in dataset.iterrows():
        if is_flake_of_stone(row['Sample_ID'], stone_id):
            weight = data_collection[stone_id]["weight"][data_index]
            volume = data_collection[stone_id]["volume"][data_index]
            surface = data_collection[stone_id]["surface"][data_index]
            scar_count = data_collection[stone_id]["scar_count"][data_index]
            data_index += 1
            G.add_node(row['Sample_ID'], weight= weight, volume=volume, surface=surface, scar_count=scar_count)
    for index, row in dataset.iterrows():
        if is_flake_of_stone(row['Sample_ID'], stone_id):
            for l in LETTERS:
                if row[f'Subsequent_removal_{l}'] == row[f'Subsequent_removal_{l}']:
                    G.add_edge(row['Sample_ID'], row[f'Subsequent_removal_{l}'])
    return G

def read_and_normalize_property_data(dataset, stone_ids):
    # collect continuous data and normalize
    data_collection = {}
    for id in stone_ids:
        data_collection[id] = {"weight": [],
                                "volume": [],
                                "surface": [],
                                "scar_count": []}
        
    for index, row in dataset.iterrows():
        id = row['Sample_ID'][:-2]
        if id not in stone_ids:
            continue
        data_collection[id]["surface"].append(row['Surface_Area_mm^2']) 
        data_collection[id]["volume"].append(row['Volume_mm^3'])
        data_collection[id]["weight"].append(row['Weight_g'])
        data_collection[id]["scar_count"].append(row['Dorsal_scar_count'])
        
    for stone_id, data in data_collection.items():
        for prop, values in data.items():
            values = np.array(values)
            #Find indices that you need to replace
            inds = np.where(np.isnan(values))
            values[inds] = np.nanmedian(values)
            # normalize the data (after replacing nans)
            values = z_score_normalize(values)  
            data_collection[stone_id][prop] = values
    return data_collection