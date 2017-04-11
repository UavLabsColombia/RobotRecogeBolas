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

#Importamos libreria GPIO
try:
 import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")

#Importamos librerias para el control de tiempos
import time

# Se inician y se cargan dependencias y configuraciones
# modo de los pines, basados en BCM o en BOARD
GPIO.setmode(GPIO.BCM)


##Elementos globales para la clase
# posiciones
# 0 = motor1A  1=motor1B 2=motor2A 3=motor2B
channel=[11,12,13,15,16,18]
#channel=[13,15]


#Inicializacion del software
print "Iniciando el software para el control del robot...."


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

#GPIO.cleanup()

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
 print "Stop	"
 GPIO.output(channel[4], GPIO.LOW) 
 GPIO.output(channel[5], GPIO.LOW)



def core():
  adelante()
  atras()
  derecha()
  izquierda()
  stop()
  time.sleep(0.5)


while (1):
 core()

