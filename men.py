import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QPushButton, QDialog, QFormLayout, QLineEdit, QMessageBox
from categorias import Categorias
from clientes import Clientes
from productos import Productos
from ventas import Ventas
from empleados import Empleados
from facturas import Facturas
from detallesventas import DetallesVentas

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Ventas")
        self.setGeometry(100, 100, 800, 600)
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        
        self.layout = QVBoxLayout(self.central_widget)
        self.tableWidget = QTableWidget(self)
        self.layout.addWidget(self.tableWidget)

        self.initUI()

    def initUI(self):
        # Crear botones de navegación
        self.btn_ventas = QPushButton("Ventas", self)
        self.btn_ventas.clicked.connect(self.mostrar_ventas)
        self.layout.addWidget(self.btn_ventas)

        self.btn_clientes = QPushButton("Clientes", self)
        self.btn_clientes.clicked.connect(self.mostrar_clientes)
        self.layout.addWidget(self.btn_clientes)

        self.btn_productos = QPushButton("Productos", self)
        self.btn_productos.clicked.connect(self.mostrar_productos)
        self.layout.addWidget(self.btn_productos)

        self.btn_empleados = QPushButton("Empleados", self)
        self.btn_empleados.clicked.connect(self.mostrar_empleados)
        self.layout.addWidget(self.btn_empleados)

        self.btn_facturas = QPushButton("Facturas", self)
        self.btn_facturas.clicked.connect(self.mostrar_facturas)
        self.layout.addWidget(self.btn_facturas)

        self.btn_categorias = QPushButton("Categorias", self)
        self.btn_categorias.clicked.connect(self.mostrar_categorias)
        self.layout.addWidget(self.btn_categorias)
        
        self.btn_detalles = QPushButton("Detalles de ventas", self)
        self.btn_detalles.clicked.connect(self.mostrar_detalles)
        self.layout.addWidget(self.btn_detalles)
        
    def mostrar_ventas(self):
        ventas = Ventas(self)
        ventas.mostrar_ventas()

    def mostrar_clientes(self):
        clientes = Clientes(self)
        clientes.mostrar_clientes()

    def mostrar_productos(self):
        productos = Productos(self)
        productos.mostrar_productos()

    def mostrar_empleados(self):
        empleados = Empleados(self)
        empleados.mostrar_empleados()

    def mostrar_facturas(self):
        facturas = Facturas(self)
        facturas.mostrar_facturas()
        
    def mostrar_categorias(self):
       ventas = Categorias(self)
       ventas.mostrar_categorias()
       
    def mostrar_detalles(self):
       ventas = DetallesVentas(self)
       ventas.mostrar_detalles_ventas()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = MainWindow()
    ventana.show()
    sys.exit(app.exec())
