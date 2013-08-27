#!/usr/bin/env python

import cPickle as pickle
import sys
import re
# import time,datetime
# import heapq
# import urllib

### build graph:
### takes as input a file in the form:
## a b dist time
### where a and b are destinations, dist is the distance between them, and
### time is the time needed to travel between them and constructs a graph.

### This graph should be represented as an adjacency list, and stored as a
### dictionary, with the key in the dictionary being the source of an edge and
### the value being a tuple containing the destination, distance, and cost.
### For example:
### g[a] = (b,dist,time)

class Graph:
    def __init__(self, infile=None) :
        self.adjlist = {}
        if infile : self.buildGraph(infile)

    ### method to print a graph.
    def __repr__(self) :
        #TODO
        return 'TODO'

    ### helper methods to construct edges and vertices. Use these in buildGraph.
    def createVertex(self, inStr) :
        name, lat, longitude = inStr.split(" ",2)
        lat = lat.split("=")[1]
        longitude = longitude.split("=")[1]
        return Vertex(name, lat, longitude)

    def createEdges(self, inStr) :
        src, dest, dist, time = inStr.split(" ",4)
        dist=dist.split("=")[1]
        time=time.split("=")[1]
        e1 = Edge(src,dest,dist, time)
        e2 = Edge(dest,src,dist, time)
        return e1, e2

### method that takes as input a file name and constructs the graph described
### above.
    def buildGraph(self, infile) :
        # pass first comment line
        line = infile.readline

        while line = infile.readline:
            if line[0]=='#' : break
            createVertex(line)
        return 'TODO'
        #TODO

### this method should take as input the name of a starting vertex
### and compute Dijkstra's algorithm,
### returning a dictionary that maps destination cities to
### a tuple containing the length of the path, and the vertices that form the path.
### Wikipedia has pseudo-Code for this - now translate it to Python,
### But do NOT copy any actual python code from anywhere else on the web
    def dijkstra(self, source) :
        #TODO
        return 'TODO'

### classes representing vertices and edges

class Vertex:
    def __init__(self, name, lat, longitude) :
        self.name = name
        self.lat = lat
        self.longitude = longitude
    def __hash__(self) :
        return hash(self.name)
    def __eq__(self, other) :
        return self.name == other.name


class Edge:
    def __init__(self, src, dest, distance, time) :
        self.src = src
        self.dest = dest
        self.distance = distance
        self.time = time


### usage: buildGraph {--pfile=outfile} {-d=startNode} infile
### if --pfile=outfile is provided, write a pickled version of the graph
### to outfile. Otherwise, print it to standard output.
### if --d=startNode is provided, compute dijkstra with the given starting node
###  as source

if __name__ == '__main__' :
    parser = argparse.ArgumentParser(description=
        """Build Graph:
        takes as input a file in the form:
        a b dist time
        where a and b are destinations, dist is the distance between them, and
        time is the time needed to travel between them and constructs a graph.

        This graph should be represented as an adjacency list, and stored as a
        dictionary, with the key in the dictionary being the source of an edge and
        the value being a tuple containing the destination, distance, and cost.
        For example:
        g[a] = (b,dist,time)
        """)
    parser.add_argument('infile', type=file, help='the input file.')
    parser.add_argument('--pfile', dest='outfile',
        help="if --pfile=outfile is provided, write a pickled version of the graph to outfile. Otherwise, print it to standard output.")
    parser.add_argument('--d', dest='startNode',
        help="if --d=startNode is provided, compute dijkstra with the given starting node as source")

    args = parser.parse_args()

    graph = Graph(args.infile)

    if args.outfile:
        pickle.dump(graph, open(args.outfile, "wb"))
    else:
        print graph

    if args.startNode:
        print graph.dijkstra(args.startNode)
