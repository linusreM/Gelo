
import logging
import sys
sys.path.insert(0, '/home/pi/Gelo/camera')
from videostream import VideoStream
from marker import *
import time
import socket
import VL53L0X
import RPi.GPIO as GPIO
from Queue import Queue
import threading
from mStepper_class import *
from tof_class import *
import numpy as np
import cv2
from Adafruit_BNO055 import BNO055
import time
import errno
from multiprocessing import Process, Value, Lock
import random
import fcntl
import struct

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

def explore(tof_fwd, tof_left, tof_right, nbrtimes):

    if (tof_fwd>300 and tof_right > 130 and tof_left >130):
        modulus = int(nbrtimes)%3
        print ("Modulus:" + str(modulus))

        if (modulus == 0):
            if (tof_fwd > 700):
                distance = 400
            else:
                distance = tof_fwd - 250

            return ("BOT1"+"#"+"MOVE"+"#"+str(distance)+"$")

        elif (modulus == 1):
            return ("BOT1"+"#"+"TURN"+"#"+"90"+"$")

        elif (modulus == 2):
            return ("BOT1"+"#"+"TURN"+"#"+"-90"+"$")

        else:
            return ("error")
    elif (tof_left>tof_right):
            rand = -50 + random.randint(-90,90)
            return ("BOT1"+"#"+"TURN"+"#"+str(rand)+"$")
    else:
            rand = 50 + random.randint(-90,90)
            return ("BOT1"+"#"+"TURN"+"#"+str(rand)+"$")

def bno_init():

    bno = BNO055.BNO055(serial_port = '/dev/ttyUSB0')

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

    return bno

def udp_init(CLIENT_IP, ID, MY_IP):
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("My IP:" + str(MY_IP))
    time.sleep(1)
    if (int(sys.argv[1]) is not 0):
        print('attempting connect\n')
        clientsocket.connect((CLIENT_IP, int(sys.argv[1])))
        print('Connected to ' + str(CLIENT_IP) + ":" + str(sys.argv[1]))
        hello_msg = (str(ID) + "#" + "HELLO!" + "#" + str(MY_IP) + "$")
        clientsocket.send(hello_msg)
        print(hello_msg)
        print('Start sending data\n')

    serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #initialize UDP stream socket
    serversocket.bind(('0.0.0.0', 8080))

    return clientsocket, serversocket

def check_rotation_error(command, expected_value, obj, more_flag):
    error_flag = 0
    if command == "MOVE":
        heading_cmp, roll_cmp, pitch_cmp = obj.read_euler()
        if heading_cmp > 180.0:
            heading_cmp = heading_cmp - 360.0
        delta = heading_cmp - expected_value
        print("Delta = " + str(delta))
        if abs(delta)>5.0:
            print("ROTATION ERROR")
            error_flag = 1

    return error_flag


def Main():

    if len(sys.argv) == 2 and sys.argv[2].lower() == '-v':
     logging.basicConfig(level=logging.DEBUG)

    #Initialize all variables and shared memory

    expCount                = 0
    command                 = ""
    instring                = ""
    ID                      = "BOT1"
    stopFlag                = 1
    collision_error         = 0
    start_flag              = 1
    gyro_error              = 0
    nbrStep                 = Value('i', 0)
    more                    = Value('i', 0)
    dir                     = Value('i', 1)
    collision               = Value('i', 0)
    lock                    = Lock()
    CLIENT_IP               = '130.229.159.163'

    #Initialize object

    m                       = MOTOR()
    t                       = TOF()
    vs                      = VideoStream(isPiCamera = True, resolution = (640,480), framerate = 90)
    md                      = MarkerDetector(id = ID)
    MY_IP                   = get_ip_address('wlan0')
    clientsocket, serversocket = udp_init(CLIENT_IP, ID, MY_IP)
    bno_status              = raw_input("Do you want BNO on [1/0]? ")
    if int(bno_status):
        bno                 = bno_init()



    vs.startCamera()
    img = vs.readUndistortedStill()
    md.detectMarkers(img, vs.stream.mtx, vs.stream.dist)

    for message in md.messages:
        print message
        if (int(sys.argv[1]) is not 0):
            clientsocket.send(message)

    vs.stop()


    while(True):

        #If motor is not running or in explore state, start listening to socket
        if (nbrStep.value == 0 and expCount == 0):
            command = ""

            try:
                buf = serversocket.recv(1024, 0X40)

            except socket.error, e:
                err = e.args[0]
                if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                    #print "n"
                    time.sleep(0.1)

            else:
                #If there is an incoming message, split instructionset by $
                #Then split individual messages at #
                if len(buf) > 0:
                    ID, command, value = buf.split('$')[0].split('#')
                    print(buf)
                    #Enter explore state?
                    if (command == "EXPLORE"):
                        expCount = value
                        expCount = int(expCount)
                        print("expCount:" + str(expCount))

                else:
                    #print 'No connection'
                    time.sleep(0.1)


        #Check if explore state is active, and if so carry out next instruction
        if (expCount > 0):
            expString= explore(tof1.get_distance(),tof2.get_distance(),tof3.get_distance(), expCount)
            ID, command, value = expString.split('$')[0].split('#')
            expCount -= 1

        if (command == "MOVE"):
            #heading_ref, x, y = bno.read_euler()
            #print("Heading_REF:" + str(heading_ref))
            #time.sleep(2)
            #if heading_ref > 180.0:
            #    heading_ref = heading_ref - 360.0
            motor_process = Process(target= m.motor_move, args = (nbrStep, more, lock, dir, collision, float(value)))
            motor_process.start()
            time.sleep(0.1)

        elif (command == "TURN"):
            rotate_process = Process(target=m.motor_turn, args = (nbrStep, more, lock, dir, float(value)))
            rotate_process.start()
            time.sleep(0.1)

        #else:
            #print("No valid command")

        #Only send data to Unity while motors are running + one last time when moreFlag is 0
        while(more.value == 1 or stopFlag == 0):
            stopFlag = 0
            if (command == "MOVE"):
                mmStep = dir.value*nbrStep.value/m.stepspermm

            else:
                mmStep = dir.value*nbrStep.value/m.stepperdegree

            tof_fwd = tof1.get_distance()
            tof_left = tof2.get_distance()
            tof_right = tof3.get_distance()
            tof_back = tof4.get_distance()
            tofVal = (str(tof_fwd) + "#" + str(tof_back) + "#" + str(tof_left) + "#" + str(tof_right))
            bnoVal = ""
            try:
                heading, roll, pitch = bno.read_euler()
                bnoVal = (str(heading) + "#" + str(roll) + "#" + str(pitch))
            except:
                #print("no bno")
		pass
            msg=str(ID) + "#" + str(command) + "#" + str(more.value) + "#" + str(mmStep) + "#" +  str(tofVal) + "#" + str(bnoVal) + "$"
            if (int(sys.argv[1]) is not 0):
                clientsocket.send(msg)

            print(msg)

            if(collision_error == 1):
                collision_error = 0
                msg=str(ID) + "#" + "ERROR" + "#" + "FRONT_COLLISION"+ "$"
                if (int(sys.argv[1]) is not 0):
                    clientsocket.send(msg)
                print(msg)

            #if(gyro_error == 1):
            #    gyro_error = 0
            #    msg=str(ID) + "#" + "ERROR" + "#" + "GYRO_OFFSET"+ "$"
            #    if (int(sys.argv[1]) is not 0):
            #        clientsocket.send(msg)
            #    print(msg)


         #   if (tof_fwd < 200 and dir.value == 1 and more.value == 1):
          #      print("CRASH IN" + str(tof_fwd) + "mm!!!")
          #      collision.value = 1
          #      lock.acquire()
          #      more.value = 0
          #      lock.release()
          #      collision_error = 1

            #gyro_error = check_rotation_error(command, heading_ref, bno, more.value)

            if (more.value == 0 and collision_error == 0):
                stopFlag = 1
                vs.startCamera()
                img = vs.readUndistortedStill()
                md.detectMarkers(img, vs.stream.mtx, vs.stream.dist)

                for message in md.messages:
                    print message
                    if (int(sys.argv[1]) is not 0):
                        clientsocket.send(message)
                vs.stop()

        command = ""

        try:
            motor_process.is_alive()
            #print ("Motor process still alive")
            motor_process.terminate()
            motor_process.join()
        except:
            #print("Motor process not alive")
	    pass


if __name__ == '__main__':
    Main()
