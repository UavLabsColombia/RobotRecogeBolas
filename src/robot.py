# Este codigo es una implementacion que se realiza con las librerias de vision por computador
# disponibles bajo python para el control de robots Recoge Bolas.
#
# Realizado por: Estudiantes de la universidad del valleself.
# Heberth Alexander Ardila Cuellar / heberthardila@gmail.com / 3128204694 / uavlabs.org
# Jaime Andres Aranda  / jaoa95@gmail.com ###
#
#
# Este software se encuentra bajo la licencia GPLv3, sientase libre de modificarlo
# ajustarlo y redistribuirlo manteniendo la licencia y los autores

#Controlador de motor L293D



#Aqui todas las librerias a importar...

#importamos libreria del sistema
import sys

#Importamos libreria GPIO
try:
 import RPi.GPIO as GPIO
except RuntimeError:
    print"Erorr al importar GPIO, ejecutelo como sudo!!"

#Importamos librerias para el control de tiempos
import time

#Importamos librerias para el control de hilos o multihilos
from threading import Thread
# se importa libreria para el control vectorial
import numpy as np

# se importa libreria OpenCV Vision por Computador 
import cv2


# Se inician y se cargan dependencias y configuraciones
# modo de los pines, basados en BCM o en BOARD
GPIO.setmode(GPIO.BCM)


##Elementos globales para la clase
# posiciones
# 0 = motor1A  1=motor1B 2=motor2A 3=motor2B
channel=[11,12,13,15,16,18]
#channel=[13,15]
#version de opencv
# se confirma version de OPENCV instalado
cversion= cv2.__version__
##
band = 0

#Inicializacion del software
print "Iniciando el software para el control del robot...."
print "Info de la PI"
print GPIO.RPI_INFO
# version de python
print "Version de python:", sys.version
# se confirma version de OPENCV instalado
print "Version de OpenCV:", cversion

# Se imprime el modo de configuracion para los pines
mode = GPIO.getmode()
if(mode==10):
 print "modo de la tarjeta:",mode ,"(BOARD)"
if(mode==11):
 print "modo de la tarjeta:", mode ,"(BCM)"



# se quitan las alertas de definicion para los pines
GPIO.setwarnings(False)

# se definen y se inician los pines a utilizar sobre la raspberry para el control de motores...
# Se definen los pines como salida

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



## MOvimientos para los motores
# los siguientes metodos describen los sentidos de giros para el robot, adelante, atras, derecha, izquierda, stop
def adelante():
 print "Adelante"
 GPIO.output(channel[0],GPIO.LOW)
 GPIO.output(channel[1],GPIO.HIGH)
 # GPIO.output(channel[0], GPIO.LOW)

def atras():
 print "Atras"
 GPIO.output(channel[1], GPIO.HIGH)
 GPIO.output(channel[0], GPIO.LOW)

def derecha():
 print "Derecha"
 GPIO.output(channel[2], GPIO.HIGH)
 GPIO.output(channel[3], GPIO.LOW)

def izquierda():
 print "Izquierda"
 GPIO.output(channel[3], GPIO.HIGH)
 GPIO.output(channel[2], GPIO.LOW)


def stop():
 print "Stop"
 GPIO.output(channel[4], GPIO.LOW) 
 GPIO.output(channel[5], GPIO.LOW)



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
  time.sleep(2*10**-6)
  ## se enciende el pulso durante 10microsegundos
  GPIO.output(trig, GPIO.HIGH)
  time.sleep(10*10**-6)
  ## se apaga el pulso
  GPIO.output(trig, GPIO.LOW)
  print "No llega senial"
  ## se empieza a contabilizar el tiempo mientras no se llegue senial. 
  while GPIO.input(echo)==0:
      pulse_start=time.time()
  ## si se recibe senial en el sensor toma el tiempo
  print "llegando senial"
  while GPIO.input(echo)==1:
      pulse_end= time.time()
  duracion_pulso= pulse_end - pulse_start
  distancia = (duracion_pulso * 34300)/2
  return distancia


## numero de sonares que tendra disponible el robot
## retornan promedio de las distancias en CM de los sensores
def sonar_derecho():
    print "sonar derecho"
    prom_dist=0
    for i in range(3):
     ## configurar los pines adecuados para el sonar de la derecha
     prom_dist += dist_objeto(21,22)
    return prom_dist/3

## configurar los pines adecuados para el sonar de la izquierda
def sonar_izquierdo():
    print "sonar izquieredo"
    prom_dist=0
    for i in range(3):
     prom_dist += dist_objeto(23,24)
    return prom_dist/3

##se define el metodo que sensara todo el sistema

def pulsador():
  estado_boton=1
  return estado_boton
 
def sensar():
    #while True:
        #Orden del como va a sensar el sistema, prioridad de sensores..
        print "Sensando.."
        
        
def cerrar_conexion():
      print " "
      print "Limpiando puerto GPIO..."
      GPIO.cleanup()
      print "Saliendo..."
      sys.exit(0)


#El core o nucleo, es el encargador de iniciar todas las ejecuciones y revisar los estados de  todos los sensores
def core():
    if (pulsador()==0):
        stop()
        time.sleep(1)
    if(pulsador()==1):
     sensar()
     time.sleep(1)
     print "Ejecutando."
    
## Fila de procesos que se ejecutaran paralelamente.
try:
    while 1:
        core()
        #time.sleep(0.01)
except KeyboardInterrupt:
    pass
    cerrar_conexion()


