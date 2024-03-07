import pandas as pd
import json
import csv
def data() -> json:
    data = {}
    cabezera = ['Modelo','Cambio de Pantalla', 'Cambio de Placa Principal','Cambio de Baterí','Reparacion de Cámara Principa','Cambio de Tapa','Reparacion de Cámara Principa','Sub Placa','Pegamento','Speaker','Bateria QBA02','Pegamento','Tapa QFR02 QLC01','Pantalla']
    ban = ['$0,00','-']

    # Lee el archivo CSV (reemplaza 'archivo.csv' con la ruta de tu archivo)
    #llamar a la funcion cuando pueda recibir el json
    with open('cotizadorDeArreglo.csv','r',encoding='utf-8') as archivo:
        lector = csv.reader(archivo,delimiter=';')
        encabezado = next(lector)
        # Itera sobre el resto de las filas
        for fila in lector:
            for index, valor in enumerate(fila):
                if (valor not in ban) and (valor.strip()):
                    cabezadoActual = encabezado[index]
                    if cabezadoActual == 'Modelo':
                        modelo = valor
                        data[modelo] = {}
                    elif cabezadoActual in cabezera:
                        cabezeraPrincipal = cabezadoActual
                        data[modelo][cabezeraPrincipal] = valor
    return json.dumps(data,ensure_ascii=False)

