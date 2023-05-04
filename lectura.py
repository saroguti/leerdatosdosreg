import time, serial, funciones

# Configuracion del dispositivo

ser = serial.Serial(port='COM4', baudrate=115200)

# Direcciones y claves

keys = ["array_current", "array_voltage", "array_power", "battery_voltage", "battery_current", "battery_SOC", 
        "battery_temp", "regulator_temp", "load_current", "load_voltage", "load_power", "load_status"]
        
dir = [0x3101, 0x3100, 0x3102, 0x331A, 0x331B, 0x311A, 
        0x3110, 0x3111, 0x310D, 0x310C, 0x310E, 0x3202]

# Crear diccionarios para los datos y el error

data_dict1 = {}

data_dict2 = {}

# Lectura de registros

while True:
    instrument1 = funciones.validar_instrumento1(puerto='COM8')
    instrument2 = funciones.validar_instrumento2(puerto='COM8')
    # Intenta crear llenar el diccionario con los datos de los registros
    if instrument1 == None:
        funciones.vacio(keys, data_dict1)
        funciones.enviar(ser, data_dict1)
        print("\nError.")
        time.sleep(0.08)
        continue
    elif instrument2 == None:
        funciones.vacio(keys, data_dict2)
        funciones.enviar(ser, data_dict2)
        print("\nError.")
        time.sleep(0.08)
        continue
    try:
        # Aqui se envian datos del regulador 1
        instrument1.serial.baudrate = 115200
        instrument1.serial.timeout = 1
        
        data_dict1["ID"] = 1
        funciones.crear_dic(instrument1, keys, data_dict1, dir)
        funciones.enviar(ser, data_dict1)
        
        # Aqui se envian datos del regulador 2
        instrument2.serial.baudrate = 115200
        instrument2.serial.timeout = 1

        data_dict2["ID"] = 2
        funciones.crear_dic(instrument2, keys, data_dict2, dir)
        funciones.enviar(ser, data_dict2)

        print("\nEnviando datos regulador 1...")
        print("\n", data_dict1)

        print("\nEnviando datos regulador 2...")
        print("\n", data_dict2)

        time.sleep(10)

    # Si existe un error envia un json vacio
    except Exception as e:
        funciones.vacio(keys, data_dict1)
        funciones.enviar(ser, data_dict1)
        print("\nError.")
        instrument1.serial.close()
        time.sleep(0.08)
