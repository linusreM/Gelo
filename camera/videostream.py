class VideoStream:
	def __init__(self, src=0, isPiCamera=False, resolution=(320,240), framerate=32):
		
		if isPiCamera:
			from pivideostream import PiVideoStream

			self.stream = PiVideoStream(resolution = resolution, framerate = framerate)

		else: 
			from usbvideostream import usbVideoStream

			self.stream = usbVideoStream(src, resolution = resolution)


	def start(self):
		return self.stream.start()

	def update(self):
		self.stream.update()

	def read(self):
		return self.stream.read()

	def stop(self):
		self.stream.stop()

		