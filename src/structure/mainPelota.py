############################################################################
from Pelota import Pelota

pelota = Pelota()

if(pelota.hubicar_pelota(1)):
    print "Encontre pelota! :)", pelota.getExistePelota()
    print "Coordenada en X:", pelota.getCordX()
    print "Coordenada en Y:", pelota.getCordY()
    print "Radio:", pelota.getRadio()
else:
    print "No veo pelota! :(", pelota.getExistePelota()

#############################################################################
# from Movimiento import PuenteH, Motor
# import time
#
# puenteh_derecho = PuenteH(16, 8, 10)
# motor_derecho = puenteh_derecho.motor_a
# motor_derecho.adelante(50)
# time.sleep(1)
# motor_derecho.detener()
# motor_derecho.atras(50)
# time.sleep(1)
# motor_derecho.detener()
#############################################################################
#
# #from Sonar import Sonar
# #
# #SONAR_DERECHO_TRIG = 16
# #SONAR_DERECHO_ECHO = 18
# #
# #print("Hi i am Pibot")
# #sonar_derecho =  Sonar(SONAR_DERECHO_TRIG,SONAR_DERECHO_ECHO)
# #
# #print "la distancia media es ", sonarderecho.getDistanciaMedia(5)
############################################################################
