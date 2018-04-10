from videostream import VideoStream
import cv2
import numpy as np
import time

with np.load('picamera320_intrinsics.npz') as X:
    mtx, dist, rvecs, tvecs = [X[i] for i in ('mtx','dist','rvecs','tvecs')]

resolution = (320,240)
isPiCamera = True
vs = VideoStream(isPiCamera = isPiCamera, resolution = resolution).start()

time.sleep(2.0)

while True:
	img = vs.read()


	h, w = img.shape[:2]
	#newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))

	map1, map2 = cv2.fisheye.initUndistortRectifyMap(mtx, dist, np.eye(3), mtx, resolution, cv2.CV_16SC2)
	undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)

	#mapx, mapy = cv2.initUndistortRectifyMap(mtx, dist, None, newcameramtx, (w,h), 5)
	#dst = cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR)
	cv2.imshow('img', undistorted_img)
	#x, y, w, h = roi
	#dst = dst[y:y+h, x:x+w]

	keypress = cv2.waitKey(1) & 0xFF
	if keypress == ord('q'):
		break

vs.stop()
cv2.destroyAllWindows()
