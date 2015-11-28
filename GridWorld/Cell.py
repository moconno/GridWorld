'''
Created on Nov 24, 2015

@author: Michael O'Connor
'''
import random

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
        
        '''The state prime as a result of taking an action'''
        self.q_table = [round(random.uniform(0.01, .1), 2), 
                   round(random.uniform(0.01, .1), 2),
                   round(random.uniform(0.01, .1), 2),
                   round(random.uniform(0.01, .1), 2)] 
                
        ''' The epsilon table'''   
        self.e_table = [0,
            0,
            0,
            0]  
    
    '''return the action with the highest action value'''    
    def select_action(self):
        high = max(self.q_table)
        return self.q_table.index(high)
        
        