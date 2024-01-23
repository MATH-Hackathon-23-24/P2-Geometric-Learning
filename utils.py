import matplotlib.pyplot as plt
import random

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

def plot_function(nodes_list, graphs, node_id, function):
    y = []
    for node in nodes_list:
        y.append(graphs[node_id].nodes[node][function])
    x = [i/len(y) for i in range(len(y))]
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