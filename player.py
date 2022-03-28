import numpy as np

class Player():

    def __init__(self, root, first_screen):
        self.root = root
        self.first_screen = first_screen
        root.after(20, self.select_difficulty)
        root.after(20, self.first_move)
        root.after(20, self.best_play)

    def select_difficulty(self):
        self.first_screen.radio_state.set(1)
        self.first_screen.action()
        self.game = self.first_screen.game

    def first_move(self):
        x_first = np.random.randint(self.first_screen.game.x_cells)
        y_first = np.random.randint(self.first_screen.game.x_cells)
        self.game.left_click(x_first,y_first)

    def best_play(self):
        self.clues = self.game.field.clues
        print(self.clues.T)
