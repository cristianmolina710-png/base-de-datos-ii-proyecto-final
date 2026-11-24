from base_datos.conexion import conectar_mysql


def listar_rutinas():
    conexion = conectar_mysql()
    cursor = conexion.cursor(dictionary=True)

    consulta = """
        SELECT 
            id_rutina,
            nombre,
            COALESCE(descripcion, 'Sin descripción') AS descripcion,
            CASE WHEN es_predefinifa = 1 THEN 'Predefinida' ELSE 'Personalizada' END AS origen
        FROM rutinas
        ORDER BY id_rutina
    """
    cursor.execute(consulta)
    rutinas = cursor.fetchall()

    cursor.close()
    conexion.close()

    return rutinas


def obtener_ejercicios_de_rutina(id_rutina):
    conexion = conectar_mysql()
    cursor = conexion.cursor(dictionary=True)

    consulta = """
        SELECT 
            e.id_ejercicio,
            e.nombre AS ejercicio,
            re.series,
            re.repeticiones
        FROM rutinasejercicios re
        INNER JOIN ejercicios e ON re.id_ejercicio = e.id_ejercicio
        WHERE re.id_rutina = %s
    """
    cursor.execute(consulta, (id_rutina,))
    ejercicios = cursor.fetchall()

    cursor.close()
    conexion.close()

    return ejercicios