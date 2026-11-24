
from base_datos.conexion import conectar_mongodb
from datetime import datetime


def guardar_sesion(id_usuario, rutina, ejercicios, observaciones):
    coleccion = conectar_mongodb()

    sesion = {
        "id_usuario": id_usuario,
        "fecha": datetime.now().strftime("%Y-%m-%d"),
        "rutina": rutina,
        "ejercicios": ejercicios,
        "observaciones": observaciones
    }

    coleccion.insert_one(sesion)

    print("Sesion guardada correctamente")


def listar_sesiones(id_usuario):
    coleccion = conectar_mongodb()

    sesiones = coleccion.find({"id_usuario": id_usuario})

    for sesion in sesiones:
        print(sesion)


def eliminar_sesion(id_sesion):
    coleccion = conectar_mongodb()

    from bson.objectid import ObjectId

    coleccion.delete_one({"_id": ObjectId(id_sesion)})

    print("Sesion eliminada correctamente")     
    
