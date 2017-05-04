# Este codigo es una implementacion que se realiza con las librerias de vision por computador
# disponibles bajo python para el control de robots Recoge Bolas.
#
# Realizado por: Estudiantes de la universidad del valle.
# Heberth Alexander Ardila Cuellar / heberthardila@gmail.com / 3128204694 / uavlabs.org
# Jaime Andres Ortiz Aranda  / jaime-aranda@outlook.com / 3023476635 ###
#
#
# Este software se encuentra bajo la licencia GPLv3 disponible sobre este repositorio, sientase libre de modificarlo
# ajustarlo y redistribuirlo manteniendo la licencia y los autores
#
# Sobre los siguientes diagramas, se describen la conexiones que se ralizan sobre los sensores y el sistema
#
######################################
# Motoreductores DC 12v
# Motor_izquierdo_adelante, motor_izquierdo_atras, motor_derecho_adelante, motor_derecho_atras:
#              _Front_
#        _________________
# --------------------------------
# M1=In1,In2         M2=In1,In2
#
#
#
# M3=In3,In4          M4= In3,In4
# --------------------------------
######################################
#
######################################
##Controladores L298N
## Se utilizaran dos controladores para los motores
# Cont1, Cont2:
# (EnA)
# (In1)
# (In2)
# (In3)
# (In4)
# (EnB)
######################################
#
######################################
##Sensor Sonar HC SR04 Utilizado para calcular el promedio de la distancia a un objeto.
#sonar_izquierdo, sonar_derecho, sonar_frente_izquierdo, sonar_frente_derecho, sonar_frente
#(Trig)
#(Echo)
######################################
#
######################################
##Conexiones con RaspberryPi
# Conexiones USB:
# Conectaremos por USB la camara SJCAM M10, el cual sera utiizada
# para trabajar con las librerias de Vision Artificial
## Pines de conexion para la raspberry pi 3 en modo BOARD
#	(01)                          (02)
#	(03)Cont1.M1.EnA              (04)
#	(05)Cont1.M1.In1              (06)
#	(07)Cont1.M1.In2              (08) sonar_izquierdo.trig
#	(09)                          (10) sonar_izquierdo.echo
#	(11)Cont1.M3.In3              (12) sonar_frente_izquierdo.trig
#	(13)Cont1.M3.In4              (14)
#	(14)Cont1.M3.EnB              (16) sonar_frente_izquierdo.echo
#	(17)                          (18) sonar_frente_derecho.trig
#	(19)                          (20)
#	(21)                          (22) sonar_frente_derecho.echo
#	(23)                          (24) sonar_derecho.trig
#	(25)                          (26) sonar_derecho.echo
#	(27)Cont2.M2.EnA              (28) sonar_frente.trig
#	(29)Cont2.M2.In1              (30) sonar_frrente.echo
#	(31)Cont2.M2.In2              (32)
#	(33)Cont2.M4.In3              (34)
#	(35)Cont2.M4.InB              (36)
#	(37)                          (38)
#	(39)                          (40)
#
#######################################

# importamos libreria del sistema
import sys
# from hcsr04sensor import sensor
# Importamos libreria GPIO
import RPi.GPIO as GPIO
# Importamos librerias para el control de tiempos
import time
# Importamos librerias para el control de hilos o multihilos
from threading import Thread
# se importa libreria SimpleCV "Vision por Computador Simple"
from SimpleCV import *

# Se inician y se cargan dependencias y configuraciones
# modo de los pines, basados en BCM o en BOARD
GPIO.setmode(GPIO.BOARD)
##Elementos globales para la clase
# posiciones
# 0 = motor1A  1=motor1B 2=motor2A 3=motor2B
channel = [11, 12, 13, 15, 16, 18]
# channel=[13,15]
# version de opencv
# se confirma version de OPENCV instalado
cversion = cv2.__version__
##
##cont=0

# Definimos las coordenadas para los objetos circulares en pantalla
xcord = 0
ycord = 0
radiopelota = 0

#Iniciando el software..
# Inicializacion del software
print "Iniciando el software para el control del robot...."
print "Info de la PI"
print GPIO.RPI_INFO
# version de python
print "Version de python:", sys.version

# Se imprime el modo de configuracion para los pines
mode = GPIO.getmode()
if (mode == 10):
    print "modo de la tarjeta:", mode, "(BOARD)"
if (mode == 11):
    print "modo de la tarjeta:", mode, "(BCM)"

# se quitan las alertas de re-definicion para los pines
GPIO.setwarnings(False)

# se definen y se inician los pines a utilizar sobre la raspberry para el control de motores...
# estado = 0 pin de salida, estado=1 pin de entrada
GPIO.setup(channel[0], GPIO.OUT)
print "Puerto:", channel[0], "Estado:", GPIO.gpio_function(channel[0])
GPIO.setup(channel[1], GPIO.OUT)
print "Puerto:", channel[1], "Estado:", GPIO.gpio_function(channel[1])
GPIO.setup(channel[2], GPIO.OUT)
print "Puerto:", channel[2], "Estado:", GPIO.gpio_function(channel[2])
GPIO.setup(channel[3], GPIO.OUT)
print "Puerto:", channel[3], "Estado:", GPIO.gpio_function(channel[3])
GPIO.setup(channel[4], GPIO.OUT)
print "Puerto:", channel[4], "Estado:", GPIO.gpio_function(channel[4])
GPIO.setup(channel[5], GPIO.OUT)
print "Puerto:", channel[5], "Estado:", GPIO.gpio_function(channel[5])

## Iniciar camara
print "Iniciando SimpleCV y camara.."
cam = SimpleCV.Camera(0)
print "Camara OK"


## MOvimientos para los motores
# los siguientes metodos describen los sentidos de giros para el robot, adelante, atras, derecha, izquierda, stop
def izquierda():
    print "Izquierda"
    GPIO.output(channel[3], GPIO.HIGH)
    GPIO.output(channel[2], GPIO.LOW)


def derecha():
    print "Derecha"
    GPIO.output(channel[2], GPIO.HIGH)
    GPIO.output(channel[3], GPIO.LOW)


def adelante():
    print "Adelante"
    GPIO.output(channel[0], GPIO.LOW)
    GPIO.output(channel[1], GPIO.HIGH)
    # GPIO.output(channel[0], GPIO.LOW)


def atras():
    print "Atras"
    GPIO.output(channel[1], GPIO.HIGH)
    GPIO.output(channel[0], GPIO.LOW)


def stop():
    print "Stop"
    GPIO.output(channel[4], GPIO.LOW)
    GPIO.output(channel[5], GPIO.LOW)


## numero de sonares que tendra disponible el robot

sonar_trig = [21, 23, 25, 27]
sonar_echo = [22, 24, 26, 28]


## Este metodo describe el funcionamiento del sensor HC-SR04, el cual retorna la distancia en CM de algun obstaculo
def dist_objeto(trig, echo):
    print "Distancia en proceso de calculo..."
    ##Se inicial a distancia en 0 indicando que no hay datos sobre la lectura de distancia.
    distancia = 0
    ## Se define el pin trig y el pin echo para el sensor
    GPIO.setup(trig, GPIO.OUT)
    GPIO.setup(echo, GPIO.IN)
    ## se apaga el pulso para no generar interferencias.
    GPIO.output(trig, GPIO.LOW)
    ## tiempo que dura el pulso apagado 2microsegundos
    time.sleep(2 * 10 ** -6)
    ## se enciende el pulso durante 10microsegundos
    GPIO.output(trig, GPIO.HIGH)
    time.sleep(10 * 10 ** -6)
    ## se apaga el pulso
    GPIO.output(trig, GPIO.LOW)
    print "No llega senial"
    ## se empieza a contabilizar el tiempo mientras no se llegue senial.
    while GPIO.input(echo) == 0:
        pulse_start = time.time()
    ## si se recibe senial en el sensor toma el tiempo
    print "llegando senial"
    while GPIO.input(echo) == 1:
        pulse_end = time.time()
    duracion_pulso = pulse_end - pulse_start
    distancia = (duracion_pulso * 34300) / 2
    return distancia


##Metodo que sensa la camara y reconoce algun objeto de esta, imprime las coordenadas en X,y y diametro de la circunferencia
def hubicar_pelota():
    tiempo_inicial = time.time()
    print "Hubicando pelota.."
    for i in range(1):
        global xcord
        global ycord
        global radiopelota
        xcord = 0
        ycord = 0
        radiopelota = 0
        img = cam.getImage().flipHorizontal()
        dist = img.colorDistance(SimpleCV.Color.WHITE).dilate(2)
        segmented = dist.stretch(230, 255)
        blobs = segmented.findBlobs()
        if blobs:
            circles = blobs.filter([b.isCircle(0.3) for b in blobs])
            if circles:
                # print "X:",circles[-1].x , "Y:", circles[-1].y, "Radio:", circles[-1].radius()
                xcord = circles[-1].x
                ycord = circles[-1].y
                radiopelota = circles[-1].radius()
    tiempo_final = time.time()
    print "Tiempo ejecucion:", tiempo_final - tiempo_inicial
    print "Xcord:", xcord, "Ycord:", ycord, "Radio", radiopelota


def donde_ir():
    print "Llengo a la pelota"


def determinar_obstaculos():
    print "Determinando obtaculos..."
    # Se toman las distancias de los sonares


# funcion que obtiene un pulso electrico de un puerto digital, sensando el dato de entrada, parando o iniciando el sistema.
def pulsador():
    estado_boton = 1
    return estado_boton


##se define el metodo que sensara todo el sistema
def sensar():
    # while True:
    # Orden de como va a sensar el sistema, prioridad de sensores..
    hubicar_pelota()
    determinar_obstaculos()


def cerrar_conexion():
    print " "
    print "Limpiando puerto GPIO..."
    GPIO.cleanup()
    print "Saliendo..."
    sys.exit(0)


def run():
    print "Logica de movimiento..."
    sensar()


# El core o nucleo, es el encargador de iniciar todas las ejecuciones y revisar los estados de  todos los sensores

def core():
    #    global cont
    #    cont = cont + 1
    if (pulsador() == 0):
        stop()
    if (pulsador() == 1):
        run()


# print "Cont:", cont

# Inicia la ejecucion de toda la clase
try:
    while 1:
        core()
        # time.sleep(1)
except KeyboardInterrupt:
    pass
    cerrar_conexion()
