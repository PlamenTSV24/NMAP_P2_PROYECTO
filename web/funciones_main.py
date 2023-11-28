from __future__ import print_function
from __main__ import app
from flask import Flask, redirect, render_template, session,request,make_response,jsonify
from database import obtener_conexion
from funciones_db import verificar_credenciales,verificar_usuario,registrar_usuario
from enymeep import scanTarget


@app.route("/",methods=['GET'])
def raiz():
    return render_template('access.html')


@app.route("/login",methods=['GET', 'POST'])
def login():
    requestLogin = request.get_json()

    # try:
    username_bd = verificar_credenciales(requestLogin['username'],requestLogin['password'])

    if username_bd == False:
        code = 406
        res = {"status": code ,"mensaje":"Usuario/clave erroneo" }
    
    elif username_bd == True:

        session["usuario"]=requestLogin['username']
        session["usuario_bd"]=username_bd

        return render_template ('control.html')
    
    return res

    # except Exception as e:
    #     print("Excepcion al validar al usuario")   
    #     print (e)
    #     ret={"status":"ERROR"}
    #     code=500
    #     return 'error', code

#    else:
#        ret={"status":"Bad request"}
#        code=401
    

@app.route("/register",methods=['POST'])
def registro():
    requestRegister = request.get_json()
        
    try:
        user_exist = verificar_usuario(requestRegister['username'])
        if user_exist == True:
            code = 406
            res = res = {"status": code ,"mensaje":"El usuario ya existe" }

        else:
            registrar_usuario(requestRegister['username'],requestRegister['password'],)
            code = 200
            res = res = {"status": code , "mensaje":"Has sido registrado correctamente" }

    except:
        code = 406
        res = res = {"status": code ,"mensaje":"No se ha podido registrar el usuario" }

    return res

@app.route("/enymeep",methods=['GET','POST'])
def enymeep():

    requestBody = request.get_json()
    res = scanTarget(requestBody['address'], requestBody['ports'])
    return res
