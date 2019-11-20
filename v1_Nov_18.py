from cmu_112_graphics import *
from tkinter import *
import copy

class RubiksCube(object):
    neighborSides = {0:[4,1,5,3],1:[4,2,5,0],2:[4,3,5,1],3:[4,0,5,2],4:[3,2,1,0],5:[1,2,3,0]}
    moves = {'F':1, 'R':2, 'L':0, 'U':4, 'D':5, 'B':3}
    def __init__(self, app):
        self.sides = ['green', 'red', 'blue', 'orange', 'white', 'yellow']
        self.rows = 3
        self.cols = 3
        self.app = app
        self.cube = self.createCube()
        self.colorCount = {'green':1, 'red':1, 'blue':1, 'orange':1, 'white':1, 'yellow':1}
        
    def createCube(self):
        cube = []
        for side in range(len(self.sides)):
            side = []
            for row in range(self.rows):
                row = []
                for col in range(self.cols):
                    row += [None]
                side += [row]
            cube += [side]
        for side in range(len(self.sides)):
            cube[side][1][1] = self.sides[side]
        return cube

    def addColors(self, color, side, row, col):
        currColor = self.cube[side][row][col]
        if currColor == None:
            self.colorCount[color] += 1
        else:
            self.colorCount[currColor] -= 1
            self.colorCount[color] += 1
        if self.colorCount[color] > 9:
            messagebox.showerror('Error', f"Can't add more {color}s")    
        else:
            self.cube[side][row][col] = color


    def printCube(self):
        for side in range(len(self.sides)):
            print('\n')
            for row in range(self.rows):
                print(self.cube[side][row])

    def getCellBounds(self, row, col):
        gridWidth  = self.app.width/4
        gridHeight = self.app.height/3
        columnWidth = gridWidth / self.cols
        rowHeight = gridHeight / self.rows
        x0 = col * columnWidth
        x1 = (col+1) * columnWidth
        y0 = row * rowHeight
        y1 = (row+1) * rowHeight
        return (x0, y0, x1, y1)
    #modified from http://www.cs.cmu.edu/~112/notes/notes-animations-part1.html

    def getSide(self, x, y):
        gridWidth  = self.app.width/4
        gridHeight = self.app.height/3
        if ((y > gridHeight) and (y < 2*gridHeight)):
            return int(x/gridWidth)
        elif ((y < gridHeight) and ((x>gridWidth) and (x < 2* gridWidth))):
            return 4
        elif ((y > 2*gridHeight) and ((x>gridWidth) and (x < 2* gridWidth))):
            return 5
        else:
            return None

    def getCell(self, x, y, side):
        gridWidth  = self.app.width/4
        gridHeight = self.app.height/3
        columnWidth = gridWidth / self.cols
        rowHeight = gridHeight / self.rows
        if side <= 3:
            col = int(x/columnWidth)
            col = col % 3
            row = int((y-gridHeight)/rowHeight)
        elif side == 4:
            row = int(y/rowHeight)
            col = int((x - gridWidth)/columnWidth)
        elif side == 5:
            row = int((y-2*gridHeight)/rowHeight)
            col = int((x - gridWidth)/columnWidth)
        return (row, col)
    #modified from http://www.cs.cmu.edu/~112/notes/notes-animations-part1.html

    def drawCube(self,canvas):
        sideWidth = self.app.width/4
        sideHeight = self.app.height/3
        for side in range(len(self.sides)):
            for row in range(self.rows):
                for col in range(self.cols):
                    (x0, y0, x1, y1) = self.getCellBounds(row, col)
                    fill = self.cube[side][row][col]
                    if (side == 4):
                        canvas.create_rectangle(x0 + sideWidth, y0, x1 + sideWidth, y1, fill = fill)
                    elif (side == 5):
                        canvas.create_rectangle(x0 + sideWidth, y0 + 2*sideHeight, x1 + sideWidth, y1 + 2*sideHeight, fill = fill)
                    else:
                        canvas.create_rectangle(x0 + side*sideWidth, y0 + sideHeight, x1 + side*sideWidth, y1 + sideHeight, fill = fill)

    def transpose(self, side):
        cube = copy.deepcopy(self.cube)
        for row in range(3):
            for col in range(3):
                cube[side][col][3-row-1] = self.cube[side][row][col]
        self.cube = copy.deepcopy(cube)

    def shiftSidesF(self,side):
        cube = copy.deepcopy(self.cube)
        adjacentSides = RubiksCube.neighborSides[side]
        for sides in range(len(adjacentSides)):
            currSide = adjacentSides[sides]
            nextSide = adjacentSides[(sides+1)%4]
            for row in range(3):
                if sides == 0:
                    cube[nextSide][row][0] = self.cube[currSide][2][row]
                elif sides == 1:
                    cube[nextSide][0][3-row-1] = self.cube[currSide][row][0]
                elif sides == 2:
                    cube[nextSide][row][2] = self.cube[currSide][0][row]
                else:
                    cube[nextSide][2][3-row-1] = self.cube[currSide][row][2]
        self.cube = copy.deepcopy(cube)

        
    def shiftSidesB(self,side):
        cube = copy.deepcopy(self.cube)
        adjacentSides = RubiksCube.neighborSides[side]
        for sides in range(len(adjacentSides)):
            currSide = adjacentSides[sides]
            nextSide = adjacentSides[(sides+1)%4]
            for row in range(3):
                if sides == 0:
                    cube[nextSide][3-row-1][0] = self.cube[currSide][0][row]
                elif sides == 1:
                    cube[nextSide][2][row] = self.cube[currSide][row][0]
                elif sides == 2:
                    cube[nextSide][3-row-1][2] = self.cube[currSide][2][row]
                else:
                    cube[nextSide][0][row] = self.cube[currSide][row][2]
        self.cube = copy.deepcopy(cube)
    
    def rotateHorizontal(self, side,row):
        cube = copy.deepcopy(self.cube)
        adjacentSides = RubiksCube.neighborSides[side]
        for sides in range(len(adjacentSides)):
            currSide = adjacentSides[sides]
            nextSide = adjacentSides[(sides+1)%4]
            for col in range(3):
                cube[nextSide][row][col] = self.cube[currSide][row][col]
        self.cube = copy.deepcopy(cube)
    
    def rotateVerticalR(self, side):
        cube = copy.deepcopy(self.cube)
        adjacentSides = RubiksCube.neighborSides[side]
        for sides in range(len(adjacentSides)):
            currSide = adjacentSides[sides]
            nextSide = adjacentSides[(sides+1)%4]
            for row in range(3):
                if (currSide == 4):                      
                    cube[nextSide][3-row-1][0] = self.cube[currSide][row][2]
                elif (currSide == 3) :
                    cube[nextSide][3-1-row][2] = self.cube[currSide][row][0]
                else:
                    cube[nextSide][row][2] = self.cube[currSide][row][2]
        self.cube = copy.deepcopy(cube)
    
    def rotateVerticalL(self, side):
        cube = copy.deepcopy(self.cube)
        adjacentSides = RubiksCube.neighborSides[side]
        for sides in range(len(adjacentSides)):
            currSide = adjacentSides[sides]
            nextSide = adjacentSides[(sides+1)%4]
            for row in range(3):
                if currSide == 5:
                    cube[nextSide][3-row-1][2] = self.cube[currSide][row][0]
                elif currSide == 3 :
                    cube[nextSide][3-row-1][0] = self.cube[currSide][row][2]
                else:
                    cube[nextSide][row][0] = self.cube[currSide][row][0]
        self.cube = copy.deepcopy(cube)
    
    
    def move(self,direction, command):
        side = RubiksCube.moves[command]
        if direction == 1:
            if command == 'U':
                self.transpose(side)
                self.rotateHorizontal(side,0)
            elif command == 'D':
                self.transpose(side)
                self.rotateHorizontal(side,2)
            if command == 'R':
                self.transpose(side)
                self.rotateVerticalR(side)
            elif command == 'L':
                self.transpose(side)
                self.rotateVerticalL(side)
            elif command == 'F':
                self.transpose(side)
                self.shiftSidesF(side)
            elif command == 'B':
                self.transpose(side)
                self.shiftSidesB(side)
        else:
            for i in range(3):
                if command == 'U':
                    self.transpose(side)
                    self.rotateHorizontal(side,0)
                elif command == 'D':
                    self.transpose(side)
                    self.rotateHorizontal(side,2)
                if command == 'R':
                    self.transpose(side)
                    self.rotateVerticalR(side)
                elif command == 'L':
                    self.transpose(side)
                    self.rotateVerticalL(side)
                elif command == 'F':
                    self.transpose(side)
                    self.shiftSides(side,0,1)
                elif command == 'B':
                    self.transpose(side)
                    self.shiftSides(side,1,0)

            

class EnterColorMode(Mode):
    def appStarted(mode):
        mode.cube = RubiksCube(mode)
    
    def mousePressed(mode, event):
        side = mode.cube.getSide(event.x, event.y)
        if side != None:
            color = mode.getUserInput('Enter the color')
            if color not in ['red', 'green', 'blue', 'yellow', 'white', 'orange']:
                messagebox.showerror('Error', 'Color not identified')
            else:
                row,col = mode.cube.getCell(event.x, event.y, side)
                mode.cube.addColors(color, side, row, col)
    
    def keyPressed(mode, event):
        if event.key == 's':
            mode.app.setActiveMode(mode.app.solverMode)
        elif event.key == 'f':
            mode.cube.move(1,'F')
        elif event.key == 'r':
            mode.cube.move(1,'R')
        elif event.key == 'l':
            mode.cube.move(1,'L')
        elif event.key == 'b':
            mode.cube.move(1,'B')
        elif event.key == 'u':
            mode.cube.move(1,'U')
        elif event.key == 'd':
            mode.cube.move(1,'D')
            
    def redrawAll(mode, canvas):
        canvas.create_rectangle(0,0,mode.width, mode.height, fill = 'grey')
        mode.cube.drawCube(canvas)

class SolverMode(Mode):
    pass
        
class MyModalApp(ModalApp):
    def appStarted(app):
        app.enterColorMode = EnterColorMode()
        app.solverMode = SolverMode()
        app.setActiveMode(app.enterColorMode)

app = MyModalApp(width = 400, height = 400)
