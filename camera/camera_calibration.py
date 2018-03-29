import sys
import glob	
import cv2
import numpy as np

if len(sys.argv) > 1:
	save_file_name = sys.argv[1]
else:
	save_file_name = 'unnamed_camera'

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((4*6,3), np.float32)
objp[:,:2] = np.mgrid[0:6,0:4].T.reshape(-1,2)

objpoints = []
imgpoints = []

numb_read = 0

images = glob.glob('./pics/*.jpg')

for file_name in images:

	img = cv2.imread(file_name)
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY, dstCn = 0)

	ret, corners = cv2.findChessboardCorners(gray, (6,4), None)

	if ret == True:
		objpoints.append(objp)

		corners_subpix = cv2.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
		imgpoints.append(corners_subpix)

		cv2.drawChessboardCorners(img, (6,4), corners_subpix, ret)
		cv2.imshow('Camera Calibration', img)
		cv2.waitKey(100)
		numb_read += 1

cv2.destroyAllWindows()

print numb_read

ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
np.savez(save_file_name + '_intrinsics.npz', mtx = mtx, dist=dist, rvecs=rvecs, tvecs=tvecs)

