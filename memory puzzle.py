# importing module

import random,pygame,sys
from pygame.locals import *



FPS = 30 # frames per second
WIDTH = 650 # width of the window's
HEIGHT = 500 # height of the window's
SLIDING_SPEED = 3 # speed of each boxes on reveals and covers
BOX_SIZE = 35 # size of box height & weight in pixels
GAP_SIZE = 10 # size of gap between boxes in pixels
BOARD_WIDTH = 10 # number of columns of icons
BOARD_HEIGHT = 6 # number of rows of icons

#sanity check
assert (BOARD_WIDTH * BOARD_HEIGHT) % 2 == 0, 'Board needs to have an even number of boxed for pairs of matches'

X_margin = int((WIDTH - (BOARD_WIDTH * (BOX_SIZE + GAP_SIZE))) / 2)
Y_margin = int((HEIGHT - (BOARD_HEIGHT * (BOX_SIZE + GAP_SIZE))) / 2)





# RGB COLORS
GRAY       =    (100,100,100)
NAVYBLUE   =    (60,60,100)
WHITE      =    (255,255,255)
RED        =    (255,0,0)
GREEN      =    (0,255,0)
BLUE       =    (0,0,255)
YELLOW     =    (255,255,0)
ORANGE     =    (255,128,0)
PURPLE     =    (255,0,255)
CYAN       =    (0,255,255)

BACKGROUND_COLOR = GREEN
LIGHT_BACKGROUND_COLOR = GRAY
BOX_COLOR = WHITE
HIGH_LIGHT_COLOR = BLUE

#Using constant variables instead of raw string
DONUT = 'donut'
SQUARE = 'square'
DIAMOND = 'diamond'
LINES   = 'lines'
OVAL    = 'oval'

#creating a (tuple) set of colors 
ALL_COLORS = (RED,GREEN,BLUE,YELLOW,ORANGE,PURPLE,CYAN)
#creating a set of shapes
ALL_SHAPES = (DONUT,SQUARE,DIAMOND,LINES,OVAL)
# check if their is enough shape/color combination for the size of the board
assert (len(ALL_COLORS) * len(ALL_SHAPES)*2) >= (BOARD_WIDTH*BOARD_HEIGHT),"Board is too big for the number of shapes/colors defined."

def memory_puzzle():

    #Game starts from Here
    global FPS_CLOCK , DISPLAYSURF
    pygame.init()
    
    FPS_CLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WIDTH,HEIGHT))
    DISPLAYSURF.fill(BACKGROUND_COLOR)

    # for score showing on screen
    myfont = pygame.font.SysFont("monospace",16)
    

    #used to store x,y coordinate of mouse event
    mouse_x = 0
    mouse_y = 0
    score = 0 # keep tracking the score when two shape or color gets matched
    

    pygame.display.set_caption("Memory Puzzle")

    main_board = getRandomizedBoard() # resturns a data structure to represent the state of the board

    #return a structure about which boxes are covered or revealed
    revealedBoxes = generateRevealedBoxesData(False)

    first_selection = None

    Start_Game_Animation(main_board)# to give us a simple hint at first

    while True: # main game loop

        mouse_Clicked = False # checking mouse click through each iteration

        DISPLAYSURF.fill(BACKGROUND_COLOR)

    
        text = myfont.render("Score :  "+str(score),1,BLUE)# create object
        score_rect = text.get_rect()
        score_rect.topleft = (5,10)
        DISPLAYSURF.blit(text,score_rect)
        
        draw_Board(main_board,revealedBoxes)#updating the screen function

        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key ==K_ESCAPE):
                pygame.quit()
                sys.exit()

            elif event.type == MOUSEMOTION:
                mouse_x,mouse_y = event.pos

            elif event.type == MOUSEBUTTONUP:
                mouse_x,mouse_y = event.pos
                mouse_Clicked = True

        #checking the mouse cursor on which box
                
        boxx , boxy = get_Box_At_Pixel(mouse_x,mouse_y)
        if boxx !=None and boxy !=None:
            
            #that means mouse is over a box
            
            if not revealedBoxes[boxx][boxy]:
                draw_Highlight_Box(boxx,boxy) # draw a highlight over covered box

            if not revealedBoxes[boxx][boxy] and mouse_Clicked:
                revealedBoxesAnimation(main_board,[(boxx,boxy)])
                revealedBoxes[boxx][boxy] = True # to uncover the clicked box in updated frame
                
                #handling the first clicked box
                
                if first_selection == None: # current box is the first box that clicked

                    first_selection = (boxx,boxy)
                else:
                    #the current box is the second box that clicked
                    # also check their is match between two icons
                    
                    icon1shape , icon1color = getShapeAndColor(main_board,first_selection[0],first_selection[1])
                    icon2shape,icon2color = getShapeAndColor(main_board,boxx,boxy)

                    #handling a mismatched pair
                    if icon1shape !=icon2shape or icon1color != icon2color:

                        #icons or colors didn't match
                        pygame.time.wait(1000) # 1 second pause

                        cover_Boxes_Animation(main_board,[(first_selection[0],first_selection[1]),(boxx,boxy)])
                        revealedBoxes[first_selection[0]][first_selection[1]] = False
                        revealedBoxes[boxx][boxy] = False

                    elif icon1shape == icon2shape and icon1color == icon2color:
                        score +=1 # increasing score
                        
                        
                        
                    #handling if player won
                    elif hasWon(revealedBoxes):

                        #check if all pairs found
                        game_Won_Animation(main_board)
                        pygame.time.wait(2000)

                        #reset the board
                        main_board = getRandmomizedBoard()
                        revealedBoxes = generateReavealedBoxesData(False)

                        #show the unrevealed board for a second

                        drawBoard(main_board,revealedBoxes)
                        pygame.display.updste()
                        pygame.time.wait(1000)

                        #Reply the start game animation
                        Start_Game_Animation(main_board)
                        score = 0 # reset the score board
                        
                    first_selection = None #reset first selection

        #redraw the screen and wait a clock tick
        pygame.display.update()
        FPS_CLOCK.tick(FPS)
                    
                

                
                
    

#creating the board data structure

def getRandomizedBoard():

    #get a list of every possible shape in every possible color
    icons = []
    for color in ALL_COLORS:
        for shape in ALL_SHAPES:
            icons.append( (shape,color) )

    random.shuffle(icons)#random order of icons list
    #calculating how many icons needed
    numOfIcon = int((BOARD_WIDTH * BOARD_HEIGHT)/2)
    icons = icons[:numOfIcon] * 2# make two of each
    random.shuffle(icons)

    #create the board data structure, with randomly placed icon
    board = []
    for x in range(BOARD_WIDTH):
        column = []
        for y in range(BOARD_HEIGHT):
            column.append(icons[0])
            del icons[0]
        board.append(column)

    return board



#spliting list into a list of lists
def split_into_groups_of(groupSize,theList):
    # inner lists have at most groupsize number of items
    result = []
    for i in range(0,len(theList),groupSize):
        result.append(theList[i:i+groupSize])
    return result



# getting board Icon's shape and color
def getShapeAndColor(board,boxx,boxy):
     # for shape it's stored in board [x][y][0]
     # for color it's stored in board [x][y][1]
     return board[boxx][boxy][0], board[boxx][boxy][1]
    
    





#"Revealed Boxes" data structure

def generateRevealedBoxesData(value):

    revealedBoxes = []
    for i in range(BOARD_WIDTH):
        revealedBoxes.append([value] * BOARD_HEIGHT)
    return revealedBoxes

def left_To_Top(x,y):
    #converting box to pixel co-ordinates
    left = x * (BOX_SIZE + GAP_SIZE) + X_margin
    top = y * (BOX_SIZE + GAP_SIZE) + Y_margin

    return (left,top)


#converting pixel to box coordinates
def get_Box_At_Pixel(x,y):
    for boxx in range(BOARD_WIDTH):
        for boxy in range(BOARD_HEIGHT):
            left , top = left_To_Top(boxx,boxy)
            boxRect = pygame.Rect(left, top, BOX_SIZE,BOX_SIZE)
            if boxRect.collidepoint(x,y):
                return (boxx,boxy) # found the box , return the coordinates
    return (None,None)



#Drawing the entire board or updated board
def draw_Board(board,revealed):
    # draw all the boxes covered or revealed
    for boxx in range(BOARD_WIDTH):
        for boxy in range(BOARD_HEIGHT):
            left , top = left_To_Top(boxx,boxy)
            if not revealed[boxx][boxy]:
                #draw a cover box
                pygame.draw.rect(DISPLAYSURF,BOX_COLOR,(left,top,BOX_SIZE,BOX_SIZE))
            else:
                #draw the revealed icon
                shape ,color = getShapeAndColor(board,boxx,boxy)
                drawIcon(shape,color,boxx,boxy)




#Telling if player has won
def hasWon(revealedBoxes):
    # return true if all the boxes have been uncovered

    for x in revealedBoxes:
        if False in x:
            return False # return false if any boxes are covered 
                
    return True


# "Game Won" animation
def game_Won_Animation(board):

    coveredBox = generateRevealedBoxesData(True)
    color1 = LIGHT_BACKGROUND_COLOR
    color2 = BACKGROUND_COLOR

    for i in range(10):
        color1,color2 = color2,color1
        DISPLAYSURF.fill(color1)
        drawBoard(board,coveredBox)
        pygame.display.update()
        pygame.time.wait(300)


# drawing box cover
def draw_box_cover(board,boxes,coverage):
    #draw boxes being covered/revealed
    # "boxes" is a list of two-item lists which have x & y spot of the box

    for box in boxes:
        #draw the background color
        #draw the icon
        #then draw however much of the white box over the icon that is needed.
        left , top = left_To_Top(box[0],box[1])
        pygame.draw.rect(DISPLAYSURF,BACKGROUND_COLOR,(left,top,BOX_SIZE,BOX_SIZE))

        shape,color = getShapeAndColor(board,box[0],box[1])
        drawIcon(shape,color,box[0],box[1])
        if coverage > 0:
             pygame.draw.rect(DISPLAYSURF, BOX_COLOR, (left, top, coverage, BOX_SIZE))

    pygame.display.update()
    FPS_CLOCK.tick(FPS)

# revealing and covering animation
def revealedBoxesAnimation(board,boxesToReveal):
    # Do the box reveal animation
    for coverage in range(BOX_SIZE,(-SLIDING_SPEED)-1,SLIDING_SPEED):
        draw_box_cover(board,boxesToReveal,coverage)

def cover_Boxes_Animation(board,boxesToCover):
    #Do the box cover animation
    for coverage in range(0,BOX_SIZE + SLIDING_SPEED ,SLIDING_SPEED):
        draw_box_cover(board,boxesToCover,coverage)

        

#Highlighting the box
def draw_Highlight_Box(boxx,boxy):
    left , top = left_To_Top(boxx,boxy)
    pygame.draw.rect(DISPLAYSURF , HIGH_LIGHT_COLOR,(left-5,top-5,BOX_SIZE+10,BOX_SIZE+10),4)


# drawing icons    
def drawIcon(shape,color,boxx,boxy):
    quarter = int(BOX_SIZE * 0.25)# many of the shape drawing func calls use the
    half  = int(BOX_SIZE * 0.5)  # mid-point or quarter point of the box as well
    

    left,top = left_To_Top(boxx,boxy) # get pixel coords from board coords
    if shape == DONUT:
        pygame.draw.circle(DISPLAYSURF, color, (left + half, top + half), half - 5)
        pygame.draw.circle(DISPLAYSURF, BACKGROUND_COLOR, (left + half, top + half), quarter - 5)

    elif shape == SQUARE:
        pygame.draw.rect(DISPLAYSURF, color, (left + quarter, top + quarter, BOX_SIZE - half, BOX_SIZE - half))

    elif shape == DIAMOND:
        pygame.draw.polygon(DISPLAYSURF, color, ((left + half, top), (left + BOX_SIZE - 1, top + half), (left + half, top + BOX_SIZE - 1), (left, top + half)))


    elif shape == LINES:
        for i in range(0,BOX_SIZE,4):
             pygame.draw.line(DISPLAYSURF, color, (left, top + i), (left + i, top))
             pygame.draw.line(DISPLAYSURF, color, (left + i, top + BOX_SIZE - 1), (left + BOX_SIZE - 1, top + i))

    elif shape == OVAL:

         pygame.draw.ellipse(DISPLAYSURF, color, (left, top + quarter, BOX_SIZE, half))


# "start Game" animation
def Start_Game_Animation(board):
    #randomly reveal the 8 boxes at a time
    cover = generateRevealedBoxesData(False)
    boxes = []
    for x in range(BOARD_WIDTH):
        for y in range(BOARD_HEIGHT):
            boxes.append((x,y))
    random.shuffle(boxes)
    box_groups = split_into_groups_of(8,boxes)
    draw_Board(board,cover)
    for box in box_groups:
        revealedBoxesAnimation(board,box) # reveal the boxes 
        cover_Boxes_Animation(board,box) # cover the boxes

    






if __name__ == '__main__':

    memory_puzzle()
