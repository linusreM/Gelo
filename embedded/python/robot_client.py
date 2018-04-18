
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
import time


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
	clientsocket.connect(('130.229.175.7', int(sys.argv[1])))
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

def explore(front,left,right,move,turn,flag, maxinstruct):

	instruction = 0

        while (instruction<=maxinstruct):

                if(front>150):
                        motor_thread = threading.Thread(target= move, args = (float(150), 1.0/1500.0))
                        motor_thread.start()
                        time.sleep(0.1)
			instruction+=1
                        while(flag==1):
                        	time.sleep(0.1)

                        rotate_thread = threading.Thread(target=turn , args = (float(90), 1.0/900.0))
                        rotate_thread.start()
                        time.sleep(0.1)

                        while(flag==1):
                        	time.sleep(0.1)

                        rotate_thread = threading.Thread(target=turn, args = (float(-90), 1.0/900.0))
                        rotate_thread.start()
                        time.sleep(.1)

                        while(flag==1):
                            time.sleep(0.1);

                if(right>left):
                        rotate_thread = threading.Thread(target=turn, args = (float(50), 1.0/900.0))

                else:
                        rotate_thread = threading.Thread(target=turn, args = (float(-50), 1.0/900.0))
 
                        rotate_thread.start()
                        time.sleep(0.1)
                        while(flag==1):
                                time.sleep(0.1)
		print(flag)
                        

def Main():

	m = MOTOR()
	t = TOF()

	if (int(sys.argv[3]) is not 0):
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
	time.sleep(0.5)

	while(True):

		if (m.nbrStep == 0):
			direction = raw_input ("[0] FW/BW" + '\n' + "[1] Rotate" + '\n' + "Choose movement type:")
			distance = raw_input("Distance [+/- mm/degrees]:")

			if (direction is "0"):
				motor_thread = threading.Thread(target= m.motor_move, args = (float(distance), 1.0/1024.0))
				motor_thread.start()
				time.sleep(0.1)

			elif (direction is "1"):
				rotate_thread = threading.Thread(target=m.motor_turn, args = (float(distance), 1.0/900.0))
				rotate_thread.start()
				time.sleep(0.1)

			elif (direction is "2"):
				explore(t.tof_Front,t.tof_Left,t.tof_Right, m.motor_move, m.motor_turn,m.more, distance)

			else:
				print("Invalid dircetion")


		else:
			if (direction is "0"):
				mmStep = m.dir*m.nbrStep/m.stepspermm

			elif (direction is "1"):
				mmStep = m.dir*m.nbrStep/m.stepperdegree

			if (int(sys.argv[3]) is not 0):
				heading, roll, pitch = bno.read_euler()

			else:
				heading = "n/a"


			tof_Front = tof1.get_distance()
			end = time.time()
			#time.sleep(0.02)
			tof_Left = tof2.get_distance()
			#time.sleep(0.02)
			tof_Right= tof3.get_distance()
			#time.sleep(0.02)
			tof_Back = tof4.get_distance()
			time.sleep(0.02)

			#print ("Front: %f, Left: %f, Right: %f, Back: %f" (tof_Front, tof_Left, tof_Right, tof_Back))
			tofVal = (str(tof_Front) + "#" + str(tof_Back) + "#" + str(tof_Left) + "#" + str(tof_Right) + "#")
			#tofVal = (str(tof1.get_distance) + "#" + str(tof4.get_distance) + "#" + str(tof2.get_distance) + "#" + str(tof3.get_distance) + "#")

			msg=str(id) + "#" + str(direction) + "#" + str(m.more) + "#" + str(mmStep) + "#" +  str(tofVal) + "$"

			if (int(sys.argv[1]) is not 0):
				clientsocket.send(msg)

			print(msg)


if __name__ == '__main__':
	Main()
