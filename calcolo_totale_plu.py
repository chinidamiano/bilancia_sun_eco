# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# install with 'pip install pyserial'
import serial.tools.list_ports
import csv
from datetime import date

today = date.today()
csv_file = f"totale_plu_{today}.csv"


def decode_byte_int(byte_string):
    return int(byte_string.decode("utf-8"))
              

class PLU:
    def __init__(self, numero_plu, numero_confezioni, totale_peso_grammi, totale_importo):
        self.numero_plu = numero_plu
        self.numero_confezioni = numero_confezioni
        self.totale_peso_grammi = totale_peso_grammi
        self.totale_importo = totale_importo
    
    def to_csv_row(self):
        return [
            self.numero_plu,
            self.numero_confezioni,
            self.totale_peso_grammi,
            self.totale_importo
        ]
    

class BilanciaManager:
    connection = None
    
    def connect(self):
        ports = serial.tools.list_ports.comports()
        port = ports[0]
        print(f"Connecting to port: {port}")        
        self.connection = serial.Serial(port.device)
        
    def get_plu(self, plu_number):
        request ="\x1by {}\r".format(plu_number).encode()
        print(request)
        self.connection.write(request)
        response = self.connection.readline()
        r_split = response.split()
        print(response)
        plu = PLU(
            decode_byte_int(r_split[1]),
            decode_byte_int(r_split[2]),
            decode_byte_int(r_split[3]),
            decode_byte_int(r_split[4])
            )
        return plu
        
    def disconnect(self):
        self.connection.close()

bilancia = BilanciaManager()
bilancia.connect()
all_plu = []

for plu_n in range(1, 33):
    plu = bilancia.get_plu(plu_n)
    all_plu.append(plu)

bilancia.disconnect()

with open(csv_file, 'w', newline='', encoding='UTF8') as f:
    writer = csv.writer(f)

    header = ["numero_plu", "numero_confezioni", "totale_peso_grammi", "totale_importo"]
    writer.writerow(header)

    # write the data
    for plu in all_plu:
        writer.writerow(plu.to_csv_row())
        
    f.close()