import socket
import time
import errno

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #initialize UDP stream socket
serversocket.bind(('localhost', 8089)) #bind socket to port 3344
serversocket.listen(5) # become a server socket, maximum 5 connections
while(1):
	connection, address = serversocket.accept()
	while (1):
		try:
			buf = connection.recv(1024, 0X40)
		except socket.error, e:
			err = e.args[0]
			if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
				print "n"
				time.sleep(0.1)
		else:
			if len(buf) > 0:
				print buf
			else:
				print 'No connection'
				time.sleep(0.1) 
				break
	#  


