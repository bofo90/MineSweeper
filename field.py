import numpy as np
from datetime import datetime

class Field():
    
    def __init__(self, x_size, y_size, num_mines):
        
        self.x_size = x_size
        self.y_size = y_size
        self.num_mines = num_mines

        self.first_click = True
        self.display_clues = ((-2)*np.ones((self.x_size, self.y_size))).astype(int)
        self.all_clues = np.zeros((self.x_size,self.y_size))
        
    def create_field(self,x,y):
        positions = np.arange(self.x_size*self.y_size).reshape((self.x_size,self.y_size))
        positions = self.removeInitalClick(x,y,positions)
        availablePos = np.unique(positions)[1:]

        mines = np.random.choice(availablePos,self.num_mines, False)

        field = np.zeros((self.x_size*self.y_size))
        field[mines] = 1
        field = field.reshape((self.x_size,self.y_size)).astype(int)
        return field

    def createClues(self, field):
        
        clues = np.zeros((self.x_size,self.y_size))
        ext_field = np.zeros((self.x_size+2,self.y_size+2))
        ext_field[1:-1,1:-1] = field
        
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                rolled = np.roll(ext_field, i, axis = 0)
                rolled = np.roll(rolled, j, axis = 1)
                
                clues = clues + rolled[1:-1,1:-1]
                
        clues[field == 1] = -1
        clues = clues.astype(int)
        return clues
        
    def removeInitalClick(self, x, y, positions):
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                if (x+i >= 0 and x+i < self.x_size and 
                    y+j >=0 and y+j < self.y_size):
                    positions[x+i,y+j] = -1
        return positions

    def get_timediff(self, ms=False):
        time_now = datetime.now()
        diff = time_now-self.time_begin
        return diff.total_seconds()

    def click(self, x, y):
        status = -1

        if self.first_click:
            self.first_click = False
            field = self.create_field(x,y)
            self.all_clues = self.createClues(field)
            self.time_begin = datetime.now()
            status = -2

        if self.display_clues[x,y] == -2: #not an active button
            if self.all_clues[x,y] == -1: #button is a mine
                self.display_clues[self.all_clues==-1] = -1
                status = 0
                return status

            self.display_clues[x,y] = self.all_clues[x,y]
            if self.display_clues[x,y] == 0: #button provoques a cascade
                self.clear_around(x, y)

        if self.check_win():
            self.display_clues[self.all_clues==-1] = -3
            status = 1

        return status

    def clear_around(self, x, y):
        if self.display_clues[x,y] == 0:
            for i in [-1,0,1]:
                for j in [-1,0,1]:
                    if (x+i >= 0 and x+i < self.x_size and 
                    y+j >=0 and y+j < self.y_size):
                        if self.display_clues[x+i,y+j] == -2:
                            self.display_clues[x+i,y+j] = self.all_clues[x+i,y+j]
                            self.clear_around(x+i, y+j)

    def click_flag(self, x, y):
        if self.display_clues[x,y] == -2:
            self.display_clues[x,y] = -3
        elif self.display_clues[x,y] == -3:
            self.display_clues[x,y] = -2

    def check_win(self):
        return ((self.display_clues<-1) == (self.all_clues==-1)).all()

    def reset(self):
        self.first_click = True
        self.display_clues = ((-2)*np.ones((self.x_size, self.y_size))).astype(int)
        self.all_clues = np.zeros((self.x_size,self.y_size))

    # def see_field(self):
    #     all_active = self.active_but+self.flag_but
    #     field = -2*np.ones((self.x_size, self.y_size)).astype(int)
    #     field[self.active_but == 0] = self.clues[self.active_but==0]
    #     return field.T