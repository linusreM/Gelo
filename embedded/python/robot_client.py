
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

#Global Variables
tof = ""
stepno = 0

# Verbose debugging if arg -v
if len(sys.argv) == 2 and sys.argv[2].lower() == '-v':
    logging.basicConfig(level=logging.DEBUG)


#Init socket


clientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print('attempting connect\n')
clientsocket.connect(('130.229.142.225', int(sys.argv[1])))
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
	tof_thread = threading.Thread(target = t.ranging, args =())
	#DISTANCE = raw_input("Distance [mm]:")
	#motor_thread = threading.Thread(target= m.motor_move, args = ("FW", DISTANCE, 1.0/1500.0))
   	tof_thread.start()
	#motor_thread.start()

	while(True):
		print(m.nbrStep)
		if (m.nbrStep == 0):
			direction = raw_input ("[1] Forward" + '\n' + "[2] Backwards" '\n' + "[3] Rotate Right" + '\n' "[4] Rotate Left" + '\n' + '\n' + "Choose movement type:")
			distance = raw_input("Distance [mm/degrees]:")

			if (int(direction) <=2):
				motor_thread = threading.Thread(target= m.motor_move, args = (int(direction), distance, 1.0/1500.0))
				motor_thread.start()
				time.sleep(0.1)

			elif (int(direction)<=4):
				rotate_thread = threading.Thread(target=m.motor_turn, args = (int(direction), distance, 1.0/1500.0))
				rotate_thread.start()
				time.sleep(0.1)
			else:
				print("Invalid dircetion")


		else:
			mmStep = m.nbrStep/m.stepspermm
			msg=str(id) + "#" + str(direction) + "#" + str(mmStep) + "#" +  str(t.tofVal) + "$"
	        	print(msg)
	        	clientsocket.send(msg)
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
