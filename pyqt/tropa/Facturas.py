import sys
import mysql.connector
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QLabel, QTableWidget, QTableWidgetItem,
    QMessageBox, QDialog, QFormLayout
)


class FacturasCRUD(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CRUD Facturas - PyQt6")
        self.setGeometry(100, 100, 800, 400)

        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="MySQL",
            database="tr23270111"
        )
        self.cursor = self.conn.cursor()

        self.init_ui()
        self.mostrar_facturas()

    def init_ui(self):
        layout = QVBoxLayout()

        self.idfactura_input = QLineEdit()
        self.idfactura_input.setPlaceholderText("ID Factura")

        self.idventa_input = QLineEdit()
        self.idventa_input.setPlaceholderText("ID Venta")

        self.total_input = QLineEdit()
        self.total_input.setPlaceholderText("Total")

        layout.addWidget(QLabel("ID Factura:"))
        layout.addWidget(self.idfactura_input)
        layout.addWidget(QLabel("ID Venta:"))
        layout.addWidget(self.idventa_input)
        layout.addWidget(QLabel("Total:"))
        layout.addWidget(self.total_input)

        botones = QHBoxLayout()
        self.btn_agregar = QPushButton("Agregar")
        self.btn_actualizar = QPushButton("Actualizar")
        self.btn_eliminar = QPushButton("Eliminar")
        botones.addWidget(self.btn_agregar)
        botones.addWidget(self.btn_actualizar)
        botones.addWidget(self.btn_eliminar)
        layout.addLayout(botones)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(4)
        self.tabla.setHorizontalHeaderLabels(["ID Factura", "ID Venta", "Fecha Emisión", "Total"])
        layout.addWidget(self.tabla)

        self.setLayout(layout)

        self.btn_agregar.clicked.connect(self.agregar_factura)
        self.btn_actualizar.clicked.connect(self.abrir_ventana_actualizar)
        self.btn_eliminar.clicked.connect(self.abrir_ventana_eliminar)

    def mostrar_facturas(self):
        self.cursor.execute("SELECT * FROM facturas")
        datos = self.cursor.fetchall()
        self.tabla.setRowCount(len(datos))
        for fila, factura in enumerate(datos):
            for col, dato in enumerate(factura):
                self.tabla.setItem(fila, col, QTableWidgetItem(str(dato)))

    def agregar_factura(self):
        try:
            idfactura = int(self.idfactura_input.text())
            idventa = int(self.idventa_input.text())
            total = float(self.total_input.text())

            if total <= 0:
                QMessageBox.warning(self, "Error", "El total debe ser positivo.")
                return

            self.cursor.execute("SELECT * FROM ventas WHERE idventa = %s", (idventa,))
            if self.cursor.fetchone() is None:
                QMessageBox.warning(self, "Error", f"No existe venta con ID {idventa}")
                return

            self.cursor.execute(
                "INSERT INTO facturas (idfactura, idventa, total) VALUES (%s, %s, %s)",
                (idfactura, idventa, total)
            )
            self.conn.commit()
            self.limpiar_campos()
            self.mostrar_facturas()

        except ValueError:
            QMessageBox.warning(self, "Error", "Datos inválidos.")

    def limpiar_campos(self):
        self.idfactura_input.clear()
        self.idventa_input.clear()
        self.total_input.clear()

    def abrir_ventana_actualizar(self):
        dialogo = QDialog(self)
        dialogo.setWindowTitle("Actualizar Factura")
        layout = QFormLayout(dialogo)

        id_input = QLineEdit()
        nuevo_total_input = QLineEdit()

        layout.addRow("ID Factura:", id_input)
        layout.addRow("Nuevo Total:", nuevo_total_input)

        btn_actualizar = QPushButton("Actualizar")
        layout.addWidget(btn_actualizar)

        def actualizar():
            try:
                idfactura = int(id_input.text())
                nuevo_total = float(nuevo_total_input.text())

                if nuevo_total <= 0:
                    QMessageBox.warning(dialogo, "Error", "Total debe ser positivo.")
                    return

                self.cursor.execute("SELECT * FROM facturas WHERE idfactura = %s", (idfactura,))
                if self.cursor.fetchone() is None:
                    QMessageBox.warning(dialogo, "Error", "No existe factura con ese ID.")
                    return

                self.cursor.execute(
                    "UPDATE facturas SET total = %s WHERE idfactura = %s",
                    (nuevo_total, idfactura)
                )
                self.conn.commit()
                self.mostrar_facturas()
                dialogo.accept()

            except ValueError:
                QMessageBox.warning(dialogo, "Error", "Datos inválidos.")

        btn_actualizar.clicked.connect(actualizar)
        dialogo.exec()

    def abrir_ventana_eliminar(self):
        dialogo = QDialog(self)
        dialogo.setWindowTitle("Eliminar Factura")
        layout = QFormLayout(dialogo)

        id_input = QLineEdit()
        layout.addRow("ID Factura a eliminar:", id_input)

        btn_eliminar = QPushButton("Eliminar")
        layout.addWidget(btn_eliminar)

        def eliminar():
            try:
                idfactura = int(id_input.text())
            except ValueError:
                QMessageBox.warning(dialogo, "Error", "ID inválido.")
                return

            self.cursor.execute("SELECT * FROM facturas WHERE idfactura = %s", (idfactura,))
            if self.cursor.fetchone() is None:
                QMessageBox.warning(dialogo, "Error", "No existe factura con ese ID.")
                return

            self.cursor.execute("DELETE FROM facturas WHERE idfactura = %s", (idfactura,))
            self.conn.commit()
            self.mostrar_facturas()
            dialogo.accept()

        btn_eliminar.clicked.connect(eliminar)
        dialogo.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = FacturasCRUD()
    ventana.show()
    sys.exit(app.exec())
