import sys
import mysql.connector
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QTableWidget, QTableWidgetItem,
    QMessageBox, QLabel, QDialog, QFormLayout
)


class InventarioCRUD(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CRUD Inventario - PyQt6")
        self.setGeometry(100, 100, 700, 400)

        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="MySQL",
            database="tr23270111"
        )
        self.cursor = self.conn.cursor()

        self.init_ui()
        self.mostrar_inventario()

    def init_ui(self):
        layout = QVBoxLayout()

        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("ID Inventario")

        self.idproducto_input = QLineEdit()
        self.idproducto_input.setPlaceholderText("ID Producto")

        self.cantidad_input = QLineEdit()
        self.cantidad_input.setPlaceholderText("Cantidad")

        layout.addWidget(QLabel("ID Inventario:"))
        layout.addWidget(self.id_input)
        layout.addWidget(QLabel("ID Producto:"))
        layout.addWidget(self.idproducto_input)
        layout.addWidget(QLabel("Cantidad:"))
        layout.addWidget(self.cantidad_input)

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
        self.tabla.setHorizontalHeaderLabels(["ID Inventario", "ID Producto", "Cantidad", "Fecha Actualización"])
        layout.addWidget(self.tabla)

        self.setLayout(layout)

        self.btn_agregar.clicked.connect(self.agregar_inventario)
        self.btn_actualizar.clicked.connect(self.abrir_ventana_actualizar)
        self.btn_eliminar.clicked.connect(self.abrir_ventana_eliminar)

    def mostrar_inventario(self):
        self.cursor.execute("SELECT * FROM inventario")
        registros = self.cursor.fetchall()
        self.tabla.setRowCount(len(registros))
        for fila, datos in enumerate(registros):
            for col, dato in enumerate(datos):
                self.tabla.setItem(fila, col, QTableWidgetItem(str(dato)))

    def agregar_inventario(self):
        try:
            idinv = int(self.id_input.text())
            idprod = int(self.idproducto_input.text())
            cantidad = int(self.cantidad_input.text())

            if cantidad < 0:
                QMessageBox.warning(self, "Error", "La cantidad no puede ser negativa.")
                return

            self.cursor.execute("SELECT * FROM productos WHERE idproducto = %s", (idprod,))
            if self.cursor.fetchone() is None:
                QMessageBox.warning(self, "Error", f"No existe producto con ID {idprod}.")
                return

            self.cursor.execute(
                "INSERT INTO inventario (idinventario, idproducto, cantidad) VALUES (%s, %s, %s)",
                (idinv, idprod, cantidad)
            )
            self.conn.commit()
            self.limpiar_campos()
            self.mostrar_inventario()

        except ValueError:
            QMessageBox.warning(self, "Error", "Datos inválidos.")
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Error", f"Error al insertar: {e}")

    def limpiar_campos(self):
        self.id_input.clear()
        self.idproducto_input.clear()
        self.cantidad_input.clear()

    def abrir_ventana_actualizar(self):
        dialogo = QDialog(self)
        dialogo.setWindowTitle("Actualizar Cantidad")
        layout = QFormLayout(dialogo)

        id_input = QLineEdit()
        nueva_cantidad_input = QLineEdit()

        layout.addRow("ID Inventario:", id_input)
        layout.addRow("Nueva cantidad:", nueva_cantidad_input)

        btn_actualizar = QPushButton("Actualizar")
        layout.addWidget(btn_actualizar)

        def actualizar():
            try:
                idinv = int(id_input.text())
                nueva_cantidad = int(nueva_cantidad_input.text())
                if nueva_cantidad < 0:
                    QMessageBox.warning(dialogo, "Error", "La cantidad no puede ser negativa.")
                    return

                self.cursor.execute("SELECT * FROM inventario WHERE idinventario = %s", (idinv,))
                if self.cursor.fetchone() is None:
                    QMessageBox.warning(dialogo, "Error", f"No existe inventario con ID {idinv}.")
                    return

                self.cursor.execute(
                    "UPDATE inventario SET cantidad = %s WHERE idinventario = %s",
                    (nueva_cantidad, idinv)
                )
                self.conn.commit()
                self.mostrar_inventario()
                dialogo.accept()

            except ValueError:
                QMessageBox.warning(dialogo, "Error", "Datos inválidos.")

        btn_actualizar.clicked.connect(actualizar)
        dialogo.exec()

    def abrir_ventana_eliminar(self):
        dialogo = QDialog(self)
        dialogo.setWindowTitle("Eliminar Inventario")
        layout = QFormLayout(dialogo)

        id_input = QLineEdit()
        layout.addRow("ID Inventario a eliminar:", id_input)

        btn_eliminar = QPushButton("Eliminar")
        layout.addWidget(btn_eliminar)

        def eliminar():
            try:
                idinv = int(id_input.text())
            except ValueError:
                QMessageBox.warning(dialogo, "Error", "ID inválido.")
                return

            self.cursor.execute("SELECT * FROM inventario WHERE idinventario = %s", (idinv,))
            if self.cursor.fetchone() is None:
                QMessageBox.warning(dialogo, "Error", f"No existe inventario con ID {idinv}.")
                return

            self.cursor.execute("DELETE FROM inventario WHERE idinventario = %s", (idinv,))
            self.conn.commit()
            self.mostrar_inventario()
            dialogo.accept()

        btn_eliminar.clicked.connect(eliminar)
        dialogo.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = InventarioCRUD()
    ventana.show()
    sys.exit(app.exec())
