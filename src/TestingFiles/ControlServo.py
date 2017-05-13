import RPi.GPIO as GPIO    #Importamos la libreria RPi.GPIO
import time                #Importamos libreria para el control de tiempos
import numpy as np

GPIO.setmode(GPIO.BOARD)   #Ponemos la Raspberry en modo BOARD
GPIO.setup(32,GPIO.OUT)    #Ponemos el pin 12 como salida
p = GPIO.PWM(32,50)        #Ponemos el pin 12 en modo PWM y enviamos 50 pulsos por segundo

print "inicio en 0"        # Se inicia el servo con un estado 0= stop
p.start(0)		   #Inicia El tren de pulsos

# Bucle de 0 a 100 con paso de 0.1 que imprime en pantalla el valor del pulso mientras ejecuta su valor sobre el ServoMotor
# de 0 a 6 Giro Inverso
# de 6 a  8 quieto
# de 8 a 100 Gira en sentido Normal o Hacia el Frente y control de la velocidad hasta 60 aproximadamente..
for pwm in np.arange(0,100.1,0.1):
	print "valor del  pwm:  ", pwm
	p.ChangeDutyCycle(pwm)
        time.sleep(0.01)
# Detiene el tren de pulsos
p.stop()
#Limpia el puerto GPIO
GPIO.cleanup()
