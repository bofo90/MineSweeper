from tkinter import Tk

import numpy as np

from screens.game_screen import GameScreen

TIME_CLICK = 700


class Player:
    def __init__(self, root: Tk):
        self.root = root
        self.made_move = None

    def play_in_window(self, game_window: GameScreen):
        print("start playing")

        self.game_window = game_window
        self.size_x = game_window.x_cells
        self.size_y = game_window.y_cells

        self.made_move = self.root.after(TIME_CLICK, self.first_click)

    def stop_play_in_window(self):
        if self.made_move is not None:
            self.root.after_cancel(self.made_move)
        self.made_move = None

    def first_click(self):
        first_x = np.random.randint(0, self.size_x)
        first_y = np.random.randint(0, self.size_y)
        self.game_window.left_click(first_x, first_y)

        self.made_move = self.root.after(TIME_CLICK, self.next_click)

    def next_click(self):
        if self.game_window.game_finished:
            return

        x, y = self.choose_next_move()
        self.game_window.left_click(x, y)

        self.made_move = self.root.after(TIME_CLICK, self.next_click)

    @staticmethod
    def choose_next_move(self):
        raise NotImplementedError("A way to play needs to be implemented.")
