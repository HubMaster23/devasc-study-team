import sys
import mysql.connector
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QTableWidget, QTableWidgetItem,
    QMessageBox, QLabel, QDialog, QFormLayout, QTextEdit
)


class ProductosCRUD(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CRUD Productos - PyQt6")
        self.setGeometry(100, 100, 800, 500)

        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="MySQL",
            database="tr23270111"
        )
        self.cursor = self.conn.cursor()

        self.init_ui()
        self.mostrar_productos()

    def init_ui(self):
        layout = QVBoxLayout()

        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("ID del producto")

        self.nombre_input = QLineEdit()
        self.nombre_input.setPlaceholderText("Nombre del producto")

        self.descripcion_input = QTextEdit()
        self.descripcion_input.setPlaceholderText("Descripción")

        self.precio_input = QLineEdit()
        self.precio_input.setPlaceholderText("Precio")

        self.idcategoria_input = QLineEdit()
        self.idcategoria_input.setPlaceholderText("ID Categoría")

        layout.addWidget(QLabel("ID:"))
        layout.addWidget(self.id_input)
        layout.addWidget(QLabel("Nombre:"))
        layout.addWidget(self.nombre_input)
        layout.addWidget(QLabel("Descripción:"))
        layout.addWidget(self.descripcion_input)
        layout.addWidget(QLabel("Precio:"))
        layout.addWidget(self.precio_input)
        layout.addWidget(QLabel("ID Categoría:"))
        layout.addWidget(self.idcategoria_input)

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
        self.tabla.setHorizontalHeaderLabels(["ID", "Nombre", "Descripción", "Precio", "ID Categoría"])
        layout.addWidget(self.tabla)

        self.setLayout(layout)

        self.btn_agregar.clicked.connect(self.agregar_producto)
        self.btn_actualizar.clicked.connect(self.abrir_ventana_actualizar)
        self.btn_eliminar.clicked.connect(self.abrir_ventana_eliminar)

    def mostrar_productos(self):
        self.cursor.execute("SELECT * FROM productos")
        registros = self.cursor.fetchall()
        self.tabla.setRowCount(len(registros))
        for fila, datos in enumerate(registros):
            for col, dato in enumerate(datos):
                self.tabla.setItem(fila, col, QTableWidgetItem(str(dato)))

    def agregar_producto(self):
        try:
            idprod = int(self.id_input.text())
            nombre = self.nombre_input.text()
            descripcion = self.descripcion_input.toPlainText()
            precio = float(self.precio_input.text())
            idcategoria = int(self.idcategoria_input.text())

            if not nombre:
                QMessageBox.warning(self, "Error", "El nombre es obligatorio.")
                return

            self.cursor.execute("SELECT * FROM categorias WHERE idcategoria = %s", (idcategoria,))
            if self.cursor.fetchone() is None:
                QMessageBox.warning(self, "Error", f"La categoría con ID {idcategoria} no existe.")
                return

            self.cursor.execute("""
                INSERT INTO productos (idproducto, nombre, descripcion, precio, idcategoria)
                VALUES (%s, %s, %s, %s, %s)
            """, (idprod, nombre, descripcion, precio, idcategoria))
            self.conn.commit()
            self.limpiar_campos()
            self.mostrar_productos()

        except ValueError:
            QMessageBox.warning(self, "Error", "Datos numéricos inválidos.")
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Error", f"Error al insertar: {e}")

    def limpiar_campos(self):
        self.id_input.clear()
        self.nombre_input.clear()
        self.descripcion_input.clear()
        self.precio_input.clear()
        self.idcategoria_input.clear()

    def abrir_ventana_actualizar(self):
        dialogo = QDialog(self)
        dialogo.setWindowTitle("Actualizar Producto")
        layout = QFormLayout(dialogo)

        id_input = QLineEdit()
        nombre_input = QLineEdit()
        descripcion_input = QTextEdit()
        precio_input = QLineEdit()
        idcat_input = QLineEdit()

        layout.addRow("ID del producto:", id_input)
        layout.addRow("Nuevo nombre:", nombre_input)
        layout.addRow("Nueva descripción:", descripcion_input)
        layout.addRow("Nuevo precio:", precio_input)
        layout.addRow("Nuevo ID categoría:", idcat_input)

        btn_actualizar = QPushButton("Actualizar")
        layout.addWidget(btn_actualizar)

        def actualizar_producto():
            try:
                idprod = int(id_input.text())
                nombre = nombre_input.text()
                descripcion = descripcion_input.toPlainText()
                precio = float(precio_input.text())
                idcat = int(idcat_input.text())

                if not nombre:
                    QMessageBox.warning(dialogo, "Error", "El nombre no puede estar vacío.")
                    return

                self.cursor.execute("SELECT * FROM productos WHERE idproducto = %s", (idprod,))
                if self.cursor.fetchone() is None:
                    QMessageBox.warning(dialogo, "Error", f"No existe producto con ID {idprod}.")
                    return

                self.cursor.execute("SELECT * FROM categorias WHERE idcategoria = %s", (idcat,))
                if self.cursor.fetchone() is None:
                    QMessageBox.warning(dialogo, "Error", f"No existe categoría con ID {idcat}.")
                    return

                self.cursor.execute("""
                    UPDATE productos SET nombre = %s, descripcion = %s,
                    precio = %s, idcategoria = %s WHERE idproducto = %s
                """, (nombre, descripcion, precio, idcat, idprod))
                self.conn.commit()
                self.mostrar_productos()
                dialogo.accept()

            except ValueError:
                QMessageBox.warning(dialogo, "Error", "Datos numéricos inválidos.")

        btn_actualizar.clicked.connect(actualizar_producto)
        dialogo.exec()

    def abrir_ventana_eliminar(self):
        dialogo = QDialog(self)
        dialogo.setWindowTitle("Eliminar Producto")
        layout = QFormLayout(dialogo)

        id_input = QLineEdit()
        layout.addRow("ID del producto a eliminar:", id_input)

        btn_eliminar = QPushButton("Eliminar")
        layout.addWidget(btn_eliminar)

        def eliminar_producto():
            try:
                idprod = int(id_input.text())
            except ValueError:
                QMessageBox.warning(dialogo, "Error", "ID inválido.")
                return

            self.cursor.execute("SELECT * FROM productos WHERE idproducto = %s", (idprod,))
            if self.cursor.fetchone() is None:
                QMessageBox.warning(dialogo, "Error", f"No existe producto con ID {idprod}.")
                return

            self.cursor.execute("DELETE FROM productos WHERE idproducto = %s", (idprod,))
            self.conn.commit()
            self.mostrar_productos()
            dialogo.accept()

        btn_eliminar.clicked.connect(eliminar_producto)
        dialogo.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = ProductosCRUD()
    ventana.show()
    sys.exit(app.exec())
