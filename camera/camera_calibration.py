import sys
import glob	
import cv2
import numpy as np

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


# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((6*9,3), np.float32)
objp[:,:2] = np.mgrid[0:9,0:6].T.reshape(-1,2)

objpoints = []
imgpoints = []

numb_read = 0

images = glob.glob('./calib_pics/' + cam_type + str(resolution[0]) + '*.jpg')

for file_name in images:

	img = cv2.imread(file_name)
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	ret, corners = cv2.findChessboardCorners(gray, (9,6), None)

	if ret == True:
		objpoints.append(objp)

		corners_subpix = cv2.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
		imgpoints.append(corners_subpix)

		cv2.drawChessboardCorners(img, (9,6), corners_subpix, ret)
		cv2.imshow('Camera Calibration', img)
		cv2.waitKey(100)
		numb_read += 1

cv2.destroyAllWindows()

print numb_read

ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

save_file_name = cam_type + str(resolution[0]) + '_intrinsics.npz'
np.savez(save_file_name, mtx = mtx, dist=dist, rvecs=rvecs, tvecs=tvecs)

