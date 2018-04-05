import time
import sys
import cv2
import zbar
from videostream import VideoStream
from PIL import Image


# Initialise OpenCV window
print "OpenCV version: %s" % (cv2.__version__)
print "Press q to exit ..."

if int(sys.argv[1]) == 1:
    isPiCamera = True
else:
    isPiCamera = False

vs = VideoStream(isPiCamera = isPiCamera, resolution = (640,480)).start()
time.sleep(2.0)

scanner = zbar.ImageScanner()
scanner.parse_config('enable')

# Capture frames from the camera
while(True):

    ticks = time.time()
    frame = vs.read()
 

    # raw detection code
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY, dstCn=0)
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
      #  print symbol.location

        try:
            frame = cv2.line(frame, symbol.location[0],symbol.location[1], (255,0,0), 3)
            frame = cv2.line(frame, symbol.location[1],symbol.location[2], (255,0,0), 3)
            frame = cv2.line(frame, symbol.location[2],symbol.location[3], (255,0,0), 3)
            frame = cv2.line(frame, symbol.location[0],symbol.location[3], (255,0,0), 3)    
        except:
            print 'Not QR'


    # show the frame
    
    cv2.imshow("#Code Reader", frame)


    # Wait for the magic key
    keypress = cv2.waitKey(1) & 0xFF
    if keypress == ord('q'):
        break
    d_time = ticks - time.time()
    print 1/d_time

cv2.destroyAllWindows()
vs.stop()
