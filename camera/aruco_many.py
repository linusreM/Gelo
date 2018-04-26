from videostream import VideoStream
from marker import Marker
import numpy as np
import cv2
import cv2.aruco as aruco
import sys
import time
import socket


clientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print('attempting connect\n')
<<<<<<< HEAD:camera/aruco_many.py
clientsocket.connect(('localhost', int(sys.argv[3])))
=======
<<<<<<< HEAD
clientsocket.connect(('130.229.145.168', int(sys.argv[3])))
=======
clientsocket.connect(('130.229.182.39', int(sys.argv[3])))
>>>>>>> 6dea015d8b2b71ee3a961aa6c4cf11e4a1278b22
>>>>>>> f53853f4c7ee2ee245db34e04b697c24e2102972:camera/aruco_unity_test.py
print('Connection open\n')
#clientsocket.send('Connection open\n')
time.sleep(1)
print('Start sending data\n')
#clientsocket.send('Start sending position update\n')
id = "BOT1"
type = "QR"


if int(sys.argv[1]) == 1:
    isPiCamera = True
else:
    isPiCamera = False

if int(sys.argv[2]) == 640:
    resolution = (640,480)
elif int(sys.argv[2]) == 320:
    resolution = (320,240)
else:
    print "Not valid resolution"
    quit()


dictionary = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)
parameters = aruco.DetectorParameters_create()



parameters.cornerRefinementMethod = 1
parameters.cornerRefinementWinSize = 5
parameters.cornerRefinementMaxIterations = 30 
parameters.cornerRefinementMinAccuracy = 0.0001

vs = VideoStream(isPiCamera = isPiCamera, resolution = resolution).start()
time.sleep(2.0)


<<<<<<< HEAD:camera/aruco_many.py
while True:
	img = vs.readUndistorted()
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #EVENTUELLT

	corners, ids, rejected = aruco.detectMarkers(gray, dictionary, parameters = parameters)
	rvecs, tvecs, obj = aruco.estimatePoseSingleMarkers(corners, 65.18, vs.mtx, vs.dist)

	markers = []

	try:
		for i in range(len(ids)):
			marker = Marker(corners[i], ids[i], tvecs[i], rvecs[i])
			markers.append(marker)


		for marker in markers:
			msg = "{}#{}#{}#{}#{}#{}#{}#{}#{}$".format(
					id, 
					type, 
					marker.data, 
					marker.tvecs_x, 
					marker.tvecs_y, 
					marker.tvecs_z, 
					marker.rvecs_x, 
					marker.rvecs_y, 
					marker.rvecs_z
			) 	
			print msg
			clientsocket.send(msg)
		time.sleep(3.0)
	except:
		print "no code"

				
=======

img = vs.readUndistorted()
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #EVENTUELLT

corners, ids, rejected = aruco.detectMarkers(gray, dictionary, parameters = parameters)
rvecs, tvecs, obj = aruco.estimatePoseSingleMarkers(corners, 65.18, vs.mtx, vs.dist)

try:
	if (rvecs.size > 0):

		for marker in tvecs:
			tvecs_x = marker[0,0]
			tvecs_y = marker[0,1]
			tvecs_z = marker[0,2]

		for marker in rvecs:
			#print marker
			rvecs_x = marker[0,0]
			rvecs_y = marker[0,1]
			rvecs_z = marker[0,2]

		msg = "{}#{}#{}#{}#{}#{}#{}#{}#{}$".format(
			id, 
			type, 
			"data", 
			tvecs_x, 
			tvecs_y, 
			tvecs_z, 
			rvecs_x, 
			rvecs_y, 
			rvecs_z
		) 
		
		print msg
		clientsocket.send(msg)

except:
	print "no code"

>>>>>>> f53853f4c7ee2ee245db34e04b697c24e2102972:camera/aruco_unity_test.py
vs.stop()
