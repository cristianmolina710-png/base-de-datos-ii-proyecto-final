from base_datos.conexion import conectar_mysql

conexion = conectar_mysql()
print("Conexion con MySQL exitosa")
conexion.close()

from logica.sesiones import listar_sesiones

listar_sesiones(2)

