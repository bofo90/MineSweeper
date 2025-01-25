from abc import ABC, abstractmethod
from tkinter import Tk

import numpy as np

from game_logic.field import GameStatus
from screens.game_screen import GameScreen

TIME_CLICK = 700


class Player(ABC):
    def __init__(self, root: Tk):
        self.root = root
        self.made_move = None
        self.game_finished = False

    def play_in_window(self, game_window: GameScreen):

        self.game_window = game_window
        self.field_interactor = game_window.field_interactor
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
        if self.field_interactor.game_status is not GameStatus.PLAYING:
            return

        x, y = self.choose_next_move()
        self.game_window.left_click(x, y)

        self.made_move = self.root.after(TIME_CLICK, self.next_click)

    @abstractmethod
    def choose_next_move(self):
        pass
