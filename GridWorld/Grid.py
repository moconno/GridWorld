'''
Created on Nov 24, 2015

@author: Michael O'Connor
'''
import random
from GridWorld.Cell import Cell
import numpy as np

class Grid(object):
    
    '''the amount of times the agent will train'''
    train = 1000
    
    '''learning rate'''
    alpha = .5
    
    '''The total moves for an episode'''
    total_moves = 0
    
    '''the descent rate for rewards'''
    gamma = .8
    
    '''the discount for the reward'''
    sarsa = .9
    
    '''total steps to reach goal'''
    step_count = 0
    
    '''the balance between exploration and exploitation'''
    epsilon = .9
    
    '''increments when a terminal state is reached'''
    episode_count = 0
    
    '''goals hit'''
    goals_hit = 0
    
    '''20 x 20 grid of type Cell'''
    grid = [[0 for x in range(20)] for x in range(20)]
    
    ''' A list of moves'''
    move_action = [[-1,0], 
            [0,1], 
            [1,0], 
            [0,-1], 
    ]
    
    def __init__(self):
        for i in range(0, len(self.grid)):
            for j in range(0, len(self.grid)):
            
                cell = Cell(i, j)
            
                '''North Action isn't playable'''
                if(i == 0):
                    cell.q_table[0] = 0
            
                '''South action isn't playable'''
                if(i == len(self.grid) - 1):
                    cell.q_table[2] = 0
            
                '''West action isn't playable'''    
                if(j == 0):
                    cell.q_table[3] = 0
            
                '''East action isn't playable'''    
                if(j == len(self.grid) - 1):
                    cell.q_table[1] = 0
                
                '''Add cell to the grid world'''
                self.grid[i][j] = cell
    
    def sarsa_lambda(self, current_cell):
        
        if current_cell.state["terminal"] == 1:
            for list in self.grid:
                for cell in list:
                    cell.clear()    
        
        s = current_cell
            
        '''Pick an action to take'''
        if current_cell.action == None:
            action = s.select_action(self.epsilon)
        else:
            action = s.action
            
        '''Get the coordinates to move in the direction of the action'''           
        move = self.move_action[action]
            
        '''Get s_prime'''
        s_prime = self.grid[s.row + move[0]][s.col + move[1]]
            
        '''Get s prime optimal action'''
        s_prime_action = s_prime.select_action(self.epsilon)
        
        '''calculate product of gamma by s prime action'''
        gamma_qsa_prime = self.gamma * s_prime.q_table[s_prime_action]
            
        '''calculate delta'''
        delta = s_prime.reward + gamma_qsa_prime - s.q_table[action]
            
        '''Update the s cell e(s,a) table'''
        s.e_table[action] = s.e_table[action] + 1
            
        '''Update every cell's Q(s,a) and e(s,a) tables'''
        for list in self.grid:
            for cell in list:
                cell.q_table = np.add(cell.q_table, self.alpha * delta * cell.e_table)
                cell.e_table = np.dot(self.gamma * self.sarsa, cell.e_table)
                
        '''Return the current cell'''
        if s_prime.state['terminal'] != 1:
            s_prime.state['transition'] = 1
        else:
            self.episode_count += 1
            if self.epsilon > .1:
                self.epsilon -= .001
            if s_prime.reward == 1:
                self.goals_hit += 1
            
        return s_prime
            
    def train(self, start_cell):
        
        current_cell = start_cell
        
        while self.episode_count < 5000: 
            current_cell = self.sarsa_lambda(current_cell)   
        
    def select_random_start(self):
        
        start_cell = self.grid[random.randint(0, len(self.grid) - 1)][random.randint(0, len(self.grid) - 1)]
        
        while(start_cell.state["terminal"] == 1):
            start_cell = self.grid[random.randint(0, len(self.grid) - 1)][random.randint(0, len(self.grid) - 1)]
        start_cell.state['start'] = 1
        return start_cell
        