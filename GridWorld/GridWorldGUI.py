'''
Created on Nov 25, 2015

@author: mycom
'''
import pygame
from GridWorld.Grid import Grid

up_arrow = u'\u2191'

left_arrow = u'\u2190'

down_arrow = u'\u2193'

right_arrow = u'\u2192'




#colors
BLACK = (0,0,0)
WHITE = (255,255,255)
GOLD = (255,215, 0)
CURRENT = (255,0,0)
GREEN = (0,255, 0)

WIDTH = 20
HEIGHT = 20

MARGIN = 5

grid = []

index = 0

cell_path = []

current_cell = None

previous_cell = None

grid_world = Grid()

grid = grid_world.grid
        
pygame.init()

myfont = pygame.font.SysFont('DejaVu Sans', 15, True)

WINDOW_SIZE = [1200, 510]
    
screen = pygame.display.set_mode(WINDOW_SIZE)

pygame.display.set_caption("Grid World")

pygame.display.update()

start_cell_selected = False

done = False

pause = False

ready = False

clock = pygame.time.Clock()


while not done:
    
    q_table_lable = myfont.render("q_table", 0, WHITE)

    screen.blit(q_table_lable, (512, 10))
    
    e_table_lable = myfont.render("e_table", 0, WHITE)

    screen.blit(e_table_lable, (512, 50))
    
    epsilon_lable = myfont.render("epsilon", 0, WHITE)
    screen.blit(epsilon_lable, (512, 80))
    
    episode_lable = myfont.render("episode count", 0 , WHITE)
    screen.blit(episode_lable, (512, 120))
    
    goals_hit_label = myfont.render("goals hit", 0, WHITE)
    screen.blit(goals_hit_label, (512, 160))

    pygame.display.update()
    
    
    for event in pygame.event.get():  # User did something
        
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
                        
        elif event.type == pygame.MOUSEMOTION:
            
            pos = pygame.mouse.get_pos()
            
            column = pos[0] // (WIDTH + MARGIN)
            row = pos[1] // (HEIGHT + MARGIN)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            
            #Sets a goal state
            if event.button == 1:
                # User clicks the mouse. Get the position
                pos = pygame.mouse.get_pos()
            # Change the x/y screen coordinates to grid coordinates
                column = pos[0] // (WIDTH + MARGIN)
                row = pos[1] // (HEIGHT + MARGIN)
            # Set that location to zero
                grid[row][column].state["terminal"] = 1
                grid[row][column].reward = 1
                
            #Sets a terminal State    
            elif event.button == 3:
            
                pos = pygame.mouse.get_pos()
            # Change the x/y screen coordinates to grid coordinates
                column = pos[0] // (WIDTH + MARGIN)
                row = pos[1] // (HEIGHT + MARGIN)
                
                grid[row][column].state["terminal"] = 1
                grid[row][column].reward = -1
                
        #Sets a start State    
        elif event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_s:
                pos = pygame.mouse.get_pos()
            # Change the x/y screen coordinates to grid coordinates
                column = pos[0] // (WIDTH + MARGIN)
                row = pos[1] // (HEIGHT + MARGIN)
                
                grid_world.train(grid_world.select_random_start())
                
                current_cell = grid_world.select_random_start()
                
            elif event.key == pygame.K_SPACE:
                
                if pause == True:
                    pause = False
                    pygame.mixer.music.unpause()
                else:
                    pause = True
                    pygame.mixer.music.pause()
    
    pos = pygame.mouse.get_pos()
            
    column = pos[0] // (WIDTH + MARGIN)
    row = pos[1] // (HEIGHT + MARGIN)
    
    if grid[row][column]:
        q_table = myfont.render(str(grid[row][column].q_table), 1, WHITE)
        e_table = myfont.render(str(grid[row][column].e_table), 1, WHITE)
        screen.blit(q_table, (512, 25))
        screen.blit(e_table, (512, 65))
        pygame.display.update()
        
    epsilon = myfont.render(str(grid_world.epsilon), 1, WHITE)
    screen.blit(epsilon, (512, 95))
    pygame.display.update()
    
    episode = myfont.render(str(grid_world.episode_count), 1, WHITE)
    screen.blit(episode, (512, 135))
    pygame.display.update()
    
    goals_hit = myfont.render(str(grid_world.goals_hit), 1, WHITE)
    screen.blit(goals_hit, (512, 175))
    pygame.display.update()
    

    if not pause:        
        if current_cell != None and current_cell.state['terminal'] != 1:
                
            previous_cell = current_cell
            current_cell = grid_world.sarsa_lambda(current_cell)
            if current_cell in cell_path:
                cell_path.remove(current_cell)
            cell_path.insert(0, current_cell)
        
        if current_cell != None and current_cell.state['terminal'] == 1:
            index += 1
 
    # Set the screen background
    screen.fill(BLACK)
 
 
        # Draw the grid
    for row in range(20):
        for column in range(20):
            '''default color'''
            color = WHITE
            
            if grid[row][column] in cell_path:
                cell_path_index = cell_path.index(grid[row][column])
                if cell_path_index > 255:
                    cell_path_index = 255
                if cell_path_index < 0:
                    cell_path_index = 0
                color = (CURRENT[0] - cell_path_index, CURRENT[1], CURRENT[2] + cell_path_index)
                        
            
            if grid[row][column].reward == 1:
                if current_cell == grid[row][column]:
                    if index % 60 < 30: 
                        color = GOLD
                    else:
                        color = WHITE
                    index += 1
                else:
                    color = GOLD
            if grid[row][column].reward == -1:
                if current_cell == grid[row][column]:
                    if index % 60 < 30:
                        color = BLACK
                    else:
                        color = WHITE
                    index += 1
                else:
                    color = BLACK
            if grid[row][column].state["start"] == 1 or grid[row][column] == current_cell and current_cell.state["terminal"] != 1:
                color = GREEN
                
            pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])
            
            if grid[row][column].select_optimal_action() == 0:
            
                arrow = myfont.render(up_arrow, True, BLACK)
                screen.blit(arrow, ((MARGIN + WIDTH) * column + 10, (MARGIN + HEIGHT) * row + 5))
                
            elif grid[row][column].select_optimal_action() == 1:
                
                arrow = myfont.render(right_arrow, True, BLACK)
                screen.blit(arrow, ((MARGIN + WIDTH) * column + 10, (MARGIN + HEIGHT) * row + 5))
                
            elif grid[row][column].select_optimal_action() == 2:
                
                arrow = myfont.render(down_arrow, 1, BLACK)
                screen.blit(arrow, ((MARGIN + WIDTH) * column + 10, (MARGIN + HEIGHT) * row + 5))
                
            elif grid[row][column].select_optimal_action() == 3:
                
                arrow = myfont.render(left_arrow, 1, BLACK)
                screen.blit(arrow, ((MARGIN + WIDTH) * column + 10, (MARGIN + HEIGHT) * row + 5))
            
            
        if current_cell != None and current_cell.state['terminal'] == 1 and index == 280:
            cell_path = []
            index = 0
            for list in grid:
                for cell in list:
                    cell.clear()
            current_cell = grid_world.select_random_start()
 
    # Limit to 60 frames per second
    clock.tick(60)
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()