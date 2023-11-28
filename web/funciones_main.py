from __future__ import print_function
from __main__ import app
from flask import Flask, redirect, render_template, session,request
from database import obtener_conexion
from funciones_db import verificar_credenciales


@app.route("/",methods=['GET'])
def raiz():
    return render_template('access.html')


@app.route("/login",methods=['GET', 'POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    print(username)
    try:
        username_bd = verificar_credenciales(username,password)
        print(username_bd)

        if username_bd == False:
            ret = {"status": "ERROR","mensaje":"Usuario/clave erroneo" }
            return render_template('access.html')
        
        elif username_bd == True:
            ret = {"status": "OK" }

            session["usuario"]=username
            session["usuario_bd"]=username_bd
            code=200
            return 'error', code

    except:
        print("Excepcion al validar al usuario")   
        ret={"status":"ERROR"}
        code=500
        return 'error', code

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
        print()
    except:
        print()
        

        '''
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
                #cursor.execute("SELECT perfil FROM usuarios WHERE usuario = %s and clave= %s",(username,password))
                cursor.execute("SELECT perfil FROM usuarios WHERE usuario = '" + username +"' and clave= '" + password + "'")
                usuario = cursor.fetchone()
                if usuario is None:
                    print("INSERT INTO usuarios(usuario,clave,perfil) VALUES('"+ username +"','"+  password+"','"+ perfil+"')") 
                    cursor.execute("INSERT INTO usuarios(usuario,clave,perfil) VALUES('"+ username +"','"+  password+"','"+ perfil+"')")
                    if cursor.rowcount == 1:
                        conexion.commit()
                        ret={"status": "OK" }
                        code=200
                    else:
                        ret={"status": "ERROR" }
                        code=500
                else:
                    ret = {"status": "ERROR","mensaje":"Usuario/clave erroneo" }
                    code=200
        conexion.close()
    except:
        print("Excepcion al registrar al usuario")   
        ret={"status":"ERROR"}
        code=500
    else:
        ret={"status":"Bad request"}
        code=401
    return json.dumps(ret), code

'''