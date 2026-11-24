from base_datos.conexion import conectar_mysql


def listar_ejercicios():
    conexion = conectar_mysql()
    cursor = conexion.cursor()

    cursor.execute("SELECT id_ejercicio, nombre FROM ejercicios")

    ejercicios = cursor.fetchall()

    cursor.close()
    conexion.close()

    return ejercicios


def listar_ejercicios_completos():
    conexion = conectar_mysql()
    cursor = conexion.cursor(dictionary=True)

    consulta = """
        SELECT 
            e.id_ejercicio,
            e.nombre AS ejercicio,
            t.nombre AS tipo,
            COALESCE(eq.nombre, 'Sin equipo') AS equipo,
            COALESCE(GROUP_CONCAT(g.nombre SEPARATOR ', '), 'General') AS grupos_musculares
        FROM ejercicios e
        INNER JOIN tiposejercicios t ON e.id_tipo = t.id_tipo
        LEFT JOIN equipos eq ON e.id_equipo = eq.id_equipo
        LEFT JOIN ejerciciosgruposmusculares eg ON e.id_ejercicio = eg.id_ejercicio
        LEFT JOIN gruposmusculares g ON eg.id_grupo = g.id_grupo
        GROUP BY e.id_ejercicio, e.nombre, t.nombre, eq.nombre
        ORDER BY e.id_ejercicio
    """
    cursor.execute(consulta)
    resultados = cursor.fetchall()

    cursor.close()
    conexion.close()

    return resultados