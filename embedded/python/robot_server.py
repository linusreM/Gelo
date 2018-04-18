
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


#Global Variables
tof = ""
stepno = 0




def client(dir,steps):
    while(True):
        print(steps)
        global tof
        global stepno
        msg=str(id) + "#" + "FW" + "#" + str(steps) + "#" +  "0.0" + "$"
        print(msg)
        clientsocket.send(msg)
        time.sleep(0.05)

def explore(tof_fwd, tof_left, tof_right, nbrtimes):

    if (tof_fwd>200):
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
            return ("BOT1"+"#"+"TURN"+"#"+"50"+"$")

        else:
            return ("BOT1"+"#"+"TURN"+"#"+"-50"+"$")

def Main():

    m = MOTOR()
    t = TOF()
    expCount = 0
    command = ""

    # Verbose debugging if arg -v
    if len(sys.argv) == 2 and sys.argv[2].lower() == '-v':
        logging.basicConfig(level=logging.DEBUG)


    #Init socket

    if (int(sys.argv[1]) is not 0):
        clientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print('attempting connect\n')
        clientsocket.connect(('localhost', int(sys.argv[1])))
        print('Connection open\n')
        clientsocket.send('Connection open\n')
        time.sleep(1)
        print('Start sending data\n')
        clientsocket.send('Start sending position update\n')
        id = "BOT1"
        packetno = 0

         #bind socket to port 3344
        #serversocket.listen(5) # become a server socket, maximum 5 connections

        print('Reading sensor data, press Ctrl-C to quit...')

    serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #initialize UDP stream socket
    serversocket.bind(('0.0.0.0', 8080))


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

    #tof_thread = threading.Thread(target = t.ranging, args =())
    #DISTANCE = raw_input("Distance [mm]:")
    #motor_thread = threading.Thread(target= m.motor_move, args = ("FW", DISTANCE, 1.0/1500.0))
       #tof_thread.start()
    #motor_thread.start()

    while(True):
        if(sys.argv[1] == 0 and m.nbrStep == 0 and expCount == 0):
            ID = BOT1
            command = raw_input("Command:")
            value = raw_input("Value")

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
                    print ("Buf:" + buf)
                    cmdArray = buf.split('$')[0].split('#')
                    #msg = str(buf.split("$"))
                    #print ("First split:" + msg)
                    #cmdArray =  str(msg.split("#"))
                    print (cmdArray)
                    ID = cmdArray[0]
                    command = cmdArray[1]
                    value = cmdArray[2]
                    print ("ID:" + ID  + "\n")
                    print ("Command:" + command + "\n")
                    print("value:" + value + "\n")
                    if (command == "EXPLORE"):
                        expCount = value
                        expCount = int(expCount)
                        print("expCount:" + str(expCount))

                    time.sleep(0.5)
                    #print ( "\n ID:" + list + "\n Command:" + command + "\n Distance/Angle:" + distance)
                else:
                    print 'No connection'
                    time.sleep(0.1)



            if (expCount > 0):

                print("Init Explore...")
                print("Value:" + str(expCount))
                tof_Front = tof1.get_distance()
                tof_Left = tof2.get_distance()
                tof_Right= tof3.get_distance()
                print("Sensor data fetched...")
                expString= explore(tof_Front,tof_Left, tof_Right, expCount)
                print("Explore function done:" + expString)
                expArray = expString.split('$')[0].split('#')
                print(expArray)
                ID = expArray[0]
                command = expArray[1]
                value = expArray[2]
                expCount -= 1
                print(str(expCount))
                #motor_thread = threading.Thread(target= m.motor_move = "", args = (str(command), float(value), 1.0/1024.0))
                #motor_thread.start()
                time.sleep(0.1)


            if (command == "MOVE"):
                print("Init Move...")
                print("Value:" + value)
                motor_thread = threading.Thread(target= m.motor_move, args = (float(value), 1.0/1024.0))
                motor_thread.start()
                time.sleep(0.1)


            elif (command == "TURN"):
                print("Init turn...")
                print("Value:" + value)
                rotate_thread = threading.Thread(target=m.motor_turn, args = (float(value), 1.0/900.0))
                rotate_thread.start()
                time.sleep(0.1)

            else:
                print("No valid command")

#            except:
 #               error = e.args[0]
  #              print("Error:" + str(error))
   #             time.sleep(0.5 )

        else:

            if (command == "MOVE"):
                mmStep = m.dir*m.nbrStep/m.stepspermm

            else:
                mmStep = m.dir*m.nbrStep/m.stepperdegree


            tof_Front = tof1.get_distance()

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

            msg=str(id) + "#" + str(command) + "#" + str(m.more) + "#" + str(mmStep) + "#" +  str(tofVal) + "$"

            if (int(sys.argv[1]) is not 0):
                clientsocket.send(msg)

            print(msg)


if __name__ == '__main__':
    Main()
