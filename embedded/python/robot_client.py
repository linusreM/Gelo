
import logging
import sys
import time
import socket
import VL53L0X
import RPi.GPIO as GPIO
from Queue import Queue
import threading
from stepper_class import *
from tof_class import *
import numpy as np
from Adafruit_BNO055 import BNO055


#Global Variables
tof = ""
stepno = 0

# Verbose debugging if arg -v
#if len(sys.argv) == 2 and sys.argv[2].lower() == '-v':
#    logging.basicConfig(level=logging.DEBUG)


#Init socket

if (int(sys.argv[1]) is not 0):
	clientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	print('attempting connect\n')
	clientsocket.connect(('130.229.166.58', int(sys.argv[1])))
	print('Connection open\n')
	clientsocket.send('Connection open\n')
	time.sleep(1)
	print('Start sending data\n')
	clientsocket.send('Start sending position update\n')
	id = "BOT1"
	packetno = 0

	print('Reading sensor data, press Ctrl-C to quit...')

def client(dir,steps):
	while(True):
		print(steps)
		global tof
		global stepno
		msg=str(id) + "#" + "FW" + "#" + str(steps) + "#" +  "0.0" + "$"
		print(msg)
		clientsocket.send(msg)
		time.sleep(0.05)

def Main():

	global tof
	m = MOTOR()
	t = TOF()
	bno = BNO055.BNO055(address=0x29)
	# Initialize the BNO055 and stop if something went wrong.

	if not bno.begin():
		raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?')

	# Print system status and self test result.
	status, self_test, error = bno.get_system_status()
	print('System status: {0}'.format(status))
	print('Self test result (0x0F is normal): 0x{0:02X}'.format(self_test))
	# Print out an error if system status is in error mode.
	if status == 0x01:
	    print('System error: {0}'.format(error))
	    print('See datasheet section 4.3.59 for the meaning.')

	# Print BNO055 software revision and other diagnostic data.
	sw, bl, accel, mag, gyro = bno.get_revision()
	print('Software version:   {0}'.format(sw))
	print('Bootloader version: {0}'.format(bl))
	print('Accelerometer ID:   0x{0:02X}'.format(accel))
	print('Magnetometer ID:    0x{0:02X}'.format(mag))
	print('Gyroscope ID:       0x{0:02X}\n'.format(gyro))

	print('Reading BNO055 data, press Ctrl-C to quit...')

	tof_thread = threading.Thread(target = t.ranging, args =())
	#DISTANCE = raw_input("Distance [mm]:")
	#motor_thread = threading.Thread(target= m.motor_move, args = ("FW", DISTANCE, 1.0/1500.0))
   	tof_thread.start()
	#motor_thread.start()

	while(True):

		if (m.nbrStep == 0):
			direction = raw_input ("[0] FW/BW" + '\n' + "[1] Rotate" + '\n' + "Choose movement type:")
			distance = raw_input("Distance [+/- mm/degrees]:")

			if (direction is "0"):
				motor_thread = threading.Thread(target= m.motor_move, args = (float(distance), 1.0/1500.0))
				motor_thread.start()
				time.sleep(0.1)

			elif (direction is "1"):
				rotate_thread = threading.Thread(target=m.motor_turn, args = (float(distance), 1.0/900.0))
				rotate_thread.start()
				time.sleep(0.1)
			else:
				print("Invalid dircetion")


		else:
			if (direction is "0"):
				mmStep = m.dir*m.nbrStep/m.stepspermm
			elif (direction is "1"):
				mmStep = m.dir*m.nbrStep/m.stepperdegree
			heading, roll, pitch = bno.read_euler()
			msg=str(id) + "#" + str(direction) + "#" + str(m.more) + "#" + str(mmStep) + "#" +  str(t.tofVal) + str(heading) +  "$"
	        	if (int(sys.argv[1]) is not 0):
				clientsocket.send(msg)

			print(msg)
	        	time.sleep(0.1)

		#if(m.nbrStep>0):
		#	print(m.nbrStep)
		#	msg=str(id) + "#" + "FW" + "#" + str(m.nbrStep) + "#" +  str(t.tofVal) + "$"
        #      		print(msg)
        #        	clientsocket.send(msg)
        #        	time.sleep(0.1)

		#else:
		#	close.motor_thread

if __name__ == '__main__':
	Main()
#tof1.stop_ranging()
#GPIO.output(sensor1_shutdown, GPIO.LOW)
#tof2.stop_ranging()
#GPIO.output(sensor2_shutdown, GPIO.LOW)
#tof3.stop_ranging()
#GPIO.output(sensor3_shutdown, GPIO.LOW)
#tof4.stop_ranging()
#GPIO.output(sensor4_shutdown, GPIO.LOW)
