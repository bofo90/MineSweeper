from datetime import datetime
from enum import Enum

import numpy as np


class GameStatus(Enum):
    WAITING = "waiting"
    PLAYING = "playing"
    LOST = "lost"
    WON = "won"


class FieldCreator:

    def __init__(self, x_size, y_size, num_mines, x_init, y_init):

        self.x_size = x_size
        self.y_size = y_size
        self.num_mines = num_mines
        self.x_init = x_init
        self.y_init = y_init

        self.positions = np.arange(self.x_size * self.y_size).reshape((self.x_size, self.y_size))
        self.removeInitalClick()
        self.availablePos = np.unique(self.positions)[1:]

        mines = np.random.choice(self.availablePos, size=self.num_mines, replace=False)

        self.field = np.zeros((self.x_size * self.y_size))
        self.field[mines] = 1
        self.field = self.field.reshape((self.x_size, self.y_size))

        self.createClues()

    def createClues(self):

        self.clues = np.zeros((self.x_size, self.y_size)).astype(int)
        ext_field = np.zeros((self.x_size + 2, self.y_size + 2))
        ext_field[1:-1, 1:-1] = self.field

        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                rolled = np.roll(ext_field, i, axis=0)
                rolled = np.roll(rolled, j, axis=1)

                self.clues = self.clues + rolled[1:-1, 1:-1]

        self.clues[self.field == 1] = -1
        self.clues = self.clues.astype(int)

    def removeInitalClick(self):
        """Sets the innitial cell and all adjacent as empty"""

        # If too many mines, just make the first click free
        if self.num_mines > (self.x_size * self.y_size - 9):
            self.positions[self.x_init, self.y_init] = -1
            return

        # Otherwise make all neighbouring cells free
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if (
                    self.x_init + i >= 0
                    and self.x_init + i < self.x_size
                    and self.y_init + j >= 0
                    and self.y_init + j < self.y_size
                ):
                    self.positions[self.x_init + i, self.y_init + j] = -1

    def get_all_clues(self):
        return self.clues

    def get_all_mines(self):
        return self.field


class FieldInteraction:

    def __init__(self, x_size, y_size, num_mines):

        self.x_size = x_size
        self.y_size = y_size
        self.num_mines = num_mines

        self.hidden = np.ones((self.x_size, self.y_size))
        self.flag = np.zeros((self.x_size, self.y_size))

        self.clues = None
        self.mine_field = np.zeros((self.x_size, self.y_size))
        self.game_status = GameStatus.WAITING
        self.left_click_turns = []
        self.right_click_turns = []

    def discover_cell(self, x, y):

        if self.game_status in [GameStatus.WON, GameStatus.LOST]:
            return

        # If button is not active do not do anything
        if self.hidden[x, y] == 0 or self.flag[x, y] == 1:
            return

        if self.clues is None:
            field_creator = FieldCreator(self.x_size, self.y_size, self.num_mines, x, y)

            self.clues = field_creator.get_all_clues()
            self.mine_field = field_creator.get_all_mines()

            self.game_status = GameStatus.PLAYING
            self.start_time = datetime.now()

        match self.clues[x, y]:
            case -1:
                self.time_played = self.get_time_played()
                mines, flags = self.show_mines_lost()
                self.left_click_turns.append(mines)
                self.right_click_turns.append(flags)
                self.game_status = GameStatus.LOST
            case 0:
                empties = self.clear_around(x, y, [])
                self.left_click_turns.append(empties)
                self.check_win()
            case _:
                self.hidden[x, y] = 0
                self.left_click_turns.append([(x, y, self.clues[x, y])])
                self.check_win()

    def update_flag(self, x, y):

        if self.game_status is not GameStatus.PLAYING:
            return

        if self.hidden[x, y] == 0:
            return

        if self.flag[x, y] == 0:
            self.flag[x, y] = 1
            self.right_click_turns.append([(x, y, 1)])
        else:
            self.flag[x, y] = 0
            self.right_click_turns.append([(x, y, 0)])

    def show_mines_lost(self):
        mines_to_show = []
        flags_to_remove = []
        for i in range(self.x_size):
            for j in range(self.y_size):
                if self.clues[i, j] == -1 and self.flag[i, j] == 0:
                    mines_to_show.append((i, j, -1))
                    self.hidden[i, j] = 0
                if self.clues[i, j] >= 0 and self.flag[i, j] == 1:
                    flags_to_remove.append((i, j, 0))
                    self.flag[i, j] = 0

        return mines_to_show, flags_to_remove

    def show_mines_win(self):
        flags_to_add = []
        for i in range(self.x_size):
            for j in range(self.y_size):
                if self.clues[i, j] == -1 and self.flag[i, j] == 0:
                    flags_to_add.append((i, j, -1))
                    self.flag[i, j] = 1

        return flags_to_add

    def check_within_board(self, x, y) -> bool:
        return (x >= 0) and (x < self.x_size) and (y >= 0) and (y < self.y_size)

    def clear_around(self, x, y, turns):

        self.hidden[x, y] = 0
        turns.append((x, y, self.clues[x, y]))

        if self.clues[x, y] == 0:
            for i in [-1, 0, 1]:
                for j in [-1, 0, 1]:
                    if self.check_within_board(x + i, y + j) and self.hidden[x + i, y + j] == 1:
                        turns = self.clear_around(x + i, y + j, turns)

        return turns

    def check_win(self):
        if (self.hidden == self.mine_field).all():
            self.game_status = GameStatus.WON
            self.time_played = self.get_time_played()
            flag_mines = self.show_mines_win()
            self.right_click_turns.append(flag_mines)

    def get_last_left_click_turn(self):
        if len(self.left_click_turns) == 0:
            return []
        else:
            return self.left_click_turns[-1]

    def get_last_right_click_turn(self):
        if len(self.right_click_turns) == 0:
            return []
        else:
            return self.right_click_turns[-1]

    def get_time_played(self):
        diff = datetime.now() - self.start_time
        return diff.seconds

    def get_time(self) -> str:

        if self.game_status is GameStatus.PLAYING:
            diff_sec = self.get_time_played()
            minutes, seconds = divmod(diff_sec, 60)
            return f"{minutes:02d}:{seconds:02d}"
        elif self.game_status is GameStatus.WAITING:
            return "00:00"
        else:
            minutes, seconds = divmod(self.time_played, 60)
            return f"{minutes:02d}:{seconds:02d}"

    def get_total_flags(self) -> int:
        return np.sum(self.flag).astype(int)
