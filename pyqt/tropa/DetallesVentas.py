import sys
import mysql.connector
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QLabel, QTableWidget, QTableWidgetItem,
    QMessageBox, QDialog, QFormLayout
)

class DetalleVentasCRUD(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CRUD Detalle Ventas - PyQt6")
        self.setGeometry(100, 100, 800, 400)

        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="MySQL",
            database="tr23270111"
        )
        self.cursor = self.conn.cursor()

        self.init_ui()
        self.mostrar_detalles()

    def init_ui(self):
        layout = QVBoxLayout()

        self.idventa_input = QLineEdit()
        self.idventa_input.setPlaceholderText("ID Venta")

        self.idproducto_input = QLineEdit()
        self.idproducto_input.setPlaceholderText("ID Producto")

        self.cantidad_input = QLineEdit()
        self.cantidad_input.setPlaceholderText("Cantidad")

        self.subtotal_input = QLineEdit()
        self.subtotal_input.setPlaceholderText("Subtotal")

        layout.addWidget(QLabel("ID Venta:"))
        layout.addWidget(self.idventa_input)
        layout.addWidget(QLabel("ID Producto:"))
        layout.addWidget(self.idproducto_input)
        layout.addWidget(QLabel("Cantidad:"))
        layout.addWidget(self.cantidad_input)
        layout.addWidget(QLabel("Subtotal:"))
        layout.addWidget(self.subtotal_input)

        botones = QHBoxLayout()
        self.btn_agregar = QPushButton("Agregar")
        self.btn_actualizar = QPushButton("Actualizar")
        self.btn_eliminar = QPushButton("Eliminar")
        botones.addWidget(self.btn_agregar)
        botones.addWidget(self.btn_actualizar)
        botones.addWidget(self.btn_eliminar)
        layout.addLayout(botones)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(5)
        self.tabla.setHorizontalHeaderLabels(["ID Detalle", "ID Venta", "ID Producto", "Cantidad", "Subtotal"])
        layout.addWidget(self.tabla)

        self.setLayout(layout)

        self.btn_agregar.clicked.connect(self.agregar_detalle)
        self.btn_actualizar.clicked.connect(self.abrir_ventana_actualizar)
        self.btn_eliminar.clicked.connect(self.abrir_ventana_eliminar)

    def mostrar_detalles(self):
        self.cursor.execute("SELECT * FROM detalleventas")
        datos = self.cursor.fetchall()
        self.tabla.setRowCount(len(datos))
        for fila, detalle in enumerate(datos):
            for col, dato in enumerate(detalle):
                self.tabla.setItem(fila, col, QTableWidgetItem(str(dato)))

    def agregar_detalle(self):
        try:
            idventa = int(self.idventa_input.text())
            idproducto = int(self.idproducto_input.text())
            cantidad = int(self.cantidad_input.text())
            subtotal = float(self.subtotal_input.text())

            if cantidad <= 0 or subtotal <= 0:
                QMessageBox.warning(self, "Error", "Cantidad y subtotal deben ser positivos.")
                return

            self.cursor.execute("SELECT * FROM ventas WHERE idventa = %s", (idventa,))
            if self.cursor.fetchone() is None:
                QMessageBox.warning(self, "Error", f"No existe venta con ID {idventa}")
                return

            self.cursor.execute("SELECT * FROM productos WHERE idproducto = %s", (idproducto,))
            if self.cursor.fetchone() is None:
                QMessageBox.warning(self, "Error", f"No existe producto con ID {idproducto}")
                return

            self.cursor.execute(
                "INSERT INTO detalleventas (idventa, idproducto, cantidad, subtotal) VALUES (%s, %s, %s, %s)",
                (idventa, idproducto, cantidad, subtotal)
            )
            self.conn.commit()
            self.limpiar_campos()
            self.mostrar_detalles()

        except ValueError:
            QMessageBox.warning(self, "Error", "Datos inválidos.")

    def limpiar_campos(self):
        self.idventa_input.clear()
        self.idproducto_input.clear()
        self.cantidad_input.clear()
        self.subtotal_input.clear()

    def abrir_ventana_actualizar(self):
        dialogo = QDialog(self)
        dialogo.setWindowTitle("Actualizar Detalle Venta")
        layout = QFormLayout(dialogo)

        iddetalle_input = QLineEdit()
        nueva_cantidad_input = QLineEdit()
        nuevo_subtotal_input = QLineEdit()

        layout.addRow("ID Detalle:", iddetalle_input)
        layout.addRow("Nueva Cantidad:", nueva_cantidad_input)
        layout.addRow("Nuevo Subtotal:", nuevo_subtotal_input)

        btn_actualizar = QPushButton("Actualizar")
        layout.addWidget(btn_actualizar)

        def actualizar():
            try:
                iddetalle = int(iddetalle_input.text())
                nueva_cantidad = int(nueva_cantidad_input.text())
                nuevo_subtotal = float(nuevo_subtotal_input.text())

                if nueva_cantidad <= 0 or nuevo_subtotal <= 0:
                    QMessageBox.warning(dialogo, "Error", "Valores deben ser positivos.")
                    return

                self.cursor.execute("SELECT * FROM detalleventas WHERE iddetalle = %s", (iddetalle,))
                if self.cursor.fetchone() is None:
                    QMessageBox.warning(dialogo, "Error", "No existe detalle con ese ID.")
                    return

                self.cursor.execute(
                    "UPDATE detalleventas SET cantidad = %s, subtotal = %s WHERE iddetalle = %s",
                    (nueva_cantidad, nuevo_subtotal, iddetalle)
                )
                self.conn.commit()
                self.mostrar_detalles()
                dialogo.accept()

            except ValueError:
                QMessageBox.warning(dialogo, "Error", "Datos inválidos.")

        btn_actualizar.clicked.connect(actualizar)
        dialogo.exec()

    def abrir_ventana_eliminar(self):
        dialogo = QDialog(self)
        dialogo.setWindowTitle("Eliminar Detalle")
        layout = QFormLayout(dialogo)

        id_input = QLineEdit()
        layout.addRow("ID Detalle a eliminar:", id_input)

        btn_eliminar = QPushButton("Eliminar")
        layout.addWidget(btn_eliminar)

        def eliminar():
            try:
                iddetalle = int(id_input.text())
            except ValueError:
                QMessageBox.warning(dialogo, "Error", "ID inválido.")
                return

            self.cursor.execute("SELECT * FROM detalleventas WHERE iddetalle = %s", (iddetalle,))
            if self.cursor.fetchone() is None:
                QMessageBox.warning(dialogo, "Error", "No existe detalle con ese ID.")
                return

            self.cursor.execute("DELETE FROM detalleventas WHERE iddetalle = %s", (iddetalle,))
            self.conn.commit()
            self.mostrar_detalles()
            dialogo.accept()

        btn_eliminar.clicked.connect(eliminar)
        dialogo.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = DetalleVentasCRUD()
    ventana.show()
    sys.exit(app.exec())
