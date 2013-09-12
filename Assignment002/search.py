#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import argparse
import buildGraph
import searchQueues

### A NodeFactory is a helper class that is used to create new Nodes.
### It stores the graph representing our problem and uses it to find successors.

class NodeFactory :
    def __init__(self, inputgraph) :
        self.inputgraph = inputgraph

    ### return a list of all nodes reachable from this state
    ### you complete this.
    ### For a given node, find the corresponding vertex in the input graph.
    ### Find the vertices it is connected to, and generate a Node for each
    ### one. Update parentState and cost to reflect the new edge added to the
    ### solution.
    ### nlist is a list of successor nodes.

    def successors(self, current_state) :
        #add code here
        nlist = []
        current_vertex = current_state.vertex
        current_name = current_vertex.name
        current_cost = current_state.cost
        current_depth = current_state.depth
        for succ_edge in self.inputgraph.adjlist[current_name]:
            succ_name = succ_edge.dest
            succ_vertex = self.inputgraph.vertex_list[succ_name]
            succ_cost = current_cost + succ_edge.distance
            succ_state = Node(succ_vertex, current_state, succ_cost, current_depth+1)
            nlist.append(succ_state)
        return nlist


class Node:

    def __init__(self, vertex, parentState=None, cost=0, depth=0) :
        self.vertex = vertex
        self.parent = parentState
        self.cost = cost
        self.depth = depth

    def isGoal(self, goalTest) :
        return goalTest(self)

    def isStart(self) :
        return self.parent is None

    def __repr__(self) :
        return self.vertex.__repr__()

    def __hash__(self) :
        return self.vertex.__hash__()

    ## you do this.
    def __lt__(self, other) :
        return other and (self.cost < other.cost)

    def __le__(self, other) :
        return other and (self.cost <= other.cost)

    def __gt__(self, other) :
        return other and (self.cost > other.cost)

    def __ge__(self, other) :
        return other and (self.cost >= other.cost)

    def __eq__(self, other) :
        return other and (self.cost == other.cost)

    def __ne__(self, other) :
        return not other or (self.cost != other.cost)


### Goaltest

def goalTest(current_node):
    return current_node.vertex.name == goal_name

### search takes as input a search queue, the initial state,
### a node factory,
### a function that returns true if the state provided as input is the goal,
### and the maximum depth to search in the search tree.
### It should print out the solution and the number of nodes enqueued, dequeued,
###  and expanded.

def search(queue, initialState, factory, goalTest, maxdepth=float('inf')) :
    closedList = {}
    nodesEnqueued = 1
    nodesDequeued = 0
    nodesExpanded = 0
    queue.insert(initialState)
    ### you complete this.
    ### While there are states in the queue,
    ###   1. Dequeue
    ###   2. If this is the goal, stop
    ###   3. If not, insert in the closed list and generate successors
    ###   4. If successors are not in the closed list, enqueue them.

    found = False
    while not queue.isEmpty():
        current_state = queue.pop()
        nodesDequeued += 1

        if current_state.isGoal(goalTest):
            found = True
            break

        if current_state.depth < maxdepth:
            successors = factory.successors(current_state)
        else:
            successors = []
        for succ_state in successors:
            if not succ_state.vertex.name in closedList:
                queue.insert(succ_state)
                nodesEnqueued += 1

        closedList[current_state.vertex.name] = current_state
        nodesExpanded += len(successors)


    print "nodes enqueued: %s" % nodesEnqueued
    print "nodes dequeued: %s" % nodesDequeued
    print "nodes expanded: %s" % nodesExpanded

    if not found:
        print "Search failed!"
        print "============================="
        return found

    printSolution(current_state)

    # Find the max depth in closedList
    max_depth = 0
    for name, state in closedList.iteritems():
        if state.depth > max_depth: max_depth = state.depth
    print "search max depth: %s" % max_depth
    print "============================="

    return found


### code for printing out a sequence of states that leads to a solution
def printSolution(node) :
    print "Solution *** "
    print "cost: ", node.cost
    moves = []                  # NOTICE: here should be empty, otherwise the first node will be append twice!
    current = node
    while current.parent != None :
        moves.append(current)
        current = current.parent
    moves.append(current)
    moves.reverse()
    for move in moves :
        print "{:>20}: {:<5}".format(move, move.cost)


### usage: search --search=[BFS| DFS | AStar] {-l=depthLimit} {-i}
###               initialState goal infile
###
### If -l is provided, only search to the given depth.
### if -i is provided, use an iterative deepening version (only applies
        ### to DFS, 10pts extra credit for IDA*)
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Search Algorithms: BFS, DFS, AStar")

    parser.add_argument('initialState', help='the init state')
    parser.add_argument('goal', help='the goal')
    parser.add_argument('infile', type=file, help='the input file')

    parser.add_argument('--search', choices=['BFS', 'DFS', 'AStar'], default='BFS',
                        help='the search algorithm, default is BFS.')
    parser.add_argument('-l', dest="depthLimit", type=int, default=float('inf'),
                        help='only search to the given depth.')
    parser.add_argument('-i', dest="isIterative", action='store_true',
                        help='use an iterative deepening version (DFS, IDA*')

    args = parser.parse_args()
    graph = buildGraph.Graph(args.infile)
    args.infile.close

    # init node
    init_vertex = graph.vertex_list[args.initialState]
    init_state = Node(init_vertex, None, 0, 0)
    goal_name = args.goal       # [Hack] Global var for goalTest()
    goal_vertex = graph.vertex_list[goal_name]
    queue = getattr(searchQueues, args.search + 'Queue')(goal_vertex)
    factory = NodeFactory(graph)

    if args.search == 'DFS':
        if args.isIterative:
            print "Searching from %s to %s by %s iteratively with %s limit..." % (args.initialState, args.goal, args.search, args.depthLimit)
            depth_limit = min(args.depthLimit, len(graph.vertex_list))
            for depth_limit in range(0, depth_limit):
                print "Now trying with limit %s..." % (depth_limit)
                if search(queue, init_state, factory, goalTest, depth_limit): break
        else:
            print "Searching from %s to %s by %s with depth limit %s..." % (args.initialState, args.goal, args.search, args.depthLimit)
            search(queue, init_state, factory, goalTest, maxdepth=args.depthLimit)
    else:
        print "Searching from %s to %s by %s..." % (args.initialState, args.goal, args.search)
        search(queue, init_state, factory, goalTest)
