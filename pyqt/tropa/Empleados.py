import sys
import mysql.connector
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QTableWidget, QTableWidgetItem,
    QMessageBox, QLabel, QDialog, QFormLayout
)


class EmpleadosCRUD(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CRUD Empleados - PyQt6")
        self.setGeometry(100, 100, 700, 450)

        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="MySQL",
            database="tr23270111"
        )
        self.cursor = self.conn.cursor()

        self.init_ui()
        self.mostrar_empleados()

    def init_ui(self):
        layout = QVBoxLayout()

        self.nombre_input = QLineEdit()
        self.nombre_input.setPlaceholderText("Nombre del empleado")

        self.cargo_input = QLineEdit()
        self.cargo_input.setPlaceholderText("Cargo")

        self.salario_input = QLineEdit()
        self.salario_input.setPlaceholderText("Salario")

        layout.addWidget(QLabel("Nombre:"))
        layout.addWidget(self.nombre_input)
        layout.addWidget(QLabel("Cargo:"))
        layout.addWidget(self.cargo_input)
        layout.addWidget(QLabel("Salario:"))
        layout.addWidget(self.salario_input)

        botones_layout = QHBoxLayout()
        self.btn_agregar = QPushButton("Agregar")
        self.btn_actualizar = QPushButton("Actualizar")
        self.btn_eliminar = QPushButton("Eliminar")

        botones_layout.addWidget(self.btn_agregar)
        botones_layout.addWidget(self.btn_actualizar)
        botones_layout.addWidget(self.btn_eliminar)
        layout.addLayout(botones_layout)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(4)
        self.tabla.setHorizontalHeaderLabels(["ID", "Nombre", "Cargo", "Salario"])
        layout.addWidget(self.tabla)

        self.btn_agregar.clicked.connect(self.agregar_empleado)
        self.btn_actualizar.clicked.connect(self.abrir_ventana_actualizar)
        self.btn_eliminar.clicked.connect(self.abrir_ventana_eliminar)

        self.setLayout(layout)

    def mostrar_empleados(self):
        self.cursor.execute("SELECT * FROM empleados")
        registros = self.cursor.fetchall()
        self.tabla.setRowCount(len(registros))

        for row_index, row_data in enumerate(registros):
            for column_index, data in enumerate(row_data):
                self.tabla.setItem(row_index, column_index, QTableWidgetItem(str(data)))

    def agregar_empleado(self):
        nombre = self.nombre_input.text()
        cargo = self.cargo_input.text()
        salario_text = self.salario_input.text()

        if not nombre:
            QMessageBox.warning(self, "Error", "El nombre es obligatorio.")
            return

        try:
            salario = float(salario_text) if salario_text else 0.00
        except ValueError:
            QMessageBox.warning(self, "Error", "Salario inválido.")
            return

        self.cursor.execute(
            "INSERT INTO empleados (nombre, cargo, salario) VALUES (%s, %s, %s)",
            (nombre, cargo, salario)
        )
        self.conn.commit()
        self.nombre_input.clear()
        self.cargo_input.clear()
        self.salario_input.clear()
        self.mostrar_empleados()

    def abrir_ventana_actualizar(self):
        dialogo = QDialog(self)
        dialogo.setWindowTitle("Actualizar Empleado")
        layout = QFormLayout(dialogo)

        id_input = QLineEdit()
        nombre_input = QLineEdit()
        cargo_input = QLineEdit()
        salario_input = QLineEdit()

        layout.addRow("ID del empleado:", id_input)
        layout.addRow("Nuevo nombre:", nombre_input)
        layout.addRow("Nuevo cargo:", cargo_input)
        layout.addRow("Nuevo salario:", salario_input)

        btn_actualizar = QPushButton("Actualizar")
        layout.addWidget(btn_actualizar)

        def actualizar_empleado():
            try:
                id_emp = int(id_input.text())
                nombre = nombre_input.text()
                cargo = cargo_input.text()
                salario = float(salario_input.text()) if salario_input.text() else 0.00
            except ValueError:
                QMessageBox.warning(dialogo, "Error", "Datos inválidos.")
                return

            self.cursor.execute("SELECT * FROM empleados WHERE idempleado = %s", (id_emp,))
            if not self.cursor.fetchone():
                QMessageBox.warning(dialogo, "Error", f"No existe empleado con ID {id_emp}.")
                return

            self.cursor.execute(
                "UPDATE empleados SET nombre = %s, cargo = %s, salario = %s WHERE idempleado = %s",
                (nombre, cargo, salario, id_emp)
            )
            self.conn.commit()
            self.mostrar_empleados()
            dialogo.accept()

        btn_actualizar.clicked.connect(actualizar_empleado)
        dialogo.exec()

    def abrir_ventana_eliminar(self):
        dialogo = QDialog(self)
        dialogo.setWindowTitle("Eliminar Empleado")
        layout = QFormLayout(dialogo)

        id_input = QLineEdit()
        layout.addRow("ID del empleado a eliminar:", id_input)

        btn_eliminar = QPushButton("Eliminar")
        layout.addWidget(btn_eliminar)

        def eliminar_empleado():
            try:
                id_emp = int(id_input.text())
            except ValueError:
                QMessageBox.warning(dialogo, "Error", "ID inválido.")
                return

            self.cursor.execute("SELECT * FROM empleados WHERE idempleado = %s", (id_emp,))
            if not self.cursor.fetchone():
                QMessageBox.warning(dialogo, "Error", f"No existe empleado con ID {id_emp}.")
                return

            self.cursor.execute("DELETE FROM empleados WHERE idempleado = %s", (id_emp,))
            self.conn.commit()
            self.mostrar_empleados()
            dialogo.accept()

        btn_eliminar.clicked.connect(eliminar_empleado)
        dialogo.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = EmpleadosCRUD()
    ventana.show()
    sys.exit(app.exec())
