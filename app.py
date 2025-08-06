
from flask import Flask, session, jsonify, render_template, make_response, g, request
import datetime as dt
import pandas as pd
import sqlite3, models, json, os, platform, shutil
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'APOCALIPTO'

UPLOAD_FOLDER = 'static/image/productos'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        elemento = request.form['elemento']
        if elemento == "articulo":
            imagen = request.files['imagen']
            categoria = request.form['categoria']
            if imagen and allowed_file(imagen.filename):
                filename = secure_filename(imagen.filename)
                os.makedirs(app.config['UPLOAD_FOLDER'] + f"/{categoria}", exist_ok=True)  # Crea la carpeta si no existe
                imagen.save(os.path.join(app.config['UPLOAD_FOLDER'] + f"/{categoria}", filename))
            else:
                print("la imagen no es valida")
            nombre = request.form['nombre']
            describcion = request.form['describcion']
            precio = request.form['precio']
            codigo = request.form['codigo']
            impuestos = request.form['impuestos']
            models.Crear.articulo(nombre, describcion, impuestos, codigo,filename, precio, categoria)
            return jsonify({"estado" : "ok"})
        nombre = request.form["nombre"]
        models.Crear.categoria(nombre)
        return jsonify({"estado" : "ok"})

@app.route('/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        try:
            usuario = request.form["usuario"]
            password = request.form["password"]
            yo = models.Usuarios.yo(usuario, password)
            if yo.empty:
                return jsonify({'status': 401, 'error': 'Usuario no encontrado'}), 401  # ⚠️ mejor que return None
            else:
                session["usuario"] = usuario
                session["password"] = password
                response = {'status': 200, 'usuario': usuario}
                return jsonify(response)
        except Exception as e:
            return jsonify({'status': 500, 'error': str(e)}), 500  # devuelve error con mensaje
    # GET method
    if 'password' in session and 'usuario' in session:
        yo = models.Usuarios.yo(session['usuario'], session['password'])
        categorias = models.Cargador.categorias()
        return make_response(render_template('ventas.html', yo=yo, categorias=categorias))
    return render_template('login.html')

@app.route('/ventas', methods=['POST', 'GET'])
def ventas():
    if request.method == 'POST':
        datos = request.get_json()
        tabla = pd.DataFrame([datos])
        models.Crear.venta(tabla['total'][0],tabla['id_usuario'][0],tabla['id_cliente'][0])
        return jsonify({"estado" : 0})
    if 'password' in session and 'usuario' in session:
        yo = models.Usuarios.yo(session['usuario'], session['password'])
        categorias = models.Cargador.categorias()
        return make_response(render_template('ajustes.html', categorias = categorias, yo = yo))
    return render_template('login.html')

@app.route('/inventario', methods=['POST', 'GET'])
def inventario():
    if request.method == 'POST':
        datos = request.get_json()
        tabla = pd.DataFrame([datos])
        models.Crear.venta(tabla['total'][0],tabla['id_usuario'][0],tabla['id_cliente'][0])
        return jsonify({"estado" : 0})
    if 'password' in session and 'usuario' in session:
        yo = models.Usuarios.yo(session['usuario'], session['password'])
        categorias = models.Cargador.categorias()
        return make_response(render_template('inventario.html', categorias = categorias, yo = yo))
    return render_template('login.html')

@app.route('/ajustes')
def config():
    if 'password' in session and 'usuario' in session:
        yo = models.Usuarios.yo(session['usuario'], session['password'])
        return make_response(render_template('ajustes.html'))
    return render_template('login.html')

@app.route('/articulos')
def articulos():
    if 'password' in session and 'usuario' in session:
        yo = models.Usuarios.yo(session['usuario'], session['password'])
        categorias = models.Cargador.categorias()
        return make_response(render_template('articulos.html', categorias = categorias))
    return render_template('login.html')


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

@app.route('/cargar', methods=['POST'])
def cargar():
    if request.method == 'POST':
        categoria = request.form["folder"]
        cargar = models.Cargador.articulo(categoria)
        tabla = json.loads(cargar.to_json(orient='records'))
        return jsonify(tabla)

if __name__ == '__main__':
    app.run(debug=True, port=8080)