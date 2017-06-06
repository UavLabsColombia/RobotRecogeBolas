import RPi.GPIO as GPIO    #Importamos la libreria RPi.GPIO
import time                #Importamos libreria para el control de tiempos
GPIO.setwarnings(False)    #Se apagan los mensajes de puertos
GPIO.setmode(GPIO.BOARD)   #Ponemos la Raspberry en modo BOARD

#Elementos Globales
GPIO.setup(32,GPIO.OUT)    #Ponemos el pin 32 como salida
servo = GPIO.PWM(32,50)        #Ponemos el pin 32 en modo PWM y enviamos 50 pulsos por segundo
servo.start(0)		   #Inicia El tren de pulsos

#Se inicia el movimiento del motor
servo.ChangeDutyCycle(60)
##tiempo en que el servo se desplazara, este tiempo no tiene razon de ser, es un espacio para provar movimiento y saber que se puede detener
time.sleep(1)
#Se detiene el servo
servo.stop()

##Para el control de la camara
from SimpleCV import *

#Inicia la camara 1 disponible sobre el SO
print "Iniciando la camara del sistema"
camara = SimpleCV.Camera(0)

# Define los elementos que retornaremos de forma global sobre la clase.
pelota_coordenada_x = 0
pelota_coordenada_y = 0
radio_pelota = 0
promedio_coordenada_x = 0
promedio_coordenada_y = 0
promedio_radio = 0
#obtiene los datos de la pelota filtrando los posibles objetos circulares de color negro
# Captura N la pelota para poder confirmar su posicion y almacenar el promedio de donde esta.
n_sensados= 2
for i in range(n_sensados):
    # Obtiene la imagen
    imagen = camara.getImage().flipHorizontal()
    # dilatacion de las cosas que ve la camara entre mas alta, mas expandido el objeto
    dilatacion = imagen.colorDistance(SimpleCV.Color.WHITE).dilate(2)
    #Filtra sobre la escala mas alta de grises, si los niveles son mas bajos, ve mejor en la noche o en la oscuridad, setear
    #en la camara con el filtro
    segmento_colores = dilatacion.stretch(220,245)
    #Busca posibles blobs sobre la toma
    blobs = segmento_colores.findBlobs()
    if blobs:
        # confirma la existencia de circulos
        circulos = blobs.filter([b.isCircle(0.4) for b in blobs])
        if circulos:
            print "X:",circulos[-1].x , "Y:", circulos[-1].y, "Radio:", circulos[-1].radius()
            promedio_coordenada_x+= circulos[-1].x
            promedio_coordenada_y+= circulos[-1].y
            promedio_radio+= circulos[-1].radius()
            #Tiempo necesario para no generar error en la lectura de las imagenes
            time.sleep(0.01)
pelota_coordenada_x = promedio_coordenada_x / n_sensados
pelota_coordenada_y = promedio_coordenada_y / n_sensados
radio_pelota =  promedio_radio / n_sensados
#Imprime en pantalla las coordenadas y radio del ultimo objeto
print "Pelota_coordenada_x", pelota_coordenada_x, "Pelota_coordenada_y:", pelota_coordenada_y , "Radio_pelota", radio_pelota
