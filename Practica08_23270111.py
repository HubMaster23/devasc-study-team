import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="usuario",
        password="contraseña",
        database="dbtaller"
    )

def crear_linea(clavein, nombre):
    conexion = conectar()
    cursor = conexion.cursor()
    sql = "INSERT INTO lineainv (clavein, nombre) VALUES (%s, %s)"
    try:
        cursor.execute(sql, (clavein, nombre))
        conexion.commit()
        print("Línea de investigación agregada correctamente.")
    except mysql.connector.Error as err:
        print("Error:", err)
    finally:
        cursor.close()
        conexion.close()

def leer_lineas():
    conexion = conectar()
    cursor = conexion.cursor()
    sql = "SELECT * FROM lineainv"
    cursor.execute(sql)
    lineas = cursor.fetchall()
    for linea in lineas:
        print(f"Clave: {linea[0]}, Nombre: {linea[1]}")
    cursor.close()
    conexion.close()

def actualizar_linea(clavein, nuevo_nombre):
    conexion = conectar()
    cursor = conexion.cursor()
    sql = "UPDATE lineainv SET nombre = %s WHERE clavein = %s"
    try:
        cursor.execute(sql, (nuevo_nombre, clavein))
        conexion.commit()
        print("Línea de investigación actualizada correctamente.")
    except mysql.connector.Error as err:
        print("Error:", err)
    finally:
        cursor.close()
        conexion.close()

def eliminar_linea(clavein):
    conexion = conectar()
    cursor = conexion.cursor()
    sql = "DELETE FROM lineainv WHERE clavein = %s"
    try:
        cursor.execute(sql, (clavein,))
        conexion.commit()
        print("Línea de investigación eliminada correctamente.")
    except mysql.connector.Error as err:
        print("Error:", err)
    finally:
        cursor.close()
        conexion.close()

def menu():
    while True:
        print("\n--- CRUD de Líneas de Investigación ---")
        print("1. Crear línea de investigación")
        print("2. Leer líneas de investigación")
        print("3. Actualizar línea de investigación")
        print("4. Eliminar línea de investigación")
        print("5. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            clavein = input("Ingrese la clave de la línea: ")
            nombre = input("Ingrese el nombre de la línea: ")
            crear_linea(clavein, nombre)
        elif opcion == "2":
            leer_lineas()
        elif opcion == "3":
            clavein = input("Ingrese la clave de la línea a actualizar: ")
            nuevo_nombre = input("Ingrese el nuevo nombre: ")
            actualizar_linea(clavein, nuevo_nombre)
        elif opcion == "4":
            clavein = input("Ingrese la clave de la línea a eliminar: ")
            eliminar_linea(clavein)
        elif opcion == "5":
            print("Saliendo...")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    menu()
