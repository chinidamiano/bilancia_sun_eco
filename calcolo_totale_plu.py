# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# install with 'pip install pyserial'
import serial.tools.list_ports
import csv
import os
from datetime import date

csv_file = "totale_plu.csv"


def decode_byte_int(byte_string):
    return int(byte_string.decode("utf-8"))
              

class PLUDetails:
    def __init__(self, numero_plu, nome, prezzo):
        self.numero_plu = numero_plu
        self.nome = nome
        self.prezzo = prezzo
        
class PLUTotal:
    def __init__(self, numero_plu, nome, prezzo, numero_confezioni, totale_peso_grammi, totale_importo):
        self.numero_plu = numero_plu
        self.nome = nome
        self.prezzo = prezzo
        self.numero_confezioni = numero_confezioni
        self.totale_peso_grammi = totale_peso_grammi
        self.totale_importo = totale_importo
    
    def to_array(self):
        return [
            self.numero_plu,
            self.nome,
            self.prezzo,
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
        plu_details = self.get_plu_details(plu_number)
        request ="\x1by {}\r".format(plu_number).encode()
        print(f"PLUTotal Request: {request}")
        self.connection.write(request)
        response = self.connection.readline()
        r_split = response.split()
        print(f"PLUTotal Response: {response}")
        plu = PLUTotal(
            decode_byte_int(r_split[1]),
            plu_details.nome,
            plu_details.prezzo,
            decode_byte_int(r_split[2]),
            decode_byte_int(r_split[3]),
            decode_byte_int(r_split[4])
            )
        
        return plu
    
    def get_plu_details(self, plu_number):
        request ="\x1bb {}\r".format(plu_number).encode()
        print(f"PLU details Request: {request}")
        self.connection.write(request)
        response = self.connection.readline()
        nome = response.decode("utf-8")[6:18].strip()
        prezzo = response.decode("utf-8")[19:25].strip()
        r_split = response.split()
        print(f"PLU details Response: {response}")
        plu_details = PLUDetails(
            decode_byte_int(r_split[1]),
            nome,
            prezzo
            )
        return plu_details
        
    def clear_total(self):
        request ="\x1bz \r".encode()
        print(f"PLU Request: {request}")
        self.connection.write(request)
        
    def disconnect(self):
        self.connection.close()

bilancia = BilanciaManager()
bilancia.connect()
all_plu = []

for plu_n in range(1, 33):
    plu = bilancia.get_plu(plu_n)
    all_plu.append(plu)

bilancia.disconnect()

file_exists = os.path.exists(csv_file)
with open(csv_file, 'a', newline='', encoding='UTF8') as f:
    writer = csv.writer(f)

    if not file_exists:
        header = ["data", "numero_plu", "nome", "prezzo", "numero_confezioni", "totale_peso_grammi", "totale_importo"]
        writer.writerow(header)

    today = date.today()
    # write the data
    for plu in all_plu:
        row = [today]
        row.extend(plu.to_array())
        
        writer.writerow(row)
        
    f.close()