from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Thread
import numpy as np
import cv2
import time

def how_long(start, op):
	print('%s took %.2fs' % (op, time.clock() - start))
	return time.clock()
	
class PiVideoStream:

	def __init__(self, resolution=(640, 480), framerate = 32):

		self.resolution = resolution
		self.framerate = framerate
		self.frame = None
		self.stopped = False
		
############
		#self.camera = PiCamera(resolution = resolution, framerate = framerate)
		#self.rawCapture = PiRGBArray(self.camera, size = resolution)
		#self.stream = self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True)
#############
		with np.load('/home/pi/Gelo/camera/picamera'+ str(resolution[0]) + '_intrinsics.npz') as X:
			self.mtx, self.dist, self.rvecs, self.tvecs = [X[i] for i in ('mtx','dist','rvecs','tvecs')]
	
	def how_long(start, op):
		print('%s took %.2fs' % (op, time.time() - start))
		return time.time()


	def startCamera(self):
		#start = time.clock()
		self.camera = PiCamera(resolution = self.resolution, framerate = self.framerate)
		#start = how_long(start,'init')
		self.rawCapture = PiRGBArray(self.camera, size = self.resolution)
		#start = how_long(start,'raw')

	def start(self):
		Thread(target=self.update, args=()).start()
		return self


	def update(self):
		for f in self.stream:
			self.frame = f.array
			self.rawCapture.truncate(0)

			if self.stopped:
				self.stream.close()
				self.rawCapture.close()
				self.camera.close()
				return


	def read(self):
		return self.frame


	def readUndistortedStill(self):
		#start = time.clock()
		self.camera.capture(self.rawCapture, format="bgr")
		img = self.rawCapture.array
		#start = how_long(start, 'capture')
		h, w = img.shape[:2]
		map1, map2 = cv2.fisheye.initUndistortRectifyMap(self.mtx, self.dist, np.eye(3), self.mtx, self.camera.resolution, cv2.CV_16SC2)
		undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
		#start = how_long(start, 'undistortion')
		return undistorted_img
		

	def readUndistorted(self):
		img = self.frame
		h, w = img.shape[:2]
		map1, map2 = cv2.fisheye.initUndistortRectifyMap(self.mtx, self.dist, np.eye(3), self.mtx, self.camera.resolution, cv2.CV_16SC2)
		undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
		return undistorted_img



	def stop(self):
		self.stopped = True
		#self.stream.close()
		self.rawCapture.close()
		self.camera.close()






		






