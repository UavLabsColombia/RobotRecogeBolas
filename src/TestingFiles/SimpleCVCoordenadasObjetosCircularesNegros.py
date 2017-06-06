#Este codigo es una implementacion en opencv el cual se encarga de
#Buscar sobre las imagenes obtenidas por la camara, los posibles circulos de color negro
#el cual puedan representar "Pelotas" si las encuentra, retorna su posicion en el plano X,Y
#y el diametro de la circunferencia

from SimpleCV import *
import time
#Inicia la camara 1 disponible sobre el SO
cam = SimpleCV.Camera(1)
# Define los elementos que retornaremos de forma global sobre la clase.
xcord = 0
ycord = 0
radiopelota = 0
# Funcion que obtiene los datos de la pelota filtrando los posibles objetos circulares de color negro
def hubicar_pelota():
    # Captura 5 veces el objeto para poder confirmar su posicion y almacena la ultima obtenida.
    for i in range(5):
        global xcord
        global ycord
        global radiopelota
        xcord = 0
        ycord = 0
        radiopelota = 0
        # Obtiene la imagen
        img = cam.getImage().flipHorizontal()
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
                xcord = circles[-1].x
                ycord = circles[-1].y
                radiopelota = circles[-1].radius()
                time.sleep(10*10**-6)
    #Imprime en pantalla las coordenadas y radio del ultimo objeto
    print "Xcord:", xcord, "Ycord:", ycord , "Radio", radiopelota


hubicar_pelota()
