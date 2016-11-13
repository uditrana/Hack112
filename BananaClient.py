# grid-demo.py

from tkinter import *
import string
###############################
#Helpers
###############################
def make2dList(rows, cols, val): #adapted from course notes
    a=[]
    for row in range(rows): a += [[val]*cols]
    return a

def init(data):
    data.rows = 8
    data.cols = 8
    data.tiles = []
    data.trayRows = int(roundHalfUp(len(data.tiles)/data.cols))
    data.trayCols = min(len(data.tiles), data.cols)
    data.tileBoard = updateTileTray(data, data.tiles, make2dList(data.trayRows, data.trayCols, ""))
    data.EMPTY = ""
    data.emptyColor = "light yellow"
    data.fillColor = "gold"
    data.sWidth = 4
    data.fillWidth = 2
    data.emptyWidth = 1 
    data.board = make2dList(data.rows, data.cols, data.EMPTY)
    data.margin = 10 # margin around grid
    data.sRow = 0 #sRow, sCol denotes user-selected cell
    data.sCol = 0

def updateTileTray(data, tiles, tileBoard):
    for row in range(data.trayRows):
        for col in range(data.trayCols):
            

#cell stuff from Course Notes
def pointInGrid(x, y, data):
    # return True if (x, y) is inside the grid defined by data.
    return ((data.margin <= x <= data.width-data.margin) and
            (data.margin <= y <= data.height-data.margin))

def getCell(x, y, data):
    # aka "viewToModel"
    # return (row, col) in which (x, y) occurred or (-1, -1) if outside grid.
    if (not pointInGrid(x, y, data)):
        return (0, 0)
    gridWidth  = data.width - 2*data.margin
    gridHeight = data.height - 2*data.margin
    cellWidth  = gridWidth / (data.cols+data.trayCols)
    cellHeight = gridHeight / (data.rows+data.trayRows)
    row = (y - data.margin) // cellHeight
    col = (x - data.margin) // cellWidth
    # triple-check that we are in bounds
    row = min(data.rows-1, max(0, row))
    col = min(data.cols-1, max(0, col))
    return (int(row), int(col))

def mousePressed(event, data):
    (data.sRow, data.sCol) = getCell(event.x, event.y, data)

def keyPressed(event, data):
    key = (event.keysym)
    if key == "Up" and data.sRow > 0: data.sRow -= 1
    elif key == "Down" and data.sRow < data.rows-1: data.sRow += 1
    elif key == "Left" and data.sCol > 0: data.sCol -= 1
    elif key == "Right" and data.sCol < data.cols-1: data.sCol += 1
    elif key in data.tiles: data.board[data.sRow][data.sCol] = key.upper()

def timerFired(data):
    pass

def getCellBounds(row, col, data):
    # aka "modelToView"
    # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
    gridWidth  = data.width - 2*data.margin
    gridHeight = data.height - 3*data.margin
    columnWidth = gridWidth / (data.cols)
    rowHeight = gridHeight / (data.rows+data.trayRows)
    x0 = data.margin + col * columnWidth
    x1 = data.margin + (col+1) * columnWidth
    y0 = data.margin + row * rowHeight
    y1 = data.margin + (row+1) * rowHeight
    return (x0, y0, x1, y1)

def redrawAll(canvas, data):
    # draw grid of cells
    drawGrid(canvas, data)
    drawLetters(canvas, data)
    drawSelection(canvas, data)
    drawTiles(canvas, data)

def drawSelection(canvas, data):
    (x0, y0, x1, y1) = getCellBounds(data.sRow, data.sCol, data)
    canvas.create_rectangle(x0, y0, x1, y1, fill=None, width=4)

def drawLetters(canvas, data):
    for row in range(data.rows):
        for col in range(data.cols):
            (x0, y0, x1, y1) = getCellBounds(row, col, data)
            if data.board[row][col] != data.EMPTY:
                canvas.create_text((x0+x1)/2, (y0+y1)/2, text=data.board[row][col], font="Helvetica 20")


def drawTiles(canvas, data):
    for row in range(data.trayRows):
        for col in range(data.trayCols):
            (x0, y0, x1, y1) = getCellBounds(row+data.rows, col, data)
            fill = data.fillColor
            width = data.fillWidth
            if data.tileBoard[row][col] != "": 
                canvas.create_rectangle(x0, y0+data.margin, x1, y1+data.margin, fill=fill, width=width)
                canvas.create_text((x0+x1)/2, (y0+y1+2*data.margin)/2, text=data.tileBoard[row][col], font="Helvetica 20")

def drawGrid(canvas, data):
    for row in range(data.rows):
        for col in range(data.cols):
            (x0, y0, x1, y1) = getCellBounds(row, col, data)
            fill = data.emptyColor
            width = data.emptyWidth
            if data.board[row][col] != data.EMPTY:
                fill = data.fillColor
                width = data.fillWidth
            canvas.create_rectangle(x0, y0, x1, y1, fill=fill, width=width)



####################################
# use the run function as-is
####################################

def run(width=300, height=347.5):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)

    def sizeChanged(event, data):
        data.width = event.width
        data.height = event.height
        redrawAll(canvas, data)

    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack(fill=BOTH, expand=YES)
    root.canvas = canvas.canvas = canvas
    canvas.data = {}
    init(canvas)
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    root.bind("<Configure>", lambda event: sizeChanged(event, data))
    timerFiredWrapper(canvas, data)
    root.minsize(data.width, data.height)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(600, 685)
