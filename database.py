import firebirdsql

def get_connection():
    conn = firebirdsql.connect(
        host='localhost',
        database='C:\\Archivos\\AppVentas\\BaseDatos\\BASEDEDATOS.FDB',
        user='SYSDBA',
        password='di03051999',
        charset='WIN1252',
        port=3050
    )
    return conn

def validate_user(username, password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM USUARIOS WHERE LOWER(USUARIO) = ? AND LOWER(SENHA) = ?", (username.lower(), password.lower()))
    user = cur.fetchone()
    conn.close()
    return user

def create_user(username, password, cargo):
    conn = get_connection()
    cur = conn.cursor()
    
    # Obtener el nuevo valor para REGISTRO
    cur.execute("SELECT COALESCE(MAX(REGISTRO), 0) + 1 FROM USUARIOS")
    new_registro = cur.fetchone()[0]
    
    # Obtener la descripción del cargo
    cur.execute("SELECT DESCRIPCION FROM CARGO WHERE REGISTRO = ?", (cargo,))
    cargo_desc = cur.fetchone()[0]
    
    cur.execute("INSERT INTO USUARIOS (REGISTRO, USUARIO, SENHA, CARGO, CARGO_DESC, ESTADO) VALUES (?, ?, ?, ?, ?, 1)", 
                (new_registro, username, password, cargo, cargo_desc))
    conn.commit()
    conn.close()

def get_cargos():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT REGISTRO, DESCRIPCION FROM CARGO")
    cargos = cur.fetchall()
    conn.close()
    return cargos

def is_database_empty():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM USUARIOS")
    count = cur.fetchone()[0]
    conn.close()
    return count == 0

# -------------------------------------------
# Funciones para gestionar clientes
# -------------------------------------------

def get_clientes():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COD_CLIENTE, DESC_CLIENTE, COD_CIUDAD, DESC_CIUDAD, DIRECCION, RUC, TELEFONO, CORREO, CORREO_2, CEDULA, ESTADO FROM CLIENTES WHERE ESTADO<>3")
    clientes = cur.fetchall()
    conn.close()
    return clientes

def get_cliente_by_id(cod_cliente):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COD_CLIENTE, DESC_CLIENTE, DIRECCION, COD_CIUDAD, DESC_CIUDAD, RUC, TELEFONO, CORREO, CORREO_2, CEDULA, ESTADO FROM CLIENTES WHERE COD_CLIENTE = ? AND ESTADO <> 3", (cod_cliente,))
    cliente = cur.fetchone()
    conn.close()
    return cliente

def create_cliente(desc_cliente, cod_ciudad, desc_ciudad, direccion, ruc, telefono, correo, correo2, cedula):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COALESCE(MAX(COD_CLIENTE), 0) + 1 FROM CLIENTES")
    new_cod_cliente = cur.fetchone()[0]
    cur.execute("""
        INSERT INTO CLIENTES (COD_CLIENTE, DESC_CLIENTE, COD_CIUDAD, DESC_CIUDAD, DIRECCION, RUC, TELEFONO, CORREO, CORREO_2, CEDULA, ESTADO) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (new_cod_cliente, desc_cliente, cod_ciudad, desc_ciudad, direccion, ruc, telefono, correo, correo2, cedula, 1))  # Estado = 1 por defecto
    conn.commit()
    conn.close()

def update_cliente(cod_cliente, desc_cliente, cod_ciudad, desc_ciudad, direccion, ruc, telefono, correo, correo2, cedula, estado=2):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE CLIENTES 
        SET DESC_CLIENTE = ?, COD_CIUDAD = ?, DESC_CIUDAD = ?, DIRECCION = ?, RUC = ?, TELEFONO = ?, CORREO = ?, CORREO_2 = ?, CEDULA = ?, ESTADO = ?
        WHERE COD_CLIENTE = ?
    """, (desc_cliente, cod_ciudad, desc_ciudad, direccion, ruc, telefono, correo, correo2, cedula, estado, cod_cliente))
    conn.commit()
    conn.close()

def delete_cliente(cod_cliente, estado):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE CLIENTES SET ESTADO = ? WHERE COD_CLIENTE = ?", (estado, cod_cliente))
    conn.commit()
    conn.close()

def get_ciudades():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COD_CIUDAD, CIUDAD FROM CIUDADES")
    ciudades = cur.fetchall()
    conn.close()
    return ciudades
