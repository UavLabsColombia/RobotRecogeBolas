from SimpleCV import *
import time
#import webbrowser
display = SimpleCV.Display()
cam = SimpleCV.Camera(1)
normaldisplay = True
#js = JpegStreamer()  #starts up an http server (defaults to port 8080)
print "Propiedades de la camara:", cam.getAllProperties()

while display.isNotDone():

	if display.mouseRight:
		normaldisplay = not(normaldisplay)
		print "Display Mode:", "Normal" if normaldisplay else "Segmented"

	img = cam.getImage().flipHorizontal()
	dist = img.colorDistance(SimpleCV.Color.WHITE).dilate(2)
	#dist.show()
	segmented = dist.stretch(230,255)
	blobs = segmented.findBlobs()
	if blobs:
		circles = blobs.filter([b.isCircle(0.3) for b in blobs])
		#help(circles)
		if circles:
			img.drawCircle((circles[-1].x, circles[-1].y), circles[-1].radius(),SimpleCV.Color.RED,2)
			#cam.getImage().save(js)
			#time.sleep(0.1)
			print "X:",circles[-1].x , "Y:", circles[-1].y, "Radio:", circles[-1].radius()
			#time.sleep(0.1)
	if normaldisplay:
		img.show()
	else:
		segmented.show()
