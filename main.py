#Author: Marcin Kapłon

import numpy as np
from tkinter import *

class App(Tk):
    def __init__(self):
        super().__init__()
        self.title("Sudoku")
        self.geometry("600x450")
        self.framesize=self.winfo_screenheight()*0.5
        #frame with sudoku board
        self.frame=Frame(self, bg="orange")
        self.frame.place(x=5, y=5, height=400, width=400)
        #first board
        board=self.generate_board(45)
        my_entries=[]
        reg_callback=self.register(self.callback)
        for i in range(9):
            for j in range(9):
                if board[i][j]==0:
                    self.entry=Entry(self.frame, borderwidth=1, relief="solid", font="Helvetica 15 bold",
                     justify="center", validate="key", validatecommand=(reg_callback, "%P"), insertontime=0)
                    self.entry.place(relheight=1/9, relwidth=1/9, relx=i/9, rely=j/9)
                    my_entries.append(self.entry)
                else:
                    self.label=Label(self.frame,text=int(board[i][j]), borderwidth=1, relief="solid")
                    self.label.place(relheight=1/9, relwidth=1/9, relx=i/9, rely=j/9)

    def generate_board(self, k):
        board = np.zeros([9, 9])
        # fill diagonal matrices
        for i in [3, 6, 9]:
            tab = np.arange(1, 10)
            np.random.shuffle(tab)
            board[i - 3:i, i - 3:i] = tab.reshape(3, 3)
        solve(board,0,0)
        delete_nums(board,k)
        return board


    def callback(self, input):
        if (input.isdigit() and len(input)==1) or input=='':
            return True
        else:
            return False

        

#checking if number can be assigned to the field
def is_safe(board, i, j, num):
    if num not in board[i, :] and num not in board[:, j] and num not in board[i - i % 3:i - i % 3 + 3,
                                                                                j - j % 3:j - j % 3 + 3]:
        return True
    return False

#sudoku solving function
#returns False if cannot be solved
#if do_solve==False it only checks whether sudoku can be solved
def solve(board, i, j, do_solve=True):
    if do_solve==False:
        board=np.matrix.copy(board)
    if i==8 and j==9:
        return True
    if j==9:
        i+=1
        j=0
    if board[i][j]>0:
        return solve(board, i, j+1)
    for num in range(1,10):
        if is_safe(board, i, j, num):
            board[i][j]=num
            if solve(board, i, j+1):
                return True
        board[i][j]=0
    return False

#deletes k number ensuring sudoku solution is unique
#k must be greater than 3
def delete_nums(board,k):
    full_board=np.matrix.copy(board)
    for i in range(3):
        coord=tuple(np.random.randint(0,9,2))
        while board[coord]==0:
            coord=tuple(np.random.randint(0,9,2))
        board[coord]=0
    i=0
    while i<k-3:
        coord=tuple(np.random.randint(0,9,2))
        while board[coord]==0:
            coord=tuple(np.random.randint(0,9,2))
        original_num=board[coord]
        for j in range(1,10):
            if j==original_num:
                continue
            if is_safe(board, coord[0], coord[1], j):
                board[coord]=j
                if solve(board, 0,0, do_solve=False):
                    i=i-1
                    board[coord]=original_num
                    break
        else:
            board[coord]=0
        i=i+1

#can be deleted
def isOnlyOneSolution(board_original, board2, i,j):
    board=np.matrix.copy(board_original)
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
        if is_safe(board, i, j, num) and num!=10:
            board[i][j]=num
            board2=np.matrix.copy(board)
            isOnlyOneSolution(board, board2, i,j+1)
        if num==10:
            if is_safe(board, i, j, board2[i,j]):
                board[i][j]=board2[i,j]
                if isOnlyOneSolution(board, board2,i, j+1):
                    return True
            board[i][j]=0
    return False
        

if __name__ == '__main__':
    app = App()
    app.mainloop()

    board = np.zeros([9, 9])
    # fill diagonal matrices
    for i in [3, 6, 9]:
        tab = np.arange(1, 10)
        np.random.shuffle(tab)
        board[i - 3:i, i - 3:i] = tab.reshape(3, 3)
    solve(board,0,0)
    delete_nums(board, 5)
    print(board)
    print(sum(sum(board==0)))
    # board2=np.matrix.copy(board)
    # print(board)
    # deleteNums(board, 40)

    # print(isOnlyOneSolution(board, board2, 0,0))
    # #print(board)
    # solve(board, 0, 0)
    # #print(board)
    # print(sum(sum(board==0)))
    # print(sum(sum(board==board2))==81)
    # board=np.array([[0,7,0,0,0,0,0,9,0],
    #                 [0,0,5,3,0,4,0,0,0],
    #                 [0,0,9,0,1,0,6,0,0],
    #                 [0,0,0,6,0,5,0,0,0],
    #                 [0,2,0,0,4,0,0,8,7],
    #                 [0,0,4,1,0,0,0,0,0],
    #                 [4,0,0,0,7,0,0,6,2],
    #                 [0,5,2,0,0,0,8,0,0],
    #                 [8,0,0,0,0,2,0,0,3]])
    # print(board)
    # board2=np.matrix.copy(board)
    # solve(board, 0,0)
    # print(board)
    # deleteNums(board, 52)
    # print(board)
    # print(solve(board, 0,0, do_solve=False))
    # print(sum(sum(board==0)))