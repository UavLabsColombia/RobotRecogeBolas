import RPi.GPIO as GPIO    #Importamos la libreria RPi.GPIO
import time
GPIO.setmode(GPIO.BOARD)

while(1):
    def dist_objeto(trig, echo):
      #print "Distancia en proceso de calculo..."
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
      #print "No llega senial"
      ## se empieza a contabilizar el tiempo mientras no se llegue senial.
      while GPIO.input(echo)==0:
          pulse_start=time.time()
          print "Esperando Pulso"
      ## si se recibe senial en el sensor toma el tiempo
      #print "llegando senial"
      while GPIO.input(echo)==1:
          pulse_end= time.time()
      duracion_pulso= pulse_end - pulse_start
      distancia = (duracion_pulso * 34300)/2
      return distancia


    print "La distancia es:", dist_objeto(16,18)
    time.sleep(0.5)
