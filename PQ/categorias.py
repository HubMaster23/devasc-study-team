from PyQt6.QtWidgets import QTableWidgetItem, QDialog, QFormLayout, QLineEdit, QPushButton, QMessageBox
import mysql.connector

class Categorias:
    def __init__(self, parent):
        self.parent = parent
        self.conn = mysql.connector.connect(user='root', password='MySQL', host='localhost', database='tr23270111')
        self.cursor = self.conn.cursor()

    def mostrar_categorias(self):
        self.cursor.execute("SELECT * FROM categorias")
        rows = self.cursor.fetchall()

        self.parent.tableWidget.setRowCount(len(rows))
        self.parent.tableWidget.setColumnCount(3)

        for row_idx, row in enumerate(rows):
            for col_idx, val in enumerate(row):
                self.parent.tableWidget.setItem(row_idx, col_idx, QTableWidgetItem(str(val)))

    def agregar_categoria(self, nombre_categoria):
        try:
            self.cursor.execute("INSERT INTO categorias (nombre) VALUES (%s)", (nombre_categoria,))
            self.conn.commit()
            QMessageBox.information(self.parent, "Éxito", "Categoría agregada correctamente.")
            self.mostrar_categorias()
        except Exception as e:
            QMessageBox.warning(self.parent, "Error", f"Error al agregar categoría: {e}")
