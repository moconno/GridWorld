'''
Created on Nov 24, 2015

@author: Michael O'Connor
'''

from GridWorld.Cell import Cell
from GridWorld.Grid import Grid
import random

if __name__ == '__main__':
    
    '''Create a new grid World'''
    grid_world = Grid() 
    
    for i in range(0, 20):
        for j in range(0, 20):

            cell = Cell(i, j)
            
            '''North Action isn't playable'''
            if(i == 0):
                cell.q_table[0] = 0
            
            '''South action isn't playable'''
            if(i == 19):
                cell.q_table[2] = 0
            
            '''West action isn't playable'''    
            if(j == 0):
                cell.q_table[3] = 0
            
            '''East action isn't playable'''    
            if(j == 19):
                cell.q_table[1] = 0
                
            '''Add cell to the grid world'''
            grid_world.grid[i][j] = cell
            
    '''set the reward for one cell to 1 - the goal state'''
    grid_world.grid[8][13].reward = 1
    
    '''set the state for the cell containing the goal'''
    grid_world.grid[8][13].state["terminal"] = 1
    
    
    grid_world.sarsa_lambda()
                
            
    