from flask import Flask, render_template, request, redirect, url_for, flash, abort
from database import validate_user, create_user, get_cargos, get_clientes, get_cliente_by_id, create_cliente, update_cliente, delete_cliente, get_ciudades
import os
import sys
import time

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Cargar ciudades una vez
ciudades_cache = None


def get_ciudades_cached():
    global ciudades_cache
    if ciudades_cache is None:
        ciudades_cache = get_ciudades()
    return ciudades_cache


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = validate_user(username, password)

    if user:
        print("Usuario encontrado:", user)
        return redirect(url_for('menu'))
    else:
        print("Usuario no encontrado")
        flash('Usuario no Registrado. Ingrese Usuario Nuevo')
        return redirect(url_for('index'))


@app.route('/new_user')
def new_user():
    cargos = get_cargos()
    return render_template('Usuario.html', cargos=cargos)


@app.route('/create_user', methods=['POST'])
def create_new_user():
    username = request.form['username']
    password = request.form['password']
    cargo = request.form['cargo']
    create_user(username, password, cargo)
    flash('Usuario creado exitosamente')
    return redirect(url_for('index'))


@app.route('/menu')
def menu():
    return render_template('menu.html')

# -------------------------------------------
# Rutas para la gestión de clientes
# -------------------------------------------


@app.route('/clientes')
def clientes():
    start_time = time.time()
    clientes = get_clientes()
    end_time = time.time()
    print(f"clientes took {end_time - start_time:.2f} seconds")
    return render_template('clientes.html', clientes=clientes)


@app.route('/nuevo_cliente')
def nuevo_cliente():
    start_time = time.time()
    ciudades = get_ciudades_cached()
    end_time = time.time()
    print(f"nuevo_cliente took {end_time - start_time:.2f} seconds")
    return render_template('nuevo_cliente.html', ciudades=ciudades)


@app.route('/crear_cliente', methods=['POST'])
def crear_cliente():
    start_time = time.time()
    desc_cliente = request.form['DESC_CLIENTE']
    cod_ciudad = request.form['COD_CIUDAD']
    desc_ciudad = next((ciudad[1] for ciudad in get_ciudades_cached() if str(
        ciudad[0]) == cod_ciudad), "")
    direccion = request.form['Direccion']
    ruc = request.form['RUC']
    telefono = request.form['TELEFONO']
    correo = request.form['CORREO']
    correo2 = request.form['CORREO_2']
    cedula = request.form['CEDULA']
    create_cliente(desc_cliente, cod_ciudad, desc_ciudad,
                   direccion, ruc, telefono, correo, correo2, cedula)
    end_time = time.time()
    print(f"crear_cliente took {end_time - start_time:.2f} seconds")
    return redirect(url_for('clientes'))


@app.route('/editar_cliente/<int:cod_cliente>', methods=['GET', 'POST'])
def editar_cliente(cod_cliente):
    if request.method == 'POST':
        start_time = time.time()
        desc_cliente = request.form['Descripcion']
        cod_ciudad = request.form['COD_CIUDAD']
        ciudad = next((ciudad[1] for ciudad in get_ciudades_cached(
        ) if ciudad[0] == int(cod_ciudad)), "")
        direccion = request.form['Direccion']
        ruc = request.form['RUC']
        telefono = request.form['TELEFONO']
        correo = request.form['CORREO']
        correo2 = request.form['CORREO2']
        cedula = request.form['CEDULA']
        estado = 2  # Estado predeterminado para actualización
        update_cliente(cod_cliente, desc_cliente, cod_ciudad, ciudad,
                       direccion, ruc, telefono, correo, correo2, cedula, estado)
        end_time = time.time()
        print(f"editar_cliente took {end_time - start_time:.2f} seconds")
        return redirect(url_for('clientes'))
    else:
        start_time = time.time()
        cliente = get_cliente_by_id(cod_cliente)
        ciudades = get_ciudades_cached()
        end_time = time.time()
        print(f"editar_cliente took {end_time - start_time:.2f} seconds")
        return render_template('editar_cliente.html', cliente=cliente, ciudades=ciudades)


@app.route('/eliminar_cliente/<int:cod_cliente>', methods=['POST'])
def eliminar_cliente(cod_cliente):
    delete_cliente(cod_cliente, 3)  # Estado predefinido para eliminación
    return redirect(url_for('clientes'))


@app.route('/close_app')
def close_app():
    shutdown = request.environ.get('werkzeug.server.shutdown')
    if shutdown is None:
        abort(500)
    shutdown()
    return 'Aplicación cerrada.'


if __name__ == '__main__':
    from waitress import serve
    serve(app, host='192.168.0.5', port=5000)
