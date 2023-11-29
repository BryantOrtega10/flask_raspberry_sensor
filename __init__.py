from flask import Flask, render_template, jsonify, request
from config.config import DevelpmentConfig, ProductionConfig
from http import HTTPStatus
import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Util.Padding import unpad
import base64
import json

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
APP_STATIC = os.path.join(APP_ROOT, 'static')

def create_app(config=ProductionConfig):
    app = Flask(__name__)
    app.config.from_object(config)
    
    @app.route("/", methods=["GET"])
    def index():
        return render_template('dashboard.html')

    @app.route("/obtener-data", methods=["GET"])
    def obtener_data():
        with open(os.path.join(APP_STATIC, 'data.json')) as f:
            return f.read()

        return jsonify({"success": True, "message" : "abc"}), HTTPStatus.OK

    @app.route("/guardar-data", methods=["POST"])
    def guardar_data():

        json_r = request.get_json()
        #contenido_enc = request.form["data"]
        contenido_enc = json_r["data"]
        llave_enc = request.headers["token"]

        private_key = RSA.import_key(open("clave_privada.pem").read())
        cipher_rsa = PKCS1_OAEP.new(private_key)
        llave_enc = base64.b64decode(llave_enc)
        llave = cipher_rsa.decrypt(llave_enc)


        contenido_desc = base64.b64decode(contenido_enc)
        iv = contenido_desc[:16]
        contenido_desc = contenido_desc[16:]
        cipher = AES.new(llave, AES.MODE_CBC, iv=iv)
        mensaje_desc = unpad(cipher.decrypt(contenido_desc), AES.block_size)
        mensaje_desc = mensaje_desc.decode('utf-8')
        

        with open(os.path.join(APP_STATIC, 'data.json'), 'w') as archivo:
            archivo.write(mensaje_desc)

        return jsonify({"success": True}), HTTPStatus.OK

    @app.route("/guardar-data-no-enc", methods=["POST"])
    def guardar_data_no_enc():

        json_r = request.get_json()
        contenido_desc = json_r["data"]
        with open(os.path.join(APP_STATIC, 'data_no_enc.json'), 'w') as archivo:
            archivo.write(json.dumps(contenido_desc))

        return jsonify({"success": True}), HTTPStatus.OK

    return app

if __name__ == "__main__":
    app_flask = create_app()
    app_flask.run(host='0.0.0.0')
