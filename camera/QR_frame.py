from videostream import VideoStream
from PIL import Image
import sys
import numpy as np 
import cv2
import time
import zbar
import socket

QR_size = 100.0

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print('attempting connect\n')
clientsocket.connect(('130.229.175.7', int(sys.argv[3])))
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


objp = np.float32([[0,0,0],[0,1,0],[1,1,0],[1,0,0]])
corners = np.zeros((4,1), np.float32)


vs = VideoStream(isPiCamera = isPiCamera, resolution = resolution).start()
time.sleep(2.0)

scanner = zbar.ImageScanner()
scanner.parse_config('enable')


	
img = vs.readUndistorted()
	
	# raw detection code
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
pil = Image.fromarray(gray)
width, height = pil.size
raw = pil.tobytes()

# create a reader
image = zbar.Image(width, height, 'Y800', raw)
scanner.scan(image)

try:
	for symbol in image:
		print 'decoded', symbol.type, 'symbol', '"%s"' % symbol.data
		corners = np.asarray(symbol.location, dtype = np.float32)
			

		ret, rvecs, tvecs = cv2.solvePnP(objp, corners, vs.mtx, vs.dist)
		tvecs_x = float(tvecs[0] * QR_size)
		tvecs_y = float(tvecs[1] * QR_size)
		tvecs_z = float(tvecs[2] * QR_size)



	msg = "{}#{}#{}#{}#{}#{}#$".format(id, type, symbol.data, tvecs_x, tvecs_y, tvecs_z) 
	print msg
	clientsocket.send(msg)
except:
	print "no code"
			
vs.stop()
