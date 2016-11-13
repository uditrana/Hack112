import socket
import threading
import random
from queue import Queue

HOST = "128.237.180.202" #current IP in GHC6115
PORT = 50003
BACKLOG = 4

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.bind((HOST,PORT))
server.listen(BACKLOG)
print("looking for connection")

class Pile(object):
  def __init__(self):
    pass
  d = ({'A':13, 'B':3, 'C':3, 'D':6, 'E':18, 'F':3, 'G':4,'H':3, 'I':12, 
    'J':2, 'K':2, 'L':5, 'M':3, 'N':8, 'O':11, 'P':3, 'Q':2, 'R':9, 
    'S':6, 'T':9, 'U':6, 'V':3, 'W':3, 'X':2, 'Y':3, 'Z':2})
  @staticmethod
  def peel():
    while True:
      n = random.randint(65,90)
      letter = chr(n)
      if Pile.d[letter] > 0:
        Pile.d[letter] -= 1
        break
    print(letter +" was peeled!")
    return letter
  def start(self):
    pass
  def exchange(self):
    pass

def handleClient(client, serverChannel, cID, clientele): #this adds the client ID and msg to Q
  client.setblocking(1)
  msg = ""
  while True:
    try:
      msg += client.recv(10).decode("UTF-8") #creates message based on input
      command = msg.split("\n") #splits message based on \n
      while (len(command) > 1): #if we have a complete command
        readyMsg = command[0] #the first part is rdy message to be run
        msg = "\n".join(command[1:]) #the rest is shit that begins the next msg
        serverChannel.put(str(cID) + "_" + readyMsg) #add client ID and rdy msg to Q
        command = msg.split("\n") #go to next command (if there is one)
    except: #if gets bad shit, remove client
      clientele.pop(cID)
      return

def serverThread(clientele, serverChannel): #processes shit on the Q
  while True:
    msg = serverChannel.get(True, None) #get first item on Q
    print("msg recv: ", msg) #print the message rcvd!
    senderID, msg = int(msg.split("_")[0]), "_".join(msg.split("_")[1:]) #separates id from msg
    if (msg):
      ind = (msg.split(":")[0])
      if ind=="Peel":
        print ("I should be peeling!")
        ind+=":"
        for cID in clientele: #for each client
          if cID != senderID: #if client not the sender
            txt = str(senderID) + " Peeled!" +":"
            info = Pile.peel()
            sendMsg = ind+txt+info+"\n" #create message to all other players!
          if cID == senderID: #if client is sender
            txt = "You Peeled!" +":"
            info = Pile.peel()
            sendMsg = ind+txt+info+"\n" #create message to player
          clientele[cID].send(sendMsg.encode()) #encode and add it to dict
    serverChannel.task_done() #remove item from Q

clientele = {}
currID = 0

serverChannel = Queue(100) #initialize Q
threading.Thread(target = serverThread, args = (clientele, serverChannel)).start()
#start_new_thread(serverThread, (clientele, serverChannel))

while True: #loop for adding clients
  client, address = server.accept()
  print(currID) #curr client ID
  for cID in clientele: #tell all other peoples that there is a new player!
    print (repr(cID), repr(currID))
    clientele[cID].send(("newPlayer %d \n" % currID).encode()) #send new player info!
    client.send(("newPlayer %d \n" % cID).encode()) #tell the new player about all the old players
  clientele[currID] = client #dont really understand this line
  print("connection received")
  threading.Thread(target = handleClient, args =  #create a new thread for this new client
                        (client ,serverChannel, currID, clientele)).start() 
  #start_new_thread(handleClient, (client,serverChannel, currID))
  currID += 1
