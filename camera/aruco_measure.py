from videostream import VideoStream
from marker import *
import time


vs = VideoStream(isPiCamera = True,resolution = (640,480), framerate = 90)
md = MarkerDetector(id = "BOT1")

while True:
	vs.startCamera()
	img = vs.readUndistortedStill()
	md.detectMarkers(img, vs.stream.mtx, vs.stream.dist)

	for message in md.messages:
		print message

	vs.stop()




