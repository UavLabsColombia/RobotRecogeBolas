from SimpleCV import *

class Pelota:
    def __init__(self):
        self.cord_x = 0
        self.ycord_y = 0
        self.radiopelota = 0
        self.pelota = False
        self.cam = SimpleCV.Camera(0)

    #Recibe el numero de veces que va a intentar buscar una pelota
    def hubicar_pelota(self,sensado):
        self.cord_x = 0
        self.cord_y = 0
        self.radiopelota = 0
        self.pelota = False
        prom_x = 0
        prom_y = 0
        radiopelota = 0
        #print "En hubicar_pelota"
        # Rango utilizado para realizar promedio de los datos obtenidos de la pelota
        for i in range(sensado):
            img = self.cam.getImage().flipHorizontal() # Obtiene la imagen
            dist = img.colorDistance(SimpleCV.Color.WHITE).dilate(2) # Filtra el color adecuado a buscar
            segmented = dist.stretch(230,255) #Filtra sobre la escala mas alta de grises
            blobs = segmented.findBlobs() #Busca posibles blobs sobre la toma
            if blobs:
                circles = blobs.filter([b.isCircle(0.4) for b in blobs]) # Pruebe dependiendo de la distancia de la camara al circulo la tolerancia de circularidad: valor de tolerancia=0.050000000000000003 valores recomendados  de 0.1 a 0.4
                if circles:
                    prom_x += circles[-1].x
                    prom_y += circles[-1].y
                    radiopelota += circles[-1].radius()
                    #tiempo necesario para no colgar el hilo sobre el procesador, si se cuelga revisar valor de ser de este tiempo
                    time.sleep(10 * 10 ** -6)
        # si existe un circulo llena las variables de la clase y retorna el estado para la pelota Verdadero si Existe Falso si no
        if circles:
            self.pelota= True
            self.cord_x = prom_x/sensado
            self.cord_y = prom_y/sensado
            self.radiopelota = radiopelota/sensado
            return self.pelota
        else:
            return self.pelota
    # metodos get para la obtencion de variables de la pelota
    def getCordX(self):
        return self.cord_x
    def getCordY(self):
        return self.cord_y
    def getRadio(self):
        return self.radiopelota
    def getPelota(self):
        return self.pelota

#pelota = Pelota()
# if(pelota.hubicar_pelota(1)):
#
#     print "Coordenada X:", pelota.getCordX()
#     print "Radio:", pelota.getRadio()
