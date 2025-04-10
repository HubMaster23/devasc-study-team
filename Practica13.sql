DROP DATABASE IF EXISTS tr23270111;
CREATE DATABASE tr23270111;
USE tr23270111;

CREATE TABLE clientes(idcliente INT AUTO_INCREMENT PRIMARY KEY, nombre VARCHAR(100) NOT NULL);

CREATE TABLE empleados(idempleado INT AUTO_INCREMENT PRIMARY KEY, nombre VARCHAR(100) NOT NULL, cargo VARCHAR(50), salario DECIMAL(10,2));

CREATE TABLE categorias(idcategoria INT PRIMARY KEY, nombre VARCHAR(50) NOT NULL);

CREATE TABLE productos(idproducto INT PRIMARY KEY,nombre VARCHAR(100) NOT NULL, descripcion TEXT, precio DECIMAL(10,2) NOT NULL, idcategoria INT,
CONSTRAINT asigna FOREIGN KEY (idcategoria) REFERENCES categorias(idcategoria));

CREATE TABLE inventario(idinventario INT PRIMARY KEY, idproducto INT, cantidad INT NOT NULL, fechaact TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
CONSTRAINT establecen FOREIGN KEY (idproducto) REFERENCES productos(idproducto));

CREATE TABLE ventas(idventa INT AUTO_INCREMENT PRIMARY KEY, idcliente INT, idempleado INT, fechaventa DATETIME DEFAULT CURRENT_TIMESTAMP, total DECIMAL(10,2) NOT NULL,
CONSTRAINT concede FOREIGN KEY (idcliente) REFERENCES clientes(idcliente),
CONSTRAINT coloca FOREIGN KEY (idempleado) REFERENCES empleados(idempleado));

CREATE TABLE detalleventas(iddetalle INT AUTO_INCREMENT PRIMARY KEY, idventa INT, idproducto INT, cantidad INT NOT NULL, subtotal DECIMAL(10,2) NOT NULL,
CONSTRAINT corresponde FOREIGN KEY (idventa) REFERENCES ventas(idventa),
CONSTRAINT disigna FOREIGN KEY (idproducto) REFERENCES productos(idproducto));

CREATE TABLE facturas(idfactura INT PRIMARY KEY,idventa INT, fechaemision DATETIME DEFAULT CURRENT_TIMESTAMP, total DECIMAL(10,2) NOT NULL,
CONSTRAINT fija FOREIGN KEY (idventa) REFERENCES ventas(idventa));
