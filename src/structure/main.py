from Movimiento import PuenteH, Motor
import time

puenteh_derecho = PuenteH(16, 8, 10)
motor_derecho = puenteh_derecho.motor_a
motor_derecho.adelante(50)
time.sleep(1)
motor_derecho.detener()
motor_derecho.atras(50)
time.sleep(1)
motor_derecho.detener()



SONAR_DERECHO_TRIG = 16
SONAR_DERECHO_ECHO = 18

print("Hi i am Pibot")
sonar_derecho =  Sonar(SONAR_DERECHO_TRIG,SONAR_DERECHO_ECHO)

print "la distancia media es ", sonar_derecho.getDistanciaMedia(5)

#from Sonar import Sonar
#
#SONAR_DERECHO_TRIG = 16
#SONAR_DERECHO_ECHO = 18
#
#print("Hi i am Pibot")
#sonar_derecho =  Sonar(SONAR_DERECHO_TRIG,SONAR_DERECHO_ECHO)
#
#print "la distancia media es ", sonarderecho.getDistanciaMedia(5)
