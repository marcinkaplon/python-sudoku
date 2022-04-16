#Author: Marcin Kapłon

import numpy as np
from tkinter import *

class App(Tk):
    def __init__(self):
        super().__init__()
        self.title("Sudoku")
        self.geometry("560x420")
        self.resizable(False, False)
        self.configure(background="#2e5921")
        self.framesize=self.winfo_screenheight()*0.5
        #frame with sudoku board
        self.frame=Frame(self)
        self.frame.place(x=10, y=10, height=400, width=400)
        #first board
        self.board=self.generate_board(45)
        #list of entries with empty cells
        self.my_entries=[]
        #registering checking function
        self.reg_callback=self.register(self.callback)
        self.frames=[[i for i in range(3)] for j in range(3)]
        #creating 3x3 boards
        for i in range(3):
            for j in range(3):
                self.frames[i][j]=Frame(self.frame, borderwidth=3, background="#2e5921")
                self.frames[i][j].place(relwidth=1/3, relheight=1/3, relx=i/3, rely=j/3)
        #filling board in GUI
        for i in range(9):
            for j in range(9):
                if self.board[i][j]==0:
                    self.entry=Entry(self.frames[i//3][j//3], borderwidth=1, relief="ridge", font="Helvetica 15 bold", state="normal",
                     justify="center", validate="key", validatecommand=(self.reg_callback, "%P"), insertontime=0)
                    self.entry.place(relheight=1/3, relwidth=1/3, relx=i%3/3, rely=j%3/3)
                    self.entry.bind("<ButtonRelease-1>",lambda event, pos=i*9+j: self.select_cell(pos))
                    for k in range(1,10):
                        self.entry.bind(str(k), lambda event, pos=i*9+j, l=k: self.change_number(pos,l))
                    self.my_entries.append(self.entry)
                else:
                    self.label=Label(self.frames[i//3][j//3],text=int(self.board[i][j]), borderwidth=1, relief="ridge",
                    bg="#525252", fg="white")
                    self.label.place(relheight=1/3, relwidth=1/3, relx=i%3/3, rely=j%3/3)
                    self.my_entries.append(self.label)
        self.button_frames=Frame(self, background="#2e5921")
        self.button_frames.place(x=420, y=10, height=400, width=130)
        self.button_frames.bind("<ButtonRelease-1>",lambda event, pos=82: self.select_cell(pos))
        #button to check solution
        self.check_button = Button(self.button_frames, text="Sprawdź", command=lambda: self.check(self.board, self.my_entries), bg="#b0ebba")
        self.check_button.pack(side="top", fill="x", pady=5)
        #button to view solution
        self.view_solution_button = Button(self.button_frames, text="Pokaż rozwiązanie", command=lambda: self.view_solution(self.board, self.my_entries),
                                    bg="#b0ebba")
        self.view_solution_button.pack(side="top", fill="x", pady=5)
        #label "new game"
        self.new_game_label=Label(self.button_frames, text="\nNowa gra:", bg="#2e5921", fg="#b0ebba")
        self.new_game_label.pack(side="top", fill="x", pady=5)
        #new game buttons
        self.easy_button=Button(self.button_frames, text="Łatwa", command=lambda: self.new_game(self.board, "e"), bg="#b0ebba")
        self.easy_button.pack(side="top", fill="x", pady=5)
        self.easy_button=Button(self.button_frames, text="Normalna", command=lambda: self.new_game(self.board, "n"), bg="#b0ebba")
        self.easy_button.pack(side="top", fill="x", pady=5)
        self.easy_button=Button(self.button_frames, text="Trudna", command=lambda: self.new_game(self.board, "t"), bg="#b0ebba")
        self.easy_button.pack(side="top", fill="x", pady=5)

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

    #function which checks whether only numbers are in cell inputs
    def callback(self, input):
        if (input.isdigit() and len(input)==1 and input!="0") or input=='':
            return True
        else:
            return False
        
    def check(self, board, my_entries):
        solve(board, 0,0)
        nums = [i.cget("text") if type(i)==Label else i.get() for i in my_entries]
        nums = [float(i) if not i=='' else 0 for i in nums]
        nums=np.array(nums).reshape([9,9])
        for i in range(9):
            for j in range(9):
                if board[i][j]!=nums[i][j]:
                    self.my_entries[i*9+j].config(bg="#fa908c")
                elif type(self.my_entries[i*9+j])==Entry:
                        self.my_entries[i*9+j].config(bg="#9fe889")

    def view_solution(self, board, my_entries):
        print(new_solver(board))
        print(board)
        for i in range(9):
            for j in range(9):
                if type(my_entries[i*9+j])==Entry:
                    my_entries[i*9+j].delete(0,1)
                    my_entries[i*9+j].insert(0,int(board[i,j]))
                    my_entries[i*9+j].config(state="disabled", disabledbackground="#9fe889")

    def new_game(self, board, level):
        if level=="e":
            k=np.random.randint(40,45)
        elif level=="n":
            k=np.random.randint(45,50)
        else:
            k=np.random.randint(55, 60)
        self.board=self.generate_board(k)
        for cell in self.my_entries:
            cell.place_forget()
        self.my_entries=[]
        for i in range(9):
            for j in range(9):
                if self.board[i][j]==0:
                    self.entry=Entry(self.frames[i//3][j//3], borderwidth=1, relief="ridge", font="Helvetica 15 bold", state="normal",
                     justify="center", validate="key", validatecommand=(self.reg_callback, "%P"), insertontime=0)
                    self.entry.place(relheight=1/3, relwidth=1/3, relx=i%3/3, rely=j%3/3)
                    self.entry.bind("<ButtonRelease-1>",lambda event, pos=i*9+j: self.select_cell(pos))
                    for k in range(1,10):
                        self.entry.bind(str(k), lambda event, pos=i*9+j, l=k: self.change_number(pos,l))
                    self.my_entries.append(self.entry)
                else:
                    self.label=Label(self.frames[i//3][j//3],text=int(self.board[i][j]), borderwidth=1, relief="ridge",
                    bg="#525252", fg="white")
                    self.label.place(relheight=1/3, relwidth=1/3, relx=i%3/3, rely=j%3/3)
                    self.my_entries.append(self.label)

    def select_cell(self, pos):
        for i in range(9):
            for j in range(9):
                if pos==i*9+j:
                    self.my_entries[pos].config(bg="#c9c9c9")
                elif type(self.my_entries[i*9+j])==Entry:
                    self.my_entries[i*9+j].config(bg="white")
    
    def change_number(self, pos,k):
        self.my_entries[pos].delete(0)
        self.my_entries[pos].insert(0,k)
                
#checking if number can be assigned to the field
def is_safe(board, i, j, num):
    if num not in board[i, :] and num not in board[:, j] and num not in board[i - i % 3:i - i % 3 + 3,
                                                                                j - j % 3:j - j % 3 + 3]:
        return True
    return False

# sudoku solving function
# returns False if cannot be solved
# if do_solve==False it only checks whether sudoku can be solved
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
    #full_board=np.matrix.copy(board)
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
                if new_solver(board,do_solve=False):
                    i=i-1
                    board[coord]=original_num
                    break
        else:
            board[coord]=0
        i=i+1

def find_only_solution(board, row, col):
    is_safe_num=[]
    #print("JEDNAK TU")
    num=0
    for i in range(1,10):
        is_safe_num.append(is_safe(board, row, col, i))
        if is_safe_num[-1]==True:
            num=i
    if sum(is_safe_num)==1:
        board[row,col]=num

def find_nines_with_one_solution(board):
    for i in range(9):
        #rows
        if sum(board[i,]==0)==1:
            h=[j for j in range(10)]
            index=0
            for j in range(9):
                #print(i,j,"RZAD",board[i,j])
                h.remove(board[i,j])
                if board[i,j]==0:
                    index=j
            board[i, index]=h[0] if h[0]!=0 else h[1]
        #columns
        if sum(board[:,i]==0)==1:
            h=[j for j in range(10)]
            index=0
            for j in range(9):
                #print(j,i, "KOLUMNA", board[j,i])
                h.remove(board[j,i])
                if board[j,i]==0:
                    index=j
            board[index, i]=h[0] if h[0]!=0 else h[1]
    #squares
    for i in range(3):
        for j in range(3):
            if sum(sum(board[i*3:i*3+3,j*3:j*3+3]==0))==1:
                h=[k for k in range(10)]
                index1=0
                index2=0
                for k in range(3):
                    for l in range(3):
                        #print(board, i*3+k, j*3+l, board[i*3+k, j*3+l], h)
                        h.remove(board[i*3+k, j*3+l])
                        if board[i*3+k, j*3+l]==0:
                            index1=i*3+k
                            index2=j*3+l
                board[index1, index2]=h[0] if h[0]!=0 else h[1]

def new_solver(board, do_solve=True):
    if do_solve==False:
        board=np.matrix.copy(board)
    try:
        while 0 in board:
            board2=np.matrix.copy(board)
            for i in range(9):
                for j in range(9):
                    if board[i][j]==0:
                        find_only_solution(board, i, j)
            find_nines_with_one_solution(board)
            for i in range(9):
                for j in range(9):
                    num=board[i,j]
                    board[i,j]=0
                    if not is_safe(board, i, j, board[i,j]) and board[i,j]!=0:
                        board[i,j]=num
                        return False
                    board[i,j]=num
            if sum(sum(board2==board))==81:
                if do_solve==True:
                    solve(board,0,0)
                return False
        return True
    except ValueError:
        return False

    

if __name__ == '__main__':
    app = App()
    app.mainloop()
    # board = np.zeros([9, 9])
    #     # fill diagonal matrices
    # for i in [3, 6, 9]:
    #     tab = np.arange(1, 10)
    #     np.random.shuffle(tab)
    #     board[i - 3:i, i - 3:i] = tab.reshape(3, 3)
    # solve(board,0,0)
    # delete_nums(board, 60)
    # print(sum(sum(board==0)))
    # print(board)
    # board=np.array([[0, 0, 4, 1, 0, 3, 0, 0, 0],
    #                 [0, 0, 0, 2, 6, 0, 0, 1, 0],
    #                 [1, 0, 0, 0, 8, 9, 2, 4, 0],
    #                 [0, 6, 0, 0, 0, 0, 0, 0, 0],
    #                 [8, 0, 0, 0, 0, 0, 4, 3, 0],
    #                 [4, 0, 0, 8, 0, 0, 6, 0, 0],
    #                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #                 [6, 0, 0, 3, 0, 2, 0, 0, 0],
    #                 [0, 0, 0, 0, 0, 0, 0, 0, 0]])
    # new_solver(board)
    # print(board)