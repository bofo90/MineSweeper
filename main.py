import layout
import tkinter as tk
import player



window = tk.Tk()

minesweeper = layout.FirstScreen(window)

playerEasy = player.Player(window, minesweeper)

window.mainloop()

