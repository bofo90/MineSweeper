from turtle import update
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
            name = simpledialog.askstring("Input", "What is your name?",parent=self.window)

            if (name is None) or (len(name) == 0):
                messagebox.showerror( "Error", "Please specify your name.")
            else:
                self.scores.check_username(name)
                if self.scores.user_id == 0:
                    MsgBox = messagebox.askquestion ('New Username','You want to create this user?')
                    if MsgBox == 'yes':
                        self.scores.add_user(name)
                        self.window.deiconify()
                        return
                else:
                    self.window.deiconify()
                    return
   
    def action(self):

        if self.scores.user_id == 0:
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
            if diff == 1:
                self.game = GameScreen(self.window, self.scores, 9, 9, 10)
            if diff == 2:
                self.game = GameScreen(self.window, self.scores, 16, 16, 40)
            if diff == 3:
                self.game = GameScreen(self.window, self.scores, 30, 15, 99)
            
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
            
            m = int(np.floor(mp/100 *x*y))
            if m < 1:
                m = 1
            if m > x*y-9:
                m = int(x*y-9)
            
            self.game = GameScreen(self.window, self.scores, x, y, m)
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
    
    def __init__(self, root, scores, x_cells, y_cells, tot_mines):        
        self.root = root
        self.scores = scores
        self.window = tk.Toplevel()
        self.window.title("MineSweeper")
        self.window.config(pady = 10, padx=10)

        self.window.protocol("WM_DELETE_WINDOW", self.close_window)
        
        self.getImages()
        
        self.x_cells, self.y_cells, self.tot_mines = (x_cells, y_cells, tot_mines)
        self.field = field.Field(self.x_cells, self.y_cells, self.tot_mines)
        
        frame_but = tk.Frame(self.window, width=self.x_cells*27, height=self.y_cells*27) #their units in pixels
        frame_but.grid_propagate(False)
        frame_but.grid(column = 0, row = 0, rowspan = 2)
        self.buts = np.full([self.x_cells, self.y_cells], None)
        for i in np.arange(self.x_cells):
            frame_but.columnconfigure(i, weight=1)
            for j in np.arange(self.y_cells):
                frame_but.rowconfigure(j, weight=1)
                self.buts[i,j] = tk.Label(frame_but, image = self.images['plain'])
                self.buts[i,j].grid(column=i, row=j, sticky = tk.NSEW, padx = 1, pady = 1)
                self.buts[i,j].bind("<Button-1>", self.left_click_wrapper(i,j))
                self.buts[i,j].bind("<Button-3>", self.right_click_wrapper(i,j))
        
        frame_info = tk.Frame(self.window)
        frame_info.grid(column = 1, row = 0, sticky = tk.N)
        #Labels
        self.label_mines = tk.Label(frame_info, text=f"0/{self.tot_mines} mines")
        self.label_mines.pack(anchor = tk.W)
        
        self.label_time = tk.Label(frame_info, text="00:00")
        self.label_time.pack(anchor = tk.W)
        
        frame_ex = tk.Frame(self.window)
        frame_ex.grid(column = 1, row = 1, sticky = tk.S)
        
        restart = tk.Button(frame_ex, text = 'Reset', command=self.reset_game)
        restart.pack(anchor = tk.E)
        
        change_dif = tk.Button(frame_ex, text = 'Change size', command=self.restart)
        change_dif.pack(anchor = tk.E)
        
        exit_but = tk.Button(frame_ex, text = 'Quit', command= self.quit_game)
        exit_but.pack(anchor = tk.E)
        
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

    def left_click_wrapper(self,i,j):
        return lambda Button : self.left_click(i,j)
    
    def right_click_wrapper(self,i,j):
        return lambda Button : self.right_click(i,j)

    def left_click(self, x,y):  
        status = self.field.click(x, y)
        self.update_field()
        if status == -2: # means that it is first click in this game
            self.timer()
        if status >= 0: # game is over, status 1 is won, statu 0 is lost
            self.show_scores(status)
                            
    def update_field(self):
        for i in np.arange(self.x_cells):
            for j in np.arange(self.y_cells):
                if self.field.display_clues[i,j] == -3:
                    self.buts[i,j].config(image = self.images['flag'])
                elif self.field.display_clues[i,j] == -2:
                    self.buts[i,j].config(image = self.images['plain']) 
                else:
                    self.buts[i,j].config(image = self.images['numbers'][self.field.display_clues[i,j]+1])  
        
    def right_click(self, x,y):
        self.field.click_flag(x,y)
        self.update_field()
        self.countMines()
        
    def countMines(self):
        tot_flags = int(np.sum(self.field.display_clues == -3))
        self.label_mines.config(text=f"{tot_flags}/{self.tot_mines} mines")
        
    def timer(self):
        diff = int(self.field.get_timediff())
        minutes, seconds = divmod(diff, 60)
        string = f"{minutes:02d}:{seconds:02d}"
        self.label_time.config(text = string)
        self.time = self.label_time.after(1000, self.timer)
        
    def reset_timer(self):
        if hasattr(self, 'time'):
            self.label_time.after_cancel(self.time)
        self.label_time.config(text = "00:00")
        self.first_click = True

    def close_window(self):
        self.root.destroy()
        self.scores.close_connection()

    def save_score(self, win):
        time_seconds = self.field.get_timediff()
        but_cleared = self.field.get_cleared_buts()
        self.scores.save_game(self.x_cells, self.y_cells, self.tot_mines, time_seconds, win, int(but_cleared))

    def show_scores(self, win):
        self.label_time.after_cancel(self.time)
        user_best = self.scores.get_user_best_games(self.x_cells, self.y_cells, self.tot_mines)
        all_best = self.scores.get_all_best_games(self.x_cells, self.y_cells, self.tot_mines)

        self.score_window = tk.Toplevel()
        self.score_window.title("Best Scores")
        self.score_window.config(pady = 10, padx=10)
        self.score_window.protocol("WM_DELETE_WINDOW", self.reset_game)
        top_score = self.x_cells*self.y_cells-self.tot_mines

        if win:
            first_message = tk.Label(self.score_window, text="You won!", font='Helvetica 12 bold')
        else:
            first_message = tk.Label(self.score_window, text="BOOM! You lost!", font='Helvetica 12 bold')
        first_message.grid(row=0, sticky = tk.N, padx = 1, pady = 1)

        user_top = tk.Label(self.score_window, text="Your top scores:")
        user_top.grid(row=1, sticky = tk.W, padx = 1, pady = 1)

        frame_user = tk.Frame(self.score_window)
        frame_user.grid(row = 2, sticky = tk.E, padx = 1, pady = 1)
        tk.Label(frame_user, text="User", font='Helvetica 9 bold').grid(row=0,column=0, sticky=tk.E, pady = 1)
        tk.Label(frame_user, text="Score", font='Helvetica 9 bold').grid(row=0,column=1, sticky=tk.E, pady = 1)
        tk.Label(frame_user, text="Time", font='Helvetica 9 bold').grid(row=0,column=2, sticky=tk.E, pady = 1)
        for i, score in enumerate(user_best):
            tk.Label(frame_user, text=score[0], width = 10, anchor="e").grid(row=i+1,column=0, padx = 1)
            tk.Label(frame_user, text=f'{np.round(score[1]/top_score*100,1)}%', width = 7, anchor="e").grid(row=i+1,column=1, padx = 1)
            tk.Label(frame_user, text=np.floor(score[2]), width = 7, anchor="e").grid(row=i+1,column=2, padx = 1)

        all_top = tk.Label(self.score_window, text="All-time top scores:")
        all_top.grid(row=3, sticky = tk.W, padx = 1, pady = 1)

        frame_all = tk.Frame(self.score_window)
        frame_all.grid(row = 4, sticky = tk.E, padx = 1, pady = 1)
        tk.Label(frame_all, text="User", font='Helvetica 9 bold').grid(row=0,column=0, sticky=tk.E, pady = 1)
        tk.Label(frame_all, text="Score", font='Helvetica 9 bold').grid(row=0,column=1, sticky=tk.E, pady = 1)
        tk.Label(frame_all, text="Time", font='Helvetica 9 bold').grid(row=0,column=2, sticky=tk.E, pady = 1)
        for i, score in enumerate(all_best):
            tk.Label(frame_all, text=score[0], width = 10, anchor="e").grid(row=i+1,column=0, padx = 1)
            tk.Label(frame_all, text=f'{np.round(score[1]/top_score*100,1)}%', width = 7, anchor="e").grid(row=i+1,column=1, padx = 1)
            tk.Label(frame_all, text=np.floor(score[2]), width = 7, anchor="e").grid(row=i+1,column=2, padx = 1)

        frame_but = tk.Frame(self.score_window)
        frame_but.grid(row = 5, sticky = tk.N, padx = 1, pady = 4)
        tk.Button(frame_but, text = 'Restart', command=self.reset_game).grid(row=0, column=0, sticky=tk.EW, padx = 7)
        tk.Button(frame_but, text = 'Change size', command=self.restart).grid(row=0, column=1, sticky=tk.EW, padx = 7)
        tk.Button(frame_but, text = 'Quit', command=self.quit_game).grid(row=0, column=2, sticky=tk.EW, padx = 7)

    def score_decor(func):
        def wrapper(self):
            if hasattr(self, 'score_window'):
                self.score_window.destroy()
            func(self)
        return wrapper    
        
    @score_decor 
    def reset_game(self):
        self.field.reset()
        for i in np.arange(self.x_cells):
            for j in np.arange(self.y_cells):
                self.buts[i,j].config(image = self.images['plain'])
        self.reset_timer()
        self.label_mines.config(text=f"0/{self.tot_mines} mines")
        return
    
    @score_decor
    def restart(self):
        self.reset_timer()
        self.window.destroy()
        self.root.deiconify()
        return
    
    @score_decor
    def quit_game(self):
        self.reset_timer()
        self.close_window()