
from base_datos.conexion import conectar_mysql


def listar_ejercicios():
    conexion = conectar_mysql()
    cursor = conexion.cursor()

    cursor.execute("SELECT id_ejercicio, nombre FROM Ejercicios")

    ejercicios = cursor.fetchall()

    cursor.close()
    conexion.close()

    return ejercicios


def listar_ejercicios_completos():
    conexion = conectar_mysql()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT Ejercicios.nombre, Equipos.nombre
        FROM Ejercicios
        INNER JOIN Equipos
        ON Ejercicios.id_equipo = Equipos.id_equipo
    """)

    resultados = cursor.fetchall()

    for resultado in resultados:
        print(resultado)

    cursor.close()
    conexion.close()