/*Creacion simulada de bases de datos*/
CREATE TABLE areas_protegidas(
    _id int unique not null ,
    TIPO varchar(40)NOT null,
    NOMBRE varchar(100) not NULL,
    SHAPE_AREA float not NULL,
    SHAPE_LEN float not NULL);

DROP TABLE IF EXISTS registro_turismo;
CREATE TABLE registro_turismo(
    ANO int(4) CHECK(ANO>2000) ,
    MES INT(2)CHECK(MES>=1 AND MES<=12),
    CODIGO_RNT INT(7) UNIQUE NOT NULL,
    COD_MUN INT(7) not NULL,
    COD_DPTO INT(2) not NULL,
  	ESTADO_RNT VARCHAR(10)DEFAULT"ACTIVO",
  	RAZON_SOCIAL_ESTABLECIMIENTO VARCHAR(150) NOT NULL,
  	DEPARTAMENTO VARCHAR (30) NOT NULL,
  	MUNICIPIO VARCHAR(30)NOT NULL,
  	CATEGORIA VARCHAR(100) NOT NULL,
  	SUB_CATEGORIA VARCHAR(100) NOT NULL,
  	HABITACIONES INT(4) default 0,
  	CAMAS INT(5) default 0,
  	NUM_EMP INT default 0);

DROP TABLE IF EXISTS teatros;
CREATE TABLE teatros(
    OBJECTID_1 INT UNIQUE NOT NULL ,
    LECCODIGO INT unique not null,
    LECNOMBRE varchar(200)not null,
  	LECDIRECCI varchar(50)not null,
	LECTELEFON varchar(50),
	LECEMAIL varchar(100),
	LECPAGWEB varchar(100),
	LECCODLOC int(2)not null,
	LECNOMLOC varchar(50)not null,
	LECCODUPZ varchar(10)not null check (LECCODUPZ LIKE "UPZ%"),
	LECNOMUPZ varchar(100)not null,
	LECCODSEC int(10)not null,
	LECNOMSEC varchar(100)not null,
	LECESTADO varchar(50),
	LECCLASIF varchar(50) CHECK(LECCLASIF="TEATRO" OR LECCLASIF="AUDITORIO"),
	LECCONTACTO varchar(50),
	LECANIO int(4));

/*1. Seleccione el registro de movimientos relacionados con el turismo del año 2021 que tuvo
como destino turístico la ciudad de Bogotá.*/

SELECT ANO,DEPARTAMENTO,MUNICIPIO,CATEGORIA,COUNT(SUB_CATEGORIA) AS CANTIDAD FROM `trabajo-final-analitica.Entrega_1.RNT` WHERE MUNICIPIO = "BOGOTA DC" GROUP BY ANO,DEPARTAMENTO,MUNICIPIO,CATEGORIA;

/*2. Ordene de manera descendente los movimientos mensuales que se presentaron en la
ciudad de Bogotá relacionado con el Registro Nacional de Turismo.*/

SELECT MUNICIPIO,MES,COUNT(MES) AS MOVIMIENTOS FROM `trabajo-final-analitica.Entrega_1.RNT`
WHERE MUNICIPIO = "BOGOTA DC" GROUP BY MUNICIPIO,MES;

/*3. Del destino turístico Bogotá ¿cuántos reportes se dieron donde se evidencia como
alojamiento un hotel? Ordene por mes.*/

DROP TABLE IF EXISTS `trabajo-final-analitica.Entrega_1.BOGOTA`;
CREATE TABLE `trabajo-final-analitica.Entrega_1.BOGOTA` AS
(SELECT ANO,MES,CODIGO_RNT,COD_MUN,COD_DPTO,ESTADO_RNT,RAZON_SOCIAL_ESTABLECIMIENTO,UPPER(TRIM(DEPARTAMENTO)) AS DEPARTAMENTO_SIN,MUNICIPIO,CATEGORIA,SUB_CATEGORIA,HABITACIONES,CAMAS,NUM_EMP FROM
`trabajo-final-analitica.Entrega_1.RNT` WHERE DEPARTAMENTO = "BOGOTA DC" OR DEPARTAMENTO = "BOGOTÁ DC");

SELECT REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(CAST(MES AS
STRING),'1','ENERO'),'2','FEBRERO'),'3','MARZO'),'4','ABRIL'),'5','MAYO'),'6','JUNIO'),'7','JULIO'),'8','AGOSTO'),'9','SEPTIEMBRE'),'ENERO0','OCTUBRE') AS NOMBRE_MES,CATEGORIA, SUB_CATEGORIA, COUNT(SUB_CATEGORIA) AS CANT_HOTELES_MES
FROM `trabajo-final-analitica.Entrega_1.BOGOTA` WHERE SUB_CATEGORIA = "HOTEL" GROUP BY MES,
CATEGORIA,SUB_CATEGORIA ORDER BY MES ASC;

/*4. ¿Qué zona forestal protegida tiene el área más grande? ¿cuál tiene el área de menor
tamaño?*/

SELECT TIPO,NOMBRE, MAX(SHAPE_AREA) AS AREA_MAYOR_TAMANO FROM `entrega1-trabajofinal.Entrega_1.areas_protegidas_t1` GROUP BY TIPO,NOMBRE ORDER BY MAX(SHAPE_AREA) DESC LIMIT 1;

/*¿Cuál tiene el área de menor tamaño?*/

SELECT TIPO,NOMBRE, MIN(SHAPE_AREA) AS AREA_MENOR_TAMANO FROM `entrega1-trabajofinal.Entrega_1.areas_protegidas_t1` GROUP BY TIPO,NOMBRE ORDER BY MIN(SHAPE_AREA) ASC LIMIT 1;

/*5. ¿Qué localidad de la ciudad de Bogotá tiene la mayor cantidad de galerías?*/

SELECT LECNOMLOC AS LOCALIDAD, TRIM(UPPER(LECCLASIF)) AS CLASIFICACION, COUNT(LECCLASIF) AS CANT_GALERIAS FROM `trabajo-final-analitica.Entrega_1.salas_expo_galeria` WHERE TRIM(UPPER(LECCLASIF)) = "GALERÍAS" OR TRIM(UPPER(LECCLASIF)) = "GALERIAS" GROUP BY LECNOMLOC, LECCLASIF ORDER BY CANT_GALERIAS DESC LIMIT 1;

/*6. ¿Cuál es la localidad con la mayor cantidad de museos? Ordene de mayor a menor*/

SELECT LECNOMLOC, COUNT(LECNOMLOC) AS CANT_MUSEOS FROM `trabajo-final-analitica.Entrega_1.museos`
GROUP BY LECNOMLOC ORDER BY CANT_MUSEOS DESC;

/*7. ¿Cuál es el cinema más común en Bogotá? ¿Cuántos tiene? ¿En qué localidad está el
mayor número de ellos? Transforme los resultados en mayúsculas.*/

SELECT LECCLASIF, COUNT(LECCLASIF) AS TOTAL_CINE FROM `trabajo-final-analitica.Entrega_1.cine_cinemateca`
GROUP BY LECCLASIF ORDER BY TOTAL_CINE DESC LIMIT 1;

SELECT UPPER(LECNOMLOC) AS LOC_MAS_CINE,UPPER(LECCLASIF) AS NOMBRE_MAYUS, COUNT(LECCLASIF) AS
TOTAL_CINE FROM `trabajo-final-analitica.Entrega_1.cine_cinemateca` GROUP BY LECNOMLOC,LECCLASIF ORDER BY
TOTAL_CINE DESC LIMIT 1;

/*8. ¿Cuántos son los centros culturales públicos de cada localidad?*/

SELECT LECNOMLOC,LECCLASIF, COUNT(LECCLASIF) AS CANT_PUBLICOS FROM `trabajo-finalanalitica.Entrega_1.centro_cultura_artistico` WHERE LECCLASIF = "PUBLICO" OR LECCLASIF = "PÚBLICO" GROUP BY
LECNOMLOC,LECCLASIF ORDER BY CANT_PUBLICOS DESC;

/*9. ¿En qué localidades hay más cines que museos?*/

WITH MUSEO AS (SELECT LECNOMLOC AS LOCALIDAD, COUNT(LECNOMBRE) AS CANT_MUSEOS, FROM `trabajo-finalanalitica.Entrega_1.museos` GROUP BY LECNOMLOC),

CINEMAS AS (SELECT LECNOMLOC, COUNT(LECCLASIF) AS CANT_CINEMAS FROM `trabajo-finalanalitica.Entrega_1.cine_cinemateca` GROUP BY LECNOMLOC)

SELECT t1.LOCALIDAD, t1.CANT_MUSEOS, t2.CANT_CINEMAS FROM MUSEO t1 INNER JOIN CINEMAS t2 ON
t1.LOCALIDAD =t2.LECNOMLOC WHERE t1.CANT_MUSEOS<t2.CANT_CINEMAS GROUP BY t1.LOCALIDAD,
t1.CANT_MUSEOS, t2.CANT_CINEMAS;

/*10. ¿Cuántos museos y cuántos cines hay en cada localidad?*/

WITH MUSEO AS (SELECT LECNOMLOC AS LOCALIDAD, COUNT(LECNOMBRE) AS CANT_MUSEOS, FROM `trabajo-finalanalitica.Entrega_1.museos` GROUP BY LECNOMLOC),

CINEMAS AS (SELECT LECNOMLOC, COUNT(LECCLASIF) AS CANT_CINEMAS FROM `trabajo-finalanalitica.Entrega_1.cine_cinemateca` GROUP BY LECNOMLOC)

SELECT t1.LOCALIDAD, t1.CANT_MUSEOS, t2.CANT_CINEMAS, FROM MUSEO t1 LEFT JOIN CINEMAS t2 ON
t1.LOCALIDAD =t2.LECNOMLOC GROUP BY t1.LOCALIDAD, t1.CANT_MUSEOS, t2.CANT_CINEMAS ORDER BY
t1.CANT_MUSEOS DESC;

/*11. ¿Cuántos cines y salas de exposición hay en la localidad de Teusaquillo?*/

WITH CINE AS (SELECT LECNOMLOC AS LOCALIDAD,COUNT(LECCLASIF) AS CINES,
FROM `trabajo-final-analitica.Entrega_1.cine_cinemateca` WHERE LECNOMLOC = 'TEUSAQUILLO' GROUP BY
LECNOMLOC),

SALAS AS (SELECT LECNOMLOC AS LOCALIDAD,COUNT(LECCLASIF) AS SALA_EXPO FROM `trabajo-finalanalitica.Entrega_1.salas_expo_galeria` WHERE LECNOMLOC = 'TEUSAQUILLO' AND LECCLASIF = "SALAS DE EXPOSICIÓN" GROUP BY LECNOMLOC)

SELECT t1.LOCALIDAD, t1.CINES,t2.SALA_EXPO FROM CINE t1 INNER JOIN SALAS t2 ON t1.LOCALIDAD = t2.LOCALIDAD;


/*12. ¿Cuál es el porcentaje de centros culturales que hay en cada localidad?*/

WITH TOT_CENTRO AS (SELECT SUM(CENTROS_LOCALIDAD) AS TOTAL_CENTROS FROM (SELECT LECNOMLOC,
COUNT(LECNOMLOC) AS CENTROS_LOCALIDAD FROM `trabajo-final-analitica.Entrega_1.centro_cultura_artistico`
GROUP BY LECNOMLOC)),

SUM_CENTRO AS (SELECT LECNOMLOC, COUNT(LECNOMLOC) AS CENTROS_LOCALIDAD FROM `trabajo-finalanalitica.Entrega_1.centro_cultura_artistico` GROUP BY LECNOMLOC)

SELECT t1.LECNOMLOC AS LOCALIDAD,(t1.CENTROS_LOCALIDAD/t2.TOTAL_CENTROS)*100 AS PORCENTAJE, FROM
SUM_CENTRO t1 INNER JOIN TOT_CENTRO t2 ON t1.LECNOMLOC = LECNOMLOC;

/*13. ¿Entre Barrios unidos y Chapinero que localidad tiene mayor cantidad de salas de cine?*/

SELECT LECNOMLOC,COUNT(LECCLASIF) AS CINES_LOCALIDAD FROM `trabajo-finalanalitica.Entrega_1.cine_cinemateca` WHERE LECNOMLOC = 'CHAPINERO' OR LECNOMLOC = 'BARRIOS UNIDOS' GROUP BY LECNOMLOC ORDER BY CINES_LOCALIDAD DESC LIMIT 1;

/*14. ¿Cuál es el área total, la longitud y el tipo de reserva humedal salitre?*/

SELECT NOMBRE,UPPER(TIPO) AS TIPO_RESERVA,SHAPE_AREA AS AREA_TOTAL,SHAPE_LEN AS LONGITUD FROM
`trabajo-final-analitica.Entrega_1.areas_protegidas` WHERE NOMBRE= TRIM('HUMEDAL SALITRE') OR NOMBRE= TRIM('humedal salitre');

/*15. ¿Cuántos centros culturales de cada tipo hay en cada localidad?*/

SELECT LECNOMLOC AS LOCALIDAD,LECCLASIF AS CLASIFICACION, COUNT(LECCLASIF) AS CANT_CENTROS_CULTURALES
FROM `trabajo-final-analitica.Entrega_1.centro_cultura_artistico` GROUP BY LECNOMLOC,LECCLASIF ORDER BY
LOCALIDAD DESC;
