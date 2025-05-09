import sys
import mysql.connector
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QTableWidget, QTableWidgetItem,
    QMessageBox, QLabel, QDialog, QFormLayout
)

class CategoriasCRUD(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CRUD Categorías - PyQt6")
        self.setGeometry(100, 100, 600, 400)

        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="MySQL",
            database="tr23270111"
        )
        self.cursor = self.conn.cursor()

        self.init_ui()
        self.mostrar_categorias()

    def init_ui(self):
        layout = QVBoxLayout()

        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("ID de categoría")
        self.nombre_input = QLineEdit()
        self.nombre_input.setPlaceholderText("Nombre de categoría")

        layout.addWidget(QLabel("ID:"))
        layout.addWidget(self.id_input)
        layout.addWidget(QLabel("Nombre:"))
        layout.addWidget(self.nombre_input)

        botones = QHBoxLayout()
        self.btn_agregar = QPushButton("Agregar")
        self.btn_actualizar = QPushButton("Actualizar")
        self.btn_eliminar = QPushButton("Eliminar")

        botones.addWidget(self.btn_agregar)
        botones.addWidget(self.btn_actualizar)
        botones.addWidget(self.btn_eliminar)
        layout.addLayout(botones)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(2)
        self.tabla.setHorizontalHeaderLabels(["ID", "Nombre"])
        layout.addWidget(self.tabla)

        self.setLayout(layout)

        self.btn_agregar.clicked.connect(self.agregar_categoria)
        self.btn_actualizar.clicked.connect(self.abrir_ventana_actualizar)
        self.btn_eliminar.clicked.connect(self.abrir_ventana_eliminar)

    def mostrar_categorias(self):
        self.cursor.execute("SELECT * FROM categorias")
        registros = self.cursor.fetchall()
        self.tabla.setRowCount(len(registros))
        for fila, datos in enumerate(registros):
            for col, dato in enumerate(datos):
                self.tabla.setItem(fila, col, QTableWidgetItem(str(dato)))

    def agregar_categoria(self):
        id_text = self.id_input.text()
        nombre = self.nombre_input.text()

        if not id_text or not nombre:
            QMessageBox.warning(self, "Error", "Completa todos los campos.")
            return

        try:
            idcat = int(id_text)
        except ValueError:
            QMessageBox.warning(self, "Error", "El ID debe ser un número.")
            return

        try:
            self.cursor.execute("INSERT INTO categorias (idcategoria, nombre) VALUES (%s, %s)", (idcat, nombre))
            self.conn.commit()
            self.id_input.clear()
            self.nombre_input.clear()
            self.mostrar_categorias()
        except mysql.connector.Error as e:
            QMessageBox.warning(self, "Error", f"No se pudo agregar: {e}")

    def abrir_ventana_actualizar(self):
        dialogo = QDialog(self)
        dialogo.setWindowTitle("Actualizar Categoría")
        layout = QFormLayout(dialogo)

        id_input = QLineEdit()
        nuevo_nombre_input = QLineEdit()

        layout.addRow("ID de categoría:", id_input)
        layout.addRow("Nuevo nombre:", nuevo_nombre_input)

        btn_actualizar = QPushButton("Actualizar")
        layout.addWidget(btn_actualizar)

        def actualizar_categoria():
            try:
                idcat = int(id_input.text())
                nuevo_nombre = nuevo_nombre_input.text()
            except ValueError:
                QMessageBox.warning(dialogo, "Error", "ID inválido.")
                return

            if not nuevo_nombre:
                QMessageBox.warning(dialogo, "Error", "El nombre no puede estar vacío.")
                return

            self.cursor.execute("SELECT * FROM categorias WHERE idcategoria = %s", (idcat,))
            if self.cursor.fetchone() is None:
                QMessageBox.warning(dialogo, "Error", f"No existe categoría con ID {idcat}.")
                return

            self.cursor.execute("UPDATE categorias SET nombre = %s WHERE idcategoria = %s", (nuevo_nombre, idcat))
            self.conn.commit()
            self.mostrar_categorias()
            dialogo.accept()

        btn_actualizar.clicked.connect(actualizar_categoria)
        dialogo.exec()

    def abrir_ventana_eliminar(self):
        dialogo = QDialog(self)
        dialogo.setWindowTitle("Eliminar Categoría")
        layout = QFormLayout(dialogo)

        id_input = QLineEdit()
        layout.addRow("ID de categoría a eliminar:", id_input)

        btn_eliminar = QPushButton("Eliminar")
        layout.addWidget(btn_eliminar)

        def eliminar_categoria():
            try:
                idcat = int(id_input.text())
            except ValueError:
                QMessageBox.warning(dialogo, "Error", "ID inválido.")
                return

            self.cursor.execute("SELECT * FROM categorias WHERE idcategoria = %s", (idcat,))
            if self.cursor.fetchone() is None:
                QMessageBox.warning(dialogo, "Error", f"No existe categoría con ID {idcat}.")
                return

            self.cursor.execute("DELETE FROM categorias WHERE idcategoria = %s", (idcat,))
            self.conn.commit()
            self.mostrar_categorias()
            dialogo.accept()

        btn_eliminar.clicked.connect(eliminar_categoria)
        dialogo.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = CategoriasCRUD()
    ventana.show()
    sys.exit(app.exec())
