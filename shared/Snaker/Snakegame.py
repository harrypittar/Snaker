import random
import pygame
import sys
import mysql.connector


from pygame.locals import *

Snakespeed = 13
Window_Width = 800
Window_Height = 500
Cell_Size = 20  # Width and height of the cells
assert Window_Width % Cell_Size == 0, "Window width must be a multiple of cell size."

# Ensuring that the cells fit perfectly in the window. eg if cell size was 10
# and window width or windowheight were 15 only 1.5 cells would fit.
assert Window_Height % Cell_Size == 0, "Window height must be a multiple of cell size."

# Ensuring that only whole integer number of cells fit perfectly in the window.
Cell_W = int(Window_Width / Cell_Size)  # Cell Width
Cell_H = int(Window_Height / Cell_Size)  # Cell Height

# Defining element colors for the program.
White = (255, 255, 255)
Black = (0, 0, 0)
Grey = (40, 40, 40)
Red = (255, 0, 0)
Green = (0, 255, 0)
DARKGreen = (0, 155, 0)
DARKGRAY = (40, 40, 40)
YELLOW = (255, 255, 0)
Red_DARK = (150, 0, 0)
BLUE = (0, 0, 255)
BLUE_DARK = (0, 0, 150)
BGCOLOR = Black  # Background color

UP = 'up'
DOWN = 'down'  # Defining keyboard keys.
LEFT = 'left'
RIGHT = 'right'

HEAD = 0  # Syntactic sugar: index of the snake's head


def main():

    global SnakespeedCLOCK, DISPLAYSURF, BASICFONT, username

    pygame.init()
    SnakespeedCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((Window_Width, Window_Height))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Snaker')

    showStartScreen()
    while True:
        runGame()
        showGameOverScreen()


def runGame():

    # Start Point
    startx = 20
    starty = 10

    wormCoords = [{'x': startx, 'y': starty},
                  {'x': startx - 1, 'y': starty},
                  {'x': startx - 2, 'y': starty}]
    direction = RIGHT


    # Start the apple in a random place.
    apple = getRandomLocation()

    while True:  # main game loop
        for event in pygame.event.get():  # event handling loop
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT) and direction != RIGHT:
                    direction = LEFT
                elif (event.key == K_RIGHT) and direction != LEFT:
                    direction = RIGHT
                elif (event.key == K_UP) and direction != DOWN:
                    direction = UP
                elif (event.key == K_DOWN) and direction != UP:
                    direction = DOWN
                elif event.key == K_ESCAPE:
                    terminate()

        # check if the Snake has hit itself or the edge
        if wormCoords[HEAD]['x'] == -1 or wormCoords[HEAD]['x'] == Cell_W or wormCoords[HEAD]['y'] == -1 or \
                wormCoords[HEAD]['y'] == Cell_H:
            return  # game over
        for wormBody in wormCoords[1:]:
            if wormBody['x'] == wormCoords[HEAD]['x'] and wormBody['y'] == wormCoords[HEAD]['y']:
                return  # game over

        # check if Snake has eaten an apple
        if wormCoords[HEAD]['x'] == apple['x'] and wormCoords[HEAD]['y'] == apple['y']:
            # don't remove worm's tail segment
            apple = getRandomLocation()  # set a new apple somewhere
        else:
            del wormCoords[-1]  # remove worm's tail segment

        # move the worm by adding a segment in the direction it is moving
        if direction == UP:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] - 1}
        elif direction == DOWN:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] + 1}
        elif direction == LEFT:
            newHead = {'x': wormCoords[HEAD]['x'] - 1, 'y': wormCoords[HEAD]['y']}
        elif direction == RIGHT:
            newHead = {'x': wormCoords[HEAD]['x'] + 1, 'y': wormCoords[HEAD]['y']}
        score = len(wormCoords) - 1
        wormCoords.insert(0, newHead)
        DISPLAYSURF.fill(BGCOLOR)
        drawGrid()
        drawWorm(wormCoords)
        drawApple(apple)
        drawScore(score)
        drawhighScore(score)
        pygame.display.update()
        SnakespeedCLOCK.tick(Snakespeed)




def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press any key to play!', True, Green)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (Window_Width - 200, Window_Height - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)





def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()
    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key


def showStartScreen():
    titleFont = pygame.font.Font('freesansbold.ttf', 70)
    titleSurf1 = titleFont.render('Snaker', True, Black, Red)

    degrees1 = 0



    while True:
        DISPLAYSURF.fill(BGCOLOR)
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (Window_Width / 2, Window_Height / 2)
        DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)


        drawPressKeyMsg()

        if checkForKeyPress():
            pygame.event.get()  # clear event queue
            return
        pygame.display.update()
        SnakespeedCLOCK.tick(Snakespeed)

        # rotate by 3 degrees each frame
        degrees1 += 5


def terminate():
    pygame.quit()
    sys.exit()


def getRandomLocation():
    return {'x': random.randint(0, Cell_W - 1), 'y': random.randint(0, Cell_H - 1)}


def showGameOverScreen():
    gameOverFont = pygame.font.Font('freesansbold.ttf', 100)
    gameSurf = gameOverFont.render('Game Over', True, Red)
    gameRect = gameSurf.get_rect()
    gameRect.midtop = (Window_Width / 2, 200)
    DISPLAYSURF.blit(gameSurf, gameRect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress()  # clear out any key presses in the event queue

    while True:
        if checkForKeyPress():
            pygame.event.get()  # clear event queue
            return


def drawScore(score):
    scoreSurf = BASICFONT.render('Score: %s' % (score), True, White)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (Window_Width - 120, 10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)


def drawhighScore(score):
    with open("highscore.txt", "r+") as hisc:
        hi = hisc.read()
        if not hi:  # not hi will only be true for strings on an empty string
            hi = '0'
        if score > int(hi):
            hisc.seek(0)  # We already read to the end. We need to go back to the start
            hisc.write(str(score))
            hisc.truncate()  # Delete anything left over... not strictly necessary
            mydb = mysql.connector.connect(host="192.168.2.12", user="webuser", passwd="insecure_db_pw", database="snaker")
            mycursor = mydb.cursor()
            mycursor.execute("INSERT INTO highscores (username, score) VALUES (%s, %s)", (username, score))

            mydb.commit()

    highscoreSurf = BASICFONT.render('Highscore: %s' % hi, True, White)
    highscoreRect = highscoreSurf.get_rect()
    highscoreRect.topright = (Window_Width - 150, 10)
    DISPLAYSURF.blit(highscoreSurf, highscoreRect)


def drawWorm(wormCoords):
    for coord in wormCoords:
        x = coord['x'] * Cell_Size
        y = coord['y'] * Cell_Size
        wormSegmentRect = pygame.Rect(x, y, Cell_Size, Cell_Size)
        pygame.draw.rect(DISPLAYSURF, DARKGreen, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, Cell_Size - 8, Cell_Size - 8)
        pygame.draw.rect(DISPLAYSURF, Green, wormInnerSegmentRect)


def drawApple(coord):
    x = coord['x'] * Cell_Size
    y = coord['y'] * Cell_Size


    appleRect = pygame.Rect(x, y, Cell_Size, Cell_Size)
    pygame.draw.rect(DISPLAYSURF, Red, appleRect)


def drawGrid():
    for x in range(0, Window_Width, Cell_Size):  # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, Window_Height))
    for y in range(0, Window_Height, Cell_Size):  # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (Window_Width, y))


if __name__ == '__main__':
    try:
        username = raw_input("Input username: ")
        main()
    except SystemExit:
        pass
