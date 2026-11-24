
import mysql.connector
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()


def conectar_mysql():
    conexion = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE")
    )

    return conexion 


def conectar_mongodb():
    cliente = MongoClient("mongodb://localhost:27017/")
    base_datos = cliente["GymTrack"]
    coleccion = base_datos["sesiones_entrenamiento"]

    return coleccion
