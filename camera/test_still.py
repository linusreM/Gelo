import time
import sys
import cv2
import zbar
from PIL import Image



# Initialise OpenCV window
print "OpenCV version: %s" % (cv2.__version__)
print "Press q to exit ..."

scanner = zbar.ImageScanner()
scanner.parse_config('enable')

# Capture frames from the camera
img = cv2.imread(sys.argv[1])

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY, dstCn=0)
pil = Image.fromarray(gray)
width, height = pil.size
raw = pil.tobytes()

   
# create a reader
image = zbar.Image(width, height, 'Y800', raw)
scanner.scan(image)


# extract results
for symbol in image:
# do something useful with results
    print 'decoded', symbol.type, 'symbol', '"%s"' % symbol.data
    print symbol.location
    topLeftCorners, bottomLeftCorners, bottomRightCorners, topRightCorners = [item for item in symbol.location]
    img = cv2.rectangle(img, topLeftCorners, bottomRightCorners, (255,0,0), 3)


# show the frame
cv2.imshow("#Code Reader", img)


# Wait for the magic key
cv2.waitKey(0)