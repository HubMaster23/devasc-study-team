INSERT INTO clientes (nombre) VALUES
('Juan Pérez'),
('Ana Gómez'),
('Carlos Díaz'),
('María Rodríguez'),
('Pedro Martínez'),
('Laura Fernández'),
('José López'),
('Marta Sánchez'),
('Luis García'),
('Isabel Torres');

INSERT INTO empleados (nombre, cargo, salario) VALUES
('Carlos Ruiz', 'Vendedor', 1500.00),
('Sofía Méndez', 'Supervisor', 2500.00),
('Gabriel Fernández', 'Gerente', 4000.00),
('Lucía Díaz', 'Vendedor', 1400.00),
('Ricardo Martínez', 'Recepcionista', 1200.00),
('Ana Pérez', 'Cajero', 1300.00),
('Oscar Gómez', 'Vendedor', 1600.00),
('Pedro Sánchez', 'Supervisor', 2200.00),
('Elena Torres', 'Cajero', 1100.00),
('David Herrera', 'Gerente', 3500.00);

INSERT INTO categorias (idcategoria, nombre) VALUES
(1, 'Electrónica'),
(2, 'Ropa'),
(3, 'Muebles'),
(4, 'Juguetes'),
(5, 'Alimentos'),
(6, 'Hogar'),
(7, 'Libros'),
(8, 'Deportes'),
(9, 'Belleza'),
(10, 'Automotriz');

INSERT INTO productos (idproducto, nombre, descripcion, precio, idcategoria) VALUES
(1, 'Televisor', 'Televisor 40" LED', 350.00, 1),
(2, 'Camiseta', 'Camiseta de algodón', 15.00, 2),
(3, 'Sofa', 'Sofa de 3 plazas', 450.00, 3),
(4, 'Muñeca', 'Muñeca de peluche', 25.00, 4),
(5, 'Galletas', 'Galletas de chocolate', 3.50, 5),
(6, 'Lámpara', 'Lámpara de escritorio', 30.00, 6),
(7, 'Libro', 'Libro de fantasía', 12.00, 7),
(8, 'Pelota', 'Pelota de fútbol', 10.00, 8),
(9, 'Shampoo', 'Shampoo de 500ml', 7.50, 9),
(10, 'Aceite motor', 'Aceite para motor 5L', 40.00, 10);

INSERT INTO ventas (idcliente, idempleado, total) VALUES
(1, 1, 700.00),
(2, 2, 2500.00),
(3, 3, 1500.00),
(4, 4, 450.00),
(5, 5, 100.00),
(6, 6, 1000.00),
(7, 7, 75.00),
(8, 8, 30.00),
(9, 9, 80.00),
(10, 10, 500.00);

INSERT INTO detalleventas (idventa, idproducto, cantidad, subtotal) VALUES
(1, 1, 2, 700.00),
(2, 2, 1, 15.00),
(3, 3, 1, 450.00),
(4, 4, 1, 25.00),
(5, 5, 2, 7.00),
(6, 6, 1, 30.00),
(7, 7, 1, 12.00),
(8, 8, 3, 30.00),
(9, 9, 1, 7.50),
(10, 10, 2, 80.00);

INSERT INTO facturas (idventa, total) VALUES
(1, 700.00),
(2, 2500.00),
(3, 1500.00),
(4, 450.00),
(5, 100.00),
(6, 1000.00),
(7, 75.00),
(8, 30.00),
(9, 80.00),
(10, 500.00);