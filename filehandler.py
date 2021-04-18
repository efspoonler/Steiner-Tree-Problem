#import os


'''
We describe the file format .gr, which is a simplification of  the STP file format.

The file starts with a line ‘SECTION Graph’. 
The next two lines are of the form ‘Nodes #nodes’ and ‘Edges #edges’, always in that order, where #nodes is the number of vertices and #edges is the number of edges of the graph. 
The #edges next lines are of the form ‘E u v w’ where u and v are integers between 1 and #nodes representing an edge between u and v of weight the positive integer w. 
The following line reads ‘END’ and finishes the list of edges.
There is then a section Terminals announced by two lines ‘SECTION Terminals’ and ‘Terminals #terminals’ where #terminals is the number of terminals. 
The next #terminals lines are of the form ‘T u’ where u is an integer from 1 to #nodes, which means that u is a terminal. Again, the section ends with the line ‘END’.

In Track 1 and 3, the file ends with a subsequent line ‘EOF’. Here is an example of a small graph.


SECTION Graph
Nodes 5
Edges 6
E 1 2 1
E 1 4 3
E 3 2 3
E 2 4 4
E 3 5 10
E 4 5 1
END

SECTION Terminals
Terminals 2
T 2
T 4
END

EOF


Note: 
"The #edges next lines are of the form ‘E u v w’ where u and v are integers between 1 and #nodes."
So we know nodes are numberd from 1,2,3,..,n-1,n
'''
def read_file_data(filepath):
    terminals = [] # List of terminals
    edges = [] # list of edges, each edge has the form: (v,u,weight)
    optimal_solution: int = -1 # optimal solution to the current problem.
    #file_path = wd + '/evaluation/' + file_name
    with open(filepath) as f:
      for line in f:
        line = line.rstrip() # Remove trailing whitespace.
        
        # Edge
        if line.startswith('E '): 
           e = line.split(' ') # ['E', 'node u', 'node v', 'weight (always positive!)'] - split ignores leading spaces.
           
           # Any hashable object can be used as a node (label). Because we want to use the lables as indexes we use integers.
           # networkx uses hashmaps to save the nodes -> dicts are hashmaps.
           edges.append((int(e[1]), int(e[2]), int(e[3])))  # cast weight to float.

        # Terminal   
        elif line.startswith('T '):
           terminals.append(int(line.split(' ')[1])) # ['T', 'Node lable']

        elif line.startswith('O '):   
           optimal_solution = int(line.split(' ')[1]) # ['OPT', 'Optimal Solution']

    return [edges, terminals, optimal_solution] 
