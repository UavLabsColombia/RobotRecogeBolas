from SimpleCV import *
#import time
import time 
cam = SimpleCV.Camera(1)
xcord = 0
ycord = 0
radiopelota = 0
def hubicar_pelota():
    for i in range(5):
        global xcord
        global ycord
        global radiopelota
        xcord = 0
        ycord = 0
        radiopelota = 0
        img = cam.getImage().flipHorizontal()
        dist = img.colorDistance(SimpleCV.Color.WHITE).dilate(2)
        segmented = dist.stretch(220,255)
        blobs = segmented.findBlobs()
        if blobs:
            circles = blobs.filter([b.isCircle(0.24) for b in blobs])
            if circles:
                #print "X:",circles[-1].x , "Y:", circles[-1].y, "Radio:", circles[-1].radius()
                xcord = circles[-1].x
                ycord = circles[-1].y
                radiopelota = circles[-1].radius()
                #time.sleep(0.001)
    print "Xcord:", xcord, "Ycord:", ycord , "Radio", radiopelota


hubicar_pelota()
