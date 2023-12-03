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

PIN_SIZE = 11
PIN_OUTLINE_SIZE = 13

FBPIN_SIZE = 6
FB_OUTLINE_SIZE = 8

GAMEMODE = 0
SUPER_MM = True
if SUPER_MM == True:
    PIN_NUMBER = 5
else: 
    PIN_NUMBER = 4

window = pyglet.window.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "Master Mind", resizable=True)
batch = pyglet.graphics.Batch()

background = shapes.Rectangle(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, color = BACKGROUND_COLOR, batch = batch)
title = pyglet.text.Label('Master Mind', font_name = 'Times New Roman', font_size=30, 
        x=SCREEN_WIDTH/4, y=SCREEN_HEIGHT - 2*GRIDSIZE, anchor_x='center', anchor_y='center')


blackCursorImage = pyglet.image.load("res/black.png")
brownCursorImage = pyglet.image.load("res/brown.png")
redCursorImage = pyglet.image.load("res/red.png")
orangeCursorImage = pyglet.image.load("res/orange.png")
yellowCursorImage = pyglet.image.load("res/yellow.png")
greenCursorImage = pyglet.image.load("res/green.png")
blueCursorImage = pyglet.image.load("res/blue.png")
grayCursorImage = pyglet.image.load("res/gray.png")
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

testCursor = window.get_system_mouse_cursor(window.CURSOR_HAND)
test2CursorImage = pyglet.image.load("res/cursor_win_default.png")
test2Cursor = pyglet.window.ImageMouseCursor(test2CursorImage, 0, 0)

#window.set_mouse_cursor(test2Cursor)
window.set_mouse_visible(True)

image = pyglet.image.load('res/red.png')
cursor = pyglet.window.ImageMouseCursor(image, 16, 8)
window.set_mouse_cursor(cursor)





class board:
    def __init__(self, mode, super):
        self.pins = [[]]
        self.feedback = [[]]
        self.activeRow = 0
        self.currentColor = (BACKGROUND_COLOR)


        if super:
            self.colors =  (RED, YELLOW, GREEN, BLUE, BLACK, WHITE, ORANGE, BROWN)
            self.solution = [1, 1, 1, 1, 1]
            self.currentGuess = [1, 1, 1, 1, 1]
        else:
            self.colors =  (RED, YELLOW, GREEN, BLUE, BLACK, WHITE)
            self.solution = [1, 1, 1, 1]
            self.currentGuess = [1, 1, 1, 1]
        

        self.super = super
        self.mode = mode

        if mode == 2 or mode == 3:
            self.colors = self.colors + (BACKGROUND_COLOR,)



    
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


    

    '''def newGuess(self, guess):
        if True or type(guess) == tuple():
            if self.super:
                if len(guess) != 5:
                    print("Please enter 5 pins!")
                    return False
            else:
                if len(guess) != 4:
                    print("Please enter 4 pins!")
                    return False
        else:
            print("Please try again!", type(guess))
            return False

        if self.pins[0] == []:
            self.pins[0] = guess
        else:
            self.pins.append(guess)'''



    def checkGuess(self):
        lastGuess = self.pins[len(self.pins) - 1]
        if self.super:
            newFeedback = [0, 0, 0, 0, 0]
        else:
            newFeedback = [0, 0, 0, 0]

        print("LAST GUESS: ", lastGuess)
        print("len(lastGuess)", len(lastGuess))

        for pin in range(len(lastGuess)):
            if lastGuess[pin] in self.solution:
                if lastGuess[pin] == self.solution[pin]:
                    newFeedback[pin] = BLACK
                else:
                    newFeedback[pin] = WHITE
            else:
                newFeedback[pin] = 0
        
        #Insert newFeedback into feedback
        if self.feedback[0] == []:
            self.feedback[0] = newFeedback
        else:
            self.feedback.append(newFeedback)
    
        def sortKey(input):
            if input == BLACK:
                return 0
            elif input == WHITE:
                return 1
            elif input == 0:
                return 2

        self.feedback[len(self.feedback) - 1].sort(key=sortKey)
        self.activeRow += 1

    def drawPins(self):
        for row in range(len(self.pins)):
            for col in range(len(self.pins[0])):
                pin(self.pins[row][col], PIN_SIZE, row = row, col = col)


    def drawBoard(self):
        background.draw()
        title.draw()
        for row in range(12):
            for col in range(PIN_NUMBER):
                newPin = pin(OUTLINE_COLOR, PIN_OUTLINE_SIZE, row = row, col = col)
                newPin.draw()
                newPin = pin(BACKGROUND_COLOR, PIN_SIZE, row=row, col=col)
                newPin.draw()

                fbPin(OUTLINE_COLOR, row, col, FB_OUTLINE_SIZE)
                fbPin(BACKGROUND_COLOR, row, col, FBPIN_SIZE)

 

class pin:
    def __init__(self, pinColor, rad, x = 0, y = 0, row = 0, col = 0):
        self.circle = shapes.Circle(col * GRIDSIZE + GRIDSIZE, GRIDSIZE + row * GRIDSIZE , rad, color = pinColor, batch = batch)
        self.velx = 0
        self.vely = 0
    
    def draw(self):
        self.circle.draw()
    
    def update(self, dt):
        self.circle.x = self.velx * dt
        self.circle.y = self.vely * dt

    
class fbPin:
    def __init__(self, color, row, col, rad):
        circle = shapes.Circle(7.5 * GRIDSIZE + col * GRIDSIZE, GRIDSIZE + row * GRIDSIZE, rad, color = color, batch = batch)
        circle.draw()









def main():
    Board = board(GAMEMODE, SUPER_MM)
    Board.randomizeSolution()
    
    newGuess = True
    
    testBall = pin(RED, 20, col = 5, row = 5)
    testBall.velx = -5
    testBall.vely = -5
    
    while True:
        @window.event
        def on_key_press(symbol, modifiers):
            global newGuess
            print("Key pressed")
            if symbol == key.ENTER:
                print("Submitted")
                newGuess = True
            elif symbol == key.LEFT:
                testBall.circle.x = 50
                testBall.circle.y  =50
                window.flip()
            elif symbol == key.RIGHT:
                testBall.circle.x = 100
                testBall.circle.y = 100
                window.flip()

        if newGuess ==True:
            #Board.newGuess() 
            @window.event
            def on_draw():
                window.clear()
                Board.drawBoard()
                #Board.drawRow() 
                #testBall.draw()
            
            @window.event
            def on_mouse_motion(x, y, dx, dy):
                redCursor.draw(x, y)
                print("Cursor drawn")

            @window.event
            def on_mouse_press(x, y, button, modifiers):
                y_min = (GRIDSIZE + Board.activeRow * GRIDSIZE) - PIN_SIZE
                y_max = y_min + 2*PIN_SIZE

                x0_min = 2*GRIDSIZE - PIN_SIZE
                x0_max = x0_min + 2*PIN_SIZE
                x1_min = 3*GRIDSIZE - PIN_SIZE
                x1_max = x1_min + 2*PIN_SIZE
                x2_min = 4*GRIDSIZE - PIN_SIZE
                x2_max = x2_min + 2*PIN_SIZE
                x3_min = 5*GRIDSIZE - PIN_SIZE
                x3_max = x3_min + 2*PIN_SIZE
                x4_min = 6*GRIDSIZE - PIN_SIZE
                x4_max = x4_min + 2*PIN_SIZE


                if (y_min < y < y_max):
                    if (x0_min < x < x0_max):
                        Board.currentGuess[0] = Board.currentColor
                        pin()
                        

            newGuess = False 
            
        #pyglet.clock.schedule_interval(testBall.update, 1/60.0)
        pyglet.app.run()


main()

    

'''
Board1 = board(0, False)
Board2 = board(1, False)
Board3 = board(2, False)
Board4 = board(3, False)

Board1.randomizeSolution()
Board2.randomizeSolution()
Board3.randomizeSolution()
Board4.randomizeSolution()

print(Board1.solution)
print(Board2.solution)
print(Board3.solution)
print(Board4.solution)

Board = board(0, False)
#Board.randomizeSolution()

Board.solution = ["GREEN", "BLUE", "RED", "BLACK"]
Board.newGuess(["RED", "WHITE", "BLUE", "BLACK"])
Board.checkGuess()
print(Board.feedback)

print("SOLUTION: ", Board.solution)
'''

'''
    pinSprite = pyglet.sprite.Sprite(pyglet.image.load("red.png"), x= 50, y=50)
    pinSprite.draw()
    pinSprite.delete()
    pinSprite.remove()
    pass'''