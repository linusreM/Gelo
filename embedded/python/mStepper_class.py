import numpy as np
from time import sleep
import RPi.GPIO as GPIO
import thread
from multiprocessing import Value, Process
import sys

M2 = 18
M1 = 15
M0 = 14

DIR1 = 20   #Direction GPIO Pin
DIR2 = 16

STEP = 21  # Step GPIO Pin
SLEEP = 27

CW = 1     # Clockwise Rotation
CCW = 0    # Counterclockwise Rotation
FW = 1
BW = 0


class MOTOR(object):

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(DIR1, GPIO.OUT)
        GPIO.setup(DIR2, GPIO.OUT)
        GPIO.setup(STEP, GPIO.OUT)
        GPIO.output(DIR1, CCW)
        GPIO.output(DIR2, CCW)
        GPIO.setup(M2, GPIO.OUT)
        GPIO.setup(M2, GPIO.OUT)
        GPIO.setup(M1, GPIO.OUT)
        GPIO.setup(M0, GPIO.OUT)
        GPIO.setup(SLEEP, GPIO.OUT)
        GPIO.output(SLEEP, 0)

        GPIO.output(M2,0)
        GPIO.output(M1,0)
        GPIO.output(M0,0)

        VELMAX=1.0/1664

        self.internal_step = 0
        self.stepspermm = 2048.0/(75.61*np.pi)
        self.more = 0
        self.stepperdegree = ((215.0*np.pi)/360)*(2048.0/(75.61*np.pi))


    def motor_turn(self, nbrStep, more, lock, dir, rotation_degree):
        max_velocity=(1.0/1500.0)
        tilt_ramp=10.0
        STEPCOUNTf = self.stepperdegree*float(rotation_degree)   # Steps per Revolution (360 / 7.5)
        STEPCOUNT = int(STEPCOUNTf) 	#Whole steps
        STARTDELAY =100 		#Denominator  of delay  fraction

        lock.acquire()
        nbrStep.value =0 			#How many steps has happened
        self.internal_step = nbrStep.value
        lock.release()

        RAMP = abs(STEPCOUNT)/2
        print(abs(STEPCOUNT))

        GPIO.output(SLEEP, 1)
        if (rotation_degree > 0):
            GPIO.output(DIR1, CW)
            GPIO.output(DIR2, CW)
            lock.acquire()
            dir.value = 1
            lock.release()

        else:
            GPIO.output(DIR2, CCW)
            GPIO.output(DIR1, CCW)
            lock.acquire()
            dir.value = -1
            lock.release()


        lock.acquire()
        more.value = 1
        lock.release()

        for x in range(abs(STEPCOUNT)):
            if self.internal_step < RAMP:	#Positive acceleration
               STARTDELAY +=1*tilt_ramp
               delay = 1.0/STARTDELAY

            if self.internal_step > RAMP:	#Negative acceleration
                STARTDELAY -=1*tilt_ramp
                delay = 1.0/STARTDELAY

            if delay<max_velocity:	#Continiuous speed
               delay = max_velocity

            GPIO.output(STEP, GPIO.HIGH)
            sleep(delay)
            GPIO.output(STEP, GPIO.LOW)
            sleep(delay)

            self.internal_step += 1
            lock.acquire()
            nbrStep.value = self.internal_step
            lock.release()


        self.internal_step = 0
        lock.acquire()
        more.value = 0
        nbrStep.value = self.internal_step
        lock.release()

        GPIO.output(SLEEP, 0)
        return False


    def motor_move(self, nbrStep, more, lock, dir, collision, movement_distance):
        max_velocity=(1.0/1500.0)
        tilt_ramp=10.0
        STEPCOUNTf = self.stepspermm*float(movement_distance)   # Steps per Revolution (360 / 7.5)
        STEPCOUNT = int(STEPCOUNTf)     #Whole steps
        STARTDELAY =100

        lock.acquire()                 #Denominator  of delay  fraction
        nbrStep.value = 0
        self.internal_step = nbrStep.value
        lock.release()
                           #How many steps has happened
        RAMP = abs(STEPCOUNT)/2
        print(abs(STEPCOUNT))

        GPIO.output(SLEEP, 1)

        if (movement_distance > 0):			#Go Forward if distance is positive
            GPIO.output(DIR1, CW)
            GPIO.output(DIR2, CCW)
            lock.acquire()
            dir.value = 1
            lock.release()

        else:
            GPIO.output(DIR1, CCW)
            GPIO.output(DIR2, CW)
            lock.acquire()
            dir.value = -1
            lock.release()
        lock.acquire()
        more.value = 1
        lock.release()

        for x in range(abs(STEPCOUNT)):
            if self.internal_step < RAMP:      #Positive acceleration
                   STARTDELAY +=1*tilt_ramp
                   delay = 1.0/STARTDELAY

            if self.internal_step > RAMP:      #Negative acceleration
                    STARTDELAY -=1*tilt_ramp
                    delay = 1.0/STARTDELAY

            if delay<max_velocity:  #Continiuous speed
                   delay = max_velocity

            GPIO.output(STEP, GPIO.HIGH)
            sleep(delay)
            GPIO.output(STEP, GPIO.LOW)
            sleep(delay)

            self.internal_step += 1
            lock.acquire()
            nbrStep.value = self.internal_step
            lock.release()
            if (collision.value == 1):
                break


        #self.more = 0
        self.internal_step = 0
        lock.acquire()
        more.value = 0
        nbrStep.value = self.internal_step
        collision.value = 0
        lock.release()

        GPIO.output(SLEEP, 0)
        return False
