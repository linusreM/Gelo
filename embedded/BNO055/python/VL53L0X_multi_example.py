#!/usr/bin/python

# MIT License
# 
# Copyright (c) 2017 John Bryan Moore
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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
time.sleep(0.50)

# Create one object per VL53L0X passing the address to give to
# each.
tof1 = VL53L0X.VL53L0X(address=0x2B)
tof2 = VL53L0X.VL53L0X(address=0x2D)
tof3 = VL53L0X.VL53L0X(address=0x2F)
tof4 = VL53L0X.VL53L0X(address=0x3B)

# Set shutdown pin high for the first VL53L0X then 
# call to start ranging 
GPIO.output(sensor1_shutdown, GPIO.HIGH)
time.sleep(0.50)
tof1.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)

# Set shutdown pin high for the second VL53L0X then 
# call to start ranging 
GPIO.output(sensor2_shutdown, GPIO.HIGH)
time.sleep(0.50)
tof2.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)

GPIO.output(sensor3_shutdown, GPIO.HIGH)
time.sleep(0.50)
tof3.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)

GPIO.output(sensor4_shutdown, GPIO.HIGH)
time.sleep(0.50)
tof4.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)

timing = tof1.get_timing()
if (timing < 20000):
    timing = 20000
print ("Timing %d ms" % (timing/1000))

for count in range(1,101):
    distance1 = tof1.get_distance()
#    if (distance1 > 0):
#        print ("sensor %d - %d mm, %d cm, iteration %d" % (tof1.my_object_number, distance, (distance/10), count))
    if (distance1 < 0):
        print ("%d - Error" % tof1.my_object_number)

    distance2 = tof2.get_distance()
#    if (distance2 > 0):
#        print ("sensor %d - %d mm, %d cm, iteration %d" % (tof2.my_object_number, distance, (distance/10), count))
    if (distance2 < 0):
        print ("%d - Error" % tof2.my_object_number)

    distance3 = tof3.get_distance()
#    if (distance3 > 0):
#        print ("sensor %d - %d mm, %d cm, iteration %d" % (tof3.my_object_number, distance, (distance/10), count))
    if (distance3 < 0):
        print ("%d - Error" % tof3.my_object_number)

    distance4 = tof4.get_distance()
#    if (distance > 0):
#        print ("sensor %d - %d mm, %d cm, iteration %d" % (tof4.my_object_number, distance, (distance/10), count))
    if (distance4 < 0): 
        print ("%d - Error" % tof4.my_object_number)
   
    print ("Front: %d, Left: %d, Right: %d, Back: %d" % (distance1, distance2, distance3, distance4))
    time.sleep(timing/100000.00)

tof1.stop_ranging()
GPIO.output(sensor2_shutdown, GPIO.LOW)
tof.stop_ranging()
GPIO.output(sensor1_shutdown, GPIO.LOW)

