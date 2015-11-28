'''
Created on Nov 24, 2015

@author: Michael O'Connor
'''
import random

class Grid(object):
    
    '''learning rate'''
    alpha = .25
    
    '''the descent rate for rewards'''
    gamma = 1
    
    '''total steps to reach goal'''
    step_count = 0
    
    '''20 x 20 grid of type Cell'''
    grid = [[0 for x in range(20)] for x in range(20)]
    
    ''' A list of moves'''
    move_action = [[1,0], 
            [0,1],
            [-1,0],
            [0,-1],
    ]
    
    def move_north(self):
        return 0
    
    def move_west(self):
        pass
    
    def move_south(self):
        pass
    
    def move_east(self):
        pass
    
    def __init__(self):
        pass
    
    def sarsa_lambda(self):
        
        '''select random starting point - Initialize s, a'''
        start_cell = self.select_random_start()
        
        current_cell = start_cell
        
        move = self.move_action[start_cell.select_action()]
        
        step = self.grid[start_cell.row + move[0]][start_cell.col + move[1]]
        
        '''Observe reward'''
        step.reward
        
        '''Observe state'''
        
        
        
        
    def select_random_start(self):
        start_cell = self.grid[random.randint(0, 19)][random.randint(0, 19)]
        start_cell.state['start'] = 1
        return start_cell
    
        