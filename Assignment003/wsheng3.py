#!/usr/bin/env python

import gameplay as god
import random
import time as timelib
from copy import deepcopy
import os

BOARD_SIZE = 8
BEGIN_DEPTH = 60
MAX_DEPTH = 3
# in second
ROUND_TIME_LIMIT = 300/((BOARD_SIZE*BOARD_SIZE-4)/2)
if os.getenv('VERBOSE'):
    VERBOSE = True
else:
    VERBOSE = False
if os.getenv('NOMP'):
    MP = False
else:
    MP = True

value_board = [[16, -6,  4,  3,  3,  4, -6, 16],
               [-6,-12, -4, -3, -3, -4,-12, -6],
               [4,  -4,  3,  2,  2,  3, -4,  4],
               [3,  -3,  2,  1,  1,  2, -3,  3],
               [3,  -3,  2,  1,  1,  2, -3,  3],
               [4,  -4,  3,  2,  2,  3, -4,  4],
               [-6,-12, -4, -3, -3, -4,-12, -6],
               [16, -6,  4,  3,  3,  4, -6, 16]]
vb = [[99, -8, 8,  6,  6, 8, -8,99],
      [-8,-24,  -4,  -3,  -3,  -4,-24, -8],
      [8,  -4,  7,  4,  4,  7,  -4, 8],
      [6,  -3,  4,  0,  0,  4,  -3,  6],
      [6,  -3,  4,  0,  0,  4,  -3,  6],
      [8,  -4,  7,  4,  4,  7,  -4, 8],
      [-8,-24,  -4,  -3,  -3,  -4,-24, -8],
      [99, -8, 8,  6,  6, 8, -8,99]]

#value_board = vb

## random
# def randomMove(board, color, time):
#     moves = []
#     for i in range(8):
#         for j in range(8):
#             if god.valid(board, color, (i,j)):
#                 moves.append((i,j))
#     if len(moves) == 0:
#         return "pass"
#     bestMove = moves[random.randint(0,len(moves) - 1)]
#     return bestMove


## greedy
def get_value(board):
    v = 0
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] == 'B':
                v += value_board[i][j]
            elif board[i][j] == 'W':
                v -= value_board[i][j]
    return v

def betterThan(val1, val2, color, reversed):
    if (color == 'W') != (reversed):
        return val1 > val2
    else:
        return val1 < val2

# def greedyMove(board, color, time, reversed = False):
#     moves = []
#     for i in range(8):
#         for j in range(8):
#             if god.valid(board, color, (i,j)):
#                 moves.append((i,j))
#     if len(moves) == 0:
#         return "pass"
#     best = None
#     for move in moves:
#         newboard = deepcopy(board)
#         god.doMove(newboard,color,move)
#         moveval = get_value(newboard)
#         if best == None or betterThan(moveval, best, color, reversed):
#             bestmove = move
#             best = moveval
#     return bestmove



## treenode
class TreeNode:
    def __init__(self, parent=None):
        if parent:
            self.board = deepcopy(parent.board)
            self.depth = parent.depth - 1
            self.color = god.opponent(parent.color)
            self.reversed = parent.reversed
        self.nextmove = None
        #self.children = []
    # def search_children(self, node, board):
    #     for child in node.children:
    #         if child.board == board:
    #             return child
    #     return None
    def validMoves(self):
        moves = []
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if god.validMove(self.board, self.color, (i,j)):
                    moves.append((i,j))
        return moves
    def value(self):
        res = get_value(self.board)
        if (self.color == 'W') != (self.reversed): res = -res
        return res
    def end_value(self):
        s = god.score(self.board)
        if (self.color == 'W') != (self.reversed):
            return s[1] - s[0]
        else:
            return s[0] - s[1]
    def worst(self):
        if (self.color == 'W') != self.reversed:
            return float('inf')
        else:
            return float('-inf')
    def best(self):
        return -self.worst()


def max_depth(board):
    d = 0
    for i in range(0,BOARD_SIZE):
        for j in range(0,BOARD_SIZE):
            if board[i][j] == '.':
                d += 1
    return d


# Alpha-beta pruning
# Return the expected value in [alpha, beta]
def alpha_beta_search(node, alpha, beta, timeout):
    #if VERBOSE: print "===Searching in %f..%f of %d" % (alpha, beta, node.depth)

    # if timeout():
    #     if VERBOSE: print "==Timeout return in %d" % (node.depth)
    #     return node.value() # Timeout do nothing

    if (node.depth == 0):
        if (god.gameOver(node.board)):
            return node.end_value()
        else:
            return node.value()

    nextMoves = node.validMoves()
    # Game not end, we can pass on.
    if (len(nextMoves) == 0): nextMoves = ['pass']

    for pos in nextMoves:
        # init next child node
        nextnode = TreeNode(node)
        god.doMove(nextnode.board, node.color, pos)

        # Update from children
        res = alpha_beta_search(nextnode, alpha, beta, timeout)

        # Update bounds
        if (node.color == 'W') != (node.reversed): # min
            if betterThan(beta, res, node.color, node.reversed):
                beta = res
        else:                   # max
            if betterThan(alpha, res, node.color, node.reversed):
                alpha = res

        # Pruning
        if (alpha >= beta):
            #if VERBOSE: print "==Pruning %f..%f in %d" % (alpha, beta, node.depth)
            break

    if (node.color == 'W') != (node.reversed): # min
        return beta
    else:
        return alpha


# from multiprocessing import Process
# import os

# def info(title):
#     print(title)
#     print('module name:', __name__)
#     if hasattr(os, 'getppid'):  # only available on Unix
#         print('parent process:', os.getppid())
#     print('process id:', os.getpid())
# def f(name):
#     info('function f')
#     a = 0
#     for i in range(1,10**7):
#         a = a+1
#     print ('hello', name)
# def run():
#     p1 = Process(target=f, args=('bob',))
#     p2 = Process(target=f, args=('bob',))
#     p3 = Process(target=f, args=('bob',))
#     p4 = Process(target=f, args=('bob',))
#     p1.start()
#     p2.start()
#     p3.start()
#     p4.start()
#     p4.join()


## Main function
def nextMove(board, color, time, reversed = False):
    # Init
    beginTime = timelib.time()  # The beginning of this round
    root = TreeNode()           # root node
    root.board = board
    root.depth = min(max_depth(root.board), MAX_DEPTH)
    root.color = color
    root.reversed = reversed

    # Begin search
    if VERBOSE: print "==========Searching in depth %d" % (root.depth)

    # use greedy at the beginning
    # if root.depth > BEGIN_DEPTH :
    #     if VERBOSE: print 'Using random in %d' % root.depth
    #     return randomMove(board, color, time)

    # then use alpha-beta pruning search
    if VERBOSE: print 'Using alpha-beta in %d' % root.depth
    timeout = lambda : ((timelib.time() - beginTime) >= ROUND_TIME_LIMIT) or ((timelib.time() - beginTime) >= time*0.8)


    nextMoves = root.validMoves()
    if (len(nextMoves) == 0) and (not god.gameOver(root.board)):
        return 'pass'

    best = root.worst()
    for pos in nextMoves:

        nextnode = TreeNode(root)
        god.doMove(nextnode.board, root.color, pos)

        res = alpha_beta_search(nextnode, float('-inf'), float('inf'), timeout)
        if VERBOSE: print "===Try %s returned by %f", (pos, res)
        if betterThan(best, res, root.color, root.reversed):
            best = res
            move = pos
            if VERBOSE: print "===Update best %f with %s in %d", (best, pos, root.depth)

    # Output
    if VERBOSE: print 'alpha-beta : %f-%s' % (best, (move,))
    return move

# Reversed
def nextMoveR(board, color, time):
    return nextMove(board, color, time, True)
