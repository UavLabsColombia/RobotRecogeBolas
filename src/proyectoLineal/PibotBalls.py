# Este codigo es una implementacion que se realiza con las librerias de vision por computador
# disponibles bajo python para el control de robots Recoge Bolas.
#
# Realizado por: Estudiantes de la universidad del valle.
# Heberth Alexander Ardila Cuellar / heberthardila@gmail.com / 3128204694 / uavlabs.org
# Jaime Andres Ortiz Aranda  / jaime-aranda@outlook.com / 3023476635 ###
# Juan Sebastian Bolivar Rivera / sebasbr_1031@hotmail.com / 3157634355 /
#
# Este software se encuentra bajo la licencia GPLv3 disponible sobre este repositorio, sientase libre de modificarlo
# ajustarlo y redistribuirlo manteniendo la licencia y los autores
#
# Sobre los siguientes diagramas, se describen la conexiones que se ralizan sobre los sensores y el sistema
#
######################################
# Motoreductores DC 12v
# Motor_izquierdo_adelante, motor_izquierdo_atras, motor_derecho_adelante, motor_derecho_atras:
#              _Front_
#        _________________
# --------------------------------
#
# M1 =In1,In2         M2=In1,In2
# GPIO.M1= 23,29,31  GPIO.M2= 37,35,33
#
#
# M3=In3,In4    M4= In3,In4
# GPIO.M3 = 19,21,7  GPIO.M4= 15,13,11
#
# --------------------------------
######################################
#
######################################
##Controladores L298N
## Se utilizaran dos controladores para los motores
# Cont1, Cont2:
# (EnA)
# (In1)
# (In2)
# (In3)
# (In4)
# (EnB)
######################################
#
######################################
##Sensor Sonar HC SR04 Utilizado para calcular el promedio de la distancia a un objeto.
#sonar_izquierdo, sonar_derecho, sonar_frente_izquierdo, sonar_frente_derecho, sonar_frente
#(Trig)
#(Echo)
######################################
#
######################################
##Conexiones con RaspberryPi
# Conexiones USB:
# Conectaremos por USB la camara SJCAM M10, el cual sera utiizada
# para trabajar con las librerias de Vision Artificial
## Pines de conexion para la raspberry pi 3 en modo BOARD
#	(01) 3.3V                     (02) 5v input/ouput
#	(03) Free                     (04) 5v input/ouput
#	(05) Free                     (06) GND
#	(07) Cont1.M3.In2*            (08) sonar_frente_derecho.trig*  // ok
#	(09) GND                      (10) sonar_frente_derecho.echo*  // ok
#	(11) Cont1.M4.In3*            (12) sonar_izquierdo.trig // ok
#	(13) Cont1.M4.In4*            (14) GND
#	(15) Cont1.M4.EnB*            (16) sonar_izquierdo.echo // ok
#	(17) 3.3V                     (18) sonar_frente.trig   // ok
#	(19) Cont1.M3.EnA*  def       (20) Tierra
#	(21) Cont1.M3.In1*  def       (22) sonar_frente_echo // ok
#	(23) Cont2.M1.EnA* //ok       (24) sonar_derecho.trig* // ok
#	(25) GND                      (26) sonar_derecho.echo* // ok
#	(27) N/C                      (28) N/C
#	(29) Cont2.M1.In1* // ok      (30) Tierra
#	(31) Cont2.M1.In2* // ok      (32) Servo motor recogedor
#	(33) Cont2.M2.In3* // ok      (34) Tierra
#	(35) Cont2.M2.In4* // ok      (36) sonar_frente_izquierdo.trig  // ok
#	(37) Cont2.M2.EnB* // ok      (38) sonar_frente_izquierdo.echo  // ok
#	(39) GND                      (40) Boton de Reset
#
#######################################

import RPi.GPIO as GPIO
import time
from SimpleCV import *

GPIO.setmode(GPIO.BOARD)

# DEFINICION DE VARIABLES
camara = SimpleCV.Camera(0)
pelota_coordenada_x = 0
pelota_coordenada_y = 0
radio_pelota = 0
pelota_confirmada = False

VELOCIDAD_PROMEDIO = 10  # cm/seg

##### configuracion de los motores #####

# motor_derecho_primario
GPIO.setup(13, GPIO.OUT)  # Pin de salida para In1
GPIO.setup(11, GPIO.OUT)  # Pin de salida para In2
GPIO.setup(7, GPIO.OUT)  # Pin de salida para EnA
motor_izquierdo_secundario = GPIO.PWM(7, 490)
motor_izquierdo_secundario.start(0)

# motor_izquierdo_primario
GPIO.setup(15, GPIO.OUT)  # Pin de salida para In1
GPIO.setup(19, GPIO.OUT)  # Pin de salida para In2
GPIO.setup(21, GPIO.OUT)  # Pin de salida para EnA
motor_derecho_secundario = GPIO.PWM(21, 490)
motor_derecho_secundario.start(0)

# motor_izquiedo_secunadario
GPIO.setup(29, GPIO.OUT)  # Pin de salida para In1
GPIO.setup(31, GPIO.OUT)  # Pin de salida para In2
GPIO.setup(23, GPIO.OUT)  # Pin de salida para EnA
motor_derecho_primario = GPIO.PWM(23, 490)
motor_derecho_primario.start(0)

# motor_derecho_secundario
GPIO.setup(33, GPIO.OUT)  # Pin de salida para In1
GPIO.setup(35, GPIO.OUT)  # Pin de salida para In2
GPIO.setup(37, GPIO.OUT)  # Pin de salida para EnA
motor_izquierdo_primario = GPIO.PWM(37, 490)
motor_izquierdo_primario.start(0)


def adelante(velocidad):
    print "adelante ..."
    GPIO.output(13, GPIO.LOW)
    GPIO.output(11, GPIO.HIGH)
    GPIO.output(15, GPIO.LOW)
    GPIO.output(19, GPIO.HIGH)
    GPIO.output(29, GPIO.LOW)
    GPIO.output(31, GPIO.HIGH)
    GPIO.output(33, GPIO.LOW)
    GPIO.output(35, GPIO.HIGH)
    motor_izquierdo_secundario.ChangeDutyCycle(velocidad)
    motor_derecho_secundario.ChangeDutyCycle(velocidad)
    motor_derecho_primario.ChangeDutyCycle(velocidad)
    motor_izquierdo_primario.ChangeDutyCycle(velocidad)


def detener():
    pelota_confirmada = False
    print "deteniendo..."
    motor_izquierdo_secundario.ChangeDutyCycle(0)
    motor_derecho_secundario.ChangeDutyCycle(0)
    motor_derecho_primario.ChangeDutyCycle(0)
    motor_izquierdo_primario.ChangeDutyCycle(0)


def atras(velocidad):
    print " atras...."
    GPIO.output(13, GPIO.HIGH)
    GPIO.output(11, GPIO.LOW)
    GPIO.output(15, GPIO.HIGH)
    GPIO.output(19, GPIO.LOW)
    GPIO.output(29, GPIO.HIGH)
    GPIO.output(31, GPIO.LOW)
    GPIO.output(33, GPIO.HIGH)
    GPIO.output(35, GPIO.LOW)
    motor_izquierdo_secundario.ChangeDutyCycle(velocidad)
    motor_derecho_secundario.ChangeDutyCycle(velocidad)
    motor_derecho_primario.ChangeDutyCycle(velocidad)
    motor_izquierdo_primario.ChangeDutyCycle(velocidad)


def girar_derecha(velocidad, tiempo):
    print "derecha ...."
    GPIO.output(13, GPIO.LOW)
    GPIO.output(11, GPIO.HIGH)
    GPIO.output(15, GPIO.HIGH)
    GPIO.output(19, GPIO.LOW)
    GPIO.output(29, GPIO.HIGH)
    GPIO.output(31, GPIO.LOW)
    GPIO.output(33, GPIO.LOW)
    GPIO.output(35, GPIO.HIGH)
    motor_izquierdo_secundario.ChangeDutyCycle(velocidad)
    motor_derecho_secundario.ChangeDutyCycle(velocidad)
    motor_derecho_primario.ChangeDutyCycle(velocidad)
    motor_izquierdo_primario.ChangeDutyCycle(velocidad)
    time.sleep(tiempo)


def girar_izquierda(velocidad, tiempo):
    print "izquierda...."
    GPIO.output(13, GPIO.HIGH)
    GPIO.output(11, GPIO.LOW)
    GPIO.output(15, GPIO.LOW)
    GPIO.output(19, GPIO.HIGH)
    GPIO.output(29, GPIO.LOW)
    GPIO.output(31, GPIO.HIGH)
    GPIO.output(33, GPIO.HIGH)
    GPIO.output(35, GPIO.LOW)
    motor_izquierdo_secundario.ChangeDutyCycle(velocidad)
    motor_derecho_secundario.ChangeDutyCycle(velocidad)
    motor_derecho_primario.ChangeDutyCycle(velocidad)
    motor_izquierdo_primario.ChangeDutyCycle(velocidad)
    time.sleep(tiempo)


####### configuracion de los sonares ######
sonar_frente_derecho = (8, 10)
sonar_derecho = (12, 16)
sonar_frente_izquierdo = (18, 22)
sonar_izquierdo = (24, 26)
sonar_frente = (36, 38)

# sonar_frente_derecho
GPIO.setup(8, GPIO.OUT)  # Configuramos Trigger como salida
GPIO.setup(10, GPIO.IN)  # Configuramos Echo como entrada
# sonar_derecho
GPIO.setup(12, GPIO.OUT)  # Configuramos Trigger como salida
GPIO.setup(16, GPIO.IN)  # Configuramos Echo como entrada
# sonar_frente_izquierdo
GPIO.setup(18, GPIO.OUT)  # Configuramos Trigger como salida
GPIO.setup(22, GPIO.IN)  # Configuramos Echo como entrada
# sonar_izquierdo
GPIO.setup(24, GPIO.OUT)  # Configuramos Trigger como salida
GPIO.setup(26, GPIO.IN)  # Configuramos Echo como entrada
# sonar_frente
GPIO.setup(36, GPIO.OUT)  # Configuramos Trigger como salida
GPIO.setup(38, GPIO.IN)  # Configuramos Echo como entrada


def sensar(sonar):
    trig = sonar[0]
    echo = sonar[1]
    start = 0
    end = 0
    # Configura el sensor
    GPIO.output(trig, False)
    time.sleep(0.5)  # 2 segundos para hacer el programa usable
    # Empezamos a medir
    GPIO.output(trig, True)
    time.sleep(10 * 10 ** -6)  # 10 microsegundos
    GPIO.output(trig, False)
    # Flanco de 0 a 1 = inicio
    while GPIO.input(echo) == GPIO.LOW:
        start = time.time()
    # Flanco de 1 a 0 = fin
    while GPIO.input(echo) == GPIO.HIGH:
        end = time.time()
    # el tiempo que devuelve time() esta en segundos
    distancia = (end - start) * 34300 / 2
    return (distancia, time.time())  # Devolvemos la distancia (en centimetros) por pantalla


### BOTON ####
channel = 40
# GPIO.setmode(GPIO.BOARD)  # Ponemos la Raspberry en modo BOARD
GPIO.setup(channel, GPIO.IN)  # Ponemos el pin 40 como entrada

#### SERVO MOTOR ####
GPIO.setup(32, GPIO.OUT)  # Ponemos el pin 32 como salida
servo = GPIO.PWM(32, 50)  # Ponemos el pin 32 en modo PWM y enviamos 50 pulsos por segundo
servo.start(60)  # Inicia El tren de pulsos


##### CAMARA ####

def reconocer_pelota(n_sensados):
    promedio_coordenada_x = 0
    promedio_coordenada_y = 0
    promedio_radio = 0

    for i in range(n_sensados):
        # Obtiene la imagen
        imagen = camara.getImage().flipHorizontal()
        # dilatacion de las cosas que ve la camara entre mas alta, mas expandido el objeto
        dilatacion = imagen.colorDistance(SimpleCV.Color.WHITE).dilate(2)
        # Filtra sobre la escala mas alta de grises, si los niveles son mas bajos, ve mejor en la noche o en la oscuridad, setear
        # en la camara con el filtro
        segmento_colores = dilatacion.stretch(215, 220)
        # Busca posibles blobs sobre la toma
        blobs = segmento_colores.findBlobs()
        if blobs:
            # confirma la existencia de circulos
            circulos = blobs.filter([b.isCircle(0.27) for b in blobs])
            if circulos:
                print "X:", circulos[-1].x, "Y:", circulos[-1].y, "Radio:", circulos[-1].radius()
                promedio_coordenada_x += circulos[-1].x
                promedio_coordenada_y += circulos[-1].y
                promedio_radio += circulos[-1].radius()
                # Tiempo necesario para no generar error en la lectura de las imagenes
                time.sleep(0.01)
    global pelota_coordenada_x
    pelota_coordenada_x = promedio_coordenada_x / n_sensados
    global pelota_coordenada_y
    pelota_coordenada_y = promedio_coordenada_y / n_sensados
    global radio_pelota
    radio_pelota = promedio_radio / n_sensados
    # Imprime en pantalla las coordenadas y radio del ultimo objeto
    print "Pelota_coordenada_x", pelota_coordenada_x, "Pelota_coordenada_y:", pelota_coordenada_y, "Radio_pelota", radio_pelota


def retroceder_distancia(sonar):
    detener()
    time.sleep(0.5)
    distancia = sensar(sonar)[0]
    print "la distancia es ", distancia
    if (distancia <= 15):
        atras(50)
        time.sleep((15 - distancia) / 5)


def buscar_pelota():
    reconocer_pelota(2)
    if (radio_pelota < 10.0):
        print "la variable es ", radio_pelota
        print "no hay pelota"
    else:
        print pelota_coordenada_x
        while (True):
            detener()
            reconocer_pelota(1)
            if 340 < pelota_coordenada_x < 380:
                pelota_confirmada = True
                adelante(80)
                break
            else:
                if 340 > pelota_coordenada_x:
                    print pelota_coordenada_x
                    detener()
                    girar_derecha(40, 0.1)
                else:
                    detener()
                    girar_izquierda(40, 0.1)
                    print pelota_coordenada_x


# buscar_pelota()
# time.sleep(10)
servo_bool = True
# codigo moviento
buscar_pelota()
distancia_minima = 40

while (True):
    boton = GPIO.input(channel)
    if boton:
        print "el estadod el boton es ", boton
        if servo_bool==False:
            servo.start(60)
            servo_bool =True
        try:
            a = sensar(sonar_frente)
            b = sensar(sonar_frente_izquierdo)
            c = sensar(sonar_frente_derecho)
            print a, " sonarfrente"
            print b, " sonarizquierdo"
            print c, "sonar derecho"
            adelante(80)
            if (pelota_confirmada):
                distancia_minima = 15
            else:
                distancia_minima = 40
            if (a[0] < distancia_minima or b[0] < distancia_minima or c[0] < distancia_minima):
                detener()
                if (a > b):
                    if (a > c):
                        retroceder_distancia(sonar_frente)
                    else:
                        retroceder_distancia(sonar_frente_derecho)
                else:
                    if (b > c):
                        retroceder_distancia(sonar_frente_izquierdo)
                    else:
                        retroceder_distancia(sonar_frente_derecho)
                # codigo de giro
                if (sensar(sonar_izquierdo)[0] < sensar(sonar_derecho)[0]):
                    girar_derecha(50, 0.5)
                    buscar_pelota()

                else:
                    girar_izquierda(50, 0.5)
                    buscar_pelota()

        except KeyboardInterrupt:
            GPIO.cleanup()
            break
    else:
        print "entro al metodo detener"
        detener()
        servo.start(0)
        time.sleep(2)
        servo_bool=False
