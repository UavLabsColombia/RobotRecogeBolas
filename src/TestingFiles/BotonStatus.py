import RPi.GPIO as GPIO    #Importamos la libreria RPi.GPIO
import time                #Importamos libreria para el control de tiempos


channel = 40
GPIO.setmode(GPIO.BOARD)   #Ponemos la Raspberry en modo BOARD
GPIO.setup(channel,GPIO.IN)    #Ponemos el pin 40 como entrada

## Leemos el ping del canal y determinamos su estatus
while(1):
	if GPIO.input(channel):
		print('Entrada fue HIGH')
	else:
		print('Entrada fue LOW')
	time.sleep(0.1)
#Limpia el puerto G
PIO
GPIO.cleanup()
