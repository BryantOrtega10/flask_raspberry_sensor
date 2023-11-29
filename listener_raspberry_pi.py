import requests
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util.py3compat import bchr, bord
from Crypto.Random import get_random_bytes

import json
import base64
# -*- coding: utf-8 -*-
import os
import re
import sys
import time
import RPi.GPIO as GPIO

URL = "http://192.168.20.3:5000/guardar-data"
URL_NO_ENC = "http://192.168.20.3:5000/guardar-data-no-enc"

KY001 = 11
KY032 = 7
KY021 = 18
GPIO.setmode(GPIO.BOARD)
GPIO.setup(KY032, GPIO.IN)
GPIO.setup(KY021, GPIO.IN)


ky001_filename = None
dev_path = '/sys/bus/w1/devices/'

if len(os.listdir(dev_path)) < 1:
    sys.exit('Have you updated config.txt and run modprobe?')

pattern = '^[1-9][1-9]-[A-Za-z0-9]*$'  
for filename in os.listdir(dev_path):
    if re.match(pattern, filename):
        ky001_filename = filename

if not ky001_filename:
    sys.exit("No se encontro el sensor de temperatura.")

def pad(s):
    return s + (AES.block_size - len(s) % AES.block_size) * bchr(AES.block_size - len(s) % AES.block_size)

try:
    while True:
        ky001_file = open("{}{}/w1_slave".format(dev_path, ky001_filename))
        data = ky001_file.read()
        ky001_file.close()
        temp_c = float(data.split(" t=")[1].strip()) / 1000
        temp_f = round(temp_c * 1.8 + 32, 2)
        proximidad = "ON"
        if GPIO.input(KY032):
            proximidad = "OFF"

        magnetico = "OFF"
        if GPIO.input(KY021):
            magnetico = "ON"
        
        llave = get_random_bytes(16)
        IV = get_random_bytes(16)

        data = {
            "KY_001": {
                "C": temp_c,
                "F": temp_f
            },
            "KY_032": proximidad,
            "KY_021": magnetico
        }

        contenido = json.dumps(data)
        contenido = contenido.encode('utf-8')

        cipher = AES.new(llave, AES.MODE_CBC, IV)
        contenido_enc = cipher.encrypt(pad(contenido))
        contenido_enc = base64.b64encode(IV + contenido_enc)
        contenido_enc = contenido_enc.decode('utf-8')

        f = open('clave_publica.pem','r')
        rsa_public_key = RSA.importKey(f.read())
        rsa_public_key = PKCS1_OAEP.new(rsa_public_key)
        llave_enc = rsa_public_key.encrypt(llave)
        llave_enc = base64.b64encode(llave_enc)
        llave_enc = llave_enc.decode('utf-8')
        response = requests.post(URL, 
            json={"data": contenido_enc},
            headers={
                "Content-Type": "application/json",
                "token" : llave_enc
            },
        )
        response2 = requests.post(URL_NO_ENC, 
            json={"data": data},
            headers={
                "Content-Type": "application/json"
            },
        )
        print("Enviado...")
        



        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()

