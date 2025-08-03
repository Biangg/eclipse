
from flask import Flask, session, jsonify, render_template, make_response, g, request
import datetime as dt
import pandas as pd
import sqlite3, models, json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'APOCALIPTO'
DATABASE = 'database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        elemento = request.form['elemento']
        if elemento == "articulo":
            nombre = request.form['nombre']
            describcion = request.form['describcion']
            precio = request.form['precio']
            categoria = request.form['categoria']
            models.Crear.articulo(nombre, describcion, precio, categoria)
            return jsonify({"estado" : "ok"})
        nombre = request.form["nombre"]
        models.Crear.categoria(nombre)
        return jsonify({"estado" : "ok"})

@app.route('/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        usuario = models.Usuarios()
        try:
            usuario = request.form["usuario"]
            password = request.form["password"]
            yo = models.Usuarios.yo(usuario, password)
            if yo.empty:
                return jsonify({"estado" : "usuario no encontrado"})
            else:
                session["usuario"] = usuario
                session["password"] = password
                response = {'status': 200, 'usuario': usuario}
                return jsonify(response)
        except:
            return None
    if 'password' in session and 'usuario' in session:
        yo = models.Usuarios.yo(session['usuario'], session['password'])
        categorias = models.Cargador.categorias()
        return make_response(render_template('ventas.html', yo=yo, categorias = categorias))
    return render_template('login.html')

@app.route('/ventas')
def ventas():
    if 'password' in session and 'usuario' in session:
        yo = models.Usuarios.yo(session['usuario'], session['password'])
        categorias = models.Cargador.categorias()
        return make_response(render_template('ventas.html', categorias = categorias))
    return render_template('login.html')

@app.route('/articulos')
def articulos():
    if 'password' in session and 'usuario' in session:
        yo = models.Usuarios.yo(session['usuario'], session['password'])
        categorias = models.Cargador.categorias()
        return make_response(render_template('articulos.html', categorias = categorias))
    return render_template('login.html')

@app.route('/cargar', methods=['POST'])
def cargar():
    if request.method == 'POST':
        categoria = request.form["folder"]
        cargar = models.Cargador.articulo(categoria)
        tabla = json.loads(cargar.to_json(orient='records'))
        return jsonify(tabla)

if __name__ == '__main__':
    app.run(debug=True)
