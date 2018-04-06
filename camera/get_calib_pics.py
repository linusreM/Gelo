from videostream import VideoStream
import cv2
import time
import sys


if int(sys.argv[1]) == 1:
	isPiCamera = True
	cam_type = "picamera"
else:
	isPiCamera = False
	cam_type = "usbcamera"


if int(sys.argv[2]) == 640:
	resolution = (640,480)
elif int(sys.argv[2]) == 320:
	resolution = (320,240)
else:
	print "Not valid resolution"
	quit()

vs = VideoStream(isPiCamera = isPiCamera, resolution = resolution).start()
numb_of_pics = 0


while(1):
	img = vs.read()

	cv2.imshow("Press Space to Save Frame", img)
	
	keypress = cv2.waitKey(1) & 0xFF
	if keypress == 32:
		numb_of_pics += 1
		file_name = cam_type + str(resolution[0]) + '_' + str(numb_of_pics)
		cv2.imwrite('./calib_pics/' + file_name + '.jpg', img)
	
	if keypress == ord('q'):
		print str(numb_of_pics) + ' pictures saved'
		break


vs.stop()
cv2.destroyAllWindows()
