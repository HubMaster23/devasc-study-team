from PyQt6.QtWidgets import QTableWidgetItem, QDialog, QFormLayout, QLineEdit, QPushButton, QMessageBox
import mysql.connector

class DetallesVentas:
    def __init__(self, parent):
        self.parent = parent
        self.conn = mysql.connector.connect(user='root', password='MySQL', host='localhost', database='tr23270111')
        self.cursor = self.conn.cursor()

    def mostrar_detalles_ventas(self):
        self.cursor.execute("SELECT * FROM detalles_ventas")
        rows = self.cursor.fetchall()

        self.parent.tableWidget.setRowCount(len(rows))
        self.parent.tableWidget.setColumnCount(5)

        for row_idx, row in enumerate(rows):
            for col_idx, val in enumerate(row):
                self.parent.tableWidget.setItem(row_idx, col_idx, QTableWidgetItem(str(val)))

    def agregar_detalle_venta(self, idventa, idproducto, cantidad, precio_unitario):
        try:
            self.cursor.execute("INSERT INTO detalles_ventas (idventa, idproducto, cantidad, precio_unitario) "
                                "VALUES (%s, %s, %s, %s)", (idventa, idproducto, cantidad, precio_unitario))
            self.conn.commit()
            QMessageBox.information(self.parent, "Éxito", "Detalle de venta agregado correctamente.")
            self.mostrar_detalles_ventas()
        except Exception as e:
            QMessageBox.warning(self.parent, "Error", f"Error al agregar detalle de venta: {e}")
