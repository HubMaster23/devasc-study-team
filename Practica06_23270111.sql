#Autor:Andrik Abilio Jonapá Méndez
#Practica06-Rubricas
DROP DATABASE IF EXISTS dbtaller;
CREATE DATABASE dbtaller;
USE dbtaller;

CREATE TABLE lineainv(clavein CHAR(10) PRIMARY KEY, nombre VARCHAR(250));

CREATE TABLE profesor(idprofesor INT AUTO_INCREMENT PRIMARY KEY, nombreProf VARCHAR(200));

CREATE TABLE tipoproyecto(tipo CHAR(10) PRIMARY KEY, nombre VARCHAR(150));

CREATE TABLE proyecto(clave CHAR(10) PRIMARY KEY, nombre VARCHAR(250), clavein CHAR(10), tipo CHAR(10),
CONSTRAINT corresponde FOREIGN KEY (clavein) REFERENCES lineainv(clavein),
CONSTRAINT asignado FOREIGN KEY (tipo) REFERENCES tipoproyecto(tipo));

CREATE TABLE alumno(nocontrol CHAR(10) PRIMARY KEY, nombre VARCHAR(150), clave CHAR(10),
CONSTRAINT elige FOREIGN KEY (clave) REFERENCES proyecto(clave));

CREATE TABLE profesorproy(idprofesor INT, clave CHAR(10), calificacion FLOAT, rol VARCHAR(45),
CONSTRAINT asesora FOREIGN KEY (idprofesor) REFERENCES profesor(idprofesor),
CONSTRAINT asigna FOREIGN KEY (clave) REFERENCES proyecto(clave));

CREATE TABLE datos(clave CHAR(8), proyecto VARCHAR(150), linea CHAR(10), tipo CHAR(5), nocontrol CHAR(10), nombre_alumno VARCHAR(150), nombreProf VARCHAR(150), revisor1 VARCHAR(150), revisor2 VARCHAR(150));

CREATE TABLE perfil(idperfil INT AUTO_INCREMENT PRIMARY KEY, nombre VARCHAR(40));

CREATE TABLE objetos(idobjeto INT AUTO_INCREMENT PRIMARY KEY, nombre VARCHAR(40));

CREATE TABLE objeto_privilegio(idperfil INT, idobjeto INT,
PRIMARY KEY (idperfil, idobjeto),
CONSTRAINT establece FOREIGN KEY (idperfil) REFERENCES perfil(idperfil),
CONSTRAINT designa FOREIGN KEY (idobjeto) REFERENCES objetos(idobjeto));

INSERT INTO lineainv VALUES
("RCISP", "Robotica, Control Inteligente Y Sistemas de Percepcion"),
("TDWM", "Tecnologias de Desarrollo Web y Móvil"),
("DSIR", "Desarrollo de Software e Infraestructura de Red");

INSERT INTO tipoproyecto VALUES
("DT", "Desarrollo Tecnologico"),
("I", "Investigacion");

INSERT INTO perfil (nombre) VALUES ('alumno'), ('profesor'), ('admin');

INSERT INTO objetos (nombre) VALUES ('alumno'), ('proyecto'), ('datos'), ('profesorproy');

CREATE TABLE rubrica (idrubrica INT AUTO_INCREMENT PRIMARY KEY, nombre VARCHAR(150), area_conocimiento VARCHAR(150));

CREATE TABLE criterio (idcriterio INT AUTO_INCREMENT PRIMARY KEY, idrubrica INT, nombre VARCHAR(255), descripcion TEXT, ponderacion INT,
CONSTRAINT concede FOREIGN KEY (idrubrica) REFERENCES rubrica(idrubrica) ON DELETE CASCADE);

CREATE TABLE evaluacion (idevaluacion INT AUTO_INCREMENT PRIMARY KEY, idcriterio INT, nocontrol CHAR(10), calificacion FLOAT,
CONSTRAINT determina FOREIGN KEY (idcriterio) REFERENCES criterio(idcriterio),
CONSTRAINT agrega FOREIGN KEY (nocontrol) REFERENCES alumno(nocontrol));