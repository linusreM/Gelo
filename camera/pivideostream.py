from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Thread
import numpy as np
import cv2


class PiVideoStream:

	def __init__(self, resolution=(640, 480), framerate = 32):

		self.camera = PiCamera()
		self.camera.resolution = resolution
		self.camera.framerate = framerate
		self.rawCapture = PiRGBArray(self.camera, size = resolution)
		self.stream = self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True)

		self.frame = None
		self.stopped = False

		with np.load('picamera'+ str(resolution[0]) + '_intrinsics.npz') as X:
			self.mtx, self.dist, self.rvecs, self.tvecs = [X[i] for i in ('mtx','dist','rvecs','tvecs')]
		

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

	def readUndistorted(self):
		img = self.frame
		h, w = img.shape[:2]
		map1, map2 = cv2.fisheye.initUndistortRectifyMap(self.mtx, self.dist, np.eye(3), self.mtx, self.camera.resolution, cv2.CV_16SC2)
		undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
		return undistorted_img

	def stop(self):
		self.stopped = True






		






