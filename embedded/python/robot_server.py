
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
import errno

def explore(tof_fwd, tof_left, tof_right, nbrtimes):

    if (tof_fwd>300 and tof_right > 200 and tof_left >200):
        modulus = int(nbrtimes)%3
        print ("Modulus:" + str(modulus))

        if (modulus == 0):
            return ("BOT1"+"#"+"MOVE"+"#"+"150"+"$")

        elif (modulus == 1):
            return ("BOT1"+"#"+"TURN"+"#"+"90"+"$")

        elif (modulus == 2):
            return ("BOT1"+"#"+"TURN"+"#"+"-90"+"$")

        else:
            return ("error")
    else:
        if (tof_left>tof_right):
            return ("BOT1"+"#"+"TURN"+"#"+"-50"+"$")
	else:	  
            return ("BOT1"+"#"+"TURN"+"#"+"50"+"$")

def Main():

    m = MOTOR()
    t = TOF()
    expCount = 0
    command = ""
    ID = "BOT1"
    stopFlag = 1

    # Verbose debugging if arg -v
    if len(sys.argv) == 2 and sys.argv[2].lower() == '-v':
        logging.basicConfig(level=logging.DEBUG)


    #Init socket

    if (int(sys.argv[1]) is not 0):
        clientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #clientsocket.bind(('130.229.189.118', int(sys.argv[1])))
        print('attempting connect\n')
        clientsocket.connect(('130.229.189.118', int(sys.argv[1])))
        print('Connection open\n')
        clientsocket.send('Connection open\n')
        time.sleep(1)
        print('Start sending data\n')
        clientsocket.send('Start sending position update\n')
        ID = "BOT1"
        packetno = 0

         #bind socket to port 3344
        #serversocket.listen(5) # become a server socket, maximum 5 connections

        print('Reading sensor data, press Ctrl-C to quit...')

    serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #initialize UDP stream socket
    serversocket.bind(('0.0.0.0', 8080))

    while(True):

        if (m.nbrStep == 0 and expCount == 0):
            command = ""

            try:
                buf = serversocket.recv(1024, 0X40)

            except socket.error, e:
                err = e.args[0]
                if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                    print "n"
                    time.sleep(0.1)

            else:

                if len(buf) > 0:
                    ID, command, value = buf.split('$')[0].split('#')

                    if (command == "EXPLORE"):
                        expCount = value
                        expCount = int(expCount)
                        print("expCount:" + str(expCount))

                else:
                    print 'No connection'
                    time.sleep(0.1)

        if (expCount > 0):
            expString= explore(tof1.get_distance(),tof2.get_distance(),tof3.get_distance(), expCount)
            ID, command, value = expString.split('$')[0].split('#')
            expCount -= 1

        if (command == "MOVE"):
            motor_thread = threading.Thread(target= m.motor_move, args = (float(value), 1.0/1024.0))
            motor_thread.start()
            time.sleep(0.1)

        elif (command == "TURN"):
            rotate_thread = threading.Thread(target=m.motor_turn, args = (float(value), 1.0/900.0))
            rotate_thread.start()
            time.sleep(0.1)

        else:
            print("No valid command")

        while(m.more == 1 or stopFlag == 0):
	    stopFlag = 0
            if (command == "MOVE"):
                mmStep = m.dir*m.nbrStep/m.stepspermm

            else:
                mmStep = m.dir*m.nbrStep/m.stepperdegree

            tofVal = (str(tof1.get_distance()) + "#" + str(tof4.get_distance()) + "#" + str(tof2.get_distance()) + "#" + str(tof3.get_distance()) + "#")
            time.sleep(0.1)
            msg=str(ID) + "#" + str(command) + "#" + str(m.more) + "#" + str(mmStep) + "#" +  str(tofVal) + "$"

            if (int(sys.argv[1]) is not 0):
                clientsocket.send(msg)

            print(msg)
	    if (m.more == 0):
		stopFlag = 1

        command = ""


if __name__ == '__main__':
    Main()
