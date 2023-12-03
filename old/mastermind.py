import random
import pygame
import sys

class board:
    def __init__(self):
        self.pins = [[]]
        self.solution = [1, 1, 1, 1]
    
    def randomizeSolution(self, mode):
        for place in range(len(self.solution)):
            
            if mode == 0:
                newPin = random.choice(("RED", "YELLOW", "GREEN", "BLUE", "BLACK", "WHITE"))
                while newPin in self.solution:
                    newPin = random.choice(("RED", "YELLOW", "GREEN", "BLUE", "BLACK", "WHITE"))
                self.solution[place] = newPin
            
            if mode == 1:
                newPin = random.choice(("RED", "YELLOW", "GREEN", "BLUE", "BLACK", "WHITE"))
                self.solution[place] = newPin
            
            if mode == 2:
                newPin = random.choice((0, "RED", "YELLOW", "GREEN", "BLUE", "BLACK", "WHITE"))
                while newPin in self.solution:
                    newPin = random.choice((0, "RED", "YELLOW", "GREEN", "BLUE", "BLACK", "WHITE"))
                self.solution[place] = newPin
            
            if mode == 3:
                newPin = random.choice((0, "RED", "YELLOW", "GREEN", "BLUE", "BLACK", "WHITE"))
                self.solution[place] = newPin


    def newGuess(self):
        pass

    def checkGuess(self):
        pass

Board = board()

Board.randomizeSolution(0)
print(Board.solution)
Board.randomizeSolution(1)
print(Board.solution)
Board.randomizeSolution(2)
print(Board.solution)
Board.randomizeSolution(3)

print(Board.solution)