INSERT INTO clientes (nombre) VALUES
('Andrea Martinez'),
('Carlos Gomez'),
('Lucia Torres'),
('Juan Perez'),
('Martha Lopez');

INSERT INTO empleados (nombre, cargo, salario) VALUES
('Sandra Ruiz', 'Vendedora', 8500.00),
('Luis Herrera', 'Cajero', 7800.00),
('Pedro Sanchez', 'Gerente', 12000.00),
('Ana Morales', 'Vendedora', 8200.00),
('Jose Ramirez', 'Cajero', 9500.00);

INSERT INTO categorias (idcategoria, nombre) VALUES
(1, 'Camisetas'),
(2, 'Pantalones'),
(3, 'Sudaderas'),
(4, 'Accesorios'),
(5, 'Zapatos');

INSERT INTO productos (idproducto, nombre, descripcion, precio, idcategoria) VALUES
(1, 'Camiseta Blanca', 'Camiseta de algodon unisex', 149.99, 1),
(2, 'Jeans Azul', 'Jeans entallado azul oscuro', 399.00, 2),
(3, 'Sudadera Negra', 'Sudadera con capucha oversize', 499.50, 3),
(4, 'Gorra Roja', 'Gorra deportiva ajustable', 129.00, 4),
(5, 'Tenis Deportivos', 'Zapatos deportivos para correr', 699.00, 5);

INSERT INTO ventas (idcliente, idempleado, total) VALUES
(1, 2, 649.49),
(2, 2, 129.00),
(3, 5, 399.00),
(4, 2, 499.50),
(5, 5, 848.99);

INSERT INTO detalleventas (idventa, idproducto, cantidad, subtotal) VALUES
(1, 1, 1, 149.99),
(1, 2, 1, 399.00),
(1, 4, 1, 129.00),
(2, 4, 1, 129.00),
(3, 2, 1, 399.00);

INSERT INTO facturas (idventa, total) VALUES
(1, 649.49),
(2, 129.00),
(3, 399.00),
(4, 499.50),
(5, 848.99);
