#!/usr/bin/env python

import gameplay as god
import random
import time as timelib
from copy import deepcopy
import os
import math

BOARD_SIZE = 8
BOARD_DEPTH = BOARD_SIZE*BOARD_SIZE-4
MIN_DEPTH = 2
MAX_DEPTH = 10
# in second
ROUND_TIME_LIMIT = 300/(BOARD_DEPTH/2)

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

## treenode
class TreeNode:
    def __init__(self, parent=None):
        if parent:
            self.board = deepcopy(parent.board)
            self.depth = parent.depth - 1
            self.color = god.opponent(parent.color)
            self.reversed = parent.reversed
        self.nextmove = None
    def validMoves(self):
        moves = []
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if god.validMove(self.board, self.color, (i,j)):
                    moves.append((i,j))
        return moves
    def value(self):
        res = get_value(self.board)
        #if (self.color == 'W') != (self.reversed): res = -res
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
    if timeout(): return node.value() # Timeout do nothing

    if (node.depth == 0):
        if (god.gameOver(node.board)):
            return node.end_value()
        else:
            return node.value()

    nextMoves = node.validMoves()
    if (len(nextMoves) == 0): nextMoves = ['pass'] # Game not end, we can pass on.

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


## Main function
def nextMove(board, color, time, reversed = False):
    # Init
    beginTime = timelib.time()  # The beginning of this round
    root = TreeNode()           # root node
    root.board = board
    d = max_depth(root.board)
    limits = math.floor(float(BOARD_DEPTH-d)/(BOARD_DEPTH-MAX_DEPTH)*(MAX_DEPTH-MIN_DEPTH))+MIN_DEPTH
    if VERBOSE: print "limits %f" % limits
    root.depth = min(d, limits)
    root.color = color
    root.reversed = reversed

    # Begin search
    if VERBOSE: print "==========Searching in depth %d" % (root.depth)

    # then use alpha-beta pruning search
    timeout = lambda : ((timelib.time() - beginTime) >= ROUND_TIME_LIMIT) or ((timelib.time() - beginTime) >= time*0.8)

    nextMoves = root.validMoves()
    if len(nextMoves) == 0: return 'pass'

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

    return move

# Reversed
def nextMoveR(board, color, time):
    return nextMove(board, color, time, True)
