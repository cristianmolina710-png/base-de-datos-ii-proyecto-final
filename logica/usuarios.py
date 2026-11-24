from base_datos.conexion import conectar_mysql


def iniciar_sesion(correo, password):
    conexion = conectar_mysql()
    cursor = conexion.cursor(dictionary=True)

    consulta = """
        SELECT u.id_usuario, u.nombre, u.correo, r.nombre AS rol
        FROM usuarios u
        INNER JOIN roles r ON u.id_rol = r.id_rol
        WHERE u.correo = %s AND u.password_hash = %s
    """
    cursor.execute(consulta, (correo, password))
    usuario = cursor.fetchone()

    cursor.close()
    conexion.close()

    return usuario