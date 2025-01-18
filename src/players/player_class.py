from tkinter import Tk

import numpy as np

from screens.game_screen import GameScreen

TIME_CLICK = 700


class Player:
    def __init__(self, game_window: GameScreen, root: Tk):

        self.game_window = game_window
        self.size_x = game_window.x_cells
        self.size_y = game_window.y_cells

        self.game_window.restart_but["state"] = "disabled"
        self.game_window.change_dif["state"] = "disabled"
        # This makes that you cannot change the game automatic play anymore

        self.root = root
        self.root.after(TIME_CLICK, self.first_click)

    def first_click(self):
        first_x = np.random.randint(0, self.size_x)
        first_y = np.random.randint(0, self.size_y)
        self.game_window.left_click(first_x, first_y)

        self.root.after(TIME_CLICK, self.next_click)

    def next_click(self):

        if self.game_window.lost_game:
            pass

        x, y = self.choose_next_move()
        self.game_window.left_click(x, y)

        self.root.after(TIME_CLICK, self.next_click)

    @staticmethod
    def choose_next_move(self):
        raise NotImplementedError("A way to play needs to be implemented.")
