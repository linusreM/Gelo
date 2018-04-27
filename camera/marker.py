

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

