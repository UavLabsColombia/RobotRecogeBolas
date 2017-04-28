#Esta funcion, define el movimiento de un motor DC que esta siendo controlado con el Driver
#L298N, implementa dos salidas de control digitales y un pulso PWM para el control de velocidad.
#El controlador permite el manejo de dos motores pero en este caso implementaremos el control de uno solo

import RPi.GPIO as GPIO    #Importamos la libreria RPi.GPIO
import time #Importamos librerias para el control de tiempos
import numpy as np

GPIO.setmode(GPIO.BOARD) # Le indicamos a python que la definicion de los pines GPIO se cataloga por numero de pines del 1 al 40
GPIO.setwarnings(False)

GPIO.setup(8, GPIO.OUT) #Pin de salida para In1
GPIO.setup(10, GPIO.OUT) #Pin de salida para In2
GPIO.setup(16,GPIO.OUT)  #Pin de salida para EnA
p = GPIO.PWM(16,490)        #Ponemos el pin 16 en modo PWM y enviamos 50 pulsos por segundo
p.start(100)

def adelante(vel):
    p.ChangeDutyCycle(vel)		   #Inicia El tren de pulsos y varia el porcentaje de 1 a 100
    GPIO.output(8, GPIO.LOW)      #Pone el pin 8 en alto
    GPIO.output(10, GPIO.HIGH)      #Pone el pin 8 en Bajo

def atras(vel):
    p.ChangeDutyCycle(vel)		   #Inicia El tren de pulsos y varia el porcentaje de 1 a 100
    GPIO.output(8, GPIO.HIGH)      #Pone el pin 8 en alto
    GPIO.output(10, GPIO.LOW)      #Pone el pin 8 en Bajo


##Inicia el movimiento de los motores, Adelante - Atras durante un tiempo estimado
for pwm in np.arange(0,101,1):
    adelante(pwm)
    time.sleep(0.1)
    print "Velocidad:", pwm,"%"

for pwm in np.arange(0,101,1):
    atras(pwm)
    time.sleep(0.1)
    print "Velocidad:", pwm,"%"

# Detiene el tren de pulsos
p.stop()
# Limpia el puerto
GPIO.cleanup()
