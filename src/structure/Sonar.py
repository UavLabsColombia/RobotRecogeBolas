import RPi.GPIO as GPIO  # Importamos la libreria RPi.GPIO
import time

GPIO.setmode(GPIO.BOARD)


class Sonar:

    def __init__(self, pin_trig, pin_echo):
        self.pin_trig = pin_trig
        self.pin_echo = pin_echo

    #recibe un parametro sensado que define cuantos datos se van a promediar
    def getDistanciaMedia(self, sensado):
        distancia = 0
        for i in range(sensado):
            distancia += self.dist_objeto()
            time.sleep(0.5)
        return distancia/sensado

    def dist_objeto(self):
        # print "Distancia en proceso de calculo..."
        ##Se inicial a distancia en 0 indicando que no hay datos sobre la lectura de distancia.
        distancia = 0
        ## Se define el pin trig y el pin echo para el sensor
        GPIO.setup(self.pin_trig, GPIO.OUT)
        GPIO.setup(self.pin_echo, GPIO.IN)
        ## se apaga el pulso para no generar interferencias.
        GPIO.output(self.pin_trig, GPIO.LOW)
        ## tiempo que dura el pulso apagado 2microsegundos
        time.sleep(2 * 10 ** -6)
        ## se enciende el pulso durante 10microsegundos
        GPIO.output(self.pin_trig, GPIO.HIGH)
        time.sleep(10 * 10 ** -6)
        ## se apaga el pulso
        GPIO.output(self.pin_trig, GPIO.LOW)
        # print "No llega senial"
        ## se empieza a contabilizar el tiempo mientras no se llegue senial.
        while GPIO.input(self.pin_echo) == 0:
            pulse_start = time.time()
            print "Esperando Pulso"
        ## si se recibe senial en el sensor toma el tiempo
        # print "llegando senial"
        while GPIO.input(self.pin_echo) == 1:
            pulse_end = time.time()
        duracion_pulso = pulse_end - pulse_start
        distancia = (duracion_pulso * 34300) / 2
        print "distancia obtenida ", distancia
        return distancia