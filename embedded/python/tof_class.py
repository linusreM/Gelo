
import time
import VL53L0X
import RPi.GPIO as GPIO

# GPIO for Sensor 1 shutdown pin
sensor1_shutdown = 5
sensor2_shutdown = 6
sensor3_shutdown = 13
sensor4_shutdown = 19
GPIO.setwarnings(False)

# Setup GPIO for shutdown pins on each VL53L0X
GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor1_shutdown, GPIO.OUT)
GPIO.setup(sensor2_shutdown, GPIO.OUT)
GPIO.setup(sensor3_shutdown, GPIO.OUT)
GPIO.setup(sensor4_shutdown, GPIO.OUT)


# Set all shutdown pins low to turn off each VL53L0X
GPIO.output(sensor1_shutdown, GPIO.LOW)
GPIO.output(sensor2_shutdown, GPIO.LOW)
GPIO.output(sensor3_shutdown, GPIO.LOW)
GPIO.output(sensor4_shutdown, GPIO.LOW)

# Keep all low for 500 ms or so to make sure they reset
time.sleep(0.5)

# Create one object per VL53L0X passing the address to give to
# each.
tof1 = VL53L0X.VL53L0X(address=0x3B)
tof2 = VL53L0X.VL53L0X(address=0x3D)
tof3 = VL53L0X.VL53L0X(address=0x3F)
tof4 = VL53L0X.VL53L0X(address=0x4B)



class TOF(object):
	def __init__(self):

		self.tof_Front = 0
		self.tof_Back = 0
		self.tof_Left = 0
		self.tof_Right = 0
		self.tofVal = "%"

		# Set shutdown pin high for the first VL53L0X then
		# call to start ranging
		GPIO.output(sensor1_shutdown, GPIO.HIGH)
		time.sleep(0.1)
		tof1.start_ranging(0)

		# Set shutdown pin high for the second VL53L0X then
		# call to start ranging
		GPIO.output(sensor2_shutdown, GPIO.HIGH)
		time.sleep(0.1)
		tof2.start_ranging(0)

		GPIO.output(sensor3_shutdown, GPIO.HIGH)
		time.sleep(0.1)
		tof3.start_ranging(0)

		GPIO.output(sensor4_shutdown, GPIO.HIGH)
		time.sleep(0.1)
		tof4.start_ranging(0)

		timing = tof1.get_timing()
		if (timing < 20000):
    			timing = 20000
		print ("Timing %d ms" % (timing/1000))


	def ranging(self):
        	while (True):
	                self.tof_Front = tof1.get_distance()
               		time.sleep(0.02)
                	self.tof_Left = tof2.get_distance()
                	time.sleep(0.02)
                	self.tof_Right= tof3.get_distance()
                	time.sleep(0.02)
                	self.tof_Back = tof4.get_distance()
                	time.sleep(0.02)
                	#print ("Front: %f, Left: %f, Right: %f, Back: %f" (tof_Front, tof_Left, tof_Right, tof_Back))
                	self.tofVal = (str(self.tof_Front) + "#" + str(self.tof_Back) + "#" + str(self.tof_Left) + "#" + str(self.tof_Right) + "#")
                	time.sleep(0.02)
