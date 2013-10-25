import gameplay
import sys
import random
from copy import deepcopy

depth = 5
ident_strategy = 54
otime = 0
def value(board):
    score = [[99, -8, 8,  6,  6, 8, -8,99],
             [-8,-24,  -4,  -3,  -3,  -4,-24, -8],
             [8,  -4,  7,  4,  4,  7,  -4, 8],
             [6,  -3,  4,  0,  0,  4,  -3,  6],
             [6,  -3,  4,  0,  0,  4,  -3,  6],
             [8,  -4,  7,  4,  4,  7,  -4, 8],
             [-8,-24,  -4,  -3,  -3,  -4,-24, -8],
             [99, -8, 8,  6,  6, 8, -8,99]]
    value = 0
    if board[0][0] == 'B':
        score[0][1] = score[1][0] = 30
    elif board[0][0] == 'W' :
        score[0][1] = score[1][0] = -30
    if board[0][7] == 'B':
        score[0][6] = score[1][7] = 30
    elif board[0][7] == 'W':
        score[0][6] = score[1][7] = -30
    if board[7][0] == 'B':
        score[7][1] = score[6][0] = 30
    elif board[7][0] == 'W' :
        score[7][1] = score[6][0] = -30
    if board[7][7] == 'B':
        score[7][6] = score[6][7] = 30
    elif board[7][7] == 'W':
        score[7][6] = score[6][7] = -30

    for i in range(8):
        for j in range(8):
            if board[i][j] == "B":
                value = value + score[i][j]
            elif board[i][j] == "W":
                value = value - score[i][j]
    return value

def evalue(board):
    score = gameplay.score(board)
    return score[0] - score[1]

def betterThan(val1, val2, color, reversed):
    if color == "W":
        retVal = val1 < val2
    else:
        retVal =  val2 < val1
    if reversed:
        return not retVal
    else:
        return retVal




def alphaBeta(board, color,reverse, depth, strategy, alpha = -sys.maxint, beta = sys.maxint) :
    if depth == 0 :
        if strategy == 1 :
            return evalue(board)
        else:
            return value(board)

    moves = []
    for i in range(8) :
        for j in range(8) :
            if gameplay.valid(board, color, (i,j)) :
                moves.append((i,j))

    if len(moves) == 0 :
        if (gameplay.gameOver(board)) :
            return evalue(board)
        else:
            if  (color == "B" and not reverse) or (color == "W" and reverse) :
                newBoard = deepcopy(board)
                gameplay.doMove(newBoard,color,'pass')
                val = max(alpha, alphaBeta(newBoard, gameplay.opponent(color), reverse, depth - 1, strategy, alpha, beta))
                return val
            else :
                newBoard = deepcopy(board)
                gameplay.doMove(newBoard,color,'pass')
                val = min(beta, alphaBeta(newBoard, gameplay.opponent(color), reverse, depth - 1, strategy, alpha, beta))
                return val
    else:
        if (color == "B" and not reverse) or (color == "W" and reverse) :
            for move in moves :
                newBoard = deepcopy(board)
                gameplay.doMove(newBoard,color,move)
                alpha = max(alpha, alphaBeta(newBoard, gameplay.opponent(color), reverse, depth - 1, strategy, alpha, beta))

                if beta <= alpha :
                    break
            return alpha
        else :
            for move in moves :
                newBoard = deepcopy(board)
                gameplay.doMove(newBoard,color,move)
                beta = min(beta, alphaBeta(newBoard, gameplay.opponent(color), reverse, depth - 1, strategy, alpha, beta))
                if beta <= alpha:
                    break
            return beta


def nextMoveR(board, color, time):
    return nextMove(board, color, time, True)

def nextMove(board, color, time, reversed = False):
    global depth
    global otime

    moves = []
    for i in range(8):
        for j in range(8):
            if gameplay.valid(board, color, (i,j)):
                moves.append((i,j))
    if len(moves) == 0:
        return "pass"
    score = gameplay.score(board)
    num = score[0] + score[1]


    if len(moves) > 9:
        depth = 5

    if len (moves) < 7:
        depth = 6

    if time < 40 and num < ident_strategy:
        depth = 3

    if depth > 6:
        depth = 6
    if num >= ident_strategy:
        d = 8*8-num
        strategy = 1
    else:
        d = depth
        strategy = 0
    best = None
    for move in moves:
        newBoard = deepcopy(board)
        gameplay.doMove(newBoard,color,move)
        moveVal = alphaBeta(newBoard, gameplay.opponent(color), reversed, d, strategy)
        if best == None or betterThan(moveVal, best, color, reversed):
            bestMove = move
            best = moveVal
    otime = time
    return bestMove
