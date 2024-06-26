import os
import pymysql

def obtener_conexion():
    return pymysql.connect(host=os.environ.get('DB_HOST'),
                                user=os.environ.get('DB_USERNAME'),
                                password=os.environ.get('DB_PASSWORD'),
                                port=int(os.environ.get('DB_PORT', 3306)),
                                db=os.environ.get('DB_DATABASE'),
                                ssl_key='/etc/ssl-certs/client-key.pem',
                                ssl_cert='/etc/ssl-certs/client-cert.pem',
                                ssl_ca='/etc/ssl-certs/ca.pem'
                                )