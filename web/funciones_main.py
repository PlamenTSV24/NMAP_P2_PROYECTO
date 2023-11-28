from __future__ import print_function
from __main__ import app
from flask import render_template, session,request
from funciones_db import verificar_credenciales,verificar_usuario,registrar_usuario
from enymeep import scanTarget


@app.route("/",methods=['GET'])
def raiz():
    return render_template('access.html')


@app.route("/login",methods=['GET', 'POST'])
def login():
    requestLogin = request.get_json()

    try:
        username_bd = verificar_credenciales(requestLogin['username'],requestLogin['password'])

        if username_bd == False:
            code = 406
            res = {"status": code ,"mensaje":"Invalid username or password" }
        
        elif username_bd == True:
            session["usuario"]=requestLogin['username']

            return render_template ('control.html')
    

    except:
        code=406
        res={"status": code, "mensaje" : "An error has occurred while loading session"}

    return res


@app.route("/register",methods=['POST'])
def registro():
    requestRegister = request.get_json()
        
    try:
        user_exist = verificar_usuario(requestRegister['username'])
        if user_exist == True:
            code = 406
            res = res = {"status": code ,"mensaje":"User exists" }

        else:
            registrar_usuario(requestRegister['username'],requestRegister['password'])
            code = 200
            res = res = {"status": code , "mensaje":"You have been registered successfully"}

    except:
        code = 406
        res = res = {"status": code ,"mensaje":"An error has occurred while registering" }

    return res

@app.route("/enymeep",methods=['GET','POST'])
def enymeep():

    requestBody = request.get_json()
    res = scanTarget(requestBody['address'], requestBody['ports'])
    return res
