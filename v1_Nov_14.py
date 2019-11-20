from cmu_112_graphics import *
from tkinter import *

class RubiksCube(object):
    def __init__(self, app):
        self.sides = 6
        self.rows = 3
        self.cols = 3
        self.app = app
        self.cube = self.createCube()
        
    def createCube(self):
        cube = []
        for side in range(self.sides):
            side = []
            for row in range(self.rows):
                row = []
                for col in range(self.cols):
                    row += [None]
                side += [row]
            cube += [side]
        return cube

    def addColors(self, color, side, row, col):
        self.cube[side][row][col] = color

    def printCube(self):
        for side in range(self.sides):
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
        for side in range(self.sides):
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

class MyApp(App):
    def appStarted(app):
        app.cube = RubiksCube(app)
    
    def mousePressed(app, event):
        side = app.cube.getSide(event.x, event.y)
        if side != None:
            color = app.getUserInput('Enter the color')
            if color not in ['red', 'green', 'blue', 'yellow', 'white', 'orange']:
                messagebox.showerror('Error', 'Color not identified')
            else:
                row,col = app.cube.getCell(event.x, event.y, side)
                app.cube.addColors(color, side, row, col)

    def redrawAll(app, canvas):
        canvas.create_rectangle(0,0,app.width, app.height, fill = 'grey')
        app.cube.drawCube(canvas)
        

MyApp(width = 400, height = 400)
