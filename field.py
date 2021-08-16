import numpy as np

class Field():
    
    def __init__(self,x_size, y_size, num_mines, x_init, y_init):
        
        self.x_size = x_size
        self.y_size = y_size
        self.num_mines = num_mines
        
        repeat = True
        
        while repeat:
        
            mines = np.random.choice(self.x_size*self.y_size,self.num_mines, False)
            
            self.field = np.zeros((self.x_size*self.y_size))
            self.field[mines] = 1
            self.field = self.field.reshape((self.x_size,self.y_size))
            
            self.createClues()
            
            if self.clues[x_init,y_init] == 0:
                repeat = False
        
    def createClues(self):
        
        self.clues = np.zeros((self.x_size,self.y_size)).astype(int)
        ext_field = np.zeros((self.x_size+2,self.y_size+2))
        ext_field[1:-1,1:-1] = self.field
        
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                rolled = np.roll(ext_field, i, axis = 0)
                rolled = np.roll(rolled, j, axis = 1)
                
                self.clues = self.clues + rolled[1:-1,1:-1]
                
        self.clues[self.field == 1] = -1
        self.clues = self.clues.astype(int)