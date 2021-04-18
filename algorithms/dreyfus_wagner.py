from helper import _sorted_k_partitions

import networkx as nx
import numpy as np
import pandas as pd
import itertools
from typing import List, Tuple
import math 

'''
graph is the previously read and consturcted networkx graph. The nodes contained in the graph must be labeld by integers in increasing order (1,2,...,n) (all the Steiner test sets we've seen so far have this form.)

Y is the list of all terminals, (this notation was introduced in the paper by Dreyfus and Wagner - in the code we use the respective small letter 'y' or 'all_terminals_y')
C is the set of Y-{q} where q is one node from Y. (in the code this set is called: terminals)
n is the number of Nodes


Note: Node lables in tupels must always be sorted!

Tested with: http://steinlib.zib.de/showset.php?LIN
- lin01
- lin02 
the implemented algorithm found the optimal solution.
'''
def dreyfus_wagner(graph, y:List[int]):
    '''
    matrix D of direct distances - contains for every u and v in the set of all nodes N the length of the shortest path. This information will be saven safed in the DataFrame: df_direct_dists.
    matrix S of shortest paths between sets of terminal nodes. will be filled bit by bit as the alorithm proceeds. This technique of building up of larger optimal solutions from optimal solutions of all possible smaller problems is the fundamental technique in the general methodology called dynamic programming.
    '''

    all_terminals_y = list(y)
    q: int  = y.pop(0)    
    terminals: List[int] = sorted(y) # list of terminals without the node q. (Y -{q})
    nodes: List[int] = sorted(graph.nodes())
    
    row_indices: List = []
    # d_row_indices: List = []
    one_elem_sets: List = []
    opt: float = math.inf # in the paper opt is denoted as v.
    u: float
    
    # creation of our datastructure.
    df_direct_dists, df_steiner =  _create_matrices(terminals, nodes, row_indices)
    
    # initialization of our data strucutre with shortes paths.
    _initialize_matrices(graph, df_direct_dists, df_steiner, nodes, all_terminals_y)

    for t in all_terminals_y:
        one_elem_sets.append(str((t,)))
    # using list comprehension to create D, which is the list of all tuples contained in C with length >= 2.
    combinations_d = [i for i in row_indices if i not in one_elem_sets]
    
    ''' 
    for each E such that D[1] (the first element of D) is in E and E is a proper subset of D
    the latter needs to be performed for each set in D.
    '''
    #print(f'algorithm stops at count: {len(combinations_d)}')
    for indx,d in enumerate(combinations_d):
        #print(f'count: {indx+1}')
        for node in nodes:
            u:float = math.inf
            tpl = eval(d) # no problem, since We know that only strings that contain a tuple (as a str) are passed.
            tpl = list(tpl)
            combinations = _sorted_k_partitions(tpl,2) # we split d into E and F. 
            for comb in combinations:
                E:Tuple 
                F:Tuple  
                E,F = comb
                u = min(u, df_steiner.loc[[str(E)], node].values[0] + df_steiner.loc[[str(F)], node].values[0])
                for n in nodes:
                    df_steiner.loc[[d], n] = min(df_steiner.loc[[d], n].values[0], df_direct_dists.loc[[n],node].values[0] + u)

    for node in nodes:
        u = math.inf
        combinationso_E = _sorted_k_partitions(terminals,2)

        for comb in combinationso_E:
            E:Tuple 
            F:Tuple  
            E,F = comb 
            u = min(u, df_steiner.loc[[str(E)], node].values[0] + df_steiner.loc[[str(F)], node].values[0])

        opt = min(opt, df_direct_dists.loc[[q], node].values[0] + u)

    return opt        


def _create_matrices(terminals:List[int], nodes:int,row_indices: List): 
    '''
    returns list of two matrices [D,S]
    D = Distance matrix of all nodes - dimension: n x n
    
    S = Distance matrix of all subsets of C - dimension: 2^{||C||}-2 x n ("power set of C-2. minus 2, because the whole set C and the empty set should not be part)
    Speaking in peudocode it the matrix combining S[{t},j] and S[D,i], wehre i and j are the \ in N,
    {t} is \ in C it denotes a single terminal. D are all proper subsets of C.
    
    Note we decided to label the rows by the string representation of each subset D of C.
    To avoid ambiguity namings, the sets are expressed as tuples. Each tuples elements are always soreted in increasing order. So the labels may look like this:
    (1,)
    (2,)
    ...
    (1,2)
    (1,3)
    
    '''
    n: int = len(nodes) #number of nodes
    inf: float = math.inf # This is a default value representing an shortest path length. Note that a default value of -1 would not work, because we always try to find a minimum in later steps. Since we hav eno negative edge weights per definition, the min-funciton would always choose the default value of -1. 
 

    # Here we determin the row labels of the Steiner-Matrix. 
    for m in range(1, len(terminals)): # range from 1,3,..,C-1, since range does not include the last value specified.
        for row in list(itertools.combinations(terminals, m)): # itertools returns all combinations of length m that can be constructed given the set of elements in 'terminals'.
            row_indices.append(str(row)) 

    #NumPy arrays are immutable! So we create them once we know the dimensions. 
    s_full = np.full([len(row_indices),n], dtype=float, fill_value=inf) 
    dd = np.full([n,n], dtype=float, fill_value=inf) #dd = direct distances.

    df_dd = pd.DataFrame(dd, columns = nodes, index=range(1, n + 1)) 
    df_s = pd.DataFrame(s_full, columns = nodes, index=row_indices)

    # take a look at the two matrices.
    #print(df_steiner)
    #print(df_direct_dists)
    return [df_dd, df_s]


def _initialize_matrices(graph, df_direct_dists, df_steiner, nodes, all_terminals_y):  #-> List[Tuple]
    '''
    calculating shortest paths between our terminals in C and all vertices in N.
    for each terminal in C (that is the whole set of terminals - {q}, wehre q can be any node in Y) we construct a list to each node in V.
    that is (3) S[{t},J] <- D(t,J)
    '''
    
    #init Matrix D of shortest distances between any two nodes in the graph.
    for row in nodes:
        for col in nodes:
           df_direct_dists.loc[row, col] = nx.shortest_path_length(graph,source=row, target=col, weight='weight') 

    
    for terminal in all_terminals_y:
        # l: List = []
        for node in nodes:
            df_steiner.loc[str((terminal,)), node] = nx.shortest_path_length(graph,source=node, target=terminal, weight='weight')
