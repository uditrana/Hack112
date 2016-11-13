import socket
import threading
from queue import Queue

HOST = "YOUR_IP_HERE"
PORT = 50003
BACKLOG = 4

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.bind((HOST,PORT))
server.listen(BACKLOG)
print("looking for connection")

def handleClient(client, serverChannel, cID, clientele):
  client.setblocking(1)
  msg = ""
  while True:
    try:
      msg += client.recv(10).decode("UTF-8")
      command = msg.split("\n")
      while (len(command) > 1):
        readyMsg = command[0]
        msg = "\n".join(command[1:])
        serverChannel.put(str(cID) + "_" + readyMsg)
        command = msg.split("\n")
    except:
      clientele.pop(cID)
      return

def serverThread(clientele, serverChannel):
  while True:
    msg = serverChannel.get(True, None)
    print("msg recv: ", msg)
    senderID, msg = int(msg.split("_")[0]), "_".join(msg.split("_")[1:])
    if (msg):
      for cID in clientele:
        if cID != senderID:
          sendMsg = "playerMoved " +  str(senderID) + " " + msg + "\n"
          clientele[cID].send(sendMsg.encode())
    serverChannel.task_done()

clientele = {}
currID = 0

serverChannel = Queue(100)
threading.Thread(target = serverThread, args = (clientele, serverChannel)).start()
#start_new_thread(serverThread, (clientele, serverChannel))

while True:
  client, address = server.accept()
  print(currID)
  for cID in clientele:
    print (repr(cID), repr(currID))
    clientele[cID].send(("newPlayer %d 100 100\n" % currID).encode())
    client.send(("newPlayer %d 100 100\n" % cID).encode())
  clientele[currID] = client
  print("connection recieved")
  threading.Thread(target = handleClient, args = 
                        (client ,serverChannel, currID, clientele)).start()
  #start_new_thread(handleClient, (client,serverChannel, currID))
  currID += 1
