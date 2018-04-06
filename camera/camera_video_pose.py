from videostream import VideoStream
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

load_file_name = cam_type + str(resolution[0]) + '_intrinsics.npz'

# Load previously saved data
with np.load(load_file_name) as X:
    mtx, dist, rvecs, tvecs = [X[i] for i in ('mtx','dist','rvecs','tvecs')]



def draw(img, corners, imgpts):
    corner = tuple(corners[0].ravel())
    img = cv2.line(img, corner, tuple(imgpts[0].ravel()), (255,0,0), 5)
    img = cv2.line(img, corner, tuple(imgpts[1].ravel()), (0,255,0), 5)
    img = cv2.line(img, corner, tuple(imgpts[2].ravel()), (0,0,255), 5)
    return img




criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
objp = np.zeros((9*6,3), np.float32)
objp[:,:2] = np.mgrid[0:9,0:6].T.reshape(-1,2)
axis = np.float32([[3,0,0], [0,3,0], [0,0,-3]]).reshape(-1,3)

vs = VideoStream(isPiCamera = isPiCamera, resolution = resolution).start()



while(1):

    img = vs.read()
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(gray, (9,6),None)

    
    if ret == True:
        corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
        # Find the rotation and translation vectors.
        ret,rvecs, tvecs = cv2.solvePnP(objp, corners2, mtx, dist)
        # project 3D points to image plane
        imgpts, jac = cv2.projectPoints(axis, rvecs, tvecs, mtx, dist)
        img = draw(img,corners2,imgpts)
        

    cv2.imshow('img',img)
    keypress = cv2.waitKey(1) & 0xFF
    if keypress == ord('q'):
        break

vs.stop()
cv2.destroyAllWindows()