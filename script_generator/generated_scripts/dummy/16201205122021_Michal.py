from PyQt5.QtCore import *

from PyQt5.QtWidgets import *

from PyQt5.QtGui import *

import os

import matplotlib.pyplot as plt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

import networkx as nx

from networkx.algorithms.bipartite.basic import color

#from filemanager import FileManager

#from graph import Graph

#from graphanalyzer import GraphAnalyzer

import numpy as np

#from bruteforce import display_nxgraph

from timeit import default_timer as timer

from datetime import timedelta



import itertools

import copy

#import networkx as nx

#import numpy as np

#import matplotlib.pyplot as plt



#import itertools

#import copy

#import networkx as nx

#import numpy as np

#import matplotlib.pyplot as plt



#import copy

#import networkx as nx

#import numpy as np

#import matplotlib.pyplot as plt

#import itertools



#import networkx as nx



#from bruteforce import getGraphFromBruteforce

#from bruteforceapproximation import getGraphFromBruteforceOptimized

#from graph import Graph

#from mcgregor import returnMinimumSupergraphMcGregor, utilizeMcGregor

#from supergraph import MinimalCommonSupergraph

#import copy

#from timeit import default_timer as timer

#from datetime import timedelta





'''

# paperG = [[0,1,0,1,0],

#           [1,0,1,0,0],

#           [0,1,0,1,0],

#           [1,0,1,0,1],

#           [0,0,0,1,0]]



paperG = [[0,1,0,0,0,0,0,1],

[1,0,1,0,0,0,0,0],

[0,1,0,1,0,0,1,0],

[0,0,1,0,1,0,0,0],

[0,0,0,1,0,0,0,0],

[0,0,0,0,0,0,1,0],

[0,0,1,0,0,1,0,1],

[1,0,0,0,0,0,1,0]]





# paperH =[[0,1,0],

#         [1,0,1],

#         [0,1,0]]



paperH = [[0,1,0,1,1],

[1,0,1,0,0],

[0,1,0,1,0],

[1,0,1,0,1],

[1,0,0,1,0]]



'''



"""Function deleting row and column that are at given index"""

def deleteVerticesAtIndex(_G, i):

    del _G[i]

    for row in _G:

        del row[i]

    return _G



"""Function switching rows in matrix"""

def changeRows(G, row_1, row_2):

    if row_1 != row_2:

        temp = []

        temp = G[row_1]

        G[row_1] = G[row_2]

        G[row_2] = temp

    return G



"""Function switching columns in matrix"""

def changeColumns(G, col_1, col_2):

    if col_1 != col_2:

        tG = []

        tmp =[]

        transpose(G,tG)

        changeRows(tG,col_1,col_2)

        transpose(tG, tmp)

        G = tmp

    return G



"""Function transposing adjacecy matrix"""

def transpose(l1, l2):

    # iterate over list l1 to the length of an item

    for i in range(len(l1[0])):

        # print(i)

        row =[]

        for item in l1:

            # appending to new list with values and index positions

            # i contains index position and item contains values

            row.append(item[i])

        l2.append(row)

    return l2



"""Function counting how many times 1 is in row.

In fact it tell us the number of edges"""

def countOnesInRow(lst):

    return lst.count(1)



"""Function that compares one of the permuatations of the bigger graph with the smaller graph,

   the permutation of th bigger graphhas exactly the same number of columns and rows as the

   smaller graph, because the bottom-most rows and right-most columns were removed from it"""

def comparator(bigReduced, small, maxCorrelation):

    g = []

    for i in range(len(bigReduced)):

        lst = list(itertools.repeat(0, len(bigReduced)))

        g.append(lst)

    n = 0

    for i in range(len(bigReduced)):

        for j in range(len(bigReduced)):

            if(bigReduced[i][j] == small[i][j] and small[i][j] == 1):

                g[i][j] = 1

                n = n + 1

    if n > maxCorrelation:

        return (g, n)

    else:

        return (None, None)



"""Function that displays graphs in a visual way using networkx package"""

def display_nxgraph(G, weighted = False):

    plt.figure(figsize=(5,5))

    pos = nx.spring_layout(G)  # positions for all nodes

    if (weighted == True):

        new_labels = dict(map(lambda x:((x[0],x[1]), str(x[2]['weight'])), G.edges(data = True)))

    nx.draw_networkx_nodes(G, pos, node_size=400)

    nx.draw_networkx_labels(G, pos, font_size=15, font_family='sans-serif')

    if (weighted == True):

        nx.draw_networkx_edge_labels(G,pos,edge_labels = new_labels)

    nx.draw_networkx_edges(G, pos, width=2)

    plt.axis('off')

    plt.show()



"""Main function, that is in charge of finding the maximum common subgraph. Internally it generates all

possible permutations of the bigger matrix i.e. all possibilities of ordering rows and columns of the matrix,

then it deletes bottom-most rows and right-most columns to adjust the size of the bigger matrix to the size of

the smaller one, and finally calls comparator() function, that actually finds maximum common subgraph"""

def generateSubgraph(big, small):

    rowOrder = list(range(len(big)))

    maxGraph = []

    maxSubgraph = []

    maxCorrelation = 0

    allRowPermutations = list(itertools.permutations(rowOrder))

    for rowPermutation in allRowPermutations:

        permutationMatrix = []

        permutationMatrixTranspose = []

        for i in range(len(big)):

            lst = list(itertools.repeat(0, len(big)))

            lst[rowPermutation[i]] = 1

            permutationMatrix.append(lst)

        transpose(permutationMatrix, permutationMatrixTranspose)

        adjMatrix = np.matmul(big, permutationMatrixTranspose)

        adjMatrix = np.matmul(permutationMatrix, adjMatrix)

        adjMatrix = adjMatrix.tolist()

        adjMatrixReduced = copy.deepcopy(adjMatrix)

        for j in range(len(big) - 1, len(small) - 1, -1):

            adjMatrixReduced = deleteVerticesAtIndex(adjMatrixReduced, j)

        subgraph, numCorrelation = comparator(adjMatrixReduced, small, maxCorrelation)

        if numCorrelation is None:

            continue

        else:

            maxGraph = adjMatrix

            maxSubgraph = subgraph

            maxCorrelation = numCorrelation

    return (maxGraph, maxSubgraph)





def getGraphFromBruteforce(paperG, paperH):



    if(len(paperG) > len(paperH)):

        big = copy.deepcopy(paperG)

        small = copy.deepcopy(paperH)

    else:

        big = copy.deepcopy(paperH)

        small = copy.deepcopy(paperG)

    maxGraph, maxSubgraph = generateSubgraph(big, small)



    # print("Bigger graph after permuting rows and columns isomorhpic to original one")

    # print(maxGraph)

    # print("Smaller graph")

    # print(small)

    # print("Maximum common subgraph")

    # print(maxSubgraph)



    ADJ = np.matrix(big)

    A = nx.from_numpy_matrix(ADJ)

    #display_nxgraph(A)

    ADJ1 = np.matrix(maxGraph)

    A1 = nx.from_numpy_matrix(ADJ1)

    #display_nxgraph(A1)

    ADJ2 = np.matrix(small)

    A2 = nx.from_numpy_matrix(ADJ2)

    #display_nxgraph(A2)

    ADJ3 = np.matrix(maxSubgraph)

    A3 = nx.from_numpy_matrix(ADJ3)

    #display_nxgraph(A3)

    #print(maxSubgraph)

    return (maxSubgraph, maxGraph)





'''

# paperG = [[0,1,0,1,0],

#           [1,0,1,0,0],

#           [0,1,0,1,0],

#           [1,0,1,0,1],

#           [0,0,0,1,0]]



# paperG = [[0,1,0,0,0,0,0,1,0,1,1,0,1,1,1,1,0,0,1,0,0,1,0,1,0,1,0,1,1,1,0,1,0],

# [0,1,0,0,0,0,0,1,0,1,1,0,1,1,1,1,0,0,1,0,0,1,0,1,0,1,0,1,1,1,0,1,0],

# [0,1,0,0,0,0,0,1,0,1,1,0,1,1,1,1,0,0,1,0,0,1,0,1,0,1,0,1,1,1,0,1,0],

# [0,1,0,0,0,0,0,1,0,1,1,0,1,1,1,1,0,0,1,0,0,1,0,1,0,1,0,1,1,1,0,1,0],

# [0,1,0,0,0,0,0,1,0,1,1,0,1,1,1,1,0,0,1,0,0,1,0,1,0,1,0,1,1,1,0,1,0],

# [0,1,0,0,0,0,0,1,0,1,1,0,1,1,1,1,0,0,1,0,0,1,0,1,0,1,0,1,1,1,0,1,0],

# [0,1,0,0,0,0,0,1,0,1,1,0,1,1,1,1,0,0,1,0,0,1,0,1,0,1,0,1,1,1,0,1,0],

# [0,1,0,0,0,0,0,1,0,1,1,0,1,1,1,1,0,0,1,0,0,1,0,1,0,1,0,1,1,1,0,1,0],

# [0,1,0,0,0,0,0,1,0,1,1,0,1,1,1,1,0,0,1,0,0,1,0,1,0,1,0,1,1,1,0,1,0],

# [0,1,0,0,0,0,0,1,0,1,1,0,1,1,1,1,0,0,1,0,0,1,0,1,0,1,0,1,1,1,0,1,0],

# [0,1,0,0,0,0,0,1,0,1,1,0,1,1,1,1,0,0,1,0,0,1,0,1,0,1,0,1,1,1,0,1,0],

# [0,1,0,0,0,0,0,1,0,1,1,0,1,1,1,1,0,0,1,0,0,1,0,1,0,1,0,1,1,1,0,1,0],

# [0,1,0,0,0,0,0,1,0,1,1,0,1,1,1,1,0,0,1,0,0,1,0,1,0,1,0,1,1,1,0,1,0],

# [0,1,0,0,0,0,0,1,0,1,1,0,1,1,1,1,0,0,1,0,0,1,0,1,0,1,0,1,1,1,0,1,0],

# [0,1,0,0,0,0,0,1,0,1,1,0,1,1,1,1,0,0,1,0,0,1,0,1,0,1,0,1,1,1,0,1,0],

# [0,1,0,0,0,0,0,1,0,1,1,0,1,1,1,1,0,0,1,0,0,1,0,1,0,1,0,1,1,1,0,1,0],

# [0,1,0,0,0,0,0,1,0,1,1,0,1,1,1,1,0,0,1,0,0,1,0,1,0,1,0,1,1,1,0,1,0],

# [0,1,0,0,0,0,0,1,0,1,1,0,1,1,1,1,0,0,1,0,0,1,0,1,0,1,0,1,1,1,0,1,0],

# [0,1,0,0,0,0,0,1,0,1,1,0,1,1,1,1,0,0,1,0,0,1,0,1,0,1,0,1,1,1,0,1,0],

# [0,1,0,0,0,0,0,1,0,1,1,0,1,1,1,1,0,0,1,0,0,1,0,1,0,1,0,1,1,1,0,1,0],

# [0,1,0,0,0,0,0,1,0,1,1,0,1,1,1,1,0,0,1,0,0,1,0,1,0,1,0,1,1,1,0,1,0],

# [0,1,0,0,0,0,0,1,0,1,1,0,1,1,1,1,0,0,1,0,0,1,0,1,0,1,0,1,1,1,0,1,0],

# [0,1,0,0,0,0,0,1,0,1,1,0,1,1,1,1,0,0,1,0,0,1,0,1,0,1,0,1,1,1,0,1,0],

# [0,1,0,0,0,0,0,1,0,1,1,0,1,1,1,1,0,0,1,0,0,1,0,1,0,1,0,1,1,1,0,1,0],

# [0,1,0,0,0,0,0,1,0,1,1,0,1,1,1,1,0,0,1,0,0,1,0,1,0,1,0,1,1,1,0,1,0],

# [0,1,0,0,0,0,0,1,0,1,1,0,1,1,1,1,0,0,1,0,0,1,0,1,0,1,0,1,1,1,0,1,0],

# [0,1,0,0,0,0,0,1,0,1,1,0,1,1,1,1,0,0,1,0,0,1,0,1,0,1,0,1,1,1,0,1,0],

# [0,1,0,0,0,0,0,1,0,1,1,0,1,1,1,1,0,0,1,0,0,1,0,1,0,1,0,1,1,1,0,1,0],

# [0,1,0,0,0,0,0,1,0,1,1,0,1,1,1,1,0,0,1,0,0,1,0,1,0,1,0,1,1,1,0,1,0],

# [0,1,0,0,0,0,0,1,0,1,1,0,1,1,1,1,0,0,1,0,0,1,0,1,0,1,0,1,1,1,0,1,0],

# [0,1,0,0,0,0,0,1,0,1,1,0,1,1,1,1,0,0,1,0,0,1,0,1,0,1,0,1,1,1,0,1,0],

# [0,1,0,0,0,0,0,1,0,1,1,0,1,1,1,1,0,0,1,0,0,1,0,1,0,1,0,1,1,1,0,1,0],

# [0,1,0,0,0,0,0,1,0,1,1,0,1,1,1,1,0,0,1,0,0,1,0,1,0,1,0,1,1,1,0,1,0],

# ]



paperG = [[0,1,0,0,0,0,0,1],

[1,0,1,0,0,0,0,0],

[0,1,0,1,0,0,1,0],

[0,0,1,0,1,0,0,0],

[0,0,0,1,0,0,0,0],

[0,0,0,0,0,0,1,0],

[0,0,1,0,0,1,0,1],

[1,0,0,0,0,0,1,0]]





# paperH =[[0,1,0],

#         [1,0,1],

#         [0,1,0]]



#paperH = [[0,1,0,1,1],

#[1,0,1,0,0],

#[0,1,0,1,0],

#[1,0,1,0,1],

#[1,0,0,1,0]]

'''



"""Main function, that is in charge of finding the approximation of the maximum common subgraph.

Internally it bubble sorts the bigger matrix by number of 1's in the row and then invokes comparator()

function, that actually finds approximation of the maximum common subgraph"""

def generateApproximation(big, small):

    maxGraph = []

    maxSubgraph = []

    maxCorrelation = 0

    maxGraph = bubbleSort(big)

    maxGraphReduced = copy.deepcopy(maxGraph)

    for j in range(len(big) - 1, len(small) - 1, -1):

        maxGraphReduced = deleteVerticesAtIndex(maxGraphReduced, j)

    maxSubgraph, maxCorrelation = comparator(maxGraphReduced, small, maxCorrelation)

    return (maxGraph, maxSubgraph)



"""Function soritng rows of the graph by number of 1's in the row. Rows with the biggest number of

1's will be moved to the top"""

def bubbleSort(Graph):

    G = copy.deepcopy(Graph)

    lstOfOnes = []

    for i in range(len(G)):

        lstOfOnes.append(countOnesInRow(G[i]))

    for i in range(len(G)):

        for j in range(len(G)):

            if j+1 < len(G) and lstOfOnes[j] < lstOfOnes[j+1]:

                tmp = lstOfOnes[j]

                lstOfOnes[j] = lstOfOnes[j+1]

                lstOfOnes[j+1] = tmp

                G = changeColumns(G,j,j+1)

                G = changeRows(G,j,j+1)

    return G



def getGraphFromBruteforceOptimized(paperG, paperH):



    if(len(paperG) > len(paperH)):

        big = copy.deepcopy(paperG)

        small = copy.deepcopy(paperH)

    else:

        big = copy.deepcopy(paperH)

        small = copy.deepcopy(paperG)



    maxGraphApproximation, maxSubgraphApproximation = generateApproximation(big, small)

    # print("Bigger graph after sorting rows and columns isomorhpic to original one")

    # print(maxGraphApproximation)

    # print("Smaller graph")

    # print(small)

    # print("Approximation of maximum common subgraph")

    # print(maxSubgraphApproximation)



    #ADJ = np.matrix(big)

    #A = nx.from_numpy_matrix(ADJ)

    #display_nxgraph(A)

    #ADJ1 = np.matrix(maxGraphApproximation)

    #A1 = nx.from_numpy_matrix(ADJ1)

    #display_nxgraph(A1)

    #ADJ2 = np.matrix(small)

    #A2 = nx.from_numpy_matrix(ADJ2)

    #display_nxgraph(A2)

    #ADJ3 = np.matrix(maxSubgraphApproximation)

    #A3 = nx.from_numpy_matrix(ADJ3)

    return (maxGraphApproximation, maxSubgraphApproximation)





"""Class representing an edge of the graph"""

class Edge:

    def __init__(self, v1, v2):

        self.v1 = v1

        self.v2 = v2



    def __str__(self):

        return (f'{self.v1}, {self.v2}')



"""Class representing the state of the graph, state represents subgraph under construction, it

contains information about corresponding vertices and edges of two graphs"""

class State:



    def __init__(self, G1, G2):

        self.countOfEdges = 0

        self.countOfNullNodes = 0

        self.G1 = copy.deepcopy(G1)

        self.G2 = copy.deepcopy(G2)

        self.correspondingVertices = []

        self.correspondingEdges = []



    """Function performing backtracking step i.e. restoring the subgraph

    associated with the previous state"""

    def Backtrack(self, count):

        if len(self.correspondingVertices) > 0:

            if self.correspondingVertices[-1][1] == -1:

                self.countOfNullNodes -= 1

            else:

                if len(self.correspondingEdges) > 0:

                    for i in range(count):

                        self.correspondingEdges.pop()

            self.correspondingVertices.pop()

            self.countOfEdges -= count



    """Function creating a new instance of the State class which is a copy of itself"""

    def Copy(self):

        s = State(self.G1, self.G2)

        s.countOfEdges = copy.deepcopy(self.countOfEdges)

        s.countOfNullNodes = copy.deepcopy(self.countOfNullNodes)

        s.correspondingEdges = copy.deepcopy(self.correspondingEdges)

        s.correspondingVertices = copy.deepcopy(self.correspondingVertices)

        return s



    """Function adding new pair of vertices into the list of corresponding vertices"""

    def addNewPair(self, n1, n2, edgesToAdd):

        if n2 == -1:

            self.countOfNullNodes += 1

        self.countOfEdges += edgesToAdd

        self.correspondingVertices.append((n1, n2))



class Algorithm:



    """Main function in charge of implementing the McGregor algorithm"""

    @staticmethod

    def mcGregor(s, G1, G2, max):

        v1 = Algorithm.firstNeighbor(s)

        if (v1 != -1):

            for pair in Algorithm.nextPair(s, v1):

                if (pair == None):

                    break

                isTrue, count = Algorithm.isFeasiblePair(s, pair, G1, G2)

                if isTrue is True:

                    s.addNewPair(pair[0], pair[1], count)

                    if (Algorithm.checkIfMaxBigger(s, max)):

                        max = s.Copy()

                    if (not Algorithm.leafOfSearchTree(s)):

                        max = Algorithm.mcGregor(s, G1, G2, max)

                    s.Backtrack(count)

                count = 0

        s.addNewPair(v1, -1, 0)

        if (not Algorithm.leafOfSearchTree(s)):

            max = Algorithm.mcGregor(s, G1, G2, max)

        s.Backtrack(0)

        return max



    """Function if the currently constructed subgraph is bigger than the

    current maximal one"""

    @staticmethod

    def checkIfMaxBigger(s, max):

        if (len(s.correspondingEdges) > len(max.correspondingEdges)):

            return True

        return False



    """Function checking if it is possible to enlarge currently constructed by new pair of vertices,

    if it is so, it also creates correspondng pairs of edges, that connect newly added vertices with the

    subgraph"""

    @staticmethod

    def isFeasiblePair(s, pair, G1, G2):

        count = 0

        for el in s.correspondingVertices:

            if(el[1] != -1):

                if((G1[el[0]][pair[0]] == 1 and G2[el[1]][pair[1]] == 0) or (G1[el[0]][pair[0]] == 0 and G2[el[1]][pair[1]] == 1)):

                    continue

                else:

                    if(G1[el[0]][pair[0]] == 1):

                        s.correspondingEdges.append((Edge(el[0], pair[0]), Edge(el[1], pair[1])))

                        count += 1

        return (True, count)



    """Function that is in charge of choosing the next vertex that we wish to include in

    the subgraph, returned vertex will be furthr used in the nextPair() function"""

    @staticmethod

    def firstNeighbor(s):

        v1 = -1

        selected = False

        contains = False

        if (len(s.correspondingVertices) - s.countOfNullNodes) != 0:

            for el in s.correspondingVertices:

                if(el[1] == -1):

                    continue

                for i in range(len(s.G1)):

                    if(s.G1[i][el[0]] == 1):

                        for el2 in s.correspondingVertices:

                            if(el2[0] == i):

                                contains = True

                                break

                        if(not contains):

                            selected = True

                        contains = False

                    if(selected):

                        v1 = i

                        break

                if(selected):

                    break

        else:

            for i in range(len(s.G1)):

                for el in s.correspondingVertices:

                    if(el[0] == i):

                        contains = True

                        break

                if(not contains):

                    v1 = i

                    break

                contains = False

        return v1



    """Function taking as the parameter vertex returned from the firstNeighbor() function and

    fidning the vertex from the seocnd graph, that we wish to pair up with the vertex returned from the

    firstNeighbor() function"""

    @staticmethod

    def nextPair(s, v1):

        used = False

        for i in range(len(s.G2)):

            for el in s.correspondingVertices:

                if(el[1] == i):

                    used = True

                    break

            if(not used):

                yield (v1, i)

            used = False

        yield None



    """Function checking if we already reached the leaf of the backtrack search tree"""

    @staticmethod

    def leafOfSearchTree(s):

        limit = len(s.G1)

        if len(s.correspondingVertices) >= limit:

            return True

        else:

            return False





# G1 = [[0,1,0,1,1],

# [1,0,1,0,0],

# [0,1,0,1,0],

# [1,0,1,0,1],

# [1,0,0,1,0]]



G1 = [[0,1,0,1,1],

[1,0,1,0,0],

[0,1,0,1,0],

[1,0,1,0,1],

[1,0,0,1,0]]



# G2 = [[0,1,0,0,0,0,0,1],[1,0,1,0,0,0,0,0],

# [0,1,0,1,0,0,1,0],[0,0,1,0,1,0,0,0],[0,0,0,1,0,0,0,0],[0,0,0,0,0,0,1,0],[0,0,1,0,0,1,0,1],[1,0,0,0,0,0,1,0]]



G2 = [[0,1,0,0,0,0,0,1,0],

[1,0,1,0,0,0,0,0,0],

[0,1,0,1,0,0,1,0,0],

[0,0,1,0,1,0,0,0,0],

[0,0,0,1,0,0,0,0,1],

[0,0,0,0,0,0,1,0,0],

[0,0,1,0,0,1,0,1,0],

[1,0,0,0,0,0,1,0,0],

[0,0,0,0,1,0,0,0,0]]





'''G1 = [[0,1,1,1,1,0],

[0,0,1,1,0,0],

[1,1,0,0,0,0],

[1,1,1,0,1,1],

[0,0,1,0,0,0],

[1,1,0,0,1,0]]



G2 = [[0,1,1,1,1,0,0],

[0,0,1,1,0,0,1],

[1,1,0,0,0,0,1],

[1,1,1,0,1,1,1],

[0,0,1,0,0,0,0],

[1,1,0,0,1,0,0],

[1,0,0,0,0,0,0]]'''



# G1 = [[0,1,1], [1,0,1], [1,1,0]]



# G2 = [[0,1,0,1], [1,0,1,0], [0,1,0,1], [1,0,1,0]]



# G2 = [[0,1,0,0,0,0,0,1,0,1,1,0,1],

# [0,1,0,0,0,0,0,1,0,1,1,0,1],

# [0,1,0,0,0,0,0,1,0,1,1,0,1],

# [0,1,0,0,0,0,0,1,0,1,1,0,1],

# [0,1,0,0,0,0,0,1,0,1,1,0,1],

# [0,1,0,0,0,0,0,1,0,1,1,0,1],

# [0,1,0,0,0,0,0,1,0,1,1,0,1],

# [0,1,0,0,0,0,0,1,0,1,1,0,1],

# [0,1,0,0,0,0,0,1,0,1,1,0,1],

# [0,1,0,0,0,0,0,1,0,1,1,0,1],

# [0,1,0,0,0,0,0,1,0,1,1,0,1],

# [0,1,0,0,0,0,0,1,0,1,1,0,1],

# [0,1,0,0,0,0,0,1,0,1,1,0,1]]



# G2 = [[0,1,0,0,0,0,0,1,0,1,1,0,1,1,1,1,0,0,1,0,0,1,0,1,0,1,0,1,1,1,0,1,0],

# [0,1,0,0,0,0,0,1,0,1,1,0,1,1,1,1,0,0,1,0,0,1,0,1,0,1,0,1,1,1,0,1,0],

# [0,1,0,0,0,0,0,1,0,1,1,0,1,1,1,1,0,0,1,0,0,1,0,1,0,1,0,1,1,1,0,1,0],

# [0,1,0,0,0,0,0,1,0,1,1,0,1,1,1,1,0,0,1,0,0,1,0,1,0,1,0,1,1,1,0,1,0],

# [0,1,0,0,0,0,0,1,0,1,1,0,1,1,1,1,0,0,1,0,0,1,0,1,0,1,0,1,1,1,0,1,0],

# [0,1,0,0,0,0,0,1,0,1,1,0,1,1,1,1,0,0,1,0,0,1,0,1,0,1,0,1,1,1,0,1,0],

# [0,1,0,0,0,0,0,1,0,1,1,0,1,1,1,1,0,0,1,0,0,1,0,1,0,1,0,1,1,1,0,1,0],

# [0,1,0,0,0,0,0,1,0,1,1,0,1,1,1,1,0,0,1,0,0,1,0,1,0,1,0,1,1,1,0,1,0],

# [0,1,0,0,0,0,0,1,0,1,1,0,1,1,1,1,0,0,1,0,0,1,0,1,0,1,0,1,1,1,0,1,0],

# [0,1,0,0,0,0,0,1,0,1,1,0,1,1,1,1,0,0,1,0,0,1,0,1,0,1,0,1,1,1,0,1,0],

# [0,1,0,0,0,0,0,1,0,1,1,0,1,1,1,1,0,0,1,0,0,1,0,1,0,1,0,1,1,1,0,1,0],

# [0,1,0,0,0,0,0,1,0,1,1,0,1,1,1,1,0,0,1,0,0,1,0,1,0,1,0,1,1,1,0,1,0],

# [0,1,0,0,0,0,0,1,0,1,1,0,1,1,1,1,0,0,1,0,0,1,0,1,0,1,0,1,1,1,0,1,0],

# [0,1,0,0,0,0,0,1,0,1,1,0,1,1,1,1,0,0,1,0,0,1,0,1,0,1,0,1,1,1,0,1,0],

# [0,1,0,0,0,0,0,1,0,1,1,0,1,1,1,1,0,0,1,0,0,1,0,1,0,1,0,1,1,1,0,1,0],

# [0,1,0,0,0,0,0,1,0,1,1,0,1,1,1,1,0,0,1,0,0,1,0,1,0,1,0,1,1,1,0,1,0],

# [0,1,0,0,0,0,0,1,0,1,1,0,1,1,1,1,0,0,1,0,0,1,0,1,0,1,0,1,1,1,0,1,0],

# [0,1,0,0,0,0,0,1,0,1,1,0,1,1,1,1,0,0,1,0,0,1,0,1,0,1,0,1,1,1,0,1,0],

# [0,1,0,0,0,0,0,1,0,1,1,0,1,1,1,1,0,0,1,0,0,1,0,1,0,1,0,1,1,1,0,1,0],

# [0,1,0,0,0,0,0,1,0,1,1,0,1,1,1,1,0,0,1,0,0,1,0,1,0,1,0,1,1,1,0,1,0],

# [0,1,0,0,0,0,0,1,0,1,1,0,1,1,1,1,0,0,1,0,0,1,0,1,0,1,0,1,1,1,0,1,0],

# [0,1,0,0,0,0,0,1,0,1,1,0,1,1,1,1,0,0,1,0,0,1,0,1,0,1,0,1,1,1,0,1,0],

# [0,1,0,0,0,0,0,1,0,1,1,0,1,1,1,1,0,0,1,0,0,1,0,1,0,1,0,1,1,1,0,1,0],

# [0,1,0,0,0,0,0,1,0,1,1,0,1,1,1,1,0,0,1,0,0,1,0,1,0,1,0,1,1,1,0,1,0],

# [0,1,0,0,0,0,0,1,0,1,1,0,1,1,1,1,0,0,1,0,0,1,0,1,0,1,0,1,1,1,0,1,0],

# [0,1,0,0,0,0,0,1,0,1,1,0,1,1,1,1,0,0,1,0,0,1,0,1,0,1,0,1,1,1,0,1,0],

# [0,1,0,0,0,0,0,1,0,1,1,0,1,1,1,1,0,0,1,0,0,1,0,1,0,1,0,1,1,1,0,1,0],

# [0,1,0,0,0,0,0,1,0,1,1,0,1,1,1,1,0,0,1,0,0,1,0,1,0,1,0,1,1,1,0,1,0],

# [0,1,0,0,0,0,0,1,0,1,1,0,1,1,1,1,0,0,1,0,0,1,0,1,0,1,0,1,1,1,0,1,0],

# [0,1,0,0,0,0,0,1,0,1,1,0,1,1,1,1,0,0,1,0,0,1,0,1,0,1,0,1,1,1,0,1,0],

# [0,1,0,0,0,0,0,1,0,1,1,0,1,1,1,1,0,0,1,0,0,1,0,1,0,1,0,1,1,1,0,1,0],

# [0,1,0,0,0,0,0,1,0,1,1,0,1,1,1,1,0,0,1,0,0,1,0,1,0,1,0,1,1,1,0,1,0],

# [0,1,0,0,0,0,0,1,0,1,1,0,1,1,1,1,0,0,1,0,0,1,0,1,0,1,0,1,1,1,0,1,0],

# ]





# G1 =[[0,1,0],[1,0,1],[0,1,0]]



# G2 = [[0,1,0,1,0],

#           [1,0,1,0,0],[0,1,0,1,0],[1,0,1,0,1],[0,0,0,1,0]]







def createSubgraphFromMax(max):

    maxSubgraph = []



    for i in range(len(max.correspondingVertices)):

        lst = list(itertools.repeat(0, len(max.correspondingVertices)))

        maxSubgraph.append(lst)



    for pair in max.correspondingVertices:

        for edge in max.correspondingEdges:

            if (edge[0].v1 == pair[0]):

                maxSubgraph[pair[0]][edge[0].v2] = 1

                maxSubgraph[edge[0].v2][pair[0]] = 1

    return maxSubgraph



def utilizeMcGregor(g1, g2):

    if(len(g1) > len(g2)):

        big = copy.deepcopy(g1)

        small = copy.deepcopy(g2)

    else:

        big = copy.deepcopy(g2)

        small = copy.deepcopy(g1)

    max = State(small, big)

    s = State(small, big)

    max = Algorithm.mcGregor(s, small, big, max)

    maxSubgraph = createSubgraphFromMax(max)

    return (maxSubgraph, max)



def returnMinimumSupergraphMcGregor(paperG, paperH):

    if(len(paperG) > len(paperH)):

        G2 = copy.deepcopy(paperG)

        G1 = copy.deepcopy(paperH)

    else:

        G2 = copy.deepcopy(paperH)

        G1 = copy.deepcopy(paperG)

    s = State(G1, G2)

    max = State(G1, G2)

    max = Algorithm.mcGregor(s, G1, G2, max)

    # print("Result:")

    # print(f'{max.correspondingVertices}')

    # for i in range(len(max.correspondingEdges)):

    #     print(f'{max.correspondingEdges[i][0]}')

    # print(f'Number of edges: {len(max.correspondingEdges)}')

    # print("Smaller graph")

    # for row in G1:

    #     print(row)

    # print("Bigger graph")

    # for row in G2:

    #     print(row)



    maxSubgraph = []

    for i in range(len(max.correspondingVertices)):

        lst = list(itertools.repeat(0, len(max.correspondingVertices)))

        maxSubgraph.append(lst)





    for pair in max.correspondingVertices:

        for edge in max.correspondingEdges:

            if (edge[0].v1 == pair[0]):

                maxSubgraph[pair[0]][edge[0].v2] = 1

                maxSubgraph[edge[0].v2][pair[0]] = 1

    # print("Maximum common subgraph")

    # for row in maxSubgraph:

    #     print(row)

    # print(max.correspondingVertices[0][0])

    # print(max.correspondingEdges[0][0].v1)

    # print("Test")

    smallGraphRowOrder = []

    bigGraphRowOrder = []

    for pair in max.correspondingVertices:

        smallGraphRowOrder.append(pair[0])

        bigGraphRowOrder.append(pair[1])

    # print(smallGraphRowOrder)

    # print(bigGraphRowOrder)

    smallGraphAuxilary = list(range(0, len(G1)))

    bigGraphAuxilary = list(range(0, len(G2)))

    smallGraphDifference = list(set(smallGraphAuxilary) - set(smallGraphRowOrder))

    bigGraphDifference = list(set(bigGraphAuxilary) - set(bigGraphRowOrder))

    # print("Test2")

    # print(smallGraphDifference)

    # print(bigGraphDifference)



    permutationMatrixBig = []

    permutationMatrixTransposeBig = []

    counterSmall = 0

    counterBig = 0

    for i in range(len(bigGraphRowOrder)):

        lst = list(itertools.repeat(0, len(G2)))

        lst[bigGraphRowOrder[i]] = 1

        permutationMatrixBig.append(lst)

    for j in range(len(bigGraphRowOrder), len(G2)):

        lst = list(itertools.repeat(0, len(G2)))

        lst[bigGraphDifference[counterBig]] = 1

        counterBig += 1

        permutationMatrixBig.append(lst)

    # print(permutationMatrixBig)

    transpose(permutationMatrixBig, permutationMatrixTransposeBig)

    adjMatrixBig = np.matmul(G2, permutationMatrixTransposeBig)

    adjMatrixBig = np.matmul(permutationMatrixBig, adjMatrixBig)

    adjMatrixBig = adjMatrixBig.tolist()



    permutationMatrixSmall = []

    permutationMatrixTransposeSmall = []

    for i in range(len(smallGraphRowOrder)):

        lst = list(itertools.repeat(0, len(G1)))

        lst[smallGraphRowOrder[i]] = 1

        permutationMatrixSmall.append(lst)

    if (len(smallGraphDifference) > 0):

        for j in range(len(smallGraphRowOrder), len(G1)):

            lst = list(itertools.repeat(0, len(G1)))

            lst[smallGraphDifference[counterSmall]] = 1

            counterSmall += 1

            permutationMatrixSmall.append(lst)

    # print(permutationMatrixSmall)

    transpose(permutationMatrixSmall, permutationMatrixTransposeSmall)

    adjMatrixSmall = np.matmul(G1, permutationMatrixTransposeSmall)

    adjMatrixSmall = np.matmul(permutationMatrixSmall, adjMatrixSmall)

    adjMatrixSmall = adjMatrixSmall.tolist()



    minSupergraph = generateSupergraph(adjMatrixBig, adjMatrixSmall)



    # print("Minimum common supergraph")

    # for row in minSupergraph:

    #     print(row)



    # ADJ = np.matrix(G2)

    # A = nx.from_numpy_matrix(ADJ)

    # display_nxgraph(A)

    # ADJ2 = np.matrix(G1)

    # A2 = nx.from_numpy_matrix(ADJ2)

    # display_nxgraph(A2)

    # ADJ3 = np.matrix(maxSubgraph)

    # A3 = nx.from_numpy_matrix(ADJ3)

    # display_nxgraph(A3)

    # # ADJ4 = np.matrix(adjMatrixSmall)

    # # A4 = nx.from_numpy_matrix(ADJ4)

    # # display_nxgraph(A4)

    # # ADJ5 = np.matrix(adjMatrixBig)

    # # A5 = nx.from_numpy_matrix(ADJ5)

    # # display_nxgraph(A5)

    # ADJ6 = np.matrix(minSupergraph)

    # A6 = nx.from_numpy_matrix(ADJ6)

    # display_nxgraph(A6)

    return minSupergraph



def generateSupergraph(big, small):

    minSupergraph = copy.deepcopy(big)

    for i in range(len(small)):

        for j in range(len(small)):

            if (small[i][j] == 1 and minSupergraph[i][j] == 0):

                minSupergraph[i][j] = 1

    return minSupergraph



class FileManager:



    def __init__(self):

        self.first_size = 0

        self.first_matrix = []

        self.second_size = 0

        self.second_matrix = []



    def size_to_int(self, line):

        size = 0

        power = len(line) - 1

        for digit in line:

            size += (pow(10, power) * int(digit))

            power -= 1

        return size



    def read_from_file(self, path):

        file = open(path, "r")

        line_count = 0

        for line in file.readlines():

            row = (line.rstrip('\n')).replace(" ", "").replace(",", "").replace(";", "")

            if line_count == 0:

                self.first_size = self.size_to_int(row)

            elif line_count == (1 + self.first_size):

                self.second_size = self.size_to_int(row)

            else:

                edges = []

                for i in range(0, len(row)):

                    edges.append(int(row[i]))

                if self.second_size == 0:

                    self.first_matrix.append(edges)

                else:

                    self.second_matrix.append(edges)

            line_count += 1

        file.close()





class Graph:



    # init functions



    def __init__(self):

        self.adjacency_matrix = []

        self.node_labels = []



    def __init__(self, size, matrix):

        self.adjacency_matrix = matrix

        self.node_labels = []

        for i in range(0, size):

            self.node_labels.append(chr(65 + i))



    # get/set functions



    def get_adjacency_matrix(self):

        return self.adjacency_matrix



    def get_node_labels(self):

        return self.node_labels



    def get_size(self):

        return len(self.node_labels)



    def get_pos_of_node(self, node):

        for i in range (0, self.get_size()):

            if self.node_labels[i] == node:

                return i

        return None



    def get_node_by_pos(self, pos):

        if type(pos) is int:

            return self.node_labels[pos]



    def add_node(self):

        if len(self.adjacency_matrix) == 0:

            self.node_labels.append('A')

            self.adjacency_matrix.append([0])

        else:

            for line in self.adjacency_matrix:

                list(line).append(0)

            self.adjacency_matrix.append([0 for i in range(0, self.get_size())])

            self.node_labels.append(chr(65 + self.get_size()))



    def swap(self, first, second):

        if type(first) is int and type(second) is int:

            tmp = first

            first = second

            second = tmp



    def swap_cols(self, first, second):

        if (type(first) is str or type(first) is chr) and (type(second) is str or type(second) is chr):

            first = self.get_pos_of_node(first)

            second = self.get_pos_of_node(second)

        if type(first) is int and type(second) is int:

            if self.get_size() > first and self.get_size() > second:

                for j in range(0, self.get_size()):

                    self.swap(self.adjacency_matrix[j][first], self.adjacency_matrix[j][second])



    def swap_rows(self, first, second):

        if (type(first) is str or type(first) is chr) and (type(second) is str or type(second) is chr):

            first = self.get_pos_of_node(first)

            second = self.get_pos_of_node(second)

        if type(first) is int and type(second) is int:

            if self.get_size() > first and self.get_size() > second:

                for j in range(0, self.get_size()):

                    self.swap(self.adjacency_matrix[first][j], self.adjacency_matrix[second][j])



    def swap_nodes(self, first, second):

        self.swap_cols(first, second)

        self.swap_rows(first, second)



    def add_node(self, node):

        if type(node) is chr or type(node) is str:

            if len(self.adjacency_matrix) == 0:

                self.node_labels.append(node)

                self.adjacency_matrix.append([0])

            else:

                for line in self.adjacency_matrix:

                    line.append(0)

                self.node_labels.append(node)

                self.adjacency_matrix.append([0 for i in range(0, self.get_size())])



    def add_edge(self, i, j):

        if type(i) is int and type(j) is int:

            self.adjacency_matrix[i][j] = 1

        elif (type(i) is str or type(i) is chr) and (type(j) is str or type(j) is chr):

            if i not in self.get_node_labels():

                self.add_node(i)

            if j not in self.get_node_labels():

                self.add_node(j)

            x = self.get_pos_of_node(i)

            y = self.get_pos_of_node(j)

            if type(x) is int and type(y) is int:

                self.adjacency_matrix[x][y] = 1



    # utility functions



    def draw(self):

        graph = nx.DiGraph()

        graph.add_nodes_from(self.node_labels)

        for i in range(0, self.get_size()):

            for j in range(0, self.get_size()):

                if self.adjacency_matrix[i][j] == 1:

                    graph.add_edge(self.get_node_by_pos(i), self.get_node_by_pos(j))

        nx.draw(graph, with_labels = True)



    def print(self, title):

        print(title)

        for line in self.adjacency_matrix:

            print(line)

        print("")



class GraphAnalyzer:



    def __init__(self):

        self.first_graph = None

        self.second_graph = None

        self.max_graph = None

        self.max_graph_approx = None

        self.bruteforce_graph = None

        self.bruteforce_mcs_graph = None

        self.bruteforce_approx = None

        self.brutefoce_approx_mcs_graph = None

        self.mcgregor_graph = None

        self.mcgregor_mcs_graph = None

        self.optimized_mcgregor_graph = None

        self.optimized_mcgregor_mcs_graph = None



    def uninitialize_all_graphs(self):

        self.first_graph = None

        self.second_graph = None

        self.max_graph = None

        self.max_graph_approx = None

        self.bruteforce_graph = None

        self.bruteforce_mcs_graph = None

        self.bruteforce_approx = None

        self.brutefoce_approx_mcs_graph = None

        self.mcgregor_graph = None

        self.mcgregor_mcs_graph = None

        self.optimized_mcgregor_graph = None

        self.optimized_mcgregor_mcs_graph = None



    def print_info(self, graph, headline):

        print(headline)

        print(graph)



    def set_first_graph(self, graph):

        if type(graph) is Graph:

            self.first_graph = graph



    def set_second_graph(self, graph):

        if type(graph) is Graph:

            self.second_graph = graph



    def useBruteforce(self):

        if self.first_graph != None:



            (result, max_graph_from_bruteforce) = getGraphFromBruteforce(self.first_graph.adjacency_matrix,

                                                       self.second_graph.adjacency_matrix)

            self.bruteforce_graph = Graph(len(result), result)

            self.max_graph = Graph(len(max_graph_from_bruteforce), max_graph_from_bruteforce)



    def useMCSBruteforce(self):

        if self.first_graph != None:

            if self.bruteforce_graph == None or self.max_graph == None:

                self.useBruteforce()

            result = self.generateMCSFromBruteforce()

            self.bruteforce_mcs_graph = Graph(len(result.adjacency_matrix), result.adjacency_matrix)



    def useBruteforceOptimized(self):

        if self.first_graph != None:

            (result, max_graph_from_bruteforce) = getGraphFromBruteforceOptimized(self.first_graph.adjacency_matrix,

                                                       self.second_graph.adjacency_matrix)

            self.bruteforce_approx = Graph(len(result), result)

            self.max_graph_approx = Graph(len(max_graph_from_bruteforce), max_graph_from_bruteforce)





    def useMCSBruteforceOptimized(self):

        if self.first_graph != None:

            if self.bruteforce_approx == None or self.max_graph_approx == None:

                self.useBruteforceOptimized()

            result = self.generateMCSFromBruteforceOptimized()

            self.brutefoce_approx_mcs_graph = Graph(len(result.adjacency_matrix), result.adjacency_matrix)



    def useMcGregor(self):

        if self.first_graph != None:

            result = utilizeMcGregor(self.first_graph.adjacency_matrix,

                                        self.second_graph.adjacency_matrix)[0]

            self.mcgregor_graph = Graph(len(result), result)



    def useMcGregorMCS(self):

        if self.first_graph != None:

            result = returnMinimumSupergraphMcGregor(self.first_graph.adjacency_matrix,

                                                     self.second_graph.adjacency_matrix)

            self.mcgregor_mcs_graph = Graph(len(result), result)



    def generateMCSFromBruteforce(self):

        minSupergraph = copy.deepcopy(self.max_graph)

        small_graph = None

        if len(self.first_graph.adjacency_matrix) > len(self.second_graph.adjacency_matrix):

            small_graph = self.second_graph.adjacency_matrix

        else:

            small_graph = self.first_graph.adjacency_matrix

        for i in range(len(small_graph)):

            for j in range(len(small_graph)):

                if small_graph[i][j] == 1 and minSupergraph.adjacency_matrix[i][j] == 0:

                    minSupergraph.adjacency_matrix[i][j] = 1

        return minSupergraph



    def generateMCSFromBruteforceOptimized(self):

        minSupergraph = copy.deepcopy(self.max_graph_approx)

        small_graph = None

        if len(self.first_graph.adjacency_matrix) > len(self.second_graph.adjacency_matrix):

            small_graph = self.second_graph.adjacency_matrix

        else:

            small_graph = self.first_graph.adjacency_matrix

        for i in range(len(small_graph)):

            for j in range(len(small_graph)):

                if small_graph[i][j] == 1 and minSupergraph.adjacency_matrix[i][j] == 0:

                    minSupergraph.adjacency_matrix[i][j] = 1

        return minSupergraph



    # def useMinimalCommonSupergraphFromMcGregor(self):

    #     if self.first_graph != None:

    #         mcgregor = utilizeMcGregor(self.first_graph.adjacency_matrix,

    #                                     self.second_graph.adjacency_matrix)

    #         algorithm = MinimalCommonSupergraph()

    #         result = algorithm.graph_addition(mcgregor[0],

    #                                             algorithm.graph_difference(self.second_graph.adjacency_matrix, mcgregor[1])[0],

    #                                             mcgregor[1],

    #                                             algorithm.graph_difference(self.second_graph.adjacency_matrix, mcgregor[1])[1])

    #         self.print_info(result, "Minimal Common Supergraph")

    #         self.minimal_common_supergraph = Graph(len(result), result)





class MinimalCommonSupergraph:



    def graph_difference(self, g1, mcs,bigger = True):

        index = 1

        if( bigger == True):

            index = 0

        diff_labels =[]



        for label in mcs.correspondingVertices:

            g1[label[index]].clear()

            diff_labels.append(label[index])

        return (copy.deepcopy(g1), diff_labels)



    def graph_addition(self, mcs, difference, max_tuples, diff_labels, bigger = True):

        index = 1



        if(bigger == True):

            index = 0

        for i in range(len(difference)):

            if difference[i]:

                indices = [i for i, x in enumerate(difference[i]) if x == 1]

                my_list = []

                for num in indices:



                    if num in diff_labels:

                        search_list = [ind for (ind, a_tuple) in enumerate(max_tuples.correspondingVertices) if a_tuple[index]==num]

                        my_list.append(search_list[0])

                        if index == 0:

                            my_tuple = (i, -1)

                        else:

                            my_tuple = (-1, i)

                        max_tuples.correspondingVertices.append(my_tuple)



                mcs = self.addColumns(mcs, my_list)

                mcs = self.addRows(mcs, my_list)



        return mcs





    def addColumns(self, graph, indexes_of_ones):

        for i in range(len(graph)):

            if i in indexes_of_ones:

                graph[i].append(1)

            else:

                graph[i].append(0)

        return graph



    def addRows(self, graph, indexes_of_ones):

        tmp = []

        for i in range(len(graph) + 1):

            if i in indexes_of_ones:

                tmp.append(1)

            else:

                tmp.append(0)

        graph.append(tmp)

        return graph



class PrettyWidget(QWidget):



    def __init__(self):



        super(PrettyWidget, self).__init__()

        self.graph_analyzer = GraphAnalyzer()

        self.initUI()



        self.mcgregor_time = 0

        self.mcgregor_mcs_time = 0

        self.mcgregor_optimized_time = 0

        self.mcgregor_optimized_time_mcs = 0

        self.bruteforce_time = 0

        self.bruteforce_mcs_time = 0

        self.bruteforce_optimized_time = 0

        self.bruteforce_optimized_mcs_time = 0



    def resetTimer(self):

        self.mcgregor_time = 0

        self.mcgregor_mcs_time = 0

        self.mcgregor_optimized_time = 0

        self.mcgregor_optimized_time_mcs = 0

        self.bruteforce_time = 0

        self.bruteforce_mcs_time = 0

        self.bruteforce_optimized_time = 0

        self.bruteforce_optimized_mcs_time = 0



    def initUI(self):



        self.setGeometry(100, 100, 800, 600)

        self.center()

        self.setWindowTitle('Graph Analyzer')



        grid = QGridLayout()

        self.setLayout(grid)



        main_layout = QVBoxLayout()



        utility_box = QGroupBox("Utility")

        graphs_box = QGroupBox("Base Graphs")

        mcgregor_box = QGroupBox("McGregor Algorithm")

        #mcgregor_optimized_box = QGroupBox("McGregor Optimized Algorithm")

        bruteforce_box = QGroupBox("Bruteforce Algorithm")

        bruteforce_optimized_box = QGroupBox("Bruteforce Optimized Algorithm")



        self.timeLabel = QLabel()

        self.updateTime("Time Elapsed: None")

        self.drawRadioButton = QRadioButton("Draw Graph In GUI")

        self.consoleRadioButton = QRadioButton("Print Graph In Console")

        self.consoleRadioButton.setCheckable(True)

        self.drawRadioButton.setCheckable(True)

        self.consoleRadioButton.setChecked(True)



        utility_layout = QVBoxLayout()

        utility_layout.addWidget(self.createButton("Open From File", self.openGraphFromTxt))

        utility_layout.setSpacing(10)

        utility_layout.addWidget(self.consoleRadioButton)

        utility_layout.setSpacing(10)

        utility_layout.addWidget(self.drawRadioButton)

        utility_layout.setSpacing(10)

        utility_layout.addWidget(self.timeLabel)

        utility_layout.setSpacing(10)



        graphs_layout = QVBoxLayout()

        graphs_layout.addWidget(self.createButton("Draw First Graph", self.plotFirstGraph))

        utility_layout.setSpacing(10)

        graphs_layout.addWidget(self.createButton("Draw Second Graph", self.plotSecondGraph))

        utility_layout.setSpacing(10)



        mcgregor_layout = QVBoxLayout()

        mcgregor_layout.addWidget(self.createButton("Maximum Common Subgraph", self.useMcGregorAlgorithm))

        mcgregor_layout.setSpacing(10)

        mcgregor_layout.addWidget(self.createButton("Minimum Common Supergraph", self.useMcGregorMCSAlgorithm))

        mcgregor_layout.setSpacing(10)



        # mcgregor_optimized_layout = QVBoxLayout()

        # mcgregor_optimized_layout.addWidget(self.createButton("Maximum Common Subgraph", self.plotSecondGraph))

        # mcgregor_optimized_layout.setSpacing(10)

        # mcgregor_optimized_layout.addWidget(self.createButton("Minimum Common Supergraph", self.openGraphFromTxt))

        # mcgregor_optimized_layout.setSpacing(10)



        bruteforce_layout = QVBoxLayout()

        bruteforce_layout.addWidget(self.createButton("Maximum Common Subgraph", self.useBruteforceAlgortithm))

        bruteforce_layout.setSpacing(10)

        bruteforce_layout.addWidget(self.createButton("Minimum Common Supegraph", self.useBruteforceMCSAlgorithm))

        bruteforce_layout.setSpacing(10)



        # There, the methods should theoretically be switched

        # However, for some reasonit looks like MCS is shown as mcs, and mcs is shown as MCS (?)

        bruteforce_optimized_layout = QVBoxLayout()

        bruteforce_optimized_layout.addWidget(self.createButton("Maximum Common Subgraph", self.useBruteforceOptimizedMCSAlgorithm))

        bruteforce_optimized_layout.setSpacing(10)

        bruteforce_optimized_layout.addWidget(self.createButton("Minimum Common Supergraph", self.useBruteforceOptimized))

        bruteforce_optimized_layout.setSpacing(10)



        utility_box.setLayout(utility_layout)

        graphs_box.setLayout(graphs_layout)

        mcgregor_box.setLayout(mcgregor_layout)

       # mcgregor_optimized_box.setLayout(mcgregor_optimized_layout)

        bruteforce_optimized_box.setLayout(bruteforce_optimized_layout)

        bruteforce_box.setLayout(bruteforce_layout)



        main_layout.addWidget(utility_box, 0)

        main_layout.addWidget(graphs_box, 1)

        main_layout.addWidget(mcgregor_box, 2)

        #main_layout.addWidget(mcgregor_optimized_box, 3)

        main_layout.addWidget(bruteforce_box, 3)

        main_layout.addWidget(bruteforce_optimized_box, 4)



        self.figure = plt.figure()

        self.canvas = FigureCanvas(self.figure)

        grid.addWidget(self.canvas, 0, 1, 9, 9)

        grid.addLayout(main_layout, 0, 0)



        self.show()



    def updateTime(self, text):

        self.timeLabel.setText(text)



    def createButton(self, text, fn):

        button = QPushButton(text)

        button.setObjectName(text)

        button.clicked.connect(fn)

        return button



    def openGraphFromTxt(self):

        try:

            response = QFileDialog.getOpenFileName(

                parent=self,

                caption="Select Graph File",

                directory=os.getcwd()

            )

            manager = FileManager()

            manager.read_from_file(response[0])

            self.graph_analyzer.uninitialize_all_graphs()

            self.graph_analyzer.first_graph = Graph(manager.first_size, manager.first_matrix)

            self.graph_analyzer.second_graph = Graph(manager.second_size, manager.second_matrix)

            self.resetTimer()

        except:

            self.createMessageBox("Can't draw graph!", "Error", QMessageBox.Ok)



    def plotFirstGraph(self):

        self.figure.clf()

        try:

            if self.drawRadioButton.isChecked() == True:

                self.graph_analyzer.first_graph.draw()

            else:

                self.graph_analyzer.first_graph.print("First Graph")

        except:

            self.createMessageBox("No graph was found!", "Error", QMessageBox.Ok)

        self.canvas.draw_idle()



    def plotSecondGraph(self):

        self.figure.clf()

        try:

            if self.drawRadioButton.isChecked() == True:

                self.graph_analyzer.second_graph.draw()

            else:

                self.graph_analyzer.second_graph.print("Second Graph")

        except:

            self.createMessageBox("No graph was found!", "Error", QMessageBox.Ok)

        self.canvas.draw_idle()



    def useBruteforceAlgortithm(self):

        if self.graph_analyzer.bruteforce_graph == None:

            start = timer()

            self.graph_analyzer.useBruteforce()

            end = timer()

            self.bruteforce_time = timedelta(seconds = end - start)

        self.figure.clf()

        try:

            if self.drawRadioButton.isChecked() == True:

                self.graph_analyzer.bruteforce_graph.draw()

            else:

                self.graph_analyzer.bruteforce_graph.print("Maximum Common Subgraph From Bruteforce")

            self.updateTime(f"Time Elapsed: {self.bruteforce_time}")

        except:

            self.createMessageBox("No graph was found!", "Error", QMessageBox.Ok)

        self.canvas.draw_idle()



    def useBruteforceMCSAlgorithm(self):

        if self.graph_analyzer.bruteforce_mcs_graph == None:

            start = timer()

            self.graph_analyzer.useMCSBruteforce()

            end = timer()

            self.bruteforce_mcs_time = timedelta(seconds = end - start)

        self.figure.clf()

        try:

            if self.drawRadioButton.isChecked() == True:

                self.graph_analyzer.bruteforce_mcs_graph.draw()

            else:

                self.graph_analyzer.bruteforce_mcs_graph.print("Minimum Common Supergraph From Bruteforce")

            self.updateTime(f"Time Elapsed: {self.bruteforce_mcs_time}")

        except:

            self.createMessageBox("No graph was found!", "Error", QMessageBox.Ok)

        self.canvas.draw_idle()



    def useBruteforceOptimized(self):

        if self.graph_analyzer.bruteforce_approx == None:

            start = timer()

            self.graph_analyzer.useBruteforceOptimized()

            end = timer()

            self.bruteforce_optimized_time = timedelta(seconds = end - start)

        self.figure.clf()

        try:

            if self.drawRadioButton.isChecked() == True:

                self.graph_analyzer.bruteforce_approx.draw()

            else:

                self.graph_analyzer.bruteforce_approx.print("Minimum Common Supergraph From Bruteforce Approximation")

            self.updateTime(f"Time Elapsed: {self.bruteforce_optimized_time}")

        except:

            self.createMessageBox("No graph was found!", "Error", QMessageBox.Ok)

        self.canvas.draw_idle()



    def useBruteforceOptimizedMCSAlgorithm(self):

        if self.graph_analyzer.brutefoce_approx_mcs_graph == None:

            start = timer()

            self.graph_analyzer.useMCSBruteforceOptimized()

            end = timer()

            self.bruteforce_optimized_mcs_time = timedelta(seconds = end - start)

        self.figure.clf()

        try:

            if self.drawRadioButton.isChecked() == True:

                self.graph_analyzer.brutefoce_approx_mcs_graph.draw()

            else:

                self.graph_analyzer.brutefoce_approx_mcs_graph.print("Maximum Common Subgraph From Bruteforce Approximation")

            self.updateTime(f"Time Elapsed: {self.bruteforce_optimized_mcs_time}")

        except:

            self.createMessageBox("No graph was found!", "Error", QMessageBox.Ok)

        self.canvas.draw_idle()



    def useMcGregorAlgorithm(self):

        if self.graph_analyzer.mcgregor_graph == None:

            start = timer()

            self.graph_analyzer.useMcGregor()

            end = timer()

            self.mcgregor_time = timedelta(seconds = end - start)

        self.figure.clf()

        try:

            if self.drawRadioButton.isChecked() == True:

                self.graph_analyzer.mcgregor_graph.draw()

            else:

                self.graph_analyzer.mcgregor_graph.print("Maximum Common Subgraph From McGregor Algorithm")

            self.updateTime(f"Time Elapsed: {self.mcgregor_time}")

        except:

            self.createMessageBox("No graph was found!", "Error", QMessageBox.Ok)

        self.canvas.draw_idle()



    def useMcGregorMCSAlgorithm(self):

        if self.graph_analyzer.mcgregor_mcs_graph == None:

            start = timer()

            self.graph_analyzer.useMcGregorMCS()

            end = timer()

            self.mcgregor_mcs_time = timedelta(seconds = end - start)

        self.figure.clf()

        try:

            if self.drawRadioButton.isChecked() == True:

                self.graph_analyzer.mcgregor_mcs_graph.draw()

            else:

                self.graph_analyzer.mcgregor_mcs_graph.print("Minimum Common Supergraph From McGregor Algorithm")

            self.updateTime(f"Time Elapsed: {self.mcgregor_mcs_time}")

        except:

            self.createMessageBox("No graph was found!", "Error", QMessageBox.Ok)

        self.canvas.draw_idle()



    def center(self):

        qr = self.frameGeometry()

        cp = QDesktopWidget().availableGeometry().center()

        qr.moveCenter(cp)

        self.move(qr.topLeft())



    def createMessageBox(self, text, title, buttons):

        msgBox = QMessageBox()

        msgBox.setIcon(QMessageBox.Information)

        msgBox.setText(text)

        msgBox.setWindowTitle(title)

        msgBox.setStandardButtons(buttons)

        msgBox.exec()



if __name__ == '__main__':



    import sys

    app = QApplication(sys.argv)

    app.aboutToQuit.connect(app.deleteLater)

    app.setStyle(QStyleFactory.create("gtk"))

    screen = PrettyWidget()

    screen.show()

    sys.exit(app.exec_())
