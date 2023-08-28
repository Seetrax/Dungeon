from tkinter import *

class Grid_Label():
    def __init__(self,world, master, i, j):
        self.text = StringVar()
        if (j,i) in world.wall_pos:
            self.label = Label(master, textvariable = self.text, height = 1, width = 4, relief = RIDGE, bg = "gray30", fg = "white", font = "Helvetica 14 bold")
        else:
            self.label = Label(master, textvariable = self.text, height = 1, width = 4, relief = RIDGE, bg = "black", fg = "white", font = "Helvetica 14 bold")
        self.label.grid(row = i, column = j, sticky = W, pady = 1)
        self.row = i
        self.col = j
    def change_text(self, updated_text):
        self.text.set(str(updated_text))
