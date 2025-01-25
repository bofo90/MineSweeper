import tkinter as tk

import numpy as np
from PIL import Image, ImageTk

from game_logic.field import FieldInteraction, GameStatus


class GameScreen:

    def __init__(self, main_window, x_cells, y_cells, tot_mines, player=None):

        self.first_click = True
        self.game_finished = False
        self.player = player
        self.update_time = None

        self.main_window = main_window
        self.main_window.withdraw()

        self.window = tk.Toplevel()
        self.window.title("MineSweeper")
        self.window.protocol("WM_DELETE_WINDOW", self.close_all_windows)
        self.window.config(pady=10, padx=10)

        self.getImages()

        self.x_cells, self.y_cells, self.tot_mines = (x_cells, y_cells, tot_mines)
        self.field_interactor = FieldInteraction(self.x_cells, self.y_cells, self.tot_mines)

        frame_but = tk.Frame(self.window, width=self.x_cells * 27, height=self.y_cells * 27)  # their units in pixels
        frame_but.grid_propagate(False)
        frame_but.grid(column=0, row=0, rowspan=2)
        self.buts = np.full([self.x_cells, self.y_cells], None)
        # self.active_but = np.ones((self.x_cells, self.y_cells))
        # self.flag_but = np.zeros((self.x_cells, self.y_cells))
        for i in range(self.x_cells):
            frame_but.columnconfigure(i, weight=1)
            for j in range(self.y_cells):
                frame_but.rowconfigure(j, weight=1)

                self.buts[i, j] = tk.Label(frame_but, image=self.images["plain"])
                self.buts[i, j].grid(column=i, row=j, sticky=tk.NSEW, padx=1, pady=1)

                if self.player is None:
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

        self.restart_but = tk.Button(frame_ex, text="Restart", command=self.restart_game)
        self.restart_but.pack(anchor=tk.W)

        exit_but = tk.Button(frame_ex, text="Go back", command=self.return_to_main_window)
        exit_but.pack(anchor=tk.W)

        if self.player is not None:
            self.player.play_in_window(self)

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

    def restart_game(self):

        if self.player is not None:
            self.player.stop_play_in_window()

        self.field_interactor = FieldInteraction(self.x_cells, self.y_cells, self.tot_mines)
        self.restart_but.config(text="Restart")
        self.update_count_mines()
        self.reset_board()
        self.reset_timer()

        if self.player is not None:
            self.player.play_in_window(self)

    def return_to_main_window(self):

        if self.player is not None:
            self.player.stop_play_in_window()
        self.reset_timer()
        self.window.destroy()
        self.main_window.deiconify()

    def close_all_windows(self):

        if self.player is not None:
            self.player.stop_play_in_window()

        self.reset_timer()
        self.window.destroy()
        self.main_window.destroy()

    def left_click_wrapper(self, i, j):
        return lambda Button: self.left_click(i, j)

    def right_click_wrapper(self, i, j):
        return lambda Button: self.right_click(i, j)

    def left_click(self, x, y):

        if self.update_time is None:
            self.set_timer()

        self.field_interactor.discover_cell(x, y)

        if self.field_interactor.game_status in [GameStatus.LOST, GameStatus.WON]:

            if self.player is not None:
                self.player.stop_play_in_window()

            self.main_window.after_cancel(self.update_time)

            if self.field_interactor.game_status is GameStatus.WON:
                self.restart_but.config(text="YOU WON!")
            else:
                self.restart_but.config(text="You lost!")
                self.update_right_click_board()

        self.update_left_click_board()

    def right_click(self, x, y):

        self.field_interactor.update_flag(x, y)

        self.update_right_click_board()
        self.update_count_mines()

    def update_left_click_board(self):
        last_turn = self.field_interactor.get_last_left_click_turn()
        for x, y, clue in last_turn:
            self.buts[x, y].config(image=self.images["numbers"][clue + 1])

    def update_right_click_board(self):
        last_flagged = self.field_interactor.get_last_right_click_turn()

        for x, y, flagged in last_flagged:
            if flagged:
                self.buts[x, y].config(image=self.images["flag"])
            else:
                self.buts[x, y].config(image=self.images["plain"])

    def update_count_mines(self):
        tot_flags = self.field_interactor.get_total_flags()
        self.label_mines.config(text=f"{tot_flags}/{self.tot_mines} mines")

    def reset_board(self):
        for i in np.arange(self.x_cells):
            for j in np.arange(self.y_cells):
                self.buts[i, j].config(image=self.images["plain"])

    def set_timer(self):
        clock_time = self.field_interactor.get_time()
        self.label_time.config(text=clock_time)
        self.update_time = self.main_window.after(1000, self.set_timer)

    def reset_timer(self):
        if self.update_time is not None:
            self.main_window.after_cancel(self.update_time)
        self.label_time.config(text="00:00")
        self.update_time = None
