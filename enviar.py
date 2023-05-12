import time, serial, funciones, threading, lecturamain

#ser = serial.Serial(port = 'COM10', baudrate = 115200)

class mihilo(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.datos = {}

    def run(self):
        while True:
            self.datos = lecturamain.leer_datos() # lectura de datos de lecturamain
            time.sleep(5) # espera de 5 segundos antes de volver a leer y enviar datos

# Crear e iniciar hilo
hilo = mihilo()
hilo.start()
