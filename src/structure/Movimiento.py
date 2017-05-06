# Esta funcion, define el movimiento de un motor DC que esta siendo controlado con el Driver
# L298N, implementa dos salidas de control digitales y un pulso PWM para el control de velocidad.
# El controlador permite el manejo de dos motores pero en este caso implementaremos el control de uno solo

import RPi.GPIO as GPIO  # Importamos la libreria RPi.GPIO

GPIO.setmode(GPIO.BOARD)  # Le indicamos a python que la definicion de los pines GPIO se cataloga por numero de pines del 1 al 40
GPIO.setwarnings(False)


class PuenteH():
    def __init__(self, enable_a, int_1, int_2):
        self.enable_a = enable_a
        self.int_1 = int_1
        self.int_2 = int_2
        self.motor_a = Motor(enable_a, int_1, int_2)

    def __init__(self, enable_a, int_1, int_2, int_3, int_4, enable_b):
        self.enable_a = enable_a
        self.int_1 = int_1
        self.int_2 = int_2
        self.int_3 = int_3
        self.int_4 = int_4
        self.enable_b = enable_b
        self.motor_a = Motor(enable_a, int_1, int_2)
        self.motor_b = Motor(enable_b, int_1, int_2)


class Motor():
    def __init__(self, enable, int1, int2):
        self.pulso = GPIO.PWM(enable, 490)  # Ponemos el pin 16 en modo PWM y enviamos 490 pulsos por segundo
        self.enable = enable
        self.int1 = int1
        self.int2 = int2
        GPIO.setup(int1, GPIO.OUT)  # Pin de salida para In1
        GPIO.setup(int2, GPIO.OUT)  # Pin de salida para In2
        GPIO.setup(enable, GPIO.OUT)  # Pin de salida para EnA

    def adelante(self, vel):
        self.pulso.start(vel)
        GPIO.output(self.int1, GPIO.LOW)  # Pone el pin 8 en alto
        GPIO.output(self.int2, GPIO.HIGH)  # Pone el pin 8 en Bajo

    def atras(self, vel):
        self.pulso.start(vel)
        GPIO.output(self.int1, GPIO.HIGH)  # Pone el pin 8 en alto
        GPIO.output(self.int2, GPIO.LOW)  # Pone el pin 8 en Bajo

    def detener(self):
        self.pulso.stop()
