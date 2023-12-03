import random
import pyglet
import sys
from pyglet import shapes
from pyglet.window import key
from pyglet import clock
import time




SCREEN_WIDTH = 500
SCREEN_HEIGHT = 700

GRIDSIZE = 40
GRIDWIDTH = SCREEN_WIDTH / GRIDSIZE
GRIDHEIGHT = SCREEN_HEIGHT / GRIDSIZE

BLACK = (0, 0, 0)
BROWN = (60, 41, 9)
RED = (242, 6, 6)
ORANGE = (253, 98, 3)
YELLOW = (255, 255, 0)
GREEN = (7, 141, 7)
BLUE = (28, 44, 237)
WHITE = (255, 255, 255)

BACKGROUND_COLOR = (31, 31, 31)
OUTLINE_COLOR = (75, 75, 75)

FONT = "Times New Roman"

PIN_SIZE = 11
PIN_OUTLINE_SIZE = 13

FBPIN_SIZE = 6
FB_OUTLINE_SIZE = 8

GAMEMODE = 0
SUPER_MM = False


window = pyglet.window.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "Master Mind", resizable=True)
window.set_location(500, 0)

#badBatch = pyglet.graphics.Batch()

layer0 = pyglet.graphics.OrderedGroup(0)
layer1 = pyglet.graphics.OrderedGroup(1)
layer2 = pyglet.graphics.OrderedGroup(2)
layer3 = pyglet.graphics.OrderedGroup(3)




blackCursorImage = pyglet.image.load("res/black.png")
brownCursorImage = pyglet.image.load("res/brown.png")
redCursorImage = pyglet.image.load("res/red.png")
orangeCursorImage = pyglet.image.load("res/orange.png")
yellowCursorImage = pyglet.image.load("res/yellow.png")
greenCursorImage = pyglet.image.load("res/green.png")
blueCursorImage = pyglet.image.load("res/blue.png")
grayCursorImage = pyglet.image.load("res/gray2.png")
whiteCursorImage = pyglet.image.load("res/white.png")

blackCursor = pyglet.window.ImageMouseCursor(blackCursorImage, 11, 11)
brownCursor = pyglet.window.ImageMouseCursor(brownCursorImage, 11, 11)
redCursor = pyglet.window.ImageMouseCursor(redCursorImage, 11, 11)
orangeCursor = pyglet.window.ImageMouseCursor(orangeCursorImage, 11, 11)
yellowCursor = pyglet.window.ImageMouseCursor(yellowCursorImage, 11, 11)
greenCursor = pyglet.window.ImageMouseCursor(greenCursorImage, 11, 11)
blueCursor = pyglet.window.ImageMouseCursor(blueCursorImage, 11, 11)
grayCursor = pyglet.window.ImageMouseCursor(grayCursorImage, 11, 11)
whiteCursor = pyglet.window.ImageMouseCursor(whiteCursorImage, 11, 11)

x0_min = 1*GRIDSIZE - PIN_SIZE
x0_max = x0_min + 2*PIN_SIZE
x1_min = 2*GRIDSIZE - PIN_SIZE
x1_max = x1_min + 2*PIN_SIZE
x2_min = 3*GRIDSIZE - PIN_SIZE
x2_max = x2_min + 2*PIN_SIZE
x3_min = 4*GRIDSIZE - PIN_SIZE
x3_max = x3_min + 2*PIN_SIZE
x4_min = 5*GRIDSIZE - PIN_SIZE
x4_max = x4_min + 2*PIN_SIZE







class board:
    def __init__(self, mode, supermm):

        global badBatch
        badBatch = pyglet.graphics.Batch()

        self.pins = []
        self.numbers = []
        self.activeRow = 0
        self.currentColor = (BLACK)
        self.correct = False

        if supermm:
            self.colors =  [RED, YELLOW, GREEN, BLUE, BLACK, WHITE, ORANGE, BROWN]
            self.possibleColors = [BLACK, BROWN, RED, ORANGE, YELLOW, GREEN, BLUE, WHITE]
            self.solution = [1, 1, 1, 1, 1]
            self.currentGuess = [1, 1, 1, 1, 1]
            self.currentFeedback = [1, 1, 1, 1, 1]
            self.pinNumber = 5
        else:
            self.colors =  [RED, YELLOW, GREEN, BLUE, BLACK, WHITE]
            self.possibleColors = [BLACK, RED, YELLOW, GREEN, BLUE, WHITE]
            self.solution = [1, 1, 1, 1]
            self.currentGuess = [1, 1, 1, 1]
            self.currentFeedback = [1, 1, 1, 1]
            self.pinNumber = 4
        

        self.superMM = supermm
        self.mode = mode

        if mode == 2 or mode == 3:
            self.colors.append(BACKGROUND_COLOR)
            self.possibleColors.append(BACKGROUND_COLOR)

        self.randomizeSolution()
        self.drawBoard()

    
    def randomizeSolution(self):
        for place in range(len(self.solution)):
            
            if self.mode == 0 or self.mode == 2:
                newPin = random.choice(self.colors)
                while newPin in self.solution:
                    newPin = random.choice(self.colors)
                
                self.solution[place] = newPin
            
            else:
                newPin = random.choice(self.colors)
                self.solution[place] = newPin

        for col in range(self.pinNumber):
            self.pins.append(pin(OUTLINE_COLOR, 13, col ,PIN_OUTLINE_SIZE))
            self.pins.append(pin(self.solution[col], 13, col, PIN_SIZE))


    def checkGuess(self):

        for PIN in range(self.pinNumber):
            if self.currentGuess[PIN] in self.solution:
                if self.currentGuess[PIN] == self.solution[PIN]:
                    self.currentFeedback[PIN] = BLACK
                else:
                    self.currentFeedback[PIN] = WHITE
            else:
                self.currentFeedback[PIN] = BACKGROUND_COLOR

            
        def sortKey(input):
            if input == BLACK:
                return 0
            elif input == WHITE:
                return 1
            elif input == BACKGROUND_COLOR:
                return 2

        self.currentFeedback.sort(key=sortKey)
        self.drawFBPins()
        print(self.solution)

        if self.currentGuess == self.solution:
            self.title.y += 2*GRIDSIZE
            self.textBoxOutline.y += 2*GRIDSIZE
            self.textBox.y += 2*GRIDSIZE
            self.correct = True
        else:


            if self.superMM:
                self.currentFeedback = [1, 1, 1, 1, 1]
                self.currentGuess = [1, 1, 1, 1, 1]
            else:
                self.currentFeedback = [1, 1, 1, 1]
                self.currentGuess = [1, 1, 1, 1]

            self.activeRow += 1



    def drawFBPins(self):
        for col in range(4):
            self.pins.append(pin(self.currentFeedback[col], self.activeRow, col, FBPIN_SIZE, fb = True))

    def drawBoard(self):
        self.background = shapes.Rectangle(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, color = BACKGROUND_COLOR,
            batch = badBatch, group = layer0)
        
        self.textBoxOutline = shapes.Rectangle((SCREEN_WIDTH / 4)- (245 / 2), 14*GRIDSIZE- 60/2, 245, 60, color = OUTLINE_COLOR, 
            batch = badBatch, group = layer2)
        
        self.textBox = shapes.Rectangle(SCREEN_WIDTH / 4 - 235 / 2, 14*GRIDSIZE - 50/2, 235, 50, color = BACKGROUND_COLOR, 
            batch = badBatch, group = layer2)
        
        self.title = pyglet.text.Label('Master Mind', font_name = FONT, font_size=30, 
            x=SCREEN_WIDTH/4, y=14*GRIDSIZE, anchor_x='center', anchor_y='center', 
            batch = badBatch, group = layer3)

        if self.superMM:
            sStr = "Mode:   S " + str(self.mode + 1)
        else:
            sStr = "Mode:   " + str(self.mode + 1)

        self.modeText = pyglet.text.Label(sStr, font_name = FONT, font_size = 25, 
            x = SCREEN_WIDTH/2 + 40, y = 16*GRIDSIZE, batch = badBatch, group = layer1)
        
        for row in range(12):
            self.numbers.append(pyglet.text.Label(str(row + 1), font_name = FONT, font_size = 14, 
                x = 6.25*GRIDSIZE, y = (1+row)*GRIDSIZE, anchor_x = "center", anchor_y = "center", 
                batch = badBatch, group = layer1))

        for row in range(12):
            for col in range(self.pinNumber):
                self.pins.append(pin(OUTLINE_COLOR, row,col,PIN_OUTLINE_SIZE))
                self.pins.append(pin(BACKGROUND_COLOR, row, col, PIN_SIZE))
                self.pins.append(pin(OUTLINE_COLOR, row, col, FB_OUTLINE_SIZE, fb = True))
                self.pins.append(pin(BACKGROUND_COLOR, row, col, FBPIN_SIZE, fb = True))

    def changeColor(self, dir):
        colorIndex = self.possibleColors.index(self.currentColor)
        if dir == 1 and colorIndex == 0:
            self.currentColor = self.possibleColors[len(self.possibleColors) - 1]
        elif dir == -1 and (colorIndex == len(self.possibleColors) - 1):
            self.currentColor = self.possibleColors[0]
        else:
            self.currentColor = self.possibleColors[colorIndex - dir]
        if self.currentColor == BLACK: window.set_mouse_cursor(blackCursor)
        if self.currentColor == BROWN: window.set_mouse_cursor(brownCursor)
        if self.currentColor == RED: window.set_mouse_cursor(redCursor)
        if self.currentColor == ORANGE: window.set_mouse_cursor(orangeCursor)
        if self.currentColor == YELLOW: window.set_mouse_cursor(yellowCursor)
        if self.currentColor == GREEN: window.set_mouse_cursor(greenCursor)
        if self.currentColor == BLUE: window.set_mouse_cursor(blueCursor)
        if self.currentColor == BACKGROUND_COLOR: window.set_mouse_cursor(grayCursor)
        if self.currentColor == WHITE: window.set_mouse_cursor(whiteCursor)





class pin:
    def __init__(self, pinColor, row, col, rad, fb = False):
        if not fb:
            self.circle = shapes.Circle(col * GRIDSIZE + GRIDSIZE, GRIDSIZE + row * GRIDSIZE , rad, color = pinColor, batch = badBatch, group = layer1)
        else: 
            self.circle = shapes.Circle((7.5+col)*GRIDSIZE, (1+row)*GRIDSIZE, rad, color = pinColor, batch = badBatch, group = layer1)









Board = board(GAMEMODE, SUPER_MM)

s = False

@window.event
def on_key_press(symbol, modifiers):
    global Board, s, badBatch
    if symbol == key.S:
        s = True

    if symbol == key.ENTER:
        if Board.correct == False:
            Board.checkGuess()
        s = False
    elif symbol == key._1:
        del Board
        del badBatch
        if s == True:
            Board = board(0, True)
        else:
            Board = board(0, False)
        s = False
    elif symbol == key._2:
        del Board
        del badBatch
        if s == True:
            Board = board(1, True)
        else:
            Board = board(1, False)
        s = False
    elif symbol == key._3:
        del Board
        del badBatch
        if s == True:
            Board = board(2, True)
        else:
            Board = board(2, False)
        s = False
    elif symbol == key._4:
        del Board
        del badBatch
        if s == True:
            Board = board(3, True)
        else:
            Board = board(3, False)
        s = False
    

    

@window.event
def on_draw():
    window.clear()
    badBatch.draw()

@window.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
    if scroll_y != 0:
        Board.changeColor(scroll_y)
        

@window.event
def on_mouse_motion(x, y, dx, dy):
    window.set_mouse_visible(True)


@window.event
def on_mouse_press(x, y, button, modifiers):
    y_min = (GRIDSIZE + Board.activeRow * GRIDSIZE) - PIN_SIZE
    y_max = y_min + 2*PIN_SIZE

    if (y_min < y < y_max)and Board.correct == False:
        if (x0_min < x < x0_max): 
            Board.pins.append(pin(Board.currentColor, Board.activeRow, 0, PIN_SIZE))
            Board.currentGuess[0] = Board.currentColor
        if (x1_min < x < x1_max): 
            Board.pins.append(pin(Board.currentColor, Board.activeRow, 1, PIN_SIZE))
            Board.currentGuess[1] = Board.currentColor
        if (x2_min < x < x2_max): 
            Board.pins.append(pin(Board.currentColor, Board.activeRow, 2, PIN_SIZE))
            Board.currentGuess[2] = Board.currentColor
        if (x3_min < x < x3_max): 
            Board.pins.append(pin(Board.currentColor, Board.activeRow, 3, PIN_SIZE))
            Board.currentGuess[3] = Board.currentColor
        if (x4_min < x < x4_max) and SUPER_MM == True: 
            Board.pins.append(pin(Board.currentColor, Board.activeRow, 4, PIN_SIZE))
            Board.currentGuess[4] = Board.currentColor


pyglet.app.run()