'''
Created on Nov 24, 2015

@author: Michael O'Connor
'''
import random
import numpy as np
import GridWorld.Grid

class Cell(object):
    '''
    classdocs
    '''
    

    def __init__(self, row, col):
        
        '''row index'''
        self.row = row
        
        '''col index'''
        self.col = col
        
        '''States aren't initialized until they are reached by the agent or the goal and start are set by the program'''
        self.state = {"start" : 0, "transition" : 0, "terminal" : 0}
        
        '''All reward values initialized to 0'''
        '''+1 = goal'''
        '''0 = transition'''
        '''-1 = terminal i.e walls'''
        self.reward = 0
        
        self.action = None
        
        '''The state prime as a result of taking an action'''
        self.q_table = np.array([round(random.uniform(0.01, .1), 2), 
                   round(random.uniform(0.01, .1), 2),
                   round(random.uniform(0.01, .1), 2),
                   round(random.uniform(0.01, .1), 2)]) 
                
        ''' The epsilon table'''   
        self.e_table = np.array([0,
            0,
            0,
            0])  
        
    def select_action(self, epsilon):
        
        random_number = random.uniform(0, 1)
        
        if random_number <= epsilon:
            self.action = random.randint(0, 3)
            while(self.q_table[self.action] == 0):
                self.action = random.randint(0, 3)
        else:
            self.action = self.select_optimal_action()
            
        return self.action
            
                
        
    def select_optimal_action(self):
        
        optimal_choice = np.where(self.q_table == max(self.q_table))
        
        max_value = -10000
        
        for value in self.q_table:
            if value > max_value and value != 0:
                max_value = value
            
        #return max_value    
        
        return random.choice(optimal_choice[0])
        
    def goal_cell(self):
        self.reward = 1
        self.q_table = 0
        self.e_table = 0
        self.state["terminal"] = 1
        
    def clear(self):
        self.state["start"] = 0
        self.state['transition'] = 0
        self.e_table.fill(0)
        