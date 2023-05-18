import pygame
import random
import time
from time import sleep
from pygame import *

global white
white = (255, 255, 255)
global black
black = (0, 0, 0)

def randomPiece():
    x = random.randint(1, 7)
    if x == 1:
        return 'O'
    if x == 2:
        return 'I'
    if x == 3:
        return 'T'
    if x == 4:
        return 'J'
    if x == 5:
        return 'L'
    if x == 6:
        return 'S'
    if x == 7:
        return 'Z'


class GameBoard:
    def __init__(self):
        self.board = []
        for i in range(24):
            self.board.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

    def printBoard(self):
        for i in self.board:
            print(i)

    def turnOn(self, y, x):
        self.board[y][x] = 1

    def turnOff(self, y, x):
        self.board[y][x] = 0

    def iterate(self, y, x):
        self.board[y][x] += 1

    def drawBoard(self, scr):
        for i in range(20):
            for j in range(10):
                if self.board[i+4][j] == 1:
                    pygame.draw.rect(scr, white, (j*30, i*30, 30, 30))

    def getBoard(self):
        return self.board

    def getVal(self, y, x):
        return self.board[y][x]

    def clearLines(self):
        for i in range(23,3,-1):
            allOne = True
            for j in range(10):
                if self.board[i][j] == 0:
                    allOne = False
                    break
            if allOne:
                for j in range(i, 4, -1):
                    for k in range(10):
                        self.board[j][k] = self.getVal(j-1, k)
                return 1 + self.clearLines()
        return 0

    def topOpen(self):
        for i in range(4):
            for j in range(10):
                if self.board[i][j] == 1:
                    return False
        return True





class Piece:
    def __init__(self, x):
        self.piece = x
        self.rotation = 0
        self.shape = []
        self.tileX = 3
        self.tileY = 0
        self.indicies = []
        for i in range(4):
            self.shape.append([0, 0, 0, 0])
        if x == 'O':
            self.shape[1][1] = 1
            self.shape[1][2] = 1
            self.shape[2][1] = 1
            self.shape[2][2] = 1
        elif x == 'I':
            for i in range(4):
                self.shape[1][i] = 1
        elif x == 'T':
            for i in range(3):
                self.shape[1][i] = 1
            self.shape[2][1] = 1
        elif x == 'J':
            for i in range(3):
                self.shape[1][i] = 1
            self.shape[2][2] = 1
        elif x == 'L':
            for i in range(3):
                self.shape[1][i] = 1
            self.shape[2][0] = 1
        elif x == 'S':
            self.shape[1][1] = 1
            self.shape[1][2] = 1
            self.shape[2][0] = 1
            self.shape[2][1] = 1
        elif x == 'Z':
            self.shape[1][0] = 1
            self.shape[1][1] = 1
            self.shape[2][1] = 1
            self.shape[2][2] = 1

    def nextRot(self, r):
        if r == 4:
            r = 0
        elif r == -1:
            r = 3
        temp = []
        for i in range(4):
            temp.append([0, 0, 0, 0])
        if self.piece == 'O':
            return self.shape
        elif self.piece == 'I':
            if r % 2 == 0:
                for i in range(4):
                    temp[1][i] = 1
            else:
                for i in range(4):
                    temp[i][2] = 1
        elif self.piece == 'T':
            if r == 0:
                for i in range(3):
                    temp[1][i] = 1
                temp[2][1] = 1
            elif r == 1:
                for i in range(3):
                    temp[i][1] = 1
                temp[1][0] = 1
            elif r == 2:
                for i in range(3):
                    temp[2][i] = 1
                temp[1][1] = 1
            else:
                for i in range(3):
                    temp[i][1] = 1
                temp[1][2] = 1
        elif self.piece == 'J':
            if r == 0:
                for i in range(3):
                    temp[1][i] = 1
                temp[2][2] = 1
            elif r == 1:
                for i in range(3):
                    temp[i][1] = 1
                temp[2][0] = 1
            elif r == 2:
                for i in range(3):
                    temp[2][i] = 1
                temp[1][0] = 1
            else:
                for i in range(3):
                    temp[i][1] = 1
                temp[0][2] = 1
        elif self.piece == 'L':
            if r == 0:
                for i in range(3):
                    temp[1][i] = 1
                temp[2][0] = 1
            elif r == 1:
                for i in range(3):
                    temp[i][1] = 1
                temp[0][0] = 1
            elif r == 2:
                for i in range(3):
                    temp[2][i] = 1
                temp[1][2] = 1
            else:
                for i in range(3):
                    temp[i][1] = 1
                temp[2][2] = 1
        elif self.piece == 'S':
            if r % 2 == 0:
                temp[1][1] = 1
                temp[1][2] = 1
                temp[2][0] = 1
                temp[2][1] = 1
            else:
                temp[0][0] = 1
                temp[1][0] = 1
                temp[1][1] = 1
                temp[2][1] = 1
        elif self.piece == 'Z':
            if r % 2 == 0:
                temp[1][0] = 1
                temp[1][1] = 1
                temp[2][1] = 1
                temp[2][2] = 1
            else:
                temp[0][2] = 1
                temp[1][2] = 1
                temp[1][1] = 1
                temp[2][1] = 1
        return temp

    def rotate(self, shift, board, scr):
        temp = GameBoard()
        for i in range(24):
            for j in range(10):
                if board.getVal(i, j) == 1:
                    temp.turnOn(i, j)
        newIndex = []
        newShape = self.nextRot(self.rotation + 1)
        for i in range(4):
            for j in range(4):
                if newShape[i][j] == 1:
                    newIndex.append(self.tileY+i)
                    newIndex.append(self.tileX+j+shift)
        for i in range(4):
            if newIndex[2*i+1] > 9 or newIndex[2*i+1] < 0:
                if shift == 0:
                    return self.rotate(-1, board, scr)
                if shift == -1:
                    return self.rotate(1, board, scr)
                return board
        for i in range(4):
            temp.turnOff(self.indicies[2*i], self.indicies[2*i+1])
        temp.drawBoard(scr)
        for i in range(4):
            temp.iterate(newIndex[2*i], newIndex[2*i+1])
        for i in temp.getBoard():
            for j in i:
                if j > 1:
                    if shift == 0:
                        return self.rotate(-1, board, scr)
                    if shift == -1:
                        return self.rotate(1, board, scr)
                    return board
        self.tileX += shift
        self.rotation += 1
        if self.rotation == 4:
            self.rotation = 0
        self.shape = self.nextRot(self.rotation)
        self.indicies = []
        for i in range(8):
            self.indicies.append(newIndex[i])
        return temp

    def getShape(self):
        return self.shape

    def seePiece(self):
        print(self.indicies)

    def getType(self):
        return self.piece

    def initialize(self, board):
        for i in range(4):
            for j in range(4):
                if self.shape[i][j] == 1:
                    board.turnOn(self.tileY+i, self.tileX+j)
                    self.indicies.append(self.tileY+i)
                    self.indicies.append(self.tileX+j)

    def moveDown(self, board, scr):
        temp = GameBoard()
        for i in range(24):
            for j in range(10):
                if board.getVal(i, j) == 1:
                    temp.turnOn(i, j)
        for i in range(4):
            temp.turnOff(self.indicies[2*i], self.indicies[2*i+1])
        temp.drawBoard(scr)
        for i in range(4):
            if self.indicies[2*i] == 23:
                return [False, board]
            temp.iterate(self.indicies[2*i]+1, self.indicies[2*i+1])
        for i in temp.getBoard():
            for j in i:
                if j > 1:
                    return [False, board]
        for i in range(4):
            self.indicies[2*i] += 1
        self.tileY += 1
        return [True, temp]

    def moveHorizontal(self, dir, board, scr):
        temp = GameBoard()
        for i in range(24):
            for j in range(10):
                if board.getVal(i, j) == 1:
                    temp.turnOn(i, j)
        for i in range(4):
            temp.turnOff(self.indicies[2*i], self.indicies[2*i+1])
            if (dir == -1 and self.indicies[2*i+1] == 0) or (dir == 1 and self.indicies[2*i+1] == 9):
                return board
        temp.drawBoard(scr)
        for i in range(4):
            temp.iterate(self.indicies[2*i], self.indicies[2*i+1]+dir)
        for i in temp.getBoard():
            for j in i:
                if j > 1:
                    return board
        for i in range(4):
            self.indicies[2*i+1] += dir
        self.tileX += dir
        return temp

class Display:
    def __init__(self, len, val, xp, yp, scr):
        self.nums = []
        self.l = len
        self.v = val
        self.x = xp
        self.y = yp
        self.val = 0
        self.s = scr
        for i in range(len):
            self.nums.append(SevenSeg(0, self.x + 30 * i, self.y, self.s))

    def updateVal(self, val):
        self.v = val
        temp = val
        for i in range(len(self.nums) - 1, -1, -1):
            self.nums[i].setVal(temp % 10)
            temp = (int)(temp / 10)

    def draw(self):
        for i in self.nums:
            i.draw()



class SevenSeg:
    def __init__(self, v, xPos, yPos, scr):
        self.data = []
        v = str(v)
        self.setVal(v)
        self.x = xPos
        self.y = yPos
        self.s = scr

    def setVal(self, val):
        val = str(val)
        if val == '1':
            self.data = [False, False, True, False, False, True, False]
        elif val == '2':
            self.data = [True, False, True, True, True, False, True]
        elif val == '3':
            self.data = [True, False, True, True, False, True, True]
        elif val == '4':
            self.data = [False, True, True, True, False, True, False]
        elif val == '5':
            self.data = [True, True, False, True, False, True, True]
        elif val == '6':
            self.data = [True, True, False, True, True, True, True]
        elif val == '7':
            self.data = [True, False, True, False, False, True, False]
        elif val == '8':
            self.data = [True, True, True, True, True, True, True]
        elif val == '9':
            self.data = [True, True, True, True, False, True, True]
        elif val == '0':
            self.data = [True, True, True, False, True, True, True]

    def draw(self):
        if self.data[0]:
            pygame.draw.rect(self.s, white, (self.x, self.y, 20, 3))
        if self.data[1]:
            pygame.draw.rect(self.s, white, (self.x, self.y, 3, 14))
        if self.data[2]:
            pygame.draw.rect(self.s, white, (self.x + 17, self.y, 3, 14))
        if self.data[3]:
            pygame.draw.rect(self.s, white, (self.x, self.y + 11, 20, 3))
        if self.data[4]:
            pygame.draw.rect(self.s, white, (self.x, self.y + 12, 3, 15))
        if self.data[5]:
            pygame.draw.rect(self.s, white, (self.x + 17, self.y + 12, 3, 15))
        if self.data[6]:
            pygame.draw.rect(self.s, white, (self.x, self.y + 24, 20, 3))

def main():
    pygame.init()
    screen = pygame.display.set_mode([450, 600])
    random.seed()
    game = GameBoard()
    block = Piece(randomPiece())
    block.initialize(game)
    next = Piece(randomPiece())
    running = True
    tickClock = 0
    lineClear = 0
    goal = 10
    tickMax = 60
    score = Display(3, 0, 350, 250, screen)
    clock = pygame.time.Clock()
    noPiece = False
    while running:
        clock.tick(60)
        screen.fill(black)
        pygame.draw.rect(screen, white, (300, 0, 10, 600))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game = block.moveHorizontal(-1, game, screen)
                if event.key == pygame.K_RIGHT:
                    game = block.moveHorizontal(1, game, screen)
                if event.key == pygame.K_z:
                    game = block.rotate(0, game, screen)
        pressed_keys = pygame.key.get_pressed()
        if noPiece:
            lineClear += game.clearLines()
            if game.topOpen():
                block = Piece(next.getType())
                next = Piece(randomPiece())
                block.initialize(game)
                noPiece = False
            else:
                sleep(1)
                running = False
        if tickClock == tickMax:
            down = block.moveDown(game, screen)
            if not down[0]:
                noPiece = True
            game = down[1]
            tickClock = 1
        if tickClock % 2 == 0 and pressed_keys[K_DOWN]:
            down = block.moveDown(game, screen)
            if not down[0]:
                noPiece = True
            game = down[1]
        if lineClear == goal:
            tickClock -= 6
            if tickClock == 0:
                tickClock = 6
            goal += 10
        tickClock += 1
        game.drawBoard(screen)
        score.updateVal(lineClear)
        score.draw()
        for i in range(4):
            for j in range(4):
                if next.getShape()[i][j] == 1:
                    pygame.draw.rect(screen, white, (350+20*j, 150+20*i, 20, 20))
        pygame.display.update()
    print(lineClear)


main()
