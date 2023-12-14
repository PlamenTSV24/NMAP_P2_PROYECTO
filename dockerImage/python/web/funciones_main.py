from __future__ import print_function
from __main__ import app
from flask import render_template, session,request
from funciones_db import verificar_credenciales,verificar_usuario,registrar_usuario,restar_token,cambiar_pass
from enymeep import scanTarget


@app.route("/",methods=['GET'])
def raiz():
    session.clear()
    return render_template('access.html')


@app.route("/login",methods=['GET', 'POST'])
def login():
    requestLogin = request.get_json()
    #try:
    username_bd = verificar_credenciales(requestLogin['username'],requestLogin['password'])
    print(username_bd)
    if username_bd is False:
        res = {"status": 406 ,"mensaje":"Invalid username or password" }
    
    else:
        session["usuario"]=requestLogin['username']
        session["tokens"]=username_bd
        # return render_template("control.html")
        res = {"status": 301 ,"mensaje":"Login correct", "target":"/dashboard"}

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
        user_exist = verificar_usuario(requestRegister['username'])
        if user_exist == True:
            res = {"status": 406 ,"mensaje":"User exists" }

        else:
            registrar_usuario(requestRegister['username'],requestRegister['password'])
            res = {"status": 200 , "mensaje":"You have been registered successfully"}

    except:
        res = {"status": 500 ,"mensaje":"An error has occurred while registering" }

    return res

@app.route("/password",methods=['POST'])
def password():
    requestBody = request.get_json()
    usuario = session.get("usuario")
    pwd = requestBody["pwd"]
    res = False
    print(pwd)
    print(usuario)
    if usuario is not None and pwd != "":
        res = cambiar_pass(usuario,pwd)
    if res:
        res={"status": 200 , "mensaje":"Okay!!"}
    else:
        res={"status": 406 , "mensaje":"Error :("}
    return res




@app.route("/enymeep",methods=['GET','POST'])
def enymeep():
    requestBody = request.get_json()
    if requestBody['free'] != "True":
        restar_token(session.get("usuario"))
    res = scanTarget(requestBody['address'], requestBody['ports'])
    return res
