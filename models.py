import datetime as dt
import psycopg2
import pandas as pd

# URL de conexión a PostgreSQL (Supabase)  nO2KMyzrxfvFQv8K ; CBoQbbb7KfXsOYzN
URL = "postgresql://postgres.unwfcldhkvziqjaqrofv:nO2KMyzrxfvFQv8K@aws-0-eu-north-1.pooler.supabase.com:5432/postgres"

# Función para obtener la conexión
def get_connection():
    try:
        return psycopg2.connect(URL)
        print("✅ Conexión exitosa a la base de datos")
    except Exception as e:
        print("❌ Error al conectar con la base de datos:", e)

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
        try:
            with conexion.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO ventas (total, id_usuario,id_cliente)
                    VALUES (%s, %s, %s, %s)
                """, (total, id_usuario,id_cliente))
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
