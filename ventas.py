from PyQt6.QtWidgets import QTableWidgetItem, QDialog, QFormLayout, QLineEdit, QPushButton, QMessageBox
import mysql.connector

class Ventas:
    def __init__(self, parent):
        self.parent = parent
        self.conn = mysql.connector.connect(user='root', password='MySQL', host='localhost', database='tr23270111')
        self.cursor = self.conn.cursor()

    def mostrar_ventas(self):
        self.cursor.execute("SELECT * FROM ventas")
        rows = self.cursor.fetchall()

        self.parent.tableWidget.setRowCount(len(rows))
        self.parent.tableWidget.setColumnCount(5)

        for row_idx, row in enumerate(rows):
            for col_idx, val in enumerate(row):
                self.parent.tableWidget.setItem(row_idx, col_idx, QTableWidgetItem(str(val)))
