import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",  
        password="MySQL", 
        database="dbtaller"
    )

def crear_profesor(idprofesor, nombreProf):
    conexion = conectar()
    cursor = conexion.cursor()
    sql = "INSERT INTO profesor (idprofesor, nombreProf) VALUES (%s, %s)"
    try:
        cursor.execute(sql, (idprofesor, nombreProf))
        conexion.commit()
        print("Profesor agregado correctamente.")
    except mysql.connector.Error as err:
        print("Error:", err)
    finally:
        cursor.close()
        conexion.close()

def leer_profesores():
    conexion = conectar()
    cursor = conexion.cursor()
    sql = "SELECT * FROM profesor"
    cursor.execute(sql)
    profesores = cursor.fetchall()
    for profesor in profesores:
        print(f"ID: {profesor[0]}, Nombre: {profesor[1]}")
    cursor.close()
    conexion.close()

def actualizar_profesor(idprofesor, nuevo_nombre):
    conexion = conectar()
    cursor = conexion.cursor()
    sql = "UPDATE profesor SET nombreProf = %s WHERE idprofesor = %s"
    try:
        cursor.execute(sql, (nuevo_nombre, idprofesor))
        conexion.commit()
        print("Datos del profesor actualizados correctamente.")
    except mysql.connector.Error as err:
        print("Error:", err)
    finally:
        cursor.close()
        conexion.close()

def eliminar_profesor(idprofesor):
    conexion = conectar()
    cursor = conexion.cursor()
    sql = "DELETE FROM profesor WHERE idprofesor = %s"
    try:
        cursor.execute(sql, (idprofesor,))
        conexion.commit()
        print("Profesor eliminado correctamente.")
    except mysql.connector.Error as err:
        print("Error:", err)
    finally:
        cursor.close()
        conexion.close()

def menu():
    while True:
        print("\n--- CRUD de Profesor ---")
        print("1. Crear profesor")
        print("2. Leer profesores")
        print("3. Actualizar profesor")
        print("4. Eliminar profesor")
        print("5. Salir")
        
        opcion = input("Seleccione una opcion: ")
        
        if opcion == "1":
            idprofesor = input("Ingrese el ID del profesor: ")
            nombreProf = input("Ingrese el nombre del profesor: ")
            crear_profesor(idprofesor, nombreProf)
        elif opcion == "2":
            leer_profesores()
        elif opcion == "3":
            idprofesor = input("Ingrese el ID del profesor a actualizar: ")
            nuevo_nombre = input("Ingrese el nuevo nombre: ")
            actualizar_profesor(idprofesor, nuevo_nombre)
        elif opcion == "4":
            idprofesor = input("Ingrese el ID del profesor a eliminar: ")
            eliminar_profesor(idprofesor)
        elif opcion == "5":
            print("Saliendo...")
            break
        else:
            print("Opcion no valida. Intente de nuevo.")

if __name__ == "__main__":
    menu()
