import cv2
import cv2.aruco as aruco
import numpy as np

class Marker:
	def __init__(self, corners, data, tvecs, rvecs):
		
		self.corners = corners
		self.data = data[0]

		self.tvecs_x = tvecs[0,0]
		self.tvecs_y = tvecs[0,1]
		self.tvecs_z = tvecs[0,2]

		self.rvecs_x = rvecs[0,0]
		self.rvecs_y = rvecs[0,1]
		self.rvecs_z = rvecs[0,2]


class MarkerDetector:
	def __init__(self, id):
		self.id = id
		self.type = "QR"
		self.dictionary = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)
		self.parameters = aruco.DetectorParameters_create()

		self.parameters.cornerRefinementMethod = 1
		self.parameters.cornerRefinementWinSize = 5
		self.parameters.cornerRefinementMaxIterations = 30
		self.parameters.cornerRefinementMinAccuracy = 0.0001

	def detectMarkers(self, img, mtx, dist):
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

		corners, ids, rejected = aruco.detectMarkers(gray, self.dictionary, parameters = self.parameters)
		rvecs, tvecs, obj = aruco.estimatePoseSingleMarkers(corners, 65.18, mtx, dist)

		markers = []
		self.messages = []

		try:
			for i in range(len(ids)):
				marker = Marker(corners[i], ids[i], tvecs[i], rvecs[i])
				markers.append(marker)
				print "HERE"
				print len(markers)

			for marker in markers:
				self.messages.append("{}#{}#{}#{}#{}#{}#{}#{}#{}$".format(
						self.id, 
						self.type, 
						marker.data, 
						marker.tvecs_x, 
						marker.tvecs_y, 
						marker.tvecs_z, 
						marker.rvecs_x, 
						marker.rvecs_y, 
						marker.rvecs_z
				)) 	
				
		except:
			print "no code"

