import networkx as nx
import itertools
from typing import List
from helper import pairwise_helper, get_list_of_edges

def shortest_paths_heuristic(G, terminals):
    shortes_paths: List = []
    steiner_graph_edges: List = []  # contains all edges of the found solution.
    root: int = terminals.pop(0)

    for terminal in terminals: #terminals is the set: terminals \ {root}
       # for every terminal t in terminals,
       # we calc the shortest path between d(root, t)
       _ , path = nx.single_source_dijkstra(G, source=root, target=terminal)
       shortes_paths.append(path)

    for paths in shortes_paths:  # could be done in one rush in the latter loop. But it is more clear in this way.
        steiner_graph_edges.append(pairwise_helper(paths))

    # Note: there could be duplicate edges in the list, but Networkx ignores them.
    # we pass a list of edges to our Graph G. The resulting graph contains all edges and their incident nodes.
    steiner_graph = G.edge_subgraph(get_list_of_edges(steiner_graph_edges))
    
    solution = steiner_graph.size(weight='weight')

    return solution

    

