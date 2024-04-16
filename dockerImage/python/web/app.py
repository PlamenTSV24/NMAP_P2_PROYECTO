import os
from flask import Flask
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)

app.config['production'] = True
app.config.update(
    SECRET_KEY=os.environ.get("SECRET_KEY")
)
# csrf = CSRFProtect(app)

import funciones_main as funciones_main
import database

if __name__ == '__main__':
    port = int(os.environ.get('PORT'))
    host = os.environ.get('HOST')
    app.run(host=host, port=port) #Añadir , ssl_context='adhoc' para https