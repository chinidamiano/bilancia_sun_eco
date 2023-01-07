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
from bilancia_sun_eco import bilancia_sun_eco

csv_file = "totale_plu.csv"

bilancia = bilancia_sun_eco.BilanciaManager()
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