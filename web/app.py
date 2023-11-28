import os
from flask import Flask
from variables_database import cargarvariables

app = Flask(__name__)

app.config.from_pyfile('settings.py')
cargarvariables()
  
import funciones_main as funciones_main

import database

if __name__ == '__main__':
    port = int(os.environ.get('PORT'))
    host = os.environ.get('HOST')
    app.run(host=host, port=port)