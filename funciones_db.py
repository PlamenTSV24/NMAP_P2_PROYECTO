import pymysql
import hashlib

def obtener_hash(password):
    return hashlib.sha256(password.encode()).hexdigest()

def obtener_ip_por_nombre(nombre_maquina):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    query = "SELECT ip FROM maquinas WHERE nombre = %s"

    cursor.execute(query, (nombre_maquina,))
    resultado = cursor.fetchone()

    cursor.close()
    conexion.close()

    if resultado:
        return resultado[0]  # Retorna la IP si se encuentra la máquina
    else:
        return None  # Retorna None si no se encuentra la máquina

def registrar_usuario(usuario, password, tokens):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    password_hasheada = obtener_hash(password)
    
    query = "INSERT INTO usuarios (usuario, pass, tokens) VALUES (%s, %s, %s)"

    cursor.execute(query, (usuario, password_hasheada, tokens))
    conexion.commit()

    cursor.close()
    conexion.close()

def verificar_credenciales(usuario, password):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    query = "SELECT pass FROM usuarios WHERE usuario = %s"
    cursor.execute(query, (usuario,))
    resultado = cursor.fetchone()

    if resultado:
        password_hasheada_bd = resultado[0]
        password_hasheada_ingresada = obtener_hash(password) 

        if password_hasheada_bd == password_hasheada_ingresada:
            return True
        else:
            return False
    else:
        return False

    cursor.close()
    conexion.close()

def restar_token(usuario):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    query = "UPDATE usuarios SET tokens = tokens - 1 WHERE usuario = %s"

    cursor.execute(query, (usuario,))
    conexion.commit()

    cursor.close()
    conexion.close()

def borrar_usuario(usuario):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    query = "DELETE FROM usuarios WHERE usuario = %s"

    cursor.execute(query, (usuario,))
    conexion.commit()

    cursor.close()
    conexion.close()
