import datetime as dt
import psycopg2
import pandas as pd

# URL de conexión a PostgreSQL (Supabase)
URL = "postgresql://postgres:S85yxyRmRKFs1yVm@db.hbqbmfydmrlcupuljpxt.supabase.co:5432/postgres"

# Función para obtener la conexión
def get_connection():
    return psycopg2.connect(URL)

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
    def articulo(nombre, descripcion, precio, categoria):
        conexion = get_connection()
        try:
            with conexion.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO productos (nombre, descripcion, precio_unitario, id_categoria)
                    VALUES (%s, %s, %s, %s)
                """, (nombre, descripcion, float(precio), int(categoria)))
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
