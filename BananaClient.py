#banana graphics!

from tkinter import *
import math
import string
import random

####################
#Multiplayer Things
####################
import socket
import threading
from queue import Queue

HOST = "128.237.209.154"
PORT = 50003

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

server.connect((HOST,PORT))
print("connected to server")

def handleServerMsg(server, serverMsg): #handles msgs from server
  server.setblocking(1)
  msg = ""
  command = ""
  while True:
    msg += server.recv(10).decode("UTF-8")
    command = msg.split("\n")
    while (len(command) > 1):
      readyMsg = command[0]
      msg = "\n".join(command[1:])
      serverMsg.put(readyMsg)
      command = msg.split("\n")

serverMsg = Queue(100)
threading.Thread(target = handleServerMsg, args = (server, serverMsg)).start()
################################
#Helpers
################################
def db(*args):
    dbOn = False
    if (dbOn): print(*args)

def make2dList(rows, cols, val): #adapted from course notes
    a=[]
    for row in range(rows): a += [[val]*cols]
    return a
###############################
#BananaGrams Graphics
###############################
def init(data):
    data.sidebarWidth = 120
    data.squareSize = 40
    data.rows = 50
    data.cols = 50
    data.tiles = ["B", "A", "N", "A", "N", "A", "G", "R", "A", "M", "S",]
    data.trayRows = int(math.ceil(len(data.tiles)/data.cols))
    data.trayCols = min(len(data.tiles), data.cols)
    data.tileBoard = updateTileTray(data, make2dList(data.trayRows, data.trayCols, "")) #make this better when you're more coherent
    data.EMPTY = ""
    data.emptyColor = "light yellow"
    data.fillColor = "gold"
    data.sWidth = 4
    data.fillWidth = 2
    data.emptyWidth = 1 
    data.board = make2dList(data.rows, data.cols, "")
    data.margin = 10 # margin around grid
    data.sRow = data.rows//2 #sRow, sCol denotes user-selected cell
    data.sCol = data.cols//2
    # data.visRows = data.height//data.squareSize
    # data.visCols = data.width//data.squareSize
    data.scrollMargin = data.squareSize
    data.cx = data.sRow
    data.cy = data.sCol #in which we are trying to draw just the visible cells
    # data.LeftRow = 
   
def getWord(board):
    wordsList = []
    for x in range(len(board)): #row
        for y in range(len(board[0])): #col
            if board[x][y] != "":
                if (y == 0 or board[x][y-1] == ""): #horizontal
                    if y < (len(board)-1) and board[x][y+1] != "":
                        word = []
                        i = x
                        j = y
                        while j < len(board[0]) and  board[i][j] != "":
                            word.append(board[i][j])
                            j+= 1
                        wordsList.append("".join(word))
                if (x == 0 or board[x-1][y] == ""): #vertical
                    if x < (len(board[0])-1) and board[x+1][y] != "":
                        word = []
                        i = x
                        j = y
                        while i < len(board) and  board[i][j] != "":
                            word.append(board[i][j])
                            i+= 1
                        wordsList.append("".join(word))
    return wordsList
    
def checkWords(board):
    toCheck = getWord(board)
    d = enchant.Dict("en_US")
    correctWords = []
    falseWords = []
    for a in toCheck:
        if d.check(a):
            correctWords.append(a)
        else:
            falseWords.append(a)
    if correctWords == toCheck:
        return True
    else:
        return falseWords

def updateRowsCols(data): #double-check/fix shit when you're awake
    data.rows = (data.height - (data.trayRows*data.squareSize))//data.squareSize
    data.cols = (data.width - data.sidebarWidth)//data.squareSize

def updateTileTray(data, tileBoard):
    index = 0
    for row in range(data.trayRows):
        for col in range(data.trayCols):
            if index < len(data.tiles):
                db("tiles/tileboard", data.tiles, tileBoard)
                tileBoard[row][col] = data.tiles[index]
            index += 1
    return tileBoard

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
    # cellWidth  = gridWidth / (data.cols+data.trayCols)
    # cellHeight = gridHeight / (data.rows+data.trayRows)
    row = (y - data.margin) // data.squareSize
    col = (x - data.margin) // data.squareSize
    # triple-check that we are in bounds
    row = min(data.rows-1, max(0, row))
    col = min(data.cols-1, max(0, col))
    return (int(row), int(col))

def moveCursor(drow, dcol, data):
    data.sRow += drow
    data.sCol += dcol
    data.sx += (dcol*data.squareSize)
    data.sy += (drow*data.squareSize)
    # if (data.sRow < data.scroll)

def mousePressed(event, data):
    (data.sRow, data.sCol) = getCell(event.x, event.y, data)

def keyPressed(event, data):
    key = (event.keysym)
    if key == "Up" and data.sRow > 0: moveCursor(-1, 0, data)
    elif key == "Down" and data.sRow < data.rows-1: moveCursor(+1, 0, data)
    elif key == "Left" and data.sCol > 0: moveCursor(0, -1, data)
    elif key == "Right" and data.sCol < data.cols-1: moveCursor(0, +1, data)
    elif key.upper() in data.tiles:
        if data.board[data.sRow][data.sCol] == data.EMPTY:
            data.tiles.remove(key.upper())
        else:
            data.tiles.remove(key.upper())
            data.tiles.append(data.board[data.sRow][data.sCol])
        data.board[data.sRow][data.sCol] = key.upper()
        data.tiles.sort()
        data.tileBoard = updateTileTray(data, make2dList(data.trayRows, data.trayCols, ""))
        # check = checkWords(data.board)
        # if isinstance(check,list):
        #     #check contains false words
        #     pass
        # elif check == True:
        #     #all words on board are correct
        #     pass
    elif key == "space": return #add in remove tile
    elif key == "1":
        msg = "Peel:\n"
        print ("sending: ", msg,)
        data.server.send(msg.encode())

def timerFired(data):
    if (serverMsg.qsize() > 0):
      msg = serverMsg.get(False)
      try:
        print("recieved: ", msg)
        msg = msg.split(":")
        ind, txt, info= msg[0], msg[1],msg[2]
        if ind=="Peel":
          print ("Text is "+txt)
          letter = info
          data.tiles.append(letter)
      except:
        print("failed")
      serverMsg.task_done()

def getTileCellBounds(row, col, data):
    # aka "modelToView"
    # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
    gridWidth  = data.width - 2*data.margin
    gridHeight = data.height - 2*data.margin
    # columnWidth = gridWidth / (data.cols)
    # rowHeight = gridHeight / (data.rows+data.trayRows)
    x0 = data.margin + col * data.squareSize
    x1 = data.margin + (col+1) * data.squareSize
    y0 = gridHeight - ((row+1) * data.squareSize)
    y1 = gridHeight - (row * data.squareSize)
    return (x0, y0, x1, y1)

def getCellBounds(row, col, data):
    # aka "modelToView"
    # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
    gridWidth  = data.width - 2*data.margin
    gridHeight = data.height - 3*data.margin
    # columnWidth = gridWidth / (data.cols)
    # rowHeight = gridHeight / (data.rows+data.trayRows)
    x0 = data.margin + col * data.squareSize
    x1 = data.margin + (col+1) * data.squareSize
    y0 = data.margin + row * data.squareSize
    y1 = data.margin + (row+1) * data.squareSize
    return (x0, y0, x1, y1)

def redrawAll(canvas, data):
    # draw grid of cells
    drawGrid(canvas, data)
    drawLetters(canvas, data)
    drawSelection(canvas, data)
    drawTiles(canvas, data)
    drawSidebar(canvas, data)

def drawSidebar(canvas, data):
    canvas.create_rectangle(data.width-data.sidebarWidth-data.margin, data.margin, data.width-data.margin, data.height-data.margin, fill="white")

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
            (x0, y0, x1, y1) = getTileCellBounds(row, col, data)
            fill = data.fillColor
            width = data.fillWidth
            if data.tileBoard[row][col] != "": 
                canvas.create_rectangle(x0, y0, x1, y1, fill=fill, width=width)
                canvas.create_text((x0+x1)/2, (y0+y1)/2, text=data.tileBoard[row][col], font="Helvetica 20")

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

def run(width=300, height=300, serverMsg=None, server=None):
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
        #updateRowsCols(data)
        redrawAll(canvas, data)

    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.server = server
    data.serverMsg = serverMsg
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

run(600, 600, serverMsg, server)