#!/usr/bin/env python

import cPickle as pickle
import argparse
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
    dist_unit='km'
    time_unit='min'

    def __init__(self, infile=None) :
        self.vertex_list = {}
        self.adjlist = {}
        if infile : self.buildGraph(infile)

    ### method to print a graph.
    def __repr__(self) :
        ans = "{\n"
        for name,edge_list in self.adjlist.iteritems():
            ans += "%s: [\n" % name
            for edge in edge_list:
                ans += "  %s dist=%s%s time=%s%s\n" % (edge.dest, edge.distance, self.dist_unit, edge.time, self.time_unit)
            ans += "]\n"
        ans += "}"
        return ans

    ### helper methods to construct edges and vertices. Use these in buildGraph.
    def createVertex(self, inStr) :
        name, lat, longitude = inStr.split(" ",2)
        lat = lat.split("=")[1]
        longitude = longitude.split("=")[1]
        return Vertex(name, lat, longitude)

    def createEdges(self, inStr) :
        src, dest, dist, time = inStr.split(" ",4)
        dist=float(dist.split("=")[1].replace(self.dist_unit, '')) # remove km, change it to float
        time=int(time.split("=")[1].replace(self.time_unit, '')) # remove min, change it to int
        e1 = Edge(src,dest,dist, time)
        e2 = Edge(dest,src,dist, time)
        return e1, e2

### method that takes as input a file name and constructs the graph described
### above.
    def buildGraph(self, infile) :
        line = infile.readline() # pass first comment line

        # Vertexs
        for line in infile:
            if line[0]=='#' : break
            vertex = self.createVertex(line)
            self.vertex_list[vertex.name] = vertex
            self.adjlist[vertex.name] = []

        # Edges
        for line in infile:
            e1,e2 = self.createEdges(line)
            self.adjlist[e1.src].append(e1)
            self.adjlist[e2.src].append(e2)

        return self

### this method should take as input the name of a starting vertex
### and compute Dijkstra's algorithm,
### returning a dictionary that maps destination cities to
### a tuple containing the length of the path, and the vertices that form the path.
### Wikipedia has pseudo-Code for this - now translate it to Python,
### But do NOT copy any actual python code from anywhere else on the web
    def dijkstra(self, source) :
        #1. Assign to every node a tentative distance value: set it to zero for
        #our initial node and to infinity for all other nodes.
        dists = {}
        for name,vertex in self.vertex_list.iteritems() : dists[name] = float('inf')
        dists[source] = 0

        pathes = {}
        pathes[source] = source

        #2. Mark all nodes unvisited. Set the initial node as current. Create a
        #set of the unvisited nodes called the unvisited set consisting of all the
        #nodes except the initial node.
        #visited = {}
        #for name, vertex in self.vertex_list.iteritems() : visited[name] = False
        unvisited = set()
        for name, vertex in self.vertex_list.iteritems() : unvisited.add(vertex)
        current = source

        while len(unvisited)>0:
            #3. For the current node, consider jall of its unvisited neighbors and
            #calculate their tentative distances. For example, if the current node A
            #is marked with a distance of 6, and the edge connecting it with a neighbor B
            #has length 2, then the distance to B (through A) will be 6 + 2 = 8.
            #If this distance is less than the previously recorded tentative distance
            #of B, then overwrite that distance. Even though a neighbor has been examined,
            #it is not marked as "visited" at this time, and it remains in the unvisited set.
            neighbor_list = self.adjlist[current]
            for edge in neighbor_list:
                target = edge.dest
                if dists[target] > dists[current] + edge.distance:
                    dists[target] = dists[current] + edge.distance
                    pathes[target] = current

            #4. When we are done considering all of the neighbors of the current node,
            #mark the current node as visited and remove it from the unvisited set.
            #A visited node will never be checked again.
            unvisited.remove(self.vertex_list[current])

            #5. If the destination node has been marked visited (when planning a route
            #between two specific nodes) or if the smallest tentative distance among
            #the nodes in the unvisited set is infinity (when planning a complete traversal),
            #then stop. The algorithm has finished.
            found_next_vertex = False
            min_dist = float('inf')
            for vertex in unvisited:
                name = vertex.name
                if dists[name] < min_dist:
                    found_next_vertex = True
                    current = name
                    min_dist = dists[name]
            if not found_next_vertex : break

            #6. Select the unvisited node that is marked with the smallest tentative distance, and set it as the new "current node" then go back to step 3.

        return dists, pathes

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
    parser.add_argument('--pfile', dest='outfile', type=argparse.FileType('w'),
        help="if --pfile=outfile is provided, write a pickled version of the graph to outfile. Otherwise, print it to standard output.")
    parser.add_argument('--d', dest='startNode',
        help="if --d=startNode is provided, compute dijkstra with the given starting node as source")

    args = parser.parse_args()

    graph = Graph(args.infile)
    args.infile.close

    if args.outfile:
        pickle.dump(graph, args.outfile)
        args.outfile.close
    else:
        print graph

    if args.startNode:
        dists,pathes = graph.dijkstra(args.startNode)
        print "Min distance:"
        print "{"
        for name,dist in dists.iteritems():
            path = [name]
            while not path[0] == args.startNode : path.insert(0,pathes[path[0]])
            print "[%s:(%s,%s)]," % (name,dist,path)
        print "}"
