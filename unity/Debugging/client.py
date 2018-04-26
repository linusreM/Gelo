import socket
import time
import random
import sys

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientsocket.connect(('localhost', int(sys.argv[1])))
#clientsocket.send('Connection open\n')
time.sleep(1)
#clientsocket.send('Start sending position update\n')
id = "BOT1"
packetno = 0
while 1:
    ID = "Unity command"
    direction = raw_input ("[0] FW/BW" + '\n' + "[1] Rotate" + '\n' + "Choose movement type:")
    distance = raw_input("Distance [+/- mm/degrees]:")

    #turn = 3.85 * random.uniform(-2.5,2.5)
    packetno += 1
    msg = id + "#" + direction + "#" + distance + "$"
    clientsocket.send(msg)
    #try:
    #    clientsocket.sendto(msg, 'localhost', 8080)
    #except:
    #    print("Connection refused!")
    #i += 1
    time.sleep(0.5)
