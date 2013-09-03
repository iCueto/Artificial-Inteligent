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

    def successors(self, oldstate) :
        #add code here
        nlist = []
        return nlist


class Node:

    def __init__(self, vertex, parentState=None, cost=0) :
        self.vertex = vertex
        self.parent = parentState
        self.cost = cost

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
        pass

    def __le__(self, other) :
        pass

    def __gt__(self, other) :
        pass
    def __ge__(self, other) :
        pass
    def __eq__(self, other) :
        pass
    def __ne__(self, other) :
        pass

        
### search takes as input a search queue, the initial state,
### a node factory,
### a function that returns true if the state provided as input is the goal,
### and the maximum depth to search in the search tree.
### It should print out the solution and the number of nodes enqueued, dequeued,
###  and expanded.

def search(queue, initialState, factory, goalTest, maxdepth=10) :
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


### code for printing out a sequence of states that leads to a solution
def printSolution(node) :
    print "Solution *** "
    print "cost: ", node.cost
    moves = [node]
    current = node
    while current.parent != None :
        moves.append(current)
        current = current.parent
    moves.append(current)
    moves.reverse()
    for move in moves :
        print move


### usage: search --search=[BFS| DFS | AStar] {-l=depthLimit} {-i}
###               initialState goal infile
###
### If -l is provided, only search to the given depth.
### if -i is provided, use an iterative deepening version (only applies
        ### to DFS, 10pts extra credit for IDA*)
if __name__ == '__main__':
    # for example if BFS is the input, start by:
    q = searchQueues.BFSQueue()

    pass



    
