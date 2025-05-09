from PyQt6.QtWidgets import QTableWidgetItem, QDialog, QFormLayout, QLineEdit, QPushButton, QMessageBox
import mysql.connector

class Facturas:
    def __init__(self, parent):
        self.parent = parent
        self.conn = mysql.connector.connect(user='root', password='MySQL', host='localhost', database='tr23270111')
        self.cursor = self.conn.cursor()

    def mostrar_facturas(self):
        self.cursor.execute("SELECT * FROM facturas")
        rows = self.cursor.fetchall()

        self.parent.tableWidget.setRowCount(len(rows))
        self.parent.tableWidget.setColumnCount(4)

        for row_idx, row in enumerate(rows):
            for col_idx, val in enumerate(row):
                self.parent.tableWidget.setItem(row_idx, col_idx, QTableWidgetItem(str(val)))

    def agregar_factura(self, idventa, total, fecha):
        try:
            self.cursor.execute("INSERT INTO facturas (idventa, total, fecha) VALUES (%s, %s, %s)",
                                (idventa, total, fecha))
            self.conn.commit()
            QMessageBox.information(self.parent, "Éxito", "Factura agregada correctamente.")
            self.mostrar_facturas()
        except Exception as e:
            QMessageBox.warning(self.parent, "Error", f"Error al agregar factura: {e}")
