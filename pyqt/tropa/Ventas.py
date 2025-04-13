import sys
import mysql.connector
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
    QTableWidget, QTableWidgetItem, QPushButton, QMessageBox,
    QLabel, QDialog, QFormLayout
)


class VentasCRUD(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CRUD Ventas - PyQt6")
        self.setGeometry(100, 100, 800, 400)

        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="MySQL",
            database="tr23270111"
        )
        self.cursor = self.conn.cursor()

        self.init_ui()
        self.mostrar_ventas()

    def init_ui(self):
        layout = QVBoxLayout()

        self.idcliente_input = QLineEdit()
        self.idcliente_input.setPlaceholderText("ID Cliente")

        self.idempleado_input = QLineEdit()
        self.idempleado_input.setPlaceholderText("ID Empleado")

        self.total_input = QLineEdit()
        self.total_input.setPlaceholderText("Total Venta")

        layout.addWidget(QLabel("ID Cliente:"))
        layout.addWidget(self.idcliente_input)
        layout.addWidget(QLabel("ID Empleado:"))
        layout.addWidget(self.idempleado_input)
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
        self.tabla.setColumnCount(5)
        self.tabla.setHorizontalHeaderLabels(["ID Venta", "ID Cliente", "ID Empleado", "Fecha", "Total"])
        layout.addWidget(self.tabla)

        self.setLayout(layout)

        self.btn_agregar.clicked.connect(self.agregar_venta)
        self.btn_actualizar.clicked.connect(self.abrir_ventana_actualizar)
        self.btn_eliminar.clicked.connect(self.abrir_ventana_eliminar)

    def mostrar_ventas(self):
        self.cursor.execute("SELECT * FROM ventas")
        datos = self.cursor.fetchall()
        self.tabla.setRowCount(len(datos))
        for fila, venta in enumerate(datos):
            for col, dato in enumerate(venta):
                self.tabla.setItem(fila, col, QTableWidgetItem(str(dato)))

    def agregar_venta(self):
        try:
            idcliente = int(self.idcliente_input.text())
            idempleado = int(self.idempleado_input.text())
            total = float(self.total_input.text())

            if total <= 0:
                QMessageBox.warning(self, "Error", "El total debe ser mayor a 0.")
                return

            self.cursor.execute("SELECT * FROM clientes WHERE idcliente = %s", (idcliente,))
            if self.cursor.fetchone() is None:
                QMessageBox.warning(self, "Error", f"No existe cliente con ID {idcliente}")
                return

            self.cursor.execute("SELECT * FROM empleados WHERE idempleado = %s", (idempleado,))
            if self.cursor.fetchone() is None:
                QMessageBox.warning(self, "Error", f"No existe empleado con ID {idempleado}")
                return

            self.cursor.execute(
                "INSERT INTO ventas (idcliente, idempleado, total) VALUES (%s, %s, %s)",
                (idcliente, idempleado, total)
            )
            self.conn.commit()
            self.limpiar_campos()
            self.mostrar_ventas()

        except ValueError:
            QMessageBox.warning(self, "Error", "Verifica los campos numéricos.")

    def limpiar_campos(self):
        self.idcliente_input.clear()
        self.idempleado_input.clear()
        self.total_input.clear()

    def abrir_ventana_actualizar(self):
        dialogo = QDialog(self)
        dialogo.setWindowTitle("Actualizar Venta")
        layout = QFormLayout(dialogo)

        idventa_input = QLineEdit()
        idcliente_input = QLineEdit()
        idempleado_input = QLineEdit()
        total_input = QLineEdit()

        layout.addRow("ID Venta:", idventa_input)
        layout.addRow("Nuevo ID Cliente:", idcliente_input)
        layout.addRow("Nuevo ID Empleado:", idempleado_input)
        layout.addRow("Nuevo Total:", total_input)

        btn_actualizar = QPushButton("Actualizar")
        layout.addWidget(btn_actualizar)

        def actualizar():
            try:
                idventa = int(idventa_input.text())
                idcliente = int(idcliente_input.text())
                idempleado = int(idempleado_input.text())
                total = float(total_input.text())

                if total <= 0:
                    QMessageBox.warning(dialogo, "Error", "El total debe ser mayor a 0.")
                    return

                self.cursor.execute("SELECT * FROM ventas WHERE idventa = %s", (idventa,))
                if self.cursor.fetchone() is None:
                    QMessageBox.warning(dialogo, "Error", f"No existe venta con ID {idventa}")
                    return

                self.cursor.execute("SELECT * FROM clientes WHERE idcliente = %s", (idcliente,))
                if self.cursor.fetchone() is None:
                    QMessageBox.warning(dialogo, "Error", f"No existe cliente con ID {idcliente}")
                    return

                self.cursor.execute("SELECT * FROM empleados WHERE idempleado = %s", (idempleado,))
                if self.cursor.fetchone() is None:
                    QMessageBox.warning(dialogo, "Error", f"No existe empleado con ID {idempleado}")
                    return

                self.cursor.execute(
                    "UPDATE ventas SET idcliente = %s, idempleado = %s, total = %s WHERE idventa = %s",
                    (idcliente, idempleado, total, idventa)
                )
                self.conn.commit()
                self.mostrar_ventas()
                dialogo.accept()

            except ValueError:
                QMessageBox.warning(dialogo, "Error", "Datos inválidos.")

        btn_actualizar.clicked.connect(actualizar)
        dialogo.exec()

    def abrir_ventana_eliminar(self):
        dialogo = QDialog(self)
        dialogo.setWindowTitle("Eliminar Venta")
        layout = QFormLayout(dialogo)

        id_input = QLineEdit()
        layout.addRow("ID Venta a eliminar:", id_input)

        btn_eliminar = QPushButton("Eliminar")
        layout.addWidget(btn_eliminar)

        def eliminar():
            try:
                idventa = int(id_input.text())
            except ValueError:
                QMessageBox.warning(dialogo, "Error", "ID inválido.")
                return

            self.cursor.execute("SELECT * FROM ventas WHERE idventa = %s", (idventa,))
            if self.cursor.fetchone() is None:
                QMessageBox.warning(dialogo, "Error", f"No existe venta con ID {idventa}")
                return

            self.cursor.execute("DELETE FROM ventas WHERE idventa = %s", (idventa,))
            self.conn.commit()
            self.mostrar_ventas()
            dialogo.accept()

        btn_eliminar.clicked.connect(eliminar)
        dialogo.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentasCRUD()
    ventana.show()
    sys.exit(app.exec())
