from videostream import VideoStream
import cv2
import sys
import time


if int(sys.argv[1]) == 1:
	isPiCamera = True
else:
	isPiCamera = False

vs = VideoStream(src = 0, isPiCamera = isPiCamera).start()
time.sleep(2.0)

while True:

	frame = vs.read()

	cv2.imshow('img', frame)

	keypress = cv2.waitKey(100) & 0xFF
	if keypress == ord("q"):
		break


vs.stop()
cv2.destroyAllWindows()
