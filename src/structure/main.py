from Movimiento import PuenteH, Motor
import time

puenteh_derecho = PuenteH(16, 8, 10)
motor_derecho = puenteh_derecho.motor_a
motor_derecho.adelante()
time.sleep(3)
motor_derecho.atras()
time.sleep(3)
motor_derecho.detener()

"""from Sonar import Sonar

SONAR_DERECHO_TRIG = 16
SONAR_DERECHO_ECHO = 18

print("Hi i am Pibot")
sonar_derecho =  Sonar(SONAR_DERECHO_TRIG,SONAR_DERECHO_ECHO)

print "la distancia media es ", sonarderecho.getDistanciaMedia(5)"""
