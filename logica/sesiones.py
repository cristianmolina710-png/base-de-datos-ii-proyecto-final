from base_datos.conexion import conectar_mongodb
from datetime import datetime
from bson.objectid import ObjectId


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


def listar_sesiones(id_usuario):
    coleccion = conectar_mongodb()

    sesiones = list(coleccion.find({"id_usuario": id_usuario}).sort("_id", -1))

    return sesiones


def eliminar_sesion(id_sesion):
    coleccion = conectar_mongodb()

    coleccion.delete_one({"_id": ObjectId(id_sesion)})