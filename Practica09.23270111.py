import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="MySQL",
        database="dbtaller"
    )

def creartipo(tipo, nombre):
    conexion = conectar()
    cursor = conexion.cursor()
    sql = "INSERT INTO tipoproyecto (tipo, nombre) VALUES (%s, %s)"
    try:
        cursor.execute(sql, (tipo, nombre))
        conexion.commit()
        print("Tipo de proyecto agregado correctamente.")
    except mysql.connector.Error as err:
        print("Error:", err)
    finally:
        cursor.close()
        conexion.close()

def leertipos():
    conexion = conectar()
    cursor = conexion.cursor()
    sql = "SELECT * FROM tipoproyecto"
    cursor.execute(sql)
    tipos = cursor.fetchall()
    for tipo in tipos:
        print(f"Tipo: {tipo[0]}, Nombre: {tipo[1]}")
    cursor.close()
    conexion.close()

def actualizartipo(tipo, nuevo_nombre):
    conexion = conectar()
    cursor = conexion.cursor()
    sql = "UPDATE tipoproyecto SET nombre = %s WHERE tipo = %s"
    try:
        cursor.execute(sql, (nuevo_nombre, tipo))
        conexion.commit()
        print("Tipo de proyecto actualizado correctamente.")
    except mysql.connector.Error as err:
        print("Error:", err)
    finally:
        cursor.close()
        conexion.close()

def eliminartipo(tipo):
    conexion = conectar()
    cursor = conexion.cursor()
    sql = "DELETE FROM tipoproyecto WHERE tipo = %s"
    try:
        cursor.execute(sql, (tipo,))
        conexion.commit()
        print("Tipo de proyecto eliminado correctamente.")
    except mysql.connector.Error as err:
        print("Error:", err)
    finally:
        cursor.close()
        conexion.close()

def menu():
    while True:
        print("\n--- CRUD de Tipos de Proyecto ---")
        print("1. Crear tipo de proyecto")
        print("2. Leer tipos de proyecto")
        print("3. Actualizar tipo de proyecto")
        print("4. Eliminar tipo de proyecto")
        print("5. Salir")
        
        opcion = input("Seleccione una opcion: ")
        
        if opcion == "1":
            tipo = input("Ingrese el codigo del tipo de proyecto (ej. DT, I): ")
            nombre = input("Ingrese el nombre del tipo de proyecto: ")
            creartipo(tipo, nombre)
        elif opcion == "2":
            leertipos()
        elif opcion == "3":
            tipo = input("Ingrese el codigo del tipo de proyecto a actualizar: ")
            nuevo_nombre = input("Ingrese el nuevo nombre: ")
            actualizartipo(tipo, nuevo_nombre)
        elif opcion == "4":
            tipo = input("Ingrese el codigo del tipo de proyecto a eliminar: ")
            eliminartipo(tipo)
        elif opcion == "5":
            print("Saliendo...")
            break
        else:
            print("Opcion no valida. Intente de nuevo.")

if __name__ == "__main__":
    menu()
