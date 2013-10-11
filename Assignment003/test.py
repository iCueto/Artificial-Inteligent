import wsheng3 as w
import dff as d
import gameplay as god

board1 = [['B','B','B','W','W','W','W','W'],
         ['B','B','W','W','W','W','W','.'],
         ['.','W','W','B','W','W','W','W'],
         ['W','W','W','W','B','W','B','W'],
         ['W','W','W','W','W','B','W','W'],
         ['W','W','W','.','W','B','W','W'],
         ['W','W','W','W','W','B','W','W'],
         ['.','.','W','.','W','B','.','W']]

board2 = [['.','.','.','.','.','.','.','.'],
          ['.','B','.','.','.','.','.','.'],
          ['.','.','B','W','W','.','.','.'],
          ['.','.','B','B','W','.','.','.'],
          ['.','.','.','B','W','.','.','.'],
          ['.','.','.','.','.','.','.','.'],
          ['.','.','.','.','.','.','.','.'],
          ['.','.','.','.','.','.','.','.']]

board3 = [['.','.','.','.','.','.','.','.'],
          ['.','.','.','.','.','.','.','.'],
          ['.','.','W','W','W','.','.','.'],
          ['.','.','B','B','W','.','.','.'],
          ['.','.','.','B','W','.','.','.'],
          ['.','.','.','.','.','.','.','.'],
          ['.','.','.','.','.','.','.','.'],
          ['.','.','.','.','.','.','.','.']]

board4 = [['.','B','.','.','.','.','.','.'],
          ['.','.','B','.','.','.','.','.'],
          ['.','.','.','B','.','W','.','.'],
          ['.','.','.','B','B','.','.','.'],
          ['.','.','B','B','B','B','.','.'],
          ['.','B','B','B','.','.','.','.'],
          ['.','.','.','.','.','.','.','.'],
          ['.','.','.','.','.','.','.','.']]

print w.get_value(board1) == 9
print w.get_value(board2) == -11
print w.get_value(board3) == -5
print w.get_value(board4) == -2
print w.betterThan(1,2,'B',False) == True
print w.betterThan(1,2,'W',True) == True
print w.betterThan(1,-2,'B',True) == True
print w.betterThan(1,-2,'W',False) == True


root = w.TreeNode()
root.board = board3
root.depth = 3
root.color = 'B'
root.reversed = False

nextMoves = root.validMoves()

best = root.worst()
bestmove = None

for pos in nextMoves:
    nextnode = w.TreeNode(root)
    god.doMove(nextnode.board, root.color, pos)

    res = w.alpha_beta_search(nextnode, float('-inf'), float('inf'), None)
    res2 = d.alphaBeta(nextnode.board, 'W', False, 3, 0)

    print "===Try %s valued %f returned by %f" % (pos, nextnode.value(), res)
    print "===Dff %s valued %f returned by %f" % (pos, nextnode.value(), res2)
    if w.betterThan(best, res, 'B', False):
        best = res
        bestmove = pos
    god.printBoard(nextnode.board)


print best
print pos
