import networkx as nx
import numpy as np

def is_flake_of_stone(flake_id, stone_id) -> bool:
    return flake_id[:len(stone_id)] == stone_id

def z_score_normalize(data):
    # normalize 1D data array
    mean = np.nanmean(data)
    std_dev = np.nanstd(data)
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

def nan_helper(y):
    """Helper to handle indices and logical indices of NaNs.

    Input:
        - y, 1d numpy array with possible NaNs
    Output:
        - nans, logical indices of NaNs
        - index, a function, with signature indices= index(logical_indices),
          to convert logical indices of NaNs to 'equivalent' indices
    Example:
        >>> # linear interpolation of NaNs
        >>> nans, x= nan_helper(y)
        >>> y[nans]= np.interp(x(nans), x(~nans), y[~nans])
    """

    return np.isnan(y), lambda z: z.nonzero()[0]

def read_and_normalize_property_data(dataset, stone_ids):
    # collect continuous data and normalize
    data_collection = {}
    for id in stone_ids:
        data_collection[id] = {"weight": [],
                                "volume": [],
                                "surface": [],
                                "scar_count": []}
        
    for index, row in dataset.iterrows():
        id1 = row['Sample_ID'][:-2]
        id2 = row['Sample_ID'][:-1]
        id3 = row['Sample_ID'][:-3]
        if id1 in stone_ids:
            id = id1
        elif id2 in stone_ids:
            id = id2
        elif id3 in stone_ids:
            id = id3
        else:
            id = None
        if id not in stone_ids:
            continue
        data_collection[id]["surface"].append(row['Surface_Area_mm^2']) 
        data_collection[id]["volume"].append(row['Volume_mm^3'])
        data_collection[id]["weight"].append(row['Weight_g'])
        data_collection[id]["scar_count"].append(row['Dorsal_scar_count'])
        
    for stone_id, data in data_collection.items():
        for prop, values in data.items():
            values = np.array(values)
            if np.isnan(values).all():
                continue
            nans, x= nan_helper(values)
            values[nans]= np.interp(x(nans), x(~nans), values[~nans])
            #Find indices that you need to replace
            #inds = np.where(np.isnan(values))
            #values[inds] = np.nanmedian(values)
            # normalize the data (after replacing nans)
            values = z_score_normalize(values)  
            data_collection[stone_id][prop] = values
    return data_collection