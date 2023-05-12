import time, serial, funciones, threading, enviar

# Configuracion del dispositivo

ser = serial.Serial(port = 'COM10', baudrate = 115200)

# Direcciones y claves

keys1 = ["array_current1", "array_voltage1", "array_power1", "battery_voltage1", 
         "battery_current1", "battery_SOC1", "battery_temp1", "regulator_temp1", 
         "load_current1", "load_voltage1", "load_power1", "load_status1"]

keys2 = ["array_current2", "array_voltage2", "array_power2", "battery_voltage2", 
         "battery_current2", "battery_SOC2", "battery_temp2", "regulator_temp2", 
         "load_current2", "load_voltage2", "load_power2", "load_status2"]
        
dir = [0x3101, 0x3100, 0x3102, 0x331A, 0x331B, 0x311A, 
        0x3110, 0x3111, 0x310D, 0x310C, 0x310E, 0x3202]

puerto = 'COM8'
id1 = 1
id2 = 3

# Crear diccionarios para los datos y el error

data_dict = {}

# Lectura de registros

while True:

    instrument1 = funciones.validar_instrumento(puerto, id1)
    instrument2 = funciones.validar_instrumento(puerto, id2)

    # Intenta crear llenar el diccionario con los datos de los registros
    if instrument1 == None:
        funciones.vacio(keys1, data_dict)
        #funciones.enviar(ser, data_dict)
        print('Error')
        time.sleep(0.08)
        continue

    elif instrument2 == None:
        funciones.vacio(keys2, data_dict)
        #funciones.enviar(ser, data_dict)
        print('Error')
        time.sleep(0.08)
        continue

    try:
        funciones.parametros(instrument1, instrument2)
        funciones.crear_dic(instrument1, instrument2, keys1, keys2, data_dict, dir)
        print("\nEnviando...")
        funciones.enviar(ser, data_dict)        
        time.sleep(0.08)

    # Si existe un error envia un json vacio
    except Exception as e:
        funciones.vacio(keys1, data_dict)
        funciones.vacio(keys2, data_dict)
        funciones.enviar(ser, data_dict)
        instrument1.serial.close()
        instrument2.serial.close()
        print(data_dict)
        time.sleep(0.08)