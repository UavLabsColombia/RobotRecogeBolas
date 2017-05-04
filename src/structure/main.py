from Sonar import Sonar



SONAR_DERECHO_TRIG = 16
SONAR_DERECHO_ECHO = 18

print("Hi i am Pibot")
sonar_derecho =  Sonar(SONAR_DERECHO_TRIG,SONAR_DERECHO_ECHO)

print "la distancia media es ", sonarderecho.getDistanciaMedia(5)