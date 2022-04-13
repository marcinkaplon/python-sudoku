#Author: Marcin Kapłon

import numpy as np

#checking if number can be assigned to the field
def isSafe(board, i, j, num):
    if (num not in board[i, :] and num not in board[:, j] and num not in board[i - i % 3:i - i % 3 + 3,
                                                                                j - j % 3:j - j % 3 + 3]):
        return True
    return False

#sudoku solving function
def solve(board, i, j):
    print(i,j)
    if (i==8 and j==9):
        return True
    if (j==9):
        i+=1
        j=0
    if (board[i][j]>0):
        return solve(board, i, j+1)
    for num in range(1,10):
        if isSafe(board, i, j, num):
            board[i][j]=num
            if solve(board, i, j+1):
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
    solve(board, 0, 0)
    print(board)