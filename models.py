
import datetime as dt
import psycopg2
import pandas as pd
import pymysql
import pymysql.cursors


# Configura las variables de entorno
URL = psycopg2.connect(
    dbname = "postgres",
    user = "postgres.hbqbmfydmrlcupuljpxt",
    password = "admin@root",
    host = "aws-0-eu-north-1.pooler.supabase.com",
    port = 6543
)

db_config = {
    'host' : 'localhost',
    'user' : 'celest',
    'password' : '',
    'database' : 'eclipse',
    'cursorclass' : pymysql.cursors.DictCursor
}

# Función para obtener la conexión a PostgreSQL
def get_connection():
    conn = URL
    #conn = pymysql.connect(**db_config)
    return conn 

class Crear:
    def categoria(nombre):
        conexion = get_connection()
        try:
            with conexion.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO categorias (nombre_categoria)
                    VALUES ( %s)
                """, (nombre))
                conexion.commit()
        finally:
            conexion.close()
    
    def articulo(nombre, describcion, precio, categoria):
        conexion = get_connection()
        try:
            with conexion.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO productos (nombre, describcion, precio_unitario, id_categoria)
                    VALUES (%s, %s, %s, %s)
                """, (nombre, describcion, int(precio), int(categoria)))
                conexion.commit()
        finally:
            conexion.close()
    

class Usuarios:
    def insertar(nombre, password):
        conexion = get_connection()
        try:
            with conexion.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO usuarios (nombre, password)
                    VALUES (%s, %s)
                """, (nombre, password))
                conexion.commit()
        finally:
            conexion.close()

    def yo(usuario, password):
        conexion = get_connection()
        try:
            with conexion.cursor() as cursor:
                cursor.execute("SELECT * FROM usuarios WHERE nombre = %s AND password = %s", (usuario, password))
                columns = [desc[0] for desc in cursor.description]
                yo = cursor.fetchall()
        finally:
            conexion.close()
        
        # Retornar un DataFrame vacío si no se encuentra el usuario
        return pd.DataFrame(yo, columns = columns)

class Cargador:
    def categorias():
        conexion = get_connection()
        try:
            with conexion.cursor() as cursor:
                cursor.execute("SELECT * FROM categorias")
                columns = [desc[0] for desc in cursor.description]
                categorias = cursor.fetchall()
        finally:
            conexion.close()
        # Retornar un DataFrame vacío si no se encuentra el usuario
        return pd.DataFrame(categorias, columns = columns)
    
    def articulo(categoria):
        conexion = get_connection()
        try:
            with conexion.cursor() as cursor:
                cursor.execute("SELECT * FROM productos WHERE id_categoria = %s", (int(categoria)))
                columns = [desc[0] for desc in cursor.description]
                articulos = cursor.fetchall()
        finally:
            conexion.close()
        # Retornar un DataFrame vacío si no se encuentra el usuario
        return pd.DataFrame(articulos, columns = columns)
