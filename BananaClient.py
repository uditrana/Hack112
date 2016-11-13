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
    data.trayHeight = 1
    data.EMPTY = ""
    data.emptyColor = "light yellow"
    data.fillColor = "gold"
    data.tiles = []
    data.sWidth = 4
    data.fillWidth = 2
    data.emptyWidth = 1 
    data.board = make2dList(data.rows, data.cols, data.EMPTY)
    data.margin = 10 # margin around grid
    data.sRow = 0 #sRow, sCol denotes user-selected cell
    data.sCol = 0

def pointInGrid(x, y, data):
    # return True if (x, y) is inside the grid defined by data.
    return ((data.margin <= x <= data.width-data.margin) and
            (data.margin <= y <= data.height-data.margin))

def getCell(x, y, data):
    # aka "viewToModel"
    # return (row, col) in which (x, y) occurred or (-1, -1) if outside grid.
    #if (not pointInGrid(x, y, data)):
    #    return (-1, -1)
    gridWidth  = data.width - 2*data.margin
    gridHeight = data.height - 2*data.margin
    cellWidth  = gridWidth / data.cols
    cellHeight = gridHeight / data.rows
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
    if key == "Up": data.sRow -= 1
    elif key == "Down": data.sRow += 1
    elif key == "Left": data.sCol -= 1
    elif key == "Right": data.sCol += 1
    elif key in data.tiles: data.board[data.sRow][data.sCol] = key.upper()

def timerFired(data):
    pass

def getCellBounds(row, col, data):
    # aka "modelToView"
    # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
    gridWidth  = data.width - 2*data.margin
    gridHeight = data.height - 2*data.margin
    columnWidth = gridWidth / data.cols
    rowHeight = gridHeight / data.rows
    x0 = data.margin + col * columnWidth
    x1 = data.margin + (col+1) * columnWidth
    y0 = data.margin + row * rowHeight
    y1 = data.margin + (row+1) * rowHeight
    return (x0, y0, x1, y1)

def sizeChanged(event):
    canvas = event.widget.canvas
    canvas.width = event.width - 10
    canvas.height = event.height - 10
    redrawAll(canvas)

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
    pass

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

def run(width=300, height=300):
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
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.winMargin = 10
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
    root.bind("<Configure>", sizeChanged)
    timerFiredWrapper(canvas, data)
    root.minsize(data.width+data.winMargin, data.height+data.winMargin)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(600, 600)
