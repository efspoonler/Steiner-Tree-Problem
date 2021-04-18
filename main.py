from filehandler import read_file_data
from algorithms.approximation import constant_factor_approximation
from algorithms.dreyfus_wagner import dreyfus_wagner
from algorithms.dreyfus_wagner_parallel import dreyfus_wagner_parallel
from algorithms.heuristic import shortest_paths_heuristic
from algorithms.networkx_steiner_tree import steiner_tree

import networkx as nx
#import itertools
from typing import List, Tuple
from time import perf_counter
import csv
import os

WRITE_DATA = True

def main():
    edges:List[int]
    terminals: List[int]
    #optimal_solution: int
    # get working directory
    wd = os.getcwd()
    data_folder = wd + '/evaluation/graphs/test/' # chage this varible to anaylse other data sets
    print(wd)
    dataset_name: str = 'xxx' 
    data_header: List[str] = ['dataset_name', 'numb_edges', 'numb_nodes', 'numb_terminals', 'algorithm','alg_solution', 'optimal_solution', 'time']
    if WRITE_DATA:
        append_list_as_row(data_header, True)

    for file in sorted(os.listdir(data_folder)):
        filename = os.fsdecode(file)
        print('\n\nfilename')
        print(filename)
        dataset_name = filename
        #dataset_name = 'e06.stp'
        #read data
        edges, terminals, optimal_solution = read_file_data(data_folder+filename) # edges: [(u,v,w),(u,v,w),..] :: terminals [u,v,x,...] (single nodes) . #LIN/lin01.stp
        
        #create graph
        G = nx.Graph()
        G.add_weighted_edges_from(edges)
        
        for_csv = [dataset_name, optimal_solution, len(edges), len(G.nodes), len(terminals)]
        
        # Special cases - get ignored.
        if len(terminals) == 0:
            print(f'\nNo terminals defined - data set: {filename} gets ignored!\n')
        elif len(terminals) == 2:
            print(f'\njust two terminals are defined: problem can be solved by finding a single shortest path between u and v - data set: {filename} gets ignored!\n')
        elif len(terminals) == len(G.nodes):
             print(f'e\nvery node is a terminal, hence we just need to calc a MST - data set: {filename} is ignored!\n')    

        # Solving the problem     
        elif len(terminals) >=3: #otherwise the problem is 
            ''' 
            Since we modify the list of terminals in some algorithms, we need to pass a deep copy of our list of terminals.
            Note: list() does not make recusive copies of the inner objects, but since we know that terminals has the type List[int], we do not have to worry about that.
            '''
            measure_time('heuristic', shortest_paths_heuristic, (G, list(terminals)), for_csv)
            measure_time('approximation', constant_factor_approximation, (G,list(terminals)), for_csv)
            measure_time('networkx_approximation', steiner_tree, (G,list(terminals)), for_csv)
            measure_time('exact_parallel', dreyfus_wagner_parallel, (G,list(terminals)), for_csv)
            measure_time('exact', dreyfus_wagner, (G,list(terminals)), for_csv)


def measure_time(function_name:str, func, args:Tuple, for_csv:List) -> None:
    print(f'\n\nfunction \t : {function_name}')
    start: float = perf_counter()
    res: float = func(*args)
    stop: float  = perf_counter()
    exec_time: float  = stop - start
    
    if WRITE_DATA:
        datase_name, optimal_solution, numb_edges, numb_nodes, numb_terminals = for_csv
        append_list_as_row([datase_name, numb_edges, numb_nodes, numb_terminals, function_name, res, optimal_solution, exec_time])

    print(f'found solution \t : {res} \nexecution time \t : {exec_time} \n')

def append_list_as_row(row:list, create_new_file=False) -> None:
    mode = 'a+'
    if create_new_file:
        mode='w'

    with open('evaluation/evaluation.csv', mode=mode) as evaluation_file:
        evaluation_writer = csv.writer(evaluation_file, delimiter=',')
        evaluation_writer.writerow(row)
    



if __name__ == "__main__":
    main()
