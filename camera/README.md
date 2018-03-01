# Camera


This program will handle recieving frames from the embedded system. It will then analyze the image based on the requested services and send the relevant information to the Unity-based main program.

Possible uses:
* Read codes bar/QR
* Calculate position based on landmarks
* Object recognition



USB-webcam flood fix:
* /sbin/modprobe uvcvideo quirks=128 (and reconnect camera)
