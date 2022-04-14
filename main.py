#Author: Marcin Kapłon

import numpy as np

#checking if number can be assigned to the field
def isSafe(board, i, j, num):
    if num not in board[i, :] and num not in board[:, j] and num not in board[i - i % 3:i - i % 3 + 3,
                                                                                j - j % 3:j - j % 3 + 3]:
        return True
    return False

#sudoku solving function
#returns False if cannot be solved
def solve(board, i, j):
    if i==8 and j==9:
        return True
    if j==9:
        i+=1
        j=0
    if board[i][j]>0:
        return solve(board, i, j+1)
    for num in range(1,10):
        if isSafe(board, i, j, num):
            board[i][j]=num
            if solve(board, i, j+1):
                return True
        board[i][j]=0
    return False

def deleteNums(board,k):
    for i in range(k):
        coord=tuple(np.random.randint(0,9,2))
        while board[coord]==0:
            coord=tuple(np.random.randint(0,9,2))
        if board[coord]>0:
            board[coord]=0

def isOnlyOneSolution(board, board2, i,j):
    if i==8 and j==9:
        return True
    if j==9:
        i+=1
        j=0
    if board[i][j]>0:
        return isOnlyOneSolution(board, board2,i, j+1)
    for num in range(1,11):
        if board2[i,j]==num:
            continue
        if isSafe(board, i, j, num) and num!=10:
            return False
        if num==10:
            if isSafe(board, i, j, board2[i,j]):
                board[i][j]=board2[i,j]
                if isOnlyOneSolution(board, board2,i, j+1):
                    return True
            board[i][j]=0

    return False
        

if __name__ == '__main__':
    board = np.zeros([9, 9])
    # fill diagonal matrices
    for i in [3, 6, 9]:
        tab = np.arange(1, 10)
        np.random.shuffle(tab)
        board[i - 3:i, i - 3:i] = tab.reshape(3, 3)
    solve(board,0,0)
    board2=np.matrix.copy(board)
    print(board)
    deleteNums(board, 20)

    print(isOnlyOneSolution(board, board2, 0,0))
    #print(board)
    solve(board, 0, 0)
    print(board)
    print(sum(sum(board==board2))==81)