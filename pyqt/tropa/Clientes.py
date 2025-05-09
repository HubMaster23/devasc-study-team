import sys
import mysql.connector
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QTableWidget, QTableWidgetItem,
    QMessageBox, QLabel, QDialog, QFormLayout
)

class ClienteCRUD(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CRUD Clientes - PyQt6")
        self.setGeometry(100, 100, 600, 400)

        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="MySQL",
            database="tr23270111"
        )
        self.cursor = self.conn.cursor()

        self.init_ui()
        self.mostrar_clientes()

    def init_ui(self):
        layout = QVBoxLayout()

        self.nombre_input = QLineEdit()
        self.nombre_input.setPlaceholderText("Nombre del cliente")
        layout.addWidget(QLabel("Nombre del nuevo cliente:"))
        layout.addWidget(self.nombre_input)

        botones_layout = QHBoxLayout()
        self.btn_agregar = QPushButton("Agregar")
        self.btn_actualizar = QPushButton("Actualizar")
        self.btn_eliminar = QPushButton("Eliminar")

        botones_layout.addWidget(self.btn_agregar)
        botones_layout.addWidget(self.btn_actualizar)
        botones_layout.addWidget(self.btn_eliminar)
        layout.addLayout(botones_layout)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(2)
        self.tabla.setHorizontalHeaderLabels(["ID", "Nombre"])
        layout.addWidget(self.tabla)

        self.btn_agregar.clicked.connect(self.agregar_cliente)
        self.btn_actualizar.clicked.connect(self.abrir_ventana_actualizar)
        self.btn_eliminar.clicked.connect(self.abrir_ventana_eliminar)

        self.setLayout(layout)

    def mostrar_clientes(self):
        self.cursor.execute("SELECT * FROM clientes")
        registros = self.cursor.fetchall()
        self.tabla.setRowCount(len(registros))

        for row_index, row_data in enumerate(registros):
            for column_index, data in enumerate(row_data):
                self.tabla.setItem(row_index, column_index, QTableWidgetItem(str(data)))

    def agregar_cliente(self):
        nombre = self.nombre_input.text()
        if nombre:
            self.cursor.execute("INSERT INTO clientes (nombre) VALUES (%s)", (nombre,))
            self.conn.commit()
            self.nombre_input.clear()
            self.mostrar_clientes()
        else:
            QMessageBox.warning(self, "Error", "El campo nombre no puede estar vacío.")

    def abrir_ventana_actualizar(self):
        dialogo = QDialog(self)
        dialogo.setWindowTitle("Actualizar Cliente")
        layout = QFormLayout(dialogo)

        id_input = QLineEdit()
        nombre_input = QLineEdit()

        layout.addRow("ID del cliente:", id_input)
        layout.addRow("Nuevo nombre:", nombre_input)

        btn_actualizar = QPushButton("Actualizar")
        layout.addWidget(btn_actualizar)

        def realizar_actualizacion():
            id_text = id_input.text()
            nuevo_nombre = nombre_input.text()

            if not id_text or not nuevo_nombre:
                QMessageBox.warning(dialogo, "Error", "Completa todos los campos.")
                return

            try:
                id_cliente = int(id_text)
            except ValueError:
                QMessageBox.warning(dialogo, "Error", "El ID debe ser un número.")
                return

            self.cursor.execute("SELECT * FROM clientes WHERE idcliente = %s", (id_cliente,))
            if self.cursor.fetchone() is None:
                QMessageBox.warning(dialogo, "Error", f"No existe cliente con ID {id_cliente}.")
                return

            self.cursor.execute("UPDATE clientes SET nombre = %s WHERE idcliente = %s", (nuevo_nombre, id_cliente))
            self.conn.commit()
            self.mostrar_clientes()
            dialogo.accept()

        btn_actualizar.clicked.connect(realizar_actualizacion)
        dialogo.exec()

    def abrir_ventana_eliminar(self):
        dialogo = QDialog(self)
        dialogo.setWindowTitle("Eliminar Cliente")
        layout = QFormLayout(dialogo)

        id_input = QLineEdit()
        layout.addRow("ID del cliente a eliminar:", id_input)

        btn_eliminar = QPushButton("Eliminar")
        layout.addWidget(btn_eliminar)

        def realizar_eliminacion():
            id_text = id_input.text()

            if not id_text:
                QMessageBox.warning(dialogo, "Error", "Ingresa el ID.")
                return

            try:
                id_cliente = int(id_text)
            except ValueError:
                QMessageBox.warning(dialogo, "Error", "El ID debe ser un número.")
                return

            self.cursor.execute("SELECT * FROM clientes WHERE idcliente = %s", (id_cliente,))
            if self.cursor.fetchone() is None:
                QMessageBox.warning(dialogo, "Error", f"No existe cliente con ID {id_cliente}.")
                return

            self.cursor.execute("DELETE FROM clientes WHERE idcliente = %s", (id_cliente,))
            self.conn.commit()
            self.mostrar_clientes()
            dialogo.accept()

        btn_eliminar.clicked.connect(realizar_eliminacion)
        dialogo.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = ClienteCRUD()
    ventana.show()
    sys.exit(app.exec())
