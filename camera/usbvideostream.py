from threading import Thread 
import cv2

class usbVideoStream:

	def __init__(self, src=0, resolution=(640,480)):

		self.stream = cv2.VideoCapture(src)
		self.stream.set(3, resolution[0])
		self.stream.set(4, resolution[1])
		(self.grabbed, self.frame) = self.stream.read()

		self.stopped = False


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

	def stop(self):
		self.stopped = True

