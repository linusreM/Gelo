from threading import Thread 
import cv2
import numpy as np

class usbVideoStream:

	def __init__(self, src=0, resolution=(640,480)):

		self.stream = cv2.VideoCapture(src)
		self.stream.set(3, resolution[0])
		self.stream.set(4, resolution[1])
		(self.grabbed, self.frame) = self.stream.read()

		self.stopped = False


		with np.load('usbcamera'+ str(resolution[0]) + '_intrinsics.npz') as X:
			self.mtx, self.dist, self.rvecs, self.tvecs = [X[i] for i in ('mtx','dist','rvecs','tvecs')]


	def start(self):
		Thread(target=self.update, args=()).start()
		return self

	def update(self):
		while True:
			if self.stopped:
				self.stream.release()
				return

			(self.grabbed, self.frame) = self.stream.read()


	def read(self):
		return self.frame

	def readUndistorted(self):
		img = self.frame
		h, w = img.shape[:2]
		newcameramtx, roi = cv2.getOptimalNewCameraMatrix(self.mtx, self.dist, (w,h), 1, (w,h))
		map1, map2 = cv2.initUndistortRectifyMap(self.mtx, self.dist, None, newcameramtx, (w,h), 5)
		undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR)
		return undistorted_img


	def stop(self):
		self.stopped = True

