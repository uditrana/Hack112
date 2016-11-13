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

HOST = "128.237.180.202"
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
      print(readyMsg)
      msg = "\n".join(command[1:])
      serverMsg.put(readyMsg)
      command = msg.split("\n")

serverMsg = Queue(100)
threading.Thread(target = handleServerMsg, args = (server, serverMsg)).start()

####################
#Dictionary Things
###################
f = open("dictionary.txt")
d = []
d = f.readlines()
for i in range(len(d)):
    d[i] = d[i].replace("\n", "")
d = set(d)
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
def init(data, canvas):
    data.sidebarWidth = 120
    data.squareSize = 40
    data.rows = 50
    data.cols = 50
    #data.tiles = ["B", "A", "N", "A", "N", "A", "G", "R", "A", "M", "S",]
    data.tiles = []
    data.trayRows = int(math.ceil(len(data.tiles)/data.cols))
    data.trayCols = min(len(data.tiles), data.cols)
    data.tileBoard = [] 
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
    data.visMargin = 50
    data.visRows = (data.height-data.visMargin)//data.squareSize
    data.visCols = (data.width-data.visMargin)//data.squareSize
    data.cRow = data.rows//2
    data.cCol = data.cols//2 #in which we are trying to draw just the visible cells
    data.leftCol = data.cCol-data.visCols//2
    data.rightCol = data.cCol+(data.visCols//2)
    data.topRow = data.cRow-data.visRows//2
    data.bottomRow = data.cRow+(data.visRows//2)
    db(data.leftCol,data.rightCol,data.topRow,data.bottomRow)
    data.printed = ""
    data.printedLength = 0
   
def getWord(data, board):
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
                            word.append((board[i][j]).upper())
                            j+= 1
                        wordsList.append("".join(word))
                if (x == 0 or board[x-1][y] == ""): #vertical
                    if x < (len(board[0])-1) and board[x+1][y] != "":
                        word = []
                        i = x
                        j = y
                        while i < len(board) and  board[i][j] != "":
                            word.append((board[i][j]).upper())
                            i+= 1
                        wordsList.append("".join(word))
    return wordsList
    
def checkWords(data, board):
    toCheck = getWord(data, board)
    correctWords = []
    falseWords = []
    if len(data.tiles) != 0: return False
    for a in toCheck:
        if a in d:
            correctWords.append(a)
        else:
            falseWords.append(a)
    if correctWords == toCheck:
        return True
    else:
        false = ""
        for word in falseWords:
            false += word + "\n"
        return "False Words"+"\n"+false

def updateRowsCols(data): #double-check/fix shit when you're awake
    data.visRows = (data.height-data.visMargin)//data.squareSize
    data.visCols = (data.width-data.visMargin)//data.squareSize
    data.leftCol = data.cCol-data.visCols//2
    data.rightCol = data.cCol+(data.visCols//2)
    data.topRow = data.cRow-data.visRows//2
    data.bottomRow = data.cRow+(data.visRows//2)

def updateTileTray(data):
    data.trayRows = int(math.ceil(len(data.tiles)/data.visCols))
    data.trayCols = min(len(data.tiles), data.visCols)
    tileBoard = make2dList(data.trayRows, data.trayCols, "")
    index = 0
    db(data.trayRows, data.trayCols, len(data.tiles))
    for row in range(data.trayRows):
        for col in range(data.trayCols):
            if index < len(data.tiles):
                # db("tiles/tileboard", data.tiles, tileBoard)
                tileBoard[row][col] = data.tiles[index]
            index += 1
    db("BOB", tileBoard)
    data.tileBoard = tileBoard

#cell stuff from Course Notes
def pointInGrid(x, y, data):
    # return True if (x, y) is inside the grid defined by data.
    return ((data.margin <= x <= data.width-data.margin) and
            (data.margin <= y <= data.height-data.margin))

def isLegal(data): #checks to see if all items on the board are connected
    # boardCheck = make2dList(data.rows, data.cols, 0)
    # startRow, startCol = None, None
    # for row in range(data.rows):
    #     for col in range(data.cols):
    #         if startRow == None: (startRow, startCol) = (row, col)
    #         if data.board[row][col] != "":
    #             boardCheck[row][col] = 1
    # def check(board, row, col):
    #     if ((row < 0) or (row >= data.rows) or
    #         (col < 0) or (col >= data.cols)):
    #         return # off-board!
    #     if (board[row][col] == 0):
    #         return # hit a wall

    #     # "fill" this cell
    #     else: board[row][col] = 1

    #     # then recursively fill its neighbors
    #     check(board, row-1, col)
    #     check(board, row+1, col)
    #     check(board, row,   col-1, depth+1)
    #     check(board, row,   col+1, depth+1)
    # board = check(boardCheck, startRow, startCol)
    # db(board)
    # if board != make2dList(data.rows, data.cols, 0): return False
    # else: return True
    return True

def getCell(x, y, data):
    # aka "viewToModel"
    # return (row, col) in which (x, y) occurred or (-1, -1) if outside grid.
    if (not pointInGrid(x, y, data)):
        return None
    gridWidth  = data.width - 2*data.margin
    gridHeight = data.height - 2*data.margin
    row = data.topRow + (y - data.margin) // data.squareSize
    col = data.leftCol + (x - data.margin) // data.squareSize
    # triple-check that we are in bounds
    row = min(data.rows-1, max(0, row))
    col = min(data.cols-1, max(0, col))
    return (int(row), int(col))

def moveCursor(drow, dcol, data):
    data.sRow += drow
    data.sCol += dcol
    if (data.sCol < data.leftCol): 
        data.cCol += dcol
        data.leftCol = data.cCol-data.visCols//2
        data.rightCol = data.cCol+(data.visCols//2)
    elif (data.sCol >= data.rightCol):  
        data.cCol += dcol
        data.leftCol = data.cCol-data.visCols//2
        data.rightCol = data.cCol+(data.visCols//2)
    elif (data.sRow < data.topRow): 
        data.cRow += drow
        data.topRow = data.cRow-data.visRows//2
        data.bottomRow = data.cRow+(data.visRows//2)
    elif (data.sRow >= data.bottomRow): 
        data.cRow += drow
        data.topRow = data.cRow-data.visRows//2
        data.bottomRow = data.cRow+(data.visRows//2)

def mousePressed(event, data):
    if getCell(event.x, event.y, data) != None:
        (data.sRow, data.sCol) = getCell(event.x, event.y, data)
        (data.cRow, data.cCol) = (data.sRow, data.sCol)
        data.leftCol = data.cCol-data.visCols//2
        data.rightCol = data.cCol+(data.visCols//2)
        data.topRow = data.cRow-data.visRows//2
        data.bottomRow = data.cRow+(data.visRows//2)

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
        data.tileBoard = updateTileTray(data)
    elif key == "space":
        if data.board[data.sRow][data.sCol] != data.EMPTY:
            data.tiles.append(data.board[data.sRow][data.sCol])
            data.board[data.sRow][data.sCol] = data.EMPTY#add in remove tile
    elif key == "1":
        check = checkWords(data, data.board)
        print(check)
        #legal = isLegal(data)
        if isinstance(check, str): printToSideBar(data,"Invalid:"+check)
        elif check==False: printToSideBar(data,"Not out of tiles yet!")
        elif check:
            msg = "Peel:\n"
            printToSideBar(data,msg)
            data.server.send(msg.encode())
    elif key == "Return":
        msg = "Start:\n"
        printToSideBar(data,msg)
        data.server.send(msg.encode())
    elif ignoreKey(event) and len(event.keysym == 1) and event.keysym.isalpha():
        msg = "Exchange:" + event.keysym + "\n"
        printToSideBar(data,msg)
        data.server.send(msg.encode())

def ignoreKey(event):
    # Helper function to return the key from the given event
    ignoreSyms = [ "Shift_L", "Shift_R", "Control_L", "Control_R", "Caps_Lock" ]
    return (event.keysym in ignoreSyms)

def timerFired(data):
    if (serverMsg.qsize() > 0):
        msg = serverMsg.get(False)
        try:
            print("recieved: ", msg)
            print("ugh " + msg)
            msg = msg.split(":")
            ind, txt, info= msg[0], msg[1],msg[2]
            if ind=="Peel":
                print ("Text is "+txt)
                letter = info
                data.tiles.append(letter)
            elif ind == "Exchange":
                print("Text is " + txt)
                letters = info.split(",")
                data.tiles.extend(letters)
            elif ind == "Start":
                print("Text is " + txt)
                letters = info.split(",")
                print(letters)
                data.tiles.extend(letters)

        except:
            print("failed")
        serverMsg.task_done()
    db(data.tiles)
    updateRowsCols(data)
    updateTileTray(data)

def getTileCellBounds(row, col, data):
    # aka "modelToView"
    # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
    gridWidth  = data.width - 2*data.margin
    gridHeight = data.height - 2*data.margin
    x0 = data.margin + col * data.squareSize
    x1 = data.margin + (col+1) * data.squareSize
    y0 = gridHeight - ((row+1) * data.squareSize)
    y1 = gridHeight - (row * data.squareSize)
    return (x0, y0, x1, y1)

def getCellBounds(row, col, data):
    row = (data.visRows//2)-(data.cRow-row)
    col = (data.visCols//2)-(data.cCol-col)
    # aka "modelToView"
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
    canvas.create_text(data.width-data.sidebarWidth,data.margin+200,text=data.printed,anchor="sw")

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
    updateTileTray(data)
    db("fuc", data.trayRows, data.trayCols)
    for row in range(data.trayRows):
        for col in range(data.trayCols):
            (x0, y0, x1, y1) = getTileCellBounds(row, col, data)
            db("ah", data.tileBoard, row, col)
            fill = data.fillColor
            width = data.fillWidth
            db("HEY", data.tileBoard[row][col])
            if data.tileBoard[row][col] != "": 
                canvas.create_rectangle(x0, y0, x1, y1, fill=fill, width=width)
                canvas.create_text((x0+x1)/2, (y0+y1)/2, text=data.tileBoard[row][col], font="Helvetica 20")

def drawGrid(canvas, data):
    for row in range(data.topRow, data.bottomRow):
        for col in range(data.leftCol, data.rightCol):
            (x0, y0, x1, y1) = getCellBounds(row, col, data)
            fill = data.emptyColor
            width = data.emptyWidth
            if data.board[row][col] != data.EMPTY:
                fill = data.fillColor
                width = data.fillWidth
            canvas.create_rectangle(x0, y0, x1, y1, fill=fill, width=width)

def printToSideBar(data,input):
    if data.printedLength % 5 == 0:
        data.printed = ""
    data.printed += "\n"+input
    data.printedLength += 1

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
        updateRowsCols(data)
        redrawAll(canvas, data)

    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.server = server
    data.serverMsg = serverMsg
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack(fill=BOTH, expand=YES)
    root.canvas = canvas.canvas = canvas
    canvas.data = {}
    init(data, canvas)
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