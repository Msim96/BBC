import pygame
from random import randrange
from copy import copy, deepcopy

#Global variables for pygame display 
s_width = s_height = 800
display_width = display_height = 400
block_size = 10
cols = rows = display_width//block_size
top_left_x = (s_width - display_width)//2
top_left_Y = (s_height - display_height)//2

def generate_random_grid(cols, rows):
    '''Returns a grid and fills randomly with live cells.'''

    grid = [[randrange(2) for x in range(cols)] for y in range(rows)]
    return grid

def create_grid(cols, rows, live_cells={}) :
    '''Returns a grid populated using positions of live cells.'''
    
    grid = [[0 for x in range(cols)] for y in range(rows)]
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if(y,x) in live_cells :
                grid[y][x] = live_cells[(y,x)]
    return grid
            

def draw_grid(surface, grid) :
    '''Draws the filled grid for the user to visualise game of life.'''
    
    #Clouring surface black
    surface.fill((0,0,0))
    colour_grid = deepcopy(grid)
    
    #Drawing grid cells depending on state 
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            colour_grid[y][x] = (0,0,0) if grid[y][x] == 0 else ((255, 255, 255))
            pygame.draw.rect(surface, colour_grid[y][x], (top_left_x + x*block_size, top_left_Y + y*block_size, block_size, block_size), 0)

    #drawing grid outline
    pygame.draw.rect(surface, (255, 255, 255), (top_left_x, top_left_x, display_width, display_height), 1)
    pygame.display.update()


def check_neighbours(x, y, grid) :
    '''Returns the number of neighbouring cells for a given cell.'''
    
    neighbour_count = 0
    coordinate_array = [-1, 0, 1]

    for i in coordinate_array :
        for j in coordinate_array :
            new_x = (x + j) % rows
            new_y = (y + i) % cols
            neighbour_count += grid[new_y][new_x]
    
    neighbour_count -= grid[y][x]
    return neighbour_count

def check_alive(grid, x, y):
    '''Returns 0 or 1 dependent on whether a cell is alive or dead according to rules.'''
    
    #Counting surrounding neighbours for the current cell
    neighbour_count = check_neighbours(x, y, grid)
    
    #Implementing rules of game of life for the cell
    if neighbour_count < 2 or neighbour_count > 3 :
        cell_state = 0
    elif grid[y][x] == 0 and neighbour_count == 3 :
        cell_state = 1
    else :
        cell_state = grid[y][x]
    
    return cell_state 

def main(surface) :
    '''Controls the set up and maintenance of the game of life.'''
    run = True
    #Generating grid filled randomly with live and dead cells
    grid = generate_random_grid(rows, cols)
    
    while run :
        
        draw_grid(win, grid)        
        #Delay to allow user to see what appears on screen
        pygame.time.delay(50)        
        #Initalising/Clearing the live cells dictionary to be replaced 
        live_cells = {}

        #Looping through grid to identify cells to be alive in next generation 
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                cell_state = check_alive(grid, x, y)
                if cell_state > 0 :
                    live_cells[(y, x)] = cell_state
        
        #Writing over grid with new cell locations
        grid = create_grid(cols,rows, live_cells)
        #Exit display when quit event occurs
        for event in pygame.event.get() :
            run = False if event.type == pygame.QUIT else True    
    pygame.display.quit()

#Setting up game
win = pygame.display.set_mode([s_width, s_height])
main(win)