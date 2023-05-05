import minimalmodbus, serial, datetime, json

# Validar instrumento 

def validar_instrumento(puerto, id):
    try:
        # Se crea instrumento para cada regulador
        instrument = minimalmodbus.Instrument(puerto, id, minimalmodbus.MODE_RTU)
    except minimalmodbus.ModbusException as e:
        return None
    except serial.SerialException as e:
        return None
    else:
        return instrument

# Crear diccionario

def crear_dic(instrument1, instrument2, keys1, keys2, data_dict, dir):

    now = datetime.datetime.now()
    fecha_hora = now.strftime("%d/%m/%Y %H:%M:%S")
    data_dict["fecha_hora"] = fecha_hora
            
    for i in range(len(dir)):
        try:
            if keys1[i] == "battery_SOC1" or keys1[i] == "load_status1":
                var1 = instrument1.read_register(dir[i], functioncode=4)
            elif keys1[i] == "battery_current1":
                var1 = (-1)*((instrument1.read_register(dir[i], functioncode=4) - 65000) / 100)
            else:
                var1 = instrument1.read_register(dir[i], functioncode=4)/100
        except:
            var = ""
        data_dict[keys1[i]] = var1

    for i in range(len(dir)):
        try:
            if keys2[i] == "battery_SOC2" or keys2[i] == "load_status2":
                var2 = instrument2.read_register(dir[i], functioncode=4)
            elif keys2[i] == "battery_current2":
                var2 = (-1)*((instrument2.read_register(dir[i], functioncode=4) - 65000) / 100)
            else:
                var2 = instrument2.read_register(dir[i], functioncode=4)/100
        except:
            var2 = ""
        data_dict[keys2[i]] = var2

# Diccionario vacio

def vacio(keys, data_dict):

    now = datetime.datetime.now()
    fecha_hora = now.strftime("%d/%m/%Y %H:%M:%S")
    data_dict["fecha_hora"] = fecha_hora
    data_dict["ID"] = 1

    for i in range(len(keys)):
        data_dict[keys[i]] = ""

# Enviar diccionario

def enviar(ser, data_dict):
    json_data = json.dumps(data_dict)
    bytes_data = json_data.encode()
    ser.write(bytes_data)

# Baudrate y timeout

def parametros(instrument1, instrument2):
    instrument1.serial.baudrate = 115200
    instrument1.serial.timeout = 1
    instrument2.serial.baudrate = 115200
    instrument2.serial.timeout = 1