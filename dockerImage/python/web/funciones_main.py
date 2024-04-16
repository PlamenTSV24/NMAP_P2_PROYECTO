from __future__ import print_function
from __main__ import app
from flask import render_template, session,request
from funciones_db import verificar_credenciales,verificar_usuario,registrar_usuario,restar_token,cambiar_pass,borrar_usuario
from enymeep import scanTarget
import datetime
from werkzeug.http import http_date
import bleach
import logging

logging.basicConfig(level="INFO")

@app.route("/",methods=['GET'])
def raiz():
    session.clear()
    return render_template('access.html')


@app.route("/login",methods=['GET', 'POST'])
def login():
    requestLogin = request.get_json()
    #try:
    username_bd = verificar_credenciales(bleach.clean(requestLogin['username']),bleach.clean(requestLogin['password']))
    if username_bd is False:
        res = {"status": 406 ,"mensaje":"Invalid username or password" }
    
    else:
        session["usuario"]=requestLogin['username']
        session["tokens"]=username_bd
        # return render_template("control.html")
        res = {"status": 301 ,"mensaje":"Login correct", "target":"/dashboard"}

    logging.info(f"Login from user {requestLogin['username']}: {res['mensaje']}")
    # except:
    #     res={"status": 406, "mensaje" : "An error has occurred while loading session"}

    return res

@app.route("/dashboard",methods=['POST'])
def dashboard():
    usuario=session.get("usuario")
    if usuario is None:
        return {"status": 403, "mensaje":"Forbidden, go suck pp"}
    return render_template("control.html",user=usuario,tokens=session.get('tokens'))

@app.route("/register",methods=['POST'])
def registro():
    requestRegister = request.get_json()
        
    try:
        user_exist = verificar_usuario(bleach.clean(requestRegister['username']))
        if user_exist == True:
            res = {"status": 406 ,"mensaje":"User exists" }

        else:
            registrar_usuario(bleach.clean(requestRegister['username']),bleach.clean(requestRegister['password']))
            res = {"status": 200 , "mensaje":"You have been registered successfully"}

    except:
        res = {"status": 500 ,"mensaje":"An error has occurred while registering" }
    logging.info(f"New user {requestRegister['username']}: {res['mensaje']}")
    return res

@app.route("/password",methods=['POST'])
def password():
    requestBody = request.get_json()
    usuario = session.get("usuario")
    pwd = bleach.clean(requestBody["pwd"])
    res = False
    if usuario is not None and pwd != "":
        res = cambiar_pass(usuario,pwd)
    if res:
        res={"status": 200 , "mensaje":"Okay!!"}
    else:
        res={"status": 406 , "mensaje":"Error :("}
    logging.info(f"User {usuario} tried to change password: {res['mensaje']}")
    return res

@app.route("/delete",methods=['POST'])
def delete():
    usuario = session.get("usuario")
    res = borrar_usuario(usuario)
    if res:
        res={"status": 200 , "mensaje":"Deleted"}
    else:
        res={"status": 406 , "mensaje":"Error >:("}
    logging.info(f"User {usuario} tried to change password: {res['mensaje']}")
    return res




@app.route("/enymeep",methods=['GET','POST'])
def enymeep():
    usuario = session.get("usuario")
    requestBody = request.get_json()
    if requestBody['free'] != "True":
        restar_token(usuario)
    res = scanTarget(bleach.clean(requestBody['address']), bleach.clean(requestBody['ports']))
    logging.info(f"User {usuario} started scan: {requestBody['address']}:{requestBody['ports']}")
    return res

@app.route("/calculariva", methods=["GET"])
def calculariva(valor=0):
    if valor == 0:
        valor = bleach.clean(request.args.get('valor', default = 1, type = int))
    return {"status": 200 , "resultado":valor*0.21}

def prepare_response_extra_headers():
    response_extra_headers = {
        # always
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0',
        'Last-Modified': http_date(datetime.datetime.now()),
    }
    response_security_headers = {
        # X-Frame-Options: page can only be shown in an iframe of the same site
        'X-Frame-Options': 'SAMEORIGIN',
        # ensure all app communication is sent over HTTPS
        'Strict-Transport-Security': 'max-age=63072000; includeSubdomains',
        # instructs the browser not to override the response content type
        'X-Content-Type-Options': 'nosniff',
        # enable browser cross-site scripting (XSS) filter
        'X-XSS-Protection': '1; mode=block',
    }
    response_extra_headers.update(response_security_headers)

    return response_extra_headers

response_extra_headers = prepare_response_extra_headers()


@app.after_request
def after_request(response):
    response.headers.extend(response_extra_headers)
    return response