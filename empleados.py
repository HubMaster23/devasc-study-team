from PyQt6.QtWidgets import QTableWidgetItem, QDialog, QFormLayout, QLineEdit, QPushButton, QMessageBox
import mysql.connector

class Empleados:
    def __init__(self, parent):
        self.parent = parent
        self.conn = mysql.connector.connect(user='root', password='MySQL', host='localhost', database='tr23270111')
        self.cursor = self.conn.cursor()

    def mostrar_empleados(self):
        self.cursor.execute("SELECT * FROM empleados")
        rows = self.cursor.fetchall()

        self.parent.tableWidget.setRowCount(len(rows))
        self.parent.tableWidget.setColumnCount(5)

        for row_idx, row in enumerate(rows):
            for col_idx, val in enumerate(row):
                self.parent.tableWidget.setItem(row_idx, col_idx, QTableWidgetItem(str(val)))

    def agregar_empleado(self, nombre, puesto, salario):
        try:
            self.cursor.execute("INSERT INTO empleados (nombre, puesto, salario) VALUES (%s, %s, %s)", 
                                (nombre, puesto, salario))
            self.conn.commit()
            QMessageBox.information(self.parent, "Éxito", "Empleado agregado correctamente.")
            self.mostrar_empleados()
        except Exception as e:
            QMessageBox.warning(self.parent, "Error", f"Error al agregar empleado: {e}")
