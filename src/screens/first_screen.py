import tkinter as tk
from tkinter import messagebox

import numpy as np

from players.random_player import RandomPlayer

from .game_screen import GameScreen

MAX_SIZE_BOARD = 30


class FirstScreen:

    def __init__(self, window):

        self.window = window
        self.window.title("MineSweeper")
        self.window.config(pady=10, padx=10)

        label_welcome = tk.Label(window, text="Welcome to Minesweeper.\nPlease select the difficulty level:")
        label_welcome.pack(anchor=tk.NW, pady=10, padx=10)

        # Variable to hold on to which radio button value is checked.
        self.radio_state = tk.IntVar()
        radiobutton1 = tk.Radiobutton(text="Beginner (9x9)", value=1, variable=self.radio_state)
        radiobutton2 = tk.Radiobutton(text="Intermediate (16x16)", value=2, variable=self.radio_state)
        radiobutton3 = tk.Radiobutton(text="Expert (30x15)", value=3, variable=self.radio_state)
        radiobutton4 = tk.Radiobutton(text="Custom", value=4, variable=self.radio_state)
        radiobutton1.pack(anchor=tk.W, pady=5)
        radiobutton2.pack(anchor=tk.W, pady=5)
        radiobutton3.pack(anchor=tk.W, pady=5)
        radiobutton4.pack(anchor=tk.W, pady=5)

        label_autoplayer = tk.Label(window, text="Do you want to have an autoplayer?")
        label_autoplayer.pack(anchor=tk.W, pady=10, padx=10)

        self.checkbutton_value = tk.BooleanVar()
        checkbutton = tk.Checkbutton(text="Autoplayer", variable=self.checkbutton_value)
        checkbutton.pack(anchor=tk.W, pady=5)

        # calls action() when pressed
        self.button = tk.Button(text="Accept", command=self.action)
        self.button.pack(anchor=tk.S, pady=5)

    def action(self):

        diff = self.radio_state.get()

        if diff == 4:
            self.button.config(state=tk.DISABLED)

            self.window_custom = tk.Toplevel()
            self.window_custom.title("Custom size")
            self.window_custom.config(pady=10, padx=10)

            lbl_top = tk.Label(
                self.window_custom,
                text="Please select the size and percentage of mines in the board:",
            )
            lbl_top.grid(column=0, columnspan=2, row=0, pady=5)

            lbl_x = tk.Label(self.window_custom, text=f"Width (4-{MAX_SIZE_BOARD})")
            lbl_x.grid(column=0, row=1, sticky=tk.W)
            lbl_y = tk.Label(self.window_custom, text=f"Length (4-{MAX_SIZE_BOARD})")
            lbl_y.grid(column=0, row=2, sticky=tk.W)
            lbl_m = tk.Label(self.window_custom, text="Mines (%)")
            lbl_m.grid(column=0, row=3, sticky=tk.W)

            vcmd = (self.window_custom.register(self.validate), "%P")

            self.etr_x = tk.Spinbox(self.window_custom, from_=4, to=30, validate="key", validatecommand=vcmd)
            self.etr_x.grid(column=1, row=1, sticky=tk.EW, pady=3)
            self.etr_y = tk.Spinbox(self.window_custom, from_=4, to=30, validate="key", validatecommand=vcmd)
            self.etr_y.grid(column=1, row=2, sticky=tk.EW, pady=3)
            self.etr_m = tk.Spinbox(self.window_custom, from_=1, to=99, validate="key", validatecommand=vcmd)
            self.etr_m.grid(column=1, row=3, sticky=tk.EW, pady=3)

            bt_acc = tk.Button(self.window_custom, text="Accept", command=self.nextWind)
            bt_acc.grid(column=0, row=4)

            bt_can = tk.Button(self.window_custom, text="Cancel", command=self.returnWind)
            bt_can.grid(column=1, row=4)

        elif diff != 0:
            if diff == 1:
                self.game = GameScreen(self.window, 9, 9, 10)
            if diff == 2:
                self.game = GameScreen(self.window, 16, 16, 40)
            if diff == 3:
                self.game = GameScreen(self.window, 30, 15, 99)

            if self.checkbutton_value.get():
                RandomPlayer(self.game, self.window)

        else:
            messagebox.showerror("Error", "Please select a difficulty.")
        return

    def nextWind(self):

        x, y, mp = (int(self.etr_x.get()), int(self.etr_y.get()), int(self.etr_m.get()))

        if x not in range(4, MAX_SIZE_BOARD + 1) or y not in range(4, MAX_SIZE_BOARD + 1) or mp not in range(1, 100):
            messagebox.showerror(
                "Error",
                f"The width and length of the board should me minimum 4 and maximum {MAX_SIZE_BOARD}."
                + "\nThe percentage of mines goes from 1 to 99.",
            )
        else:
            m = int(np.floor(mp / 100 * x * y))
            if m < 1:
                m = 1
            if m == (x * y):
                m = int(x * y - 1)

            self.window_custom.destroy()
            self.game = GameScreen(self.window, x, y, m)

    def returnWind(self):

        self.button.config(state=tk.ACTIVE)

        self.window_custom.destroy()

    def validate(self, P):

        if P != "":
            try:
                int(P)
            except ValueError:
                return False
        return True
