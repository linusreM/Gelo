import time
import socket

c = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
c.connect(('127.0.0.1', 8089))
#msg = raw_input("Send via UDP: ")
i = -10
while(1):
	c.send(str(i))
	#msg = raw_input("\nSend: ")
	time.sleep(0.0167)
	i += 0.1
	if(i > 10):
		i=-10
