
## Recibe el numero de veces que va a validar la existencia de las pelotas
from Pelota import *
class Camara:
    def __init__(self):
        print "En camara"
        self.existe_pelota = False

    def buscar_pelota(self,sensado):
        pelota_negra = Pelota()
        if pelota_negra.hubicar_pelota(sensado):
            self.existe_pelota = True
            return existe_pelota
        else:
            self.existe_pelota = False
            return existe_pelota

camara = Camara()
camara.buscar_pelota(5)
