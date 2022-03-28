import field
import scoredata
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from PIL import ImageTk, Image
import numpy as np
from datetime import datetime

class FirstScreen():
    
    def __init__(self, window):
        
        self.window = window
        self.window.title("MineSweeper")
        self.window.config(pady = 10, padx=10)
        self.window.protocol("WM_DELETE_WINDOW", self.close_window)

        self.scores = scoredata.Scores_Admin()
        self.user = None

        label_welcome = tk.Label(window, text="Welcome to Minesweeper.\nPlease select the difficulty level:")
        label_welcome.pack(anchor = tk.NW, pady = 10, padx = 10)

        #Variable to hold on to which radio button value is checked.
        self.radio_state = tk.IntVar()
        radiobutton1 = tk.Radiobutton(text="Beginner (9x9)", value=1, variable=self.radio_state)
        radiobutton2 = tk.Radiobutton(text="Intermediate (16x16)", value=2, variable=self.radio_state)
        radiobutton3 = tk.Radiobutton(text="Expert (30x15)", value=3, variable=self.radio_state)
        radiobutton4 = tk.Radiobutton(text="Custom", value=4, variable=self.radio_state)
        radiobutton1.pack(anchor = tk.W, pady = 5)
        radiobutton2.pack(anchor = tk.W, pady = 5)
        radiobutton3.pack(anchor = tk.W, pady = 5)
        radiobutton4.pack(anchor = tk.W, pady = 5)
        
        #calls action() when pressed
        self.button = tk.Button(text="Accept", command=self.action)
        self.button.pack(anchor = tk.S, pady = 5)

    def getUser(self):
        self.window.withdraw()
        while True:
            self.user = simpledialog.askstring("Input", "What is your name?",parent=self.window)

            if (self.user is None) or (len(self.user) == 0):
                messagebox.showerror( "Error", "Please specify your name.")
            else:
                if not self.scores.check_username(self.user):
                    MsgBox = messagebox.askquestion ('New Username','You want to create this user?')
                    if MsgBox == 'yes':
                        self.scores.add_user(self.user)
                        self.window.deiconify()
                        return
                else:
                    self.window.deiconify()
                    return

        
    def action(self):

        if self.user == None:
            self.getUser()
        
        diff = self.radio_state.get()
        
        if diff == 4:
            self.button.config(state = tk.DISABLED)
            
            self.window_custom = tk.Tk()
            self.window_custom.title('Custom size')
            self.window_custom.config(pady = 10, padx = 10)

            self.window_custom.protocol("WM_DELETE_WINDOW", self.returnWind)
            
            lbl_top = tk.Label(self.window_custom, text = 'Please select the size and percentage of mines in the board:')
            lbl_top.grid(column = 0, columnspan = 2, row = 0, pady = 5)

            lbl_x = tk.Label(self.window_custom, text = 'Width (4-50)')
            lbl_x.grid(column = 0, row = 1, sticky = tk.W)
            lbl_y = tk.Label(self.window_custom, text = 'Length (4-50)')
            lbl_y.grid(column = 0, row = 2, sticky = tk.W)
            lbl_m = tk.Label(self.window_custom, text = 'Mines (%)')
            lbl_m.grid(column = 0, row = 3, sticky = tk.W)
            
            vcmd = (self.window_custom.register(self.validate),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
            
            self.etr_x = tk.Spinbox(self.window_custom, from_=4, to=30, 
                                    validate = 'key', validatecommand = vcmd)
            self.etr_x.grid(column = 1, row = 1, sticky = tk.EW, pady = 3)
            self.etr_y = tk.Spinbox(self.window_custom, from_=4, to=30, 
                                    validate = 'key', validatecommand = vcmd)
            self.etr_y.grid(column = 1, row = 2, sticky = tk.EW, pady = 3)
            self.etr_m = tk.Spinbox(self.window_custom, from_=1, to=99, 
                                    validate = 'key', validatecommand = vcmd)
            self.etr_m.grid(column = 1, row = 3, sticky = tk.EW, pady = 3)    
            
            bt_acc = tk.Button(self.window_custom, text = 'Accept', command = self.nextWind)
            bt_acc.grid(column = 0, row = 4)            
            
            bt_can = tk.Button(self.window_custom, text = 'Cancel', command = self.returnWind)
            bt_can.grid(column = 1, row = 4)            
            
        elif diff != 0:
            self.window.withdraw()
            self.window_game = tk.Toplevel()
            if diff == 1:
                self.game = GameScreen(self.window, self.scores, self.window_game, 9, 9, 10)
            if diff == 2:
                self.game = GameScreen(self.window, self.scores, self.window_game, 16, 16, 40)
            if diff == 3:
                self.game = GameScreen(self.window, self.scores, self.window_game, 30, 15, 99)
            
        else:
            messagebox.showerror( "Error", "Please select a difficulty.")
            
        # print(self.radio_state.get())
        return
    
    def nextWind(self):
        
        x, y, mp = (int(self.etr_x.get()), int(self.etr_y.get()), int(self.etr_m.get()))
        
        if x not in range (4,31) or y not in range (4,31) or mp not in range(1,100):
            messagebox.showerror( "Error", "The width and length of the board should me minimum 4 and maximum 30.\nThe percentage of mines goes from 1 to 99.")
        else:
            self.window.withdraw()
            self.window_custom.destroy()
            self.window_game = tk.Toplevel()
            
            m = int(np.floor(mp/100 *x*y))
            if m < 1:
                m = 1
            if m > x*y-9:
                m = int(x*y-9)
            
            self.game = GameScreen(self.window, self.scores, self.window_game, x, y, m)
            self.button.config(state = tk.ACTIVE)

    
    def returnWind(self):
        
        self.button.config(state = tk.ACTIVE)
        
        self.window_custom.destroy()
        
    def validate(self, d, i, P, s, S, v, V, W):

        if P == '':
            return True
        else:
            try:
                a = int(P)     
                # if a not in range(4, 50):
                #     print ("Out of range")
                #     return False
                return True
            except ValueError:
                return False

    def close_window(self):
        self.window.destroy()
        self.scores.close_connection()
            

class GameScreen():
    
    def __init__(self, root, scores, window, x_cells, y_cells, tot_mines):
        
        self.first_click = True
        
        self.root = root
        self.scores = scores
        self.window = window
        self.window.title("MineSweeper")
        self.window.config(pady = 10, padx=10)

        self.window.protocol("WM_DELETE_WINDOW", self.close_window)
        
        self.getImages()
        
        self.x_cells, self.y_cells,self.tot_mines = (x_cells, y_cells, tot_mines)
        
        frame_but = tk.Frame(self.window, width=self.x_cells*27, height=self.y_cells*27) #their units in pixels
        frame_but.grid_propagate(False)
        frame_but.grid(column = 0, row = 0, rowspan = 2)
        self.buts = np.full([self.x_cells, self.y_cells], None)
        self.active_but = np.ones((self.x_cells, self.y_cells))
        self.flag_but = np.zeros((self.x_cells, self.y_cells))
        for i in np.arange(self.x_cells):
            frame_but.columnconfigure(i, weight=1)
            for j in np.arange(self.y_cells):
                frame_but.rowconfigure(j, weight=1)
                
                self.buts[i,j] = tk.Label(frame_but, image = self.images['plain'])
                self.buts[i,j].grid(column=i, row=j, sticky = tk.NSEW, padx = 1, pady = 1)
                self.buts[i,j].bind("<Button-1>", self.left_click_wrapper(i,j))
                self.buts[i,j].bind("<Button-3>", self.right_click_wrapper(i,j))
                
                # self.buts.append(cell)
        # self.buts = np.reshape(self.buts, (self.x_cells,self.y_cells))
        
        frame_info = tk.Frame(self.window)
        frame_info.grid(column = 1, row = 0, sticky = tk.N)
        #Labels
        self.label_mines = tk.Label(frame_info, text=f"0/{self.tot_mines} mines")
        # label.config(text="This is new text")
        self.label_mines.pack(anchor = tk.W)
        
        self.label_time = tk.Label(frame_info, text="00:00")
        # label.config(text="This is new text")
        self.label_time.pack(anchor = tk.W)
        
        frame_ex = tk.Frame(self.window)
        frame_ex.grid(column = 1, row = 1, sticky = tk.S)
        
        restart = tk.Button(frame_ex, text = 'Reset', command=self.reset_game)
        restart.pack(anchor = tk.W)
        
        change_dif = tk.Button(frame_ex, text = 'Change difficulty', command=self.restart)
        change_dif.pack(anchor = tk.W)
        
        exit_but = tk.Button(frame_ex, text = 'Quit', command= self.quit_game)
        exit_but.pack(anchor = tk.W)
        
    def getImages(self):
        
        image_plain = Image.open("images/facingDown.png")
        image_plain = image_plain.resize((25, 25), Image.ANTIALIAS)
        
        image_flag = Image.open("images/flagged.png")
        image_flag = image_flag.resize((25, 25), Image.ANTIALIAS)
        
        
        self.images = {
            "plain": ImageTk.PhotoImage(image_plain),
            "flag": ImageTk.PhotoImage(image_flag),
            "numbers": []
        }
        for i in np.arange(10):
            image_num = Image.open(f"images/{i-1}.png")
            image_num = image_num.resize((25, 25), Image.ANTIALIAS)
            self.images["numbers"].append(ImageTk.PhotoImage(image_num))
            
        
        
    def reset_game(self):
        self.active_but = np.ones((self.x_cells, self.y_cells))
        self.flag_but = np.zeros((self.x_cells, self.y_cells))
        self.countMines()
        for i in np.arange(self.x_cells):
            for j in np.arange(self.y_cells):
                self.buts[i,j].config(image = self.images['plain'])
        self.reset_timer()
        return
    
    def restart(self):
        self.reset_timer()
        self.window.destroy()
        self.root.deiconify()
        return
    
    def quit_game(self):
        self.reset_timer()
        self.close_window()

    def left_click_wrapper(self,i,j):
        return lambda Button : self.left_click(i,j)
    
    def right_click_wrapper(self,i,j):
        return lambda Button : self.right_click(i,j)

    def left_click(self, x,y):
        # x = pos[0]
        # y = pos[1]
        
        if self.active_but[x,y]:   
            if self.first_click:
                self.first_click = False
                self.time_begin = datetime.now()
                self.timer()
                self.field = field.Field(self.x_cells, self.y_cells, self.tot_mines, x, y)
                
            if self.field.clues[x,y] == -1:
                self.clickBut(x, y)
                self.showMines()
                self.label_time.after_cancel(self.time)
                answer_fail = messagebox.askyesno( "BOOM!", "You exploded! Do you want to start a new game?")
                if answer_fail:
                    self.reset_game()
                else:
                    self.quit_game()
            
            if self.field.clues[x,y] == 0:
                self.clearAround(x,y)
                
            if self.field.clues[x,y] > 0:
                self.clickBut(x, y)
                
            if self.checkWin():
                for i in np.arange(self.x_cells):
                    for j in np.arange(self.y_cells):
                        if self.field.clues[i,j] == -1:
                            self.buts[i,j].config(image = self.images['flag'])
                self.label_time.after_cancel(self.time)
                answer_win = messagebox.askyesno( "Hurray!", "You won! Do you want to start a new game?")
                if answer_win:
                    self.reset_game()
                else:
                    self.quit_game()
                
    def clearAround(self, x, y):
        if self.field.clues[x,y] >= 0:
            self.clickBut(x, y)
        if self.field.clues[x,y] == 0:
            for i in [-1,0,1]:
                for j in [-1,0,1]:
                    if (x+i >= 0 and x+i < self.x_cells and 
                    y+j >=0 and y+j < self.y_cells):
                        if self.active_but[x+i,y+j]:
                            self.clearAround(x+i, y+j)
                            
    def showMines(self):
        for i in np.arange(self.x_cells):
            for j in np.arange(self.y_cells):
                if self.field.clues[i,j] == -1:
                    self.clickBut(i,j)
                    
    def clickBut(self, x, y):
        self.active_but[x,y] = 0
        self.buts[x,y].config(image = self.images['numbers'][self.field.clues[x,y]+1])
        
    def right_click(self, x,y):
        # x = pos[0]
        # y = pos[1]
        if self.active_but[x,y]:
            self.active_but[x,y] = 0
            self.flag_but[x,y] = 1
            self.buts[x,y].config(image = self.images['flag'])
        
        elif self.flag_but[x,y]:
            self.active_but[x,y] = 1
            self.flag_but[x,y] = 0
            self.buts[x,y].config(image = self.images['plain'])     
        
        self.countMines()
        
    def countMines(self):
        tot_flags = np.sum(self.flag_but).astype(int)
        self.label_mines.config(text=f"{tot_flags}/{self.tot_mines} mines")
        
        
    def timer(self):
        time_now = datetime.now()
        diff = time_now-self.time_begin
        minutes, seconds = divmod(diff.seconds, 60)
        string = f"{minutes:02d}:{seconds:02d}"
        self.label_time.config(text = string)
        self.time = self.label_time.after(1000, self.timer)
        
    def reset_timer(self):
        if hasattr(self, 'time'):
            self.label_time.after_cancel(self.time)
        self.label_time.config(text = "00:00")
        self.first_click = True
            
    def checkWin(self):
        left_but = self.active_but + self.flag_but
        
        if (left_but == self.field.field).all():
            return True
        else:
            return False

    def close_window(self):
        self.root.destroy()
        self.scores.close_connection()
