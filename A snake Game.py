# Python - 3.8.2
# A Snake Game

import random,pygame,sys,time
from pygame.locals import *

FPS = 15
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 500
CELL_SIZE = 20

assert WINDOW_WIDTH % CELL_SIZE == 0 ,"Window width must be a multiple of cell size"
assert WINDOW_HEIGHT % CELL_SIZE == 0 ,"Window height must be a multiplr of cell size"

CELL_WIDTH = int(WINDOW_WIDTH / CELL_SIZE)
CELL_HEIGHT = int(WINDOW_HEIGHT / CELL_SIZE)

#RGB

WHITE = (255,255,255)
RED   =  (255,0,0)
BLACK = (0,0,0)
GREEN = (0,155,0)
DARKGRAY = (40,40,40)
DARKGREEN = (0,155,0)
YELLOW = ( 255,255,0)
OLIVE = (128,128,0)
BACKGROUND_COLOR = DARKGRAY

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0 # index of the snake's head

def main():

    global FPS_CLOCK,DISPLAYSURF,BASIC_FONT

    pygame.init()

    FPS_CLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT)) # display object
    BASIC_FONT = pygame.font.Font('freesansbold.ttf',18) # font object
    pygame.display.set_caption("@Snake")

    show_Start_Screen()

    while True:

        run_Game()

        show_GameOver_Screen()

def run_Game(): 

    # starting position in a random number 
    start_x = random.randint(5,CELL_WIDTH - 5) 
    start_y = random.randint(5,CELL_HEIGHT - 5)

    # body of the snake in a list of dictionary
    worm_coords = [ {'x' : start_x , 'y' : start_y},
                    {'x' : start_x - 1 , 'y' : start_y },
                    {'x' : start_x - 2 , 'y' : start_y } ]

    direction = RIGHT

    # start the apple in random direction
    apple = getRandomLocation()

    while True: #Game Loop

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                    direction = LEFT
                elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                    direction = RIGHT
                elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                    direction = UP
                elif (event.key == K_DOWN or event.key == K_s) and direction !=UP:
                    direction = DOWN
                elif event.key == K_ESCAPE:
                    terminate()

        #check the snake has hit itself or the edge of the cell

        if worm_coords[HEAD]['x'] == -1 or worm_coords[HEAD]['x'] == CELL_WIDTH \
        or worm_coords[HEAD]['y'] == -1 or worm_coords[HEAD]['y']== CELL_HEIGHT:

            return # game over

        for worm_body in worm_coords[1:]: # leave the first index( or first Head)
            if worm_body['x'] == worm_coords[HEAD]['x'] and worm_body['y'] == worm_coords[HEAD]['y']:
                return # game over

        # check if snake has eaten the apple or not

        if worm_coords[HEAD]['x'] == apple['x'] and worm_coords[HEAD]['y'] == apple['y']:

            # don't need to remove tail segments
            apple = getRandomLocation()
        else:

            del worm_coords[-1] # remove snake's tail segments

        # move the snake by adding a segment (always at the begining)
        # in the direction it is moving

        if direction == UP: # decrement 1 from y direction
            new_head = {'x':worm_coords[HEAD]['x'],'y':worm_coords[HEAD]['y']-1}
            
        elif direction == DOWN : # increment 1 from y direction
            new_head = { 'x':worm_coords[HEAD]['x'],'y':worm_coords[HEAD]['y']+1}

        elif direction == LEFT: # decrement 1 from x direction
            new_head = { 'x':worm_coords[HEAD]['x']-1,'y':worm_coords[HEAD]['y'] }

        elif direction == RIGHT: # increment 1 from x direction
            new_head = {'x':worm_coords[HEAD]['x']+1,'y':worm_coords[HEAD]['y'] }

        worm_coords.insert(0,new_head)

        DISPLAYSURF.fill(BACKGROUND_COLOR)
        draw_Grid() # draw the Grid inside the window
        draw_Worm(worm_coords) # draw the body of the snake
        draw_Apple(apple) # draw the apple
        draw_Score(len(worm_coords) -3) # display the score
        pygame.display.update()
        FPS_CLOCK.tick(FPS)



def draw_Grid():
    
    # just to make it easier to visualize the grid of cells,
    # draw ou each of the vertical and horizontal lines of the grid

    for i in range(0,WINDOW_WIDTH,CELL_SIZE): # draw vertical lines
        pygame.draw.line(DISPLAYSURF,WHITE,(i,0),(i,WINDOW_HEIGHT))

    for j in range(0,WINDOW_HEIGHT,CELL_SIZE): # draw horizontal lines
        pygame.draw.line(DISPLAYSURF,WHITE,(0,j),(WINDOW_WIDTH,j))


def draw_Worm(worm_coords):

    # draw the green box or body for the snake

    for coords in worm_coords:
        x = coords['x']*CELL_SIZE
        y = coords['y']*CELL_SIZE

        # for shade or cover
        snake_segment_rect = pygame.Rect(x,y,CELL_SIZE,CELL_SIZE)
        pygame.draw.rect(DISPLAYSURF,RED,snake_segment_rect)

        # inner body color
        snake_inner_segment_rect = pygame.Rect(x+4,y+4,CELL_SIZE-6,CELL_SIZE-6)
        pygame.draw.rect(DISPLAYSURF,GREEN,snake_inner_segment_rect)


def draw_Apple(coord):

    # draw the snake food
    
    
        x = coord['x'] * CELL_SIZE
        y = coord['y']*  CELL_SIZE
        apple_rect = pygame.Rect(x,y,CELL_SIZE,CELL_SIZE)
        pygame.draw.rect(DISPLAYSURF,YELLOW,apple_rect)
        

def draw_Score(score):
    
    # score line
    score_surf = BASIC_FONT.render('Score : %s' %(score),True,WHITE,BLACK)
    score_Rect = score_surf.get_rect()
    score_Rect.topleft = (WINDOW_WIDTH - 120,10)
    DISPLAYSURF.blit(score_surf,score_Rect)
        
        
        

def terminate():

    # this function works for shut down process
    pygame.quit()
    sys.exit()


def getRandomLocation():
    # apple in random location
    return { 'x' : random.randint(0,CELL_WIDTH-3),'y':
             random.randint(0,CELL_HEIGHT-3)}

def draw_Press_key_Msg():

    press_surf = BASIC_FONT.render('Press any key To play.',True,YELLOW)
    press_Rect = press_surf.get_rect()
    press_Rect.topleft = (WINDOW_WIDTH - 200, WINDOW_HEIGHT - 40)
    DISPLAYSURF.blit(press_surf,press_Rect)
    

def show_GameOver_Screen():

    # Game Over
    game_over_font = pygame.font.Font('freesansbold.ttf',100)

    # surface object
    game_surf = game_over_font.render('Game ', True, WHITE)
    over_surf = game_over_font.render('Over ',True,WHITE)

    #Rect object
    game_Rect = game_surf.get_rect()
    over_Rect = over_surf.get_rect()

    game_Rect.midtop = (int(WINDOW_WIDTH / 2), 60)
    over_Rect.midtop = (int(WINDOW_WIDTH / 2),game_Rect.height+60)

    # blit the surface and rect 
    DISPLAYSURF.blit(game_surf,game_Rect)
    DISPLAYSURF.blit(over_surf,over_Rect)

    
    draw_Press_key_Msg()

    pygame.display.update()

    # wait for a second and again press any key to continue

    pygame.time.wait(400)

    Check_For_press_key() #check out any key pressed or not

    while True:

        if Check_For_press_key():

            pygame.event.get() # clear event

            return

    


def show_Start_Screen():
    # starting screen

    title_font = pygame.font.Font('freesansbold.ttf',80)
    title_surf1 = title_font.render('SNAKE!',True,WHITE,DARKGREEN)
    title_surf2 = title_font.render("GAME!",True,GREEN)

    degree1 = 0
    degree2 = 0

    while True:
        DISPLAYSURF.fill(BACKGROUND_COLOR)

        # rotating the msg 

        rotated_surf1 = pygame.transform.rotate(title_surf1,degree1)
        rotated_Rect1 = rotated_surf1.get_rect()

        rotated_Rect1.center = (int(WINDOW_WIDTH / 2), int(WINDOW_HEIGHT / 2))
        DISPLAYSURF.blit(rotated_surf1,rotated_Rect1)

        rotated_surf2 = pygame.transform.rotate(title_surf2,degree2)
        rotated_Rect2 = rotated_surf2.get_rect()

        rotated_Rect2.center = (int(WINDOW_WIDTH / 2), int(WINDOW_HEIGHT / 2))
        DISPLAYSURF.blit(rotated_surf2,rotated_Rect2)


        draw_Press_key_Msg() #"Press a key to play "

        if Check_For_press_key(): # confirming a key is pressed or not Nine value

            pygame.event.get() #  clear all the events in event queue
            return
        pygame.display.update()
        FPS_CLOCK.tick(FPS)

        degree1 += 3 # rotate 3 by each fraem
        degree2 += 5 # rotate 5 by each frame

        # keep in mind if the rotating value gets higher , most of the
        # time it will get error :  pygame.error: Width or height is too large.
        # even rotating image are slightly bigger then original image


def Check_For_press_key():

    if len(pygame.event.get(QUIT)) > 0: # return empty list [] if 
        terminate()                     # their is no QUIT

    event = pygame.event.get(KEYUP) # all the events

    if len(event) == 0:
        return None
    if event[0].key == K_ESCAPE: # excape key
        terminate()

    return event[0].key # return first key event object



if __name__ == '__main__':

    main()

    
        
        


        

        

        
    

    
    

    
    
    
    
    
