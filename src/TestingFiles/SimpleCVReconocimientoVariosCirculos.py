from SimpleCV import *
import time
display = SimpleCV.Display()
cam = SimpleCV.Camera(1)
normaldisplay = True
print "Propiedades de la camara:", cam.getAllProperties()

while display.isNotDone():

	if display.mouseRight:
		normaldisplay = not(normaldisplay)
		print "Display Mode:", "Normal" if normaldisplay else "Segmented"

	img = cam.getImage().flipHorizontal()
	dist = img.colorDistance(SimpleCV.Color.WHITE).dilate(2)
	segmented = dist.stretch(225,255)
	blobs = segmented.findBlobs()
	if blobs:
		circles = blobs.filter([b.isCircle(0.3) for b in blobs])
        if circles:
                    for i in circles:
            			img.drawCircle((i.x, i.y), i.radius(),SimpleCV.Color.RED,2)
            			print "X:",i.x , "Y:", i.y, "Radio:", i.radius()
	if normaldisplay:
		img.show()
	else:
		segmented.show()
