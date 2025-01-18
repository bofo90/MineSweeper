import tkinter as tk
from datetime import datetime
from tkinter import messagebox

import numpy as np
from PIL import Image, ImageTk

from game_logic.field import Field


class GameScreen:

    def __init__(self, main_window, x_cells, y_cells, tot_mines):

        self.first_click = True
        self.lost_game = False

        self.main_window = main_window
        self.main_window.withdraw()

        self.window = tk.Toplevel()
        self.window.title("MineSweeper")
        self.window.config(pady=10, padx=10)

        self.getImages()

        self.x_cells, self.y_cells, self.tot_mines = (x_cells, y_cells, tot_mines)

        frame_but = tk.Frame(self.window, width=self.x_cells * 27, height=self.y_cells * 27)  # their units in pixels
        frame_but.grid_propagate(False)
        frame_but.grid(column=0, row=0, rowspan=2)
        self.buts = np.full([self.x_cells, self.y_cells], None)
        self.active_but = np.ones((self.x_cells, self.y_cells))
        self.flag_but = np.zeros((self.x_cells, self.y_cells))
        for i in np.arange(self.x_cells):
            frame_but.columnconfigure(i, weight=1)
            for j in np.arange(self.y_cells):
                frame_but.rowconfigure(j, weight=1)

                self.buts[i, j] = tk.Label(frame_but, image=self.images["plain"])
                self.buts[i, j].grid(column=i, row=j, sticky=tk.NSEW, padx=1, pady=1)
                self.buts[i, j].bind("<Button-1>", self.left_click_wrapper(i, j))
                self.buts[i, j].bind("<Button-3>", self.right_click_wrapper(i, j))

        frame_info = tk.Frame(self.window)
        frame_info.grid(column=1, row=0, sticky=tk.N)
        # Labels
        self.label_mines = tk.Label(frame_info, text=f"0/{self.tot_mines} mines")
        self.label_mines.pack(anchor=tk.W)

        self.label_time = tk.Label(frame_info, text="00:00")
        self.label_time.pack(anchor=tk.W)

        frame_ex = tk.Frame(self.window)
        frame_ex.grid(column=1, row=1, sticky=tk.S)

        self.restart_but = tk.Button(frame_ex, text="Reset", command=self.reset_game)
        self.restart_but.pack(anchor=tk.W)

        self.change_dif = tk.Button(frame_ex, text="Change difficulty", command=self.restart)
        self.change_dif.pack(anchor=tk.W)

        exit_but = tk.Button(frame_ex, text="Quit", command=self.quit_game)
        exit_but.pack(anchor=tk.W)

    def getImages(self):

        image_plain = Image.open("images/facingDown.png")
        image_plain = image_plain.resize((25, 25), Image.LANCZOS)

        image_flag = Image.open("images/flagged.png")
        image_flag = image_flag.resize((25, 25), Image.LANCZOS)

        self.images = {
            "plain": ImageTk.PhotoImage(image_plain),
            "flag": ImageTk.PhotoImage(image_flag),
            "numbers": [],
        }
        for i in np.arange(10):
            image_num = Image.open(f"images/{i-1}.png")
            image_num = image_num.resize((25, 25), Image.LANCZOS)
            self.images["numbers"].append(ImageTk.PhotoImage(image_num))

    def reset_game(self):
        self.active_but = np.ones((self.x_cells, self.y_cells))
        self.flag_but = np.zeros((self.x_cells, self.y_cells))
        self.countMines()
        for i in np.arange(self.x_cells):
            for j in np.arange(self.y_cells):
                self.buts[i, j].config(image=self.images["plain"])
        self.reset_timer()
        return

    def restart(self):
        self.reset_timer()
        self.window.destroy()
        self.main_window.deiconify()
        return

    def quit_game(self):
        self.reset_timer()
        self.window.destroy()
        self.main_window.destroy()

    def left_click_wrapper(self, i, j):
        return lambda Button: self.left_click(i, j)

    def right_click_wrapper(self, i, j):
        return lambda Button: self.right_click(i, j)

    def left_click(self, x, y):

        if self.active_but[x, y]:
            if self.first_click:
                self.first_click = False
                self.time_begin = datetime.now()
                self.timer()
                self.field = Field(self.x_cells, self.y_cells, self.tot_mines, x, y)

            if self.field.clues[x, y] == -1:
                self.clickBut(x, y)
                self.showMines()
                self.label_time.after_cancel(self.time)
                answer_fail = messagebox.askyesno("BOOM!", "You exploded! Do you want to start a new game?")
                if answer_fail:
                    self.reset_game()
                else:
                    self.quit_game()

            if self.field.clues[x, y] == 0:
                self.clearAround(x, y)

            if self.field.clues[x, y] > 0:
                self.clickBut(x, y)

            if self.checkWin():
                for i in np.arange(self.x_cells):
                    for j in np.arange(self.y_cells):
                        if self.field.clues[i, j] == -1:
                            self.buts[i, j].config(image=self.images["flag"])
                self.label_time.after_cancel(self.time)
                answer_win = messagebox.askyesno("Hurray!", "You won! Do you want to start a new game?")
                if answer_win:
                    self.reset_game()
                else:
                    self.quit_game()

    def clearAround(self, x, y):
        if self.field.clues[x, y] >= 0:
            self.clickBut(x, y)
        if self.field.clues[x, y] == 0:
            for i in [-1, 0, 1]:
                for j in [-1, 0, 1]:
                    if x + i >= 0 and x + i < self.x_cells and y + j >= 0 and y + j < self.y_cells:
                        if self.active_but[x + i, y + j]:
                            self.clearAround(x + i, y + j)

    def showMines(self):

        self.lost_game = True

        for i in np.arange(self.x_cells):
            for j in np.arange(self.y_cells):
                if self.field.clues[i, j] == -1:
                    self.clickBut(i, j)

    def clickBut(self, x, y):
        self.active_but[x, y] = 0
        self.buts[x, y].config(image=self.images["numbers"][self.field.clues[x, y] + 1])

    def right_click(self, x, y):

        if self.active_but[x, y]:
            self.active_but[x, y] = 0
            self.flag_but[x, y] = 1
            self.buts[x, y].config(image=self.images["flag"])

        elif self.flag_but[x, y]:
            self.active_but[x, y] = 1
            self.flag_but[x, y] = 0
            self.buts[x, y].config(image=self.images["plain"])

        self.countMines()

    def countMines(self):
        tot_flags = np.sum(self.flag_but).astype(int)
        self.label_mines.config(text=f"{tot_flags}/{self.tot_mines} mines")

    def timer(self):
        time_now = datetime.now()
        diff = time_now - self.time_begin
        minutes, seconds = divmod(diff.seconds, 60)
        string = f"{minutes:02d}:{seconds:02d}"
        self.label_time.config(text=string)
        self.time = self.label_time.after(1000, self.timer)

    def reset_timer(self):
        if hasattr(self, "time"):
            self.label_time.after_cancel(self.time)
        self.label_time.config(text="00:00")
        self.first_click = True

    def checkWin(self):
        left_but = self.active_but + self.flag_but

        if (left_but == self.field.field).all():
            return True
        else:
            return False
