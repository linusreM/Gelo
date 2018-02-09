import socket
import time
import random
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(('localhost', 8089))
clientsocket.send('Connection open\n')
time.sleep(1)
clientsocket.send('Start sending position update\n')
id = "BOT2"
packetno = 0
while 1:
	typeid = "MOVE"
	forward = 5.64 * random.uniform(-2.5,2.5)
	turn = 3.85 * random.uniform(-2.5,2.5)
	packetno += 1
	msg = "$" + id + "#" + typeid + "#" + str(forward) + "#" + str(turn) + "#" + str(packetno) 
	clientsocket.send(msg)
	
	#i += 1
	time.sleep(0.05)
