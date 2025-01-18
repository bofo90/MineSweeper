import numpy as np


class Field:

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
