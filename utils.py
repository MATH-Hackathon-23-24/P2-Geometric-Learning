import matplotlib.pyplot as plt
import random
import geomstats.backend as gs
from geomstats.geometry.discrete_curves import insert_zeros

##################################################################
# --------- Resample curves ----------- -------------------------#
##################################################################

def get_curve_from_graph(node_id, graphs, function):
    nodes_list1 = random_graph_sequence(graphs[node_id])

    y1 = []
    for node in nodes_list1:
        y1.append(graphs[node_id].nodes[node][function])
    x1 = [i/(len(y1)-1) for i in range(len(y1))]
    return x1, y1

def extrapolate_discrete_function(x_vals, y_vals, domain=[0.0, 1.0]):
    def new_fct(x):
        if not domain[0] <= x <= domain[1]:
            return 0
        i = 0
        while x > x_vals[i] and i < len(x_vals):
            i += 1
        if x >= x_vals[i] or i == 0:
            return y_vals[i]
        a = x_vals[i - 1]
        b = x_vals[i]
        fa = y_vals[i - 1]
        fb = y_vals[i]
        return fa + (x - a) * (fb - fa) / (b - a)
    return new_fct

def sample_curve(fct, k_sampling_points=100, domain=[0.0, 1.0]):
    x_vals = [domain[0] + k * (domain[1] - domain[0]) / (k_sampling_points - 1) for k in range(k_sampling_points)]
    y_vals = [fct(x) for x in x_vals]
    return x_vals, y_vals

def resample_curve(x_vals, y_vals,  k_sampling_points=100, domain=[0.0, 1.0]):
    return sample_curve(
        extrapolate_discrete_function(x_vals, y_vals, domain), k_sampling_points, domain
    )

##################################################################
# --------- Function for networkx graph -------------------------#
##################################################################

def remove_undirected_edges(G):
    rem = set()
    for x, y in G.edges:
        if (y,x) in G.edges:
            rem.add((x,y))
            rem.add((y,x))
    for x,y in rem:
        G.remove_edge(x,y)

##################################################################
# --------- Plot function ---------------------------------------#
##################################################################

def plot_curve(curve, fmt="o-k", ax=None, add_origin=True):
    if ax is None:
        fig, ax = plt.subplots(figsize=(7, 7))

    if add_origin:
        curve = insert_zeros(curve, axis=-2)
    ax.plot(curve[:, 0], curve[:, 1], fmt)

    return ax

def plot_function(nodes_list, graphs, node_id, function):
    y = []
    for node in nodes_list:
        y.append(graphs[node_id].nodes[node][function])
    x = [i/(len(y)-1) for i in range(len(y))]
    plt.plot(x,y)
        
##################################################################
# --------- Make Sequence from Graph-----------------------------#
##################################################################

def core_node(graph):
    for n in graph.nodes():
        if graph.out_degree(n) == 0:
            return n
    return None

def extend_tail_randomly(graph, tail):
    if len(tail) == len(graph.nodes):
        return tail
    interlayer = set()
    for n in tail:
        for p in graph.predecessors(n):
            interlayer.add(p)
    for n in tail:
        if n in interlayer:
            interlayer.remove(n)
    tail.append(random.choice([i for i in interlayer]))
    return tail
    
def random_graph_sequence(graph):
    core = core_node(graph)
    tail = [core]
    for i in range(len(graph.nodes)):
        tail = extend_tail_randomly(graph, tail)
    tail.reverse()
    return tail