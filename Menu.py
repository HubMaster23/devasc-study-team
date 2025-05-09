import sys
import mysql.connector
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QMainWindow,
    QPushButton, QLineEdit, QTableWidget, QTableWidgetItem,
    QMessageBox, QLabel, QDialog, QFormLayout, QStackedWidget, QTextEdit
)
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Gestión - PyQt6")
        self.setGeometry(100, 100, 1000, 600)
        
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="MySQL",
            database="tr23270111"
        )
        
        self.init_ui()
        
    def init_ui(self):
       
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        menu_layout = QVBoxLayout()
        menu_layout.setContentsMargins(10, 10, 10, 10)
        
        btn_categorias = QPushButton("Categorías")
        btn_clientes = QPushButton("Clientes")
        btn_productos = QPushButton("Productos")
        btn_empleados = QPushButton("Empleados")
        btn_ventas = QPushButton("Ventas")
        btn_detalle_ventas = QPushButton("Detalle Ventas")
        btn_facturas = QPushButton("Facturas")
        btn_salir = QPushButton("Salir")
        
        for btn in [btn_categorias, btn_clientes, btn_productos, 
                   btn_empleados, btn_ventas, btn_detalle_ventas, 
                   btn_facturas, btn_salir]:
            btn.setFixedHeight(40)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    font-size: 14px;
                    text-align: left;
                    padding-left: 20px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
            """)
        
        menu_layout.addWidget(btn_categorias)
        menu_layout.addWidget(btn_clientes)
        menu_layout.addWidget(btn_productos)
        menu_layout.addWidget(btn_empleados)
        menu_layout.addWidget(btn_ventas)
        menu_layout.addWidget(btn_detalle_ventas)
        menu_layout.addWidget(btn_facturas)
        menu_layout.addStretch()
        menu_layout.addWidget(btn_salir)
        
        self.stacked_widget = QStackedWidget()
        
        self.categorias_page = CategoriasCRUD(self.conn)
        self.clientes_page = ClientesCRUD(self.conn)
        self.productos_page = ProductosCRUD(self.conn)
        self.empleados_page = EmpleadosCRUD(self.conn)
        self.ventas_page = VentasCRUD(self.conn)
        self.detalle_ventas_page = DetalleVentasCRUD(self.conn)
        self.facturas_page = FacturasCRUD(self.conn)
        
        self.stacked_widget.addWidget(self.categorias_page)
        self.stacked_widget.addWidget(self.clientes_page)
        self.stacked_widget.addWidget(self.productos_page)
        self.stacked_widget.addWidget(self.empleados_page)
        self.stacked_widget.addWidget(self.ventas_page)
        self.stacked_widget.addWidget(self.detalle_ventas_page)
        self.stacked_widget.addWidget(self.facturas_page)
        
        btn_categorias.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.categorias_page))
        btn_clientes.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.clientes_page))
        btn_productos.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.productos_page))
        btn_empleados.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.empleados_page))
        btn_ventas.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.ventas_page))
        btn_detalle_ventas.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.detalle_ventas_page))
        btn_facturas.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.facturas_page))
        btn_salir.clicked.connect(self.close)
        
        main_layout.addLayout(menu_layout, 1)
        main_layout.addWidget(self.stacked_widget, 4)
        
        self.stacked_widget.setCurrentWidget(self.categorias_page)

class PlaceholderPage(QWidget):
    def __init__(self, title):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel(f"Página de {title} - En desarrollo")
        label.setStyleSheet("font-size: 24px; color: #555;")
        layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)

class CategoriasCRUD(QWidget):
    def __init__(self, conn):
        super().__init__()
        self.conn = conn
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

class ClientesCRUD(QWidget):
    def __init__(self, conn):
        super().__init__()
        self.conn = conn
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

class ProductosCRUD(QWidget):
    def __init__(self, conn):
        super().__init__()
        self.conn = conn
        self.cursor = self.conn.cursor()
        self.init_ui()
        self.mostrar_productos()

    def init_ui(self):
        layout = QVBoxLayout()

        self.nombre_input = QLineEdit()
        self.nombre_input.setPlaceholderText("Nombre del producto")
        self.precio_input = QLineEdit()
        self.precio_input.setPlaceholderText("Precio")
        self.idcategoria_input = QLineEdit()
        self.idcategoria_input.setPlaceholderText("ID Categoría")

        layout.addWidget(QLabel("Nombre:"))
        layout.addWidget(self.nombre_input)
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
        self.tabla.setColumnCount(4)
        self.tabla.setHorizontalHeaderLabels(["ID", "Nombre", "Precio", "ID Categoría"])
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
        nombre = self.nombre_input.text()
        precio_text = self.precio_input.text()
        idcategoria_text = self.idcategoria_input.text()

        if not nombre or not precio_text or not idcategoria_text:
            QMessageBox.warning(self, "Error", "Completa todos los campos.")
            return

        try:
            precio = float(precio_text)
            idcategoria = int(idcategoria_text)
        except ValueError:
            QMessageBox.warning(self, "Error", "Precio o ID Categoría inválidos.")
            return

        self.cursor.execute("SELECT * FROM categorias WHERE idcategoria = %s", (idcategoria,))
        if self.cursor.fetchone() is None:
            QMessageBox.warning(self, "Error", f"No existe categoría con ID {idcategoria}.")
            return

        try:
            self.cursor.execute(
                "INSERT INTO productos (nombre, precio, idcategoria) VALUES (%s, %s, %s)",
                (nombre, precio, idcategoria)
            )
            self.conn.commit()
            self.nombre_input.clear()
            self.precio_input.clear()
            self.idcategoria_input.clear()
            self.mostrar_productos()
        except mysql.connector.Error as e:
            QMessageBox.warning(self, "Error", f"No se pudo agregar: {e}")

    def abrir_ventana_actualizar(self):
        dialogo = QDialog(self)
        dialogo.setWindowTitle("Actualizar Producto")
        layout = QFormLayout(dialogo)

        id_input = QLineEdit()
        nombre_input = QLineEdit()
        precio_input = QLineEdit()
        idcategoria_input = QLineEdit()

        layout.addRow("ID Producto:", id_input)
        layout.addRow("Nuevo nombre:", nombre_input)
        layout.addRow("Nuevo precio:", precio_input)
        layout.addRow("Nuevo ID Categoría:", idcategoria_input)

        btn_actualizar = QPushButton("Actualizar")
        layout.addWidget(btn_actualizar)

        def actualizar_producto():
            try:
                idprod = int(id_input.text())
                nombre = nombre_input.text()
                precio = float(precio_input.text())
                idcategoria = int(idcategoria_input.text())
            except ValueError:
                QMessageBox.warning(dialogo, "Error", "Datos inválidos.")
                return

            if not nombre:
                QMessageBox.warning(dialogo, "Error", "El nombre no puede estar vacío.")
                return

            self.cursor.execute("SELECT * FROM productos WHERE idproducto = %s", (idprod,))
            if self.cursor.fetchone() is None:
                QMessageBox.warning(dialogo, "Error", f"No existe producto con ID {idprod}.")
                return

            self.cursor.execute("SELECT * FROM categorias WHERE idcategoria = %s", (idcategoria,))
            if self.cursor.fetchone() is None:
                QMessageBox.warning(dialogo, "Error", f"No existe categoría con ID {idcategoria}.")
                return

            self.cursor.execute(
                "UPDATE productos SET nombre = %s, precio = %s, idcategoria = %s WHERE idproducto = %s",
                (nombre, precio, idcategoria, idprod)
            )
            self.conn.commit()
            self.mostrar_productos()
            dialogo.accept()

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

class EmpleadosCRUD(QWidget):
    def __init__(self, conn):
        super().__init__()
        self.conn = conn
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

class VentasCRUD(QWidget):
    def __init__(self, conn):
        super().__init__()
        self.conn = conn
        self.cursor = self.conn.cursor()
        self.init_ui()
        self.mostrar_ventas()

    def init_ui(self):
        layout = QVBoxLayout()

        self.idcliente_input = QLineEdit()
        self.idcliente_input.setPlaceholderText("ID Cliente")
        self.idempleado_input = QLineEdit()
        self.idempleado_input.setPlaceholderText("ID Empleado")
        self.fecha_input = QLineEdit()
        self.fecha_input.setPlaceholderText("Fecha (YYYY-MM-DD)")
        self.total_input = QLineEdit()
        self.total_input.setPlaceholderText("Total")

        layout.addWidget(QLabel("ID Cliente:"))
        layout.addWidget(self.idcliente_input)
        layout.addWidget(QLabel("ID Empleado:"))
        layout.addWidget(self.idempleado_input)
        layout.addWidget(QLabel("Fecha:"))
        layout.addWidget(self.fecha_input)
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
        self.tabla.setHorizontalHeaderLabels(["ID", "ID Cliente", "ID Empleado", "Fecha", "Total"])
        layout.addWidget(self.tabla)

        self.setLayout(layout)

        self.btn_agregar.clicked.connect(self.agregar_venta)
        self.btn_actualizar.clicked.connect(self.abrir_ventana_actualizar)
        self.btn_eliminar.clicked.connect(self.abrir_ventana_eliminar)

    def mostrar_ventas(self):
        self.cursor.execute("SELECT * FROM ventas")
        registros = self.cursor.fetchall()
        self.tabla.setRowCount(len(registros))
        for fila, datos in enumerate(registros):
            for col, dato in enumerate(datos):
                self.tabla.setItem(fila, col, QTableWidgetItem(str(dato)))

    def agregar_venta(self):
        idcliente_text = self.idcliente_input.text()
        idempleado_text = self.idempleado_input.text()
        fecha = self.fecha_input.text()
        total_text = self.total_input.text()

        if not all([idcliente_text, idempleado_text, fecha, total_text]):
            QMessageBox.warning(self, "Error", "Completa todos los campos.")
            return

        try:
            idcliente = int(idcliente_text)
            idempleado = int(idempleado_text)
            total = float(total_text)
        except ValueError:
            QMessageBox.warning(self, "Error", "Datos inválidos.")
            return

        self.cursor.execute("SELECT * FROM clientes WHERE idcliente = %s", (idcliente,))
        if self.cursor.fetchone() is None:
            QMessageBox.warning(self, "Error", f"No existe cliente con ID {idcliente}.")
            return

        self.cursor.execute("SELECT * FROM empleados WHERE idempleado = %s", (idempleado,))
        if self.cursor.fetchone() is None:
            QMessageBox.warning(self, "Error", f"No existe empleado con ID {idempleado}.")
            return

        try:
            self.cursor.execute(
                "INSERT INTO ventas (idcliente, idempleado, fecha, total) VALUES (%s, %s, %s, %s)",
                (idcliente, idempleado, fecha, total)
            )
            self.conn.commit()
            self.idcliente_input.clear()
            self.idempleado_input.clear()
            self.fecha_input.clear()
            self.total_input.clear()
            self.mostrar_ventas()
        except mysql.connector.Error as e:
            QMessageBox.warning(self, "Error", f"No se pudo agregar: {e}")

    def abrir_ventana_actualizar(self):
        dialogo = QDialog(self)
        dialogo.setWindowTitle("Actualizar Venta")
        layout = QFormLayout(dialogo)

        id_input = QLineEdit()
        idcliente_input = QLineEdit()
        idempleado_input = QLineEdit()
        fecha_input = QLineEdit()
        total_input = QLineEdit()

        layout.addRow("ID Venta:", id_input)
        layout.addRow("Nuevo ID Cliente:", idcliente_input)
        layout.addRow("Nuevo ID Empleado:", idempleado_input)
        layout.addRow("Nueva Fecha:", fecha_input)
        layout.addRow("Nuevo Total:", total_input)

        btn_actualizar = QPushButton("Actualizar")
        layout.addWidget(btn_actualizar)

        def actualizar_venta():
            try:
                idventa = int(id_input.text())
                idcliente = int(idcliente_input.text())
                idempleado = int(idempleado_input.text())
                fecha = fecha_input.text()
                total = float(total_input.text())
            except ValueError:
                QMessageBox.warning(dialogo, "Error", "Datos inválidos.")
                return

            if not all([idcliente, idempleado, fecha, total]):
                QMessageBox.warning(dialogo, "Error", "Completa todos los campos.")
                return

            self.cursor.execute("SELECT * FROM ventas WHERE idventa = %s", (idventa,))
            if self.cursor.fetchone() is None:
                QMessageBox.warning(dialogo, "Error", f"No existe venta con ID {idventa}.")
                return

            self.cursor.execute("SELECT * FROM clientes WHERE idcliente = %s", (idcliente,))
            if self.cursor.fetchone() is None:
                QMessageBox.warning(dialogo, "Error", f"No existe cliente con ID {idcliente}.")
                return

            self.cursor.execute("SELECT * FROM empleados WHERE idempleado = %s", (idempleado,))
            if self.cursor.fetchone() is None:
                QMessageBox.warning(dialogo, "Error", f"No existe empleado con ID {idempleado}.")
                return

            self.cursor.execute(
                "UPDATE ventas SET idcliente = %s, idempleado = %s, fecha = %s, total = %s WHERE idventa = %s",
                (idcliente, idempleado, fecha, total, idventa)
            )
            self.conn.commit()
            self.mostrar_ventas()
            dialogo.accept()

        btn_actualizar.clicked.connect(actualizar_venta)
        dialogo.exec()

    def abrir_ventana_eliminar(self):
        dialogo = QDialog(self)
        dialogo.setWindowTitle("Eliminar Venta")
        layout = QFormLayout(dialogo)

        id_input = QLineEdit()
        layout.addRow("ID de la venta a eliminar:", id_input)

        btn_eliminar = QPushButton("Eliminar")
        layout.addWidget(btn_eliminar)

        def eliminar_venta():
            try:
                idventa = int(id_input.text())
            except ValueError:
                QMessageBox.warning(dialogo, "Error", "ID inválido.")
                return

            self.cursor.execute("SELECT * FROM ventas WHERE idventa = %s", (idventa,))
            if self.cursor.fetchone() is None:
                QMessageBox.warning(dialogo, "Error", f"No existe venta con ID {idventa}.")
                return

            self.cursor.execute("DELETE FROM ventas WHERE idventa = %s", (idventa,))
            self.conn.commit()
            self.mostrar_ventas()
            dialogo.accept()

        btn_eliminar.clicked.connect(eliminar_venta)
        dialogo.exec()

class DetalleVentasCRUD(QWidget):
    def __init__(self, conn):
        super().__init__()
        self.conn = conn
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

class FacturasCRUD(QWidget):
    def __init__(self, conn):
        super().__init__()
        self.conn = conn
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

class ProductosCRUD(QWidget):
    def __init__(self, conn):
        super().__init__()
        self.conn = conn
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
        self.descripcion_input.setMaximumHeight(100)

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

            if precio <= 0:
                QMessageBox.warning(self, "Error", "El precio debe ser positivo.")
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
        descripcion_input.setMaximumHeight(100)
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

                if precio <= 0:
                    QMessageBox.warning(dialogo, "Error", "El precio debe ser positivo.")
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
        
class VentasCRUD(QWidget):
    def __init__(self, conn):
        super().__init__()
        self.conn = conn
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
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Error", f"Error al insertar: {e}")

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
    
    app.setStyleSheet("""
        QMainWindow {
            background-color: #dd8435;
        }
        QTableWidget {
            background-color: #d4ac0d;
            border: 1px solid #ddd;
        }
        QLineEdit {
            padding: 5px;
            border: 1px solid #ddd;
            border-radius: 3px;
        }
    """)
    
    ventana = MainWindow()
    ventana.show()
    sys.exit(app.exec())