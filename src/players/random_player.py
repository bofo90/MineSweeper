import numpy as np

from .player_class import Player


class RandomPlayer(Player):

    def choose_next_move(self):

        x_pos_active, y_pos_acttive = np.where(self.game_window.active_but == 1)
        next_pos = np.random.randint(0, len(x_pos_active))

        return x_pos_active[next_pos], y_pos_acttive[next_pos]
