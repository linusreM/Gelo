import cv2
import numpy as np



camera = cv2.VideoCapture(0)
numb_of_pics = 0


while(1):
	ret, img = camera.read()
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY, dstCn=0)

	cv2.imshow("Press Space to Save Frame", gray)
	
	keypress = cv2.waitKey(1) & 0xFF
	if keypress == 32:
		numb_of_pics += 1
		file_name = 'chess_' + str(numb_of_pics)
		cv2.imwrite('./calib_pics/' + file_name + '.jpg', gray)
	
	if keypress == ord('q'):
		print str(numb_of_pics) + ' pictures saved'
		break


camera.release()
cv2.destroyAllWindows()
