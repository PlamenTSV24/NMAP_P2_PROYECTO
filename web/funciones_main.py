from __future__ import print_function
from __main__ import app
from flask import Flask, redirect, render_template, session,request
from database import obtener_conexion
from funciones_db import verificar_credenciales,verificar_usuario,registrar_usuario
from enymeep import scanTarget


@app.route("/",methods=['GET'])
def raiz():
    return render_template('access.html')


@app.route("/login",methods=['GET', 'POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    # try:
    username_bd = verificar_credenciales(username,password)

    if username_bd == False:
        ret = {"status": "ERROR","mensaje":"Usuario/clave erroneo" }
        return ret
    
    elif username_bd == True:
        ret = {"status": "OK" }

        session["usuario"]=username
        session["usuario_bd"]=username_bd
        code=200
        return render_template ('control.html')

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
    username = request.form['username']
    password = request.form['password']
    password2 = request.form['password2']
    print(username)
    try:
        print("he entrado altry")
        user_exist = verificar_usuario(username)
        if user_exist == True:
            print("estoy en el if")

            print("el usuario ya existe 'haz lo que veas' ")
        else:
            print("estoy en el else")
            registrar_usuario(username,password,)
            print("has sido registrado correctamente")


    except:
        print("Error no se ha podido introducir el usuario")
        

@app.route("/enymeep",methods=['GET','POST'])
def enymeep():

    requestBody = request.get_json()
    res = scanTarget(requestBody['address'], requestBody['ports'])

    return res


