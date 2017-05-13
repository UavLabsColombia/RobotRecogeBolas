from SimpleCV import *

class Pelota:
    def __init__(self):
        print "En pelota :)"
        self.cord_x = 0
        self.ycord_y = 0
        self.radiopelota = 0
        self.cam = SimpleCV.Camera(0)
        self.pelota = False
#Recibe el numero de veces que va a intentar buscar una pelota
    def hubicar_pelota(self,sensado):
        self.cord_x = 0
        self.cord_y = 0
        self.radiopelota = 0
        self.pelota = False
        cord_x=0
        cord_y=0
        radiopelota=0
        # Captura 5 veces el objeto para poder confirmar su posicion y almacena la ultima obtenida.
        for i in range(sensado):
            # Obtiene la imagen
            img = self.cam.getImage().flipHorizontal()
            # Filtra el color adecuado a buscar
            dist = img.colorDistance(SimpleCV.Color.WHITE).dilate(2)
            #Filtra sobre la escala mas alta de grises
            segmented = dist.stretch(220,255)
            #Busca posibles blobs sobre la toma
            blobs = segmented.findBlobs()
            if blobs:
                # confirma la existencia de circulos
                circles = blobs.filter([b.isCircle(0.24) for b in blobs])
                if circles:
                    #print "X:",circles[-1].x , "Y:", circles[-1].y, "Radio:", circles[-1].radius()
                    cord_x += circles[-1].x
                    cord_y += circles[-1].y
                    radiopelota += circles[-1].radius()
                    #time.sleep(0.001)

        #Imprime en pantalla las coordenadas y radio del ultimo objeto
        ##print "Xcord:", xcord, "Ycord:", ycord , "Radio", radiopelota
        if (cord_x!=0):
            self.pelota= True
            self.cord_x = cord_x/sensado
            self.cord_y = cord_y/sensado
            self.radiopelota = radiopelota/sensado
            return pelota
        else:
            return pelota

pelota = Pelota()
#print pelota.hubicar_pelota(5)
