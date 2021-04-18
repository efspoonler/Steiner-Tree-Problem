'''
This code was copied from: 
https://networkx.org/documentation/networkx-2.2/_modules/networkx/algorithms/approximation/steinertree.html#steiner_tree

It will be used to evaluate/compare our implementation against another, pre-defined one.

'''


import networkx as nx
import itertools

from helper import pairwise_helper, get_list_of_edges


'''
Shortest distance graph.
'''
def constant_factor_approximation(G, terminals):
    # create metric closure G_L on the terminal set
    # 1. create fully connected graph on the terminal set (default weight = 11.11)
    # update edges with the calculated weights

    #metric_closure = []
    steiner = []

    '''
    The graph MC contains the metric closure.
    The metric closure is a complete graph in which we connect all terminal nodes.
    The edge weights are equal to the shortest path length in our graph G! 
    '''
    
    MC = nx.Graph() #MC => Metric Closure
   
    # 1.
    for e in itertools.combinations(terminals,2): #creates all combinations of tuples (Note: (1,2) === (2,1)! Since we are undirected.) .  
        weight, path = nx.single_source_dijkstra(G, source=e[0], target=e[1]) # we save the path for later use, so we do not have to calc it twice!
        MC.add_edge(*e, weight=weight, path=path) #the metric closures edges have the weight of the shortest path between v and w in G.
    
    '''
    Calculate a minimum sapnning tree (MST). Networkx uses Kruskal's algorithm.  
    '''
    MST = nx.minimum_spanning_tree(MC, weight='weight') # define which key/value pair defines the edges's weight. In our case it is 'weight'
    list_of_paths = [data['path'] for (u,v, data) in sorted(MST.edges(data=True))] #each list contains a sequence of nodes representing an edge.
    
    
    #create a list of paths which define our steiner graph
    for paths in list_of_paths: 
        steiner.append(list(pairwise_helper(paths)))
    
    #Note: there could be duplicate edges in the list, but Networkx ignores them.
    Steiner_Graph = G.edge_subgraph(get_list_of_edges(steiner)) # we pass a list of edges to our Graph G. The resulting graph contains all edges and their incident nodes.
    

    ''' 
    #here we empirically searched for leafe node that are steiner nodes. -> did not found any.
    degrees = [ node for (node, val) in Steiner_Graph.degree() if val == 1]
    for node in degrees:
        if node not in terminals:
            print(f'node: {node} is a steiner node and is a leaf. therefore we can remove it and get a smaller steiner graph!')
    '''
    
    approx = Steiner_Graph.size(weight='weight') 
    return approx 