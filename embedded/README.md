# Embedded

## Camera

Camera acquisition to be based on:

	https://github.com/igrr/esp32-cam-demo

Using camera:

	OV2640 - Camera with built in JPEG-compression

Basic layout of camera will be to just send raw data to a server which will do any computation needed of the picture. If possible frames might be sent with tags to determine what needs to be done with the frame.


JPEG-compression will be needed to be able to send images at any at all reasonable rate. 


#TODO

* Get camera demo working
* Investigate how to tag data
* Optimize networking and CPU usage

##Sensors

Excluding the camera the robot will need two main sensors:
* Integrated gyro/compass/accellerometer
	* Ex. GY-9250 MPU-9250
* Rangefinders
	* Ex. VL53L0X
