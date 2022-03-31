import numpy as np
from datetime import datetime

class Field():
    
    def __init__(self,x_size, y_size, num_mines, x_init, y_init):
        
        self.x_size = x_size
        self.y_size = y_size
        self.num_mines = num_mines
        self.x_init = x_init
        self.y_init = y_init       
        
        self.positions = np.arange(self.x_size*self.y_size).reshape((self.x_size,self.y_size))
        self.removeInitalClick()
        self.availablePos = np.unique(self.positions)[1:]
        
        mines = np.random.choice(self.availablePos,self.num_mines, False)
        
        self.field = np.zeros((self.x_size*self.y_size))
        self.field[mines] = 1
        self.field = self.field.reshape((self.x_size,self.y_size)).astype(int)
        
        self.createClues()

        self.time_begin = datetime.now()

        self.active_but = np.ones((self.x_size, self.y_size)).astype(int)
        
    def createClues(self):
        
        self.clues = np.zeros((self.x_size,self.y_size))
        ext_field = np.zeros((self.x_size+2,self.y_size+2))
        ext_field[1:-1,1:-1] = self.field
        
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                rolled = np.roll(ext_field, i, axis = 0)
                rolled = np.roll(rolled, j, axis = 1)
                
                self.clues = self.clues + rolled[1:-1,1:-1]
                
        self.clues[self.field == 1] = -1
        self.clues = self.clues.astype(int)
        
    def removeInitalClick(self):
        
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                if (self.x_init+i >= 0 and self.x_init+i < self.x_size and 
                self.y_init+j >=0 and self.y_init+j < self.y_size):
                    self.positions[self.x_init+i,self.y_init+j] = -1

    def get_timediff(self, ms=False):
        time_now = datetime.now()
        diff = time_now-self.time_begin
        return diff.total_seconds()

    def click(self, x, y):
        if self.active_but[x,y] == 0:
            return -2

        self.active_but[x,y] = 0
        if self.field[x,y]:
            self.active_but -= self.active_but & self.field
            return -1

        if self.clues[x,y] == 0:
            self.clear_around(x, y)
            return 0
        return 0


    def unclick(self, x, y):
        self.active_but[x,y] = 1

    def clear_around(self, x, y):
        if self.clues[x,y] == 0:
            for i in [-1,0,1]:
                for j in [-1,0,1]:
                    if (x+i >= 0 and x+i < self.x_size and 
                    y+j >=0 and y+j < self.y_size):
                        if self.active_but[x+i,y+j]:
                            self.active_but[x+i,y+j] = 0
                            self.clear_around(x+i, y+j)
