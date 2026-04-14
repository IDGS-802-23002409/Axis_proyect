/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19-11.8.6-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: mysql    Database: flask_db
-- ------------------------------------------------------
-- Server version	8.0.45

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*M!100616 SET @OLD_NOTE_VERBOSITY=@@NOTE_VERBOSITY, NOTE_VERBOSITY=0 */;

--
-- Table structure for table `categorias`
--

DROP TABLE IF EXISTS `categorias`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `categorias` (
  `uuid_categoria` varchar(36) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `descripcion` varchar(255) DEFAULT NULL,
  `imagen_url` varchar(255) DEFAULT NULL,
  `estatus_visible` tinyint(1) DEFAULT NULL,
  `fecha_creacion` datetime DEFAULT (now()),
  `fecha_actualizacion` datetime DEFAULT (now()),
  `usuario_creo_uuid` varchar(36) DEFAULT NULL,
  `usuario_actualizo_uuid` varchar(36) DEFAULT NULL,
  PRIMARY KEY (`uuid_categoria`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categorias`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `categorias` WRITE;
/*!40000 ALTER TABLE `categorias` DISABLE KEYS */;
INSERT INTO `categorias` VALUES
('4b32b928-d6c7-41d4-96aa-5df4cd6fc2dd','Camisetas','Prendas de cuerpo superior','/static/images/default/default-image.png',1,'2026-04-13 02:58:16','2026-04-13 02:58:16',NULL,NULL),
('4df813e6-6988-4739-bef5-7659cd47a3a1','Chaquetas','Abrigos y chamarras','/static/images/default/default-image.png',1,'2026-04-13 02:58:16','2026-04-13 02:58:16',NULL,NULL),
('54ce7cf0-8bac-427f-a43f-0b422d5b4344','Shorts','Pantalones cortos','/static/images/default/default-image.png',1,'2026-04-13 02:58:16','2026-04-13 02:58:16',NULL,NULL),
('5feb81e8-247b-4741-93c1-53172ebd152f','Pantalones','Prendas inferiores','/static/images/default/default-image.png',1,'2026-04-13 02:58:16','2026-04-13 02:58:16',NULL,NULL),
('aa95482f-5424-4465-a8ea-5342d0d585bd','Accesorios','Gorras y complementos','/static/images/default/default-image.png',1,'2026-04-13 02:58:16','2026-04-13 02:58:16',NULL,NULL),
('fc4f7540-5ed5-4fdd-9ec7-6056bb62653f','Hoodies','Sudaderas urbanas','/static/images/default/default-image.png',1,'2026-04-13 02:58:16','2026-04-13 02:58:16',NULL,NULL);
/*!40000 ALTER TABLE `categorias` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `clientes`
--

DROP TABLE IF EXISTS `clientes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `clientes` (
  `uuid_cliente` varchar(36) NOT NULL,
  `uuid_usuario` varchar(36) NOT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `direccion_completa` text,
  `fecha_creacion` datetime DEFAULT (now()),
  `fecha_actualizacion` datetime DEFAULT (now()),
  `usuario_actualizo_uuid` varchar(36) DEFAULT NULL,
  PRIMARY KEY (`uuid_cliente`),
  UNIQUE KEY `uuid_usuario` (`uuid_usuario`),
  CONSTRAINT `clientes_ibfk_1` FOREIGN KEY (`uuid_usuario`) REFERENCES `usuarios` (`uuid_usuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clientes`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `clientes` WRITE;
/*!40000 ALTER TABLE `clientes` DISABLE KEYS */;
INSERT INTO `clientes` VALUES
('10fb9e73-761a-48f7-81f8-0a80c7b7fae2','565b7dbe-56da-4422-a121-10225988882d','555-123-4567','Av. Reforma 123, CDMX','2026-04-13 02:58:16','2026-04-13 02:58:16',NULL),
('320e552f-651d-4828-881e-a0e956ab5180','ae564347-e661-4e9d-95aa-9f64379afa57','555-987-6543','Insurgentes Sur 456, CDMX','2026-04-13 02:58:16','2026-04-13 02:58:16',NULL);
/*!40000 ALTER TABLE `clientes` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `compras_detalle`
--

DROP TABLE IF EXISTS `compras_detalle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `compras_detalle` (
  `uuid_detalle_compra` varchar(36) NOT NULL,
  `uuid_compra` varchar(36) NOT NULL,
  `uuid_insumo` varchar(36) NOT NULL,
  `cantidad_comprada` decimal(12,4) NOT NULL,
  `costo_unitario_compra` decimal(12,2) NOT NULL,
  PRIMARY KEY (`uuid_detalle_compra`),
  KEY `idx_cdetalle_compra` (`uuid_compra`),
  KEY `idx_cdetalle_insumo` (`uuid_insumo`),
  CONSTRAINT `compras_detalle_ibfk_1` FOREIGN KEY (`uuid_compra`) REFERENCES `compras_encabezado` (`uuid_compra`),
  CONSTRAINT `compras_detalle_ibfk_2` FOREIGN KEY (`uuid_insumo`) REFERENCES `insumos` (`uuid_insumo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `compras_detalle`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `compras_detalle` WRITE;
/*!40000 ALTER TABLE `compras_detalle` DISABLE KEYS */;
INSERT INTO `compras_detalle` VALUES
('01e92299-0626-473a-8f2c-01906635c686','07d61dcd-c1be-4714-8d13-c79532bfeb28','4fe663b5-eaa7-45de-8cd4-695152be9da6',5.0000,220.00),
('184a207f-c57a-4ef0-a524-b45adb3e2339','0a0dcf90-2fc3-4f92-baff-28a13ad4f017','3106963b-7eba-4c5f-85a5-0c21d51ff34d',100.0000,12.00),
('d828960c-1448-4478-8fd8-0406a870dd7d','2515d145-a596-4a39-808d-236875bb4fd9','eb1443ea-070b-404a-a771-17022e20f230',500.0000,5.00),
('dce3d79e-ee9e-46aa-9445-5cccb445ceb0','f64a0d7a-9bde-4074-95e4-2a2bc45788d3','527bde95-e733-4955-98f7-4430cedea805',10.0000,150.00);
/*!40000 ALTER TABLE `compras_detalle` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `compras_encabezado`
--

DROP TABLE IF EXISTS `compras_encabezado`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `compras_encabezado` (
  `uuid_compra` varchar(36) NOT NULL,
  `folio_factura` varchar(50) DEFAULT NULL,
  `uuid_proveedor` varchar(36) NOT NULL,
  `uuid_usuario_registro` varchar(36) NOT NULL,
  `uuid_pedido` varchar(36) DEFAULT NULL,
  `fecha_compra` datetime DEFAULT (now()),
  `estatus` enum('PENDIENTE','RECIBIDO','CANCELADO') DEFAULT NULL,
  PRIMARY KEY (`uuid_compra`),
  KEY `uuid_proveedor` (`uuid_proveedor`),
  KEY `uuid_usuario_registro` (`uuid_usuario_registro`),
  KEY `uuid_pedido` (`uuid_pedido`),
  KEY `idx_compra_fecha` (`fecha_compra`),
  CONSTRAINT `compras_encabezado_ibfk_1` FOREIGN KEY (`uuid_proveedor`) REFERENCES `proveedores` (`uuid_proveedor`),
  CONSTRAINT `compras_encabezado_ibfk_2` FOREIGN KEY (`uuid_usuario_registro`) REFERENCES `usuarios` (`uuid_usuario`),
  CONSTRAINT `compras_encabezado_ibfk_3` FOREIGN KEY (`uuid_pedido`) REFERENCES `pedidos_proveedor_encabezado` (`uuid_pedido`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `compras_encabezado`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `compras_encabezado` WRITE;
/*!40000 ALTER TABLE `compras_encabezado` DISABLE KEYS */;
INSERT INTO `compras_encabezado` VALUES
('07d61dcd-c1be-4714-8d13-c79532bfeb28','FAC-INS-TEX-002-99','8bcc0405-5f72-4af0-854a-eb8a5187c2b7','4a8f4a27-5ad9-4bfc-8ac6-14886bdfa651','fa57def4-f357-4a08-ab56-4bcb0a5b1b7a','2026-04-13 02:58:16','RECIBIDO'),
('0a0dcf90-2fc3-4f92-baff-28a13ad4f017','FAC-INS-ACC-001-99','87ef0d2a-d32d-4e69-91ce-55c57608756c','4a8f4a27-5ad9-4bfc-8ac6-14886bdfa651','31c3c238-8887-4093-95a2-85dd0b573f0d','2026-04-13 02:58:16','RECIBIDO'),
('2515d145-a596-4a39-808d-236875bb4fd9','FAC-INS-ACC-003-99','87ef0d2a-d32d-4e69-91ce-55c57608756c','4a8f4a27-5ad9-4bfc-8ac6-14886bdfa651','362bdc54-3c62-4bd8-a4ed-d249ed8c4a5f','2026-04-13 02:58:16','RECIBIDO'),
('f64a0d7a-9bde-4074-95e4-2a2bc45788d3','FAC-INS-TEX-001-99','8bcc0405-5f72-4af0-854a-eb8a5187c2b7','4a8f4a27-5ad9-4bfc-8ac6-14886bdfa651','c92d788f-fe54-4586-97e4-e1c32415ec91','2026-04-13 02:58:16','RECIBIDO');
/*!40000 ALTER TABLE `compras_encabezado` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `ejecucion_corte`
--

DROP TABLE IF EXISTS `ejecucion_corte`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `ejecucion_corte` (
  `uuid_corte` varchar(36) NOT NULL,
  `uuid_op` varchar(36) NOT NULL,
  `uuid_rollo_used` varchar(36) NOT NULL,
  `metros_teoricos_requeridos` decimal(12,4) NOT NULL,
  `metros_sacados_bodega` decimal(12,4) NOT NULL,
  `prendas_reales_logradas` int NOT NULL,
  `merma_real_calculada` decimal(12,4) NOT NULL,
  `fecha_proceso` datetime DEFAULT (now()),
  `usuario_corto_uuid` varchar(36) DEFAULT NULL,
  PRIMARY KEY (`uuid_corte`),
  KEY `uuid_op` (`uuid_op`),
  KEY `uuid_rollo_used` (`uuid_rollo_used`),
  CONSTRAINT `ejecucion_corte_ibfk_1` FOREIGN KEY (`uuid_op`) REFERENCES `ordenes_produccion` (`uuid_op`),
  CONSTRAINT `ejecucion_corte_ibfk_2` FOREIGN KEY (`uuid_rollo_used`) REFERENCES `rollos_inventario` (`uuid_rollo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ejecucion_corte`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `ejecucion_corte` WRITE;
/*!40000 ALTER TABLE `ejecucion_corte` DISABLE KEYS */;
INSERT INTO `ejecucion_corte` VALUES
('c1714458-cd0d-449b-b530-6e718cb07d38','4a836b93-349b-4964-a953-02c3800fe4c3','3a4e0182-6b95-4a20-8328-dfe1cc1ac8ae',25.0000,26.5000,10,1.5000,'2026-04-13 02:58:16','4a8f4a27-5ad9-4bfc-8ac6-14886bdfa651');
/*!40000 ALTER TABLE `ejecucion_corte` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `empleados`
--

DROP TABLE IF EXISTS `empleados`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `empleados` (
  `uuid_empleado` varchar(36) NOT NULL,
  `uuid_usuario` varchar(36) NOT NULL,
  `numero_empleado` varchar(50) DEFAULT NULL,
  `puesto` varchar(100) DEFAULT NULL,
  `departamento` varchar(100) DEFAULT NULL,
  `fecha_ingreso` datetime DEFAULT NULL,
  `fecha_creacion` datetime DEFAULT (now()),
  `fecha_actualizacion` datetime DEFAULT (now()),
  PRIMARY KEY (`uuid_empleado`),
  UNIQUE KEY `uuid_usuario` (`uuid_usuario`),
  UNIQUE KEY `numero_empleado` (`numero_empleado`),
  CONSTRAINT `empleados_ibfk_1` FOREIGN KEY (`uuid_usuario`) REFERENCES `usuarios` (`uuid_usuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `empleados`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `empleados` WRITE;
/*!40000 ALTER TABLE `empleados` DISABLE KEYS */;
INSERT INTO `empleados` VALUES
('2c34b7e3-f441-46e3-a017-7bdb1bd36678','cfeecc67-0ffa-4531-a877-7d53b7c62b57','EMP-004','Analista de Suministros','Compras','2025-04-13 02:58:16','2026-04-13 02:58:16','2026-04-13 02:58:16'),
('4eb3ecca-7f95-4b91-b69f-01d31516bd25','85e6e654-8374-4206-b8ed-d33bf5ce697b','EMP-002','Jefe de Taller','Producción','2025-04-13 02:58:16','2026-04-13 02:58:15','2026-04-13 02:58:15'),
('7eff05b2-dd51-46f5-a8a4-07693a6b92cb','bfcdf757-d0f6-4201-84bc-f19227c562bc','EMP-003','Ejecutivo Comercial','Ventas','2025-04-13 02:58:16','2026-04-13 02:58:16','2026-04-13 02:58:16'),
('a4f87ce0-f9f9-4380-9a29-1f953a0b97f8','4a8f4a27-5ad9-4bfc-8ac6-14886bdfa651','EMP-001','Director General','Dirección','2025-04-13 02:58:16','2026-04-13 02:58:15','2026-04-13 02:58:15');
/*!40000 ALTER TABLE `empleados` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `explosion_materiales_cabecera`
--

DROP TABLE IF EXISTS `explosion_materiales_cabecera`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `explosion_materiales_cabecera` (
  `uuid_explosion` varchar(36) NOT NULL,
  `instrucciones_proceso` text,
  `fecha_actualizacion` datetime DEFAULT (now()),
  `uuid_usuario` varchar(36) NOT NULL,
  `estatus` enum('ACTIVO','INACTIVO') NOT NULL,
  PRIMARY KEY (`uuid_explosion`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `explosion_materiales_cabecera`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `explosion_materiales_cabecera` WRITE;
/*!40000 ALTER TABLE `explosion_materiales_cabecera` DISABLE KEYS */;
INSERT INTO `explosion_materiales_cabecera` VALUES
('b19529a2-8d4e-48d8-844a-230f70500667','Corte láser y costura reforzada.','2026-04-13 02:58:16','4a8f4a27-5ad9-4bfc-8ac6-14886bdfa651','ACTIVO'),
('bf9dfe37-4231-4bec-99da-3fc436095ba7','Costura plana a dos hilos.','2026-04-13 02:58:16','4a8f4a27-5ad9-4bfc-8ac6-14886bdfa651','ACTIVO');
/*!40000 ALTER TABLE `explosion_materiales_cabecera` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `explosion_materiales_detalle`
--

DROP TABLE IF EXISTS `explosion_materiales_detalle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `explosion_materiales_detalle` (
  `uuid_detalle` varchar(36) NOT NULL,
  `uuid_explosion` varchar(36) NOT NULL,
  `uuid_insumo` varchar(36) NOT NULL,
  `consumo_teorico_unitario` decimal(12,4) NOT NULL,
  `ancho_referencia` decimal(5,2) DEFAULT NULL,
  PRIMARY KEY (`uuid_detalle`),
  KEY `idx_expdet_insumo` (`uuid_insumo`),
  KEY `idx_expdet_explosion` (`uuid_explosion`),
  CONSTRAINT `explosion_materiales_detalle_ibfk_1` FOREIGN KEY (`uuid_explosion`) REFERENCES `explosion_materiales_cabecera` (`uuid_explosion`),
  CONSTRAINT `explosion_materiales_detalle_ibfk_2` FOREIGN KEY (`uuid_insumo`) REFERENCES `insumos` (`uuid_insumo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `explosion_materiales_detalle`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `explosion_materiales_detalle` WRITE;
/*!40000 ALTER TABLE `explosion_materiales_detalle` DISABLE KEYS */;
INSERT INTO `explosion_materiales_detalle` VALUES
('24a567c5-f112-42aa-ae4d-b086f63608b3','b19529a2-8d4e-48d8-844a-230f70500667','eb1443ea-070b-404a-a771-17022e20f230',1.0000,NULL),
('a0e47dc6-47f7-4ad9-98e2-e761e61cd2bd','bf9dfe37-4231-4bec-99da-3fc436095ba7','eb1443ea-070b-404a-a771-17022e20f230',1.0000,NULL),
('a676a358-f346-4c76-b1dc-e736ec6a1abb','bf9dfe37-4231-4bec-99da-3fc436095ba7','527bde95-e733-4955-98f7-4430cedea805',1.2000,NULL),
('c47f7c6a-3a03-4b9b-997f-1804aed8ac24','b19529a2-8d4e-48d8-844a-230f70500667','3106963b-7eba-4c5f-85a5-0c21d51ff34d',1.0000,NULL),
('e5b0d14c-b3ae-4732-bf79-05bf49c00050','b19529a2-8d4e-48d8-844a-230f70500667','4fe663b5-eaa7-45de-8cd4-695152be9da6',2.5000,NULL);
/*!40000 ALTER TABLE `explosion_materiales_detalle` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `insumos`
--

DROP TABLE IF EXISTS `insumos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `insumos` (
  `uuid_insumo` varchar(36) NOT NULL,
  `sku` varchar(50) DEFAULT NULL,
  `nombre` varchar(100) NOT NULL,
  `uuid_categoria` varchar(36) DEFAULT NULL,
  `unidad_medida` enum('ROLLO','PIEZA') NOT NULL,
  `contenido_cantidad` decimal(12,4) NOT NULL,
  `contenido_unidad_medida` enum('METRO','PIEZA') NOT NULL,
  `stock_total_acumulado` decimal(12,4) DEFAULT NULL,
  `stock_minimo_alerta` decimal(12,4) DEFAULT NULL,
  `ancho` decimal(5,2) DEFAULT NULL,
  `fecha_creacion` datetime DEFAULT (now()),
  `fecha_actualizacion` datetime DEFAULT (now()),
  `estatus` enum('ACTIVO','INACTIVO') DEFAULT NULL,
  `usuario_actualizo_uuid` varchar(36) DEFAULT NULL,
  PRIMARY KEY (`uuid_insumo`),
  UNIQUE KEY `sku` (`sku`),
  KEY `uuid_categoria` (`uuid_categoria`),
  CONSTRAINT `insumos_ibfk_1` FOREIGN KEY (`uuid_categoria`) REFERENCES `categorias` (`uuid_categoria`),
  CONSTRAINT `check_stock_insumo_positivo` CHECK ((`stock_total_acumulado` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `insumos`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `insumos` WRITE;
/*!40000 ALTER TABLE `insumos` DISABLE KEYS */;
INSERT INTO `insumos` VALUES
('0e3a69ba-df99-4a39-8702-79e3813e3452','INS-ACC-002','Botón Acero Inoxidable','5feb81e8-247b-4741-93c1-53172ebd152f','PIEZA',1.0000,'PIEZA',0.0000,10.0000,NULL,'2026-04-13 02:58:16','2026-04-13 02:58:16','ACTIVO',NULL),
('3106963b-7eba-4c5f-85a5-0c21d51ff34d','INS-ACC-001','Cierre Metálico YKK 15cm','4df813e6-6988-4739-bef5-7659cd47a3a1','PIEZA',1.0000,'PIEZA',100.0000,10.0000,NULL,'2026-04-13 02:58:16','2026-04-13 02:58:16','ACTIVO',NULL),
('4fe663b5-eaa7-45de-8cd4-695152be9da6','INS-TEX-002','Poliéster Gris Roll','fc4f7540-5ed5-4fdd-9ec7-6056bb62653f','ROLLO',50.0000,'METRO',250.0000,10.0000,NULL,'2026-04-13 02:58:16','2026-04-13 02:58:16','ACTIVO',NULL),
('527bde95-e733-4955-98f7-4430cedea805','INS-TEX-001','Algodón Negro Roll','4b32b928-d6c7-41d4-96aa-5df4cd6fc2dd','ROLLO',100.0000,'METRO',1000.0000,10.0000,NULL,'2026-04-13 02:58:16','2026-04-13 02:58:16','ACTIVO',NULL),
('9034fde1-ac4d-4fdb-9e56-fffa3bae7b53','INS-TEX-003','Denim Azul 14oz','5feb81e8-247b-4741-93c1-53172ebd152f','ROLLO',40.0000,'METRO',0.0000,10.0000,NULL,'2026-04-13 02:58:16','2026-04-13 02:58:16','ACTIVO',NULL),
('eb1443ea-070b-404a-a771-17022e20f230','INS-ACC-003','Etiqueta Axis Bordada','aa95482f-5424-4465-a8ea-5342d0d585bd','PIEZA',1.0000,'PIEZA',500.0000,10.0000,NULL,'2026-04-13 02:58:16','2026-04-13 02:58:16','ACTIVO',NULL);
/*!40000 ALTER TABLE `insumos` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `merma_piezas`
--

DROP TABLE IF EXISTS `merma_piezas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `merma_piezas` (
  `uuid_merma` varchar(36) NOT NULL,
  `uuid_op` varchar(36) NOT NULL,
  `uuid_insumo` varchar(36) NOT NULL,
  `cantidad_teorica` decimal(12,4) NOT NULL,
  `cantidad_real_consumida` decimal(12,4) NOT NULL,
  `motivo` enum('DEFECTO_PROVEEDOR','DAÑO_EN_PROCESO','ERROR_OPERARIO','MUESTRA_PRUEBA','OTRO') DEFAULT NULL,
  `observaciones` text,
  `fecha_registro` datetime DEFAULT (now()),
  `usuario_registro_uuid` varchar(36) DEFAULT NULL,
  PRIMARY KEY (`uuid_merma`),
  KEY `uuid_op` (`uuid_op`),
  KEY `uuid_insumo` (`uuid_insumo`),
  CONSTRAINT `merma_piezas_ibfk_1` FOREIGN KEY (`uuid_op`) REFERENCES `ordenes_produccion` (`uuid_op`),
  CONSTRAINT `merma_piezas_ibfk_2` FOREIGN KEY (`uuid_insumo`) REFERENCES `insumos` (`uuid_insumo`),
  CONSTRAINT `check_merma_real_no_negativa` CHECK ((`cantidad_real_consumida` >= 0)),
  CONSTRAINT `check_merma_teorica_positiva` CHECK ((`cantidad_teorica` > 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `merma_piezas`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `merma_piezas` WRITE;
/*!40000 ALTER TABLE `merma_piezas` DISABLE KEYS */;
INSERT INTO `merma_piezas` VALUES
('c627a969-2ed6-40c4-bf8c-83c886028f2d','4a836b93-349b-4964-a953-02c3800fe4c3','eb1443ea-070b-404a-a771-17022e20f230',10.0000,12.0000,'ERROR_OPERARIO','2 etiquetas se dañaron al coser.','2026-04-13 02:58:16','4a8f4a27-5ad9-4bfc-8ac6-14886bdfa651');
/*!40000 ALTER TABLE `merma_piezas` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `modelos_ropa`
--

DROP TABLE IF EXISTS `modelos_ropa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `modelos_ropa` (
  `uuid_modelo` varchar(36) NOT NULL,
  `nombre_modelo` varchar(100) NOT NULL,
  `descripcion` text,
  `uuid_categoria` varchar(36) NOT NULL,
  `imagen_url` varchar(255) DEFAULT NULL,
  `fecha_creacion` datetime DEFAULT (now()),
  `fecha_actualizacion` datetime DEFAULT (now()),
  `estatus` enum('ACTIVO','INACTIVO') NOT NULL,
  PRIMARY KEY (`uuid_modelo`),
  KEY `uuid_categoria` (`uuid_categoria`),
  CONSTRAINT `modelos_ropa_ibfk_1` FOREIGN KEY (`uuid_categoria`) REFERENCES `categorias` (`uuid_categoria`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `modelos_ropa`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `modelos_ropa` WRITE;
/*!40000 ALTER TABLE `modelos_ropa` DISABLE KEYS */;
INSERT INTO `modelos_ropa` VALUES
('2c186a23-664e-4bd3-89ab-4b829a36a619','Axis Logo Tee White','Camiseta 100% algodón alta densidad.','4b32b928-d6c7-41d4-96aa-5df4cd6fc2dd','/static/images/products/tshirt-white.jpg','2026-04-13 02:58:16','2026-04-13 02:58:16','ACTIVO'),
('a928cbe9-d18a-40bc-8bbb-c79c5b66e94c','Hoodie Oversight Black','Sudadera pesada con fit urbano.','fc4f7540-5ed5-4fdd-9ec7-6056bb62653f','/static/images/products/hoodie-black.jpg','2026-04-13 02:58:16','2026-04-13 02:58:16','ACTIVO');
/*!40000 ALTER TABLE `modelos_ropa` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `ordenes_produccion`
--

DROP TABLE IF EXISTS `ordenes_produccion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `ordenes_produccion` (
  `uuid_op` varchar(36) NOT NULL,
  `uuid_producto` varchar(36) NOT NULL,
  `uuid_venta_detalle` varchar(36) DEFAULT NULL,
  `uuid_pedido_detalle` varchar(36) DEFAULT NULL,
  `cantidad_a_producir` int NOT NULL,
  `estado` enum('Pendiente','En Corte','Confección','Terminado') DEFAULT NULL,
  `fecha_solicitud` datetime DEFAULT (now()),
  PRIMARY KEY (`uuid_op`),
  KEY `uuid_venta_detalle` (`uuid_venta_detalle`),
  KEY `uuid_pedido_detalle` (`uuid_pedido_detalle`),
  KEY `idx_op_producto` (`uuid_producto`),
  KEY `idx_op_estado` (`estado`),
  CONSTRAINT `ordenes_produccion_ibfk_1` FOREIGN KEY (`uuid_producto`) REFERENCES `productos_terminados` (`uuid_producto`),
  CONSTRAINT `ordenes_produccion_ibfk_2` FOREIGN KEY (`uuid_venta_detalle`) REFERENCES `ventas_detalle` (`uuid_detalle`),
  CONSTRAINT `ordenes_produccion_ibfk_3` FOREIGN KEY (`uuid_pedido_detalle`) REFERENCES `pedidos_cliente_detalle` (`uuid_detalle_pedido`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ordenes_produccion`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `ordenes_produccion` WRITE;
/*!40000 ALTER TABLE `ordenes_produccion` DISABLE KEYS */;
INSERT INTO `ordenes_produccion` VALUES
('0e9c6b71-20db-4685-b2de-cb5a0d24a026','5db8bfe1-35fc-4355-804e-58b33358aa42',NULL,NULL,30,'Pendiente','2026-04-13 02:58:16'),
('4a836b93-349b-4964-a953-02c3800fe4c3','df050db0-6adb-4df9-a8e7-7d165910a1c1','1a10e895-f44d-4f79-af30-63f70a5db932',NULL,10,'Terminado','2026-04-13 02:58:16');
/*!40000 ALTER TABLE `ordenes_produccion` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `pedidos_cliente_detalle`
--

DROP TABLE IF EXISTS `pedidos_cliente_detalle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `pedidos_cliente_detalle` (
  `uuid_detalle_pedido` varchar(36) NOT NULL,
  `uuid_pedido` varchar(36) NOT NULL,
  `uuid_producto` varchar(36) NOT NULL,
  `cantidad` int NOT NULL,
  `precio_unitario_historico` decimal(12,2) NOT NULL,
  `estatus_item` enum('Pendiente','En Producción','Terminado') DEFAULT NULL,
  PRIMARY KEY (`uuid_detalle_pedido`),
  KEY `uuid_pedido` (`uuid_pedido`),
  KEY `uuid_producto` (`uuid_producto`),
  CONSTRAINT `pedidos_cliente_detalle_ibfk_1` FOREIGN KEY (`uuid_pedido`) REFERENCES `pedidos_cliente_encabezado` (`uuid_pedido`),
  CONSTRAINT `pedidos_cliente_detalle_ibfk_2` FOREIGN KEY (`uuid_producto`) REFERENCES `productos_terminados` (`uuid_producto`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pedidos_cliente_detalle`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `pedidos_cliente_detalle` WRITE;
/*!40000 ALTER TABLE `pedidos_cliente_detalle` DISABLE KEYS */;
/*!40000 ALTER TABLE `pedidos_cliente_detalle` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `pedidos_cliente_encabezado`
--

DROP TABLE IF EXISTS `pedidos_cliente_encabezado`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `pedidos_cliente_encabezado` (
  `uuid_pedido` varchar(36) NOT NULL,
  `numero_pedido` varchar(25) NOT NULL,
  `uuid_cliente` varchar(36) NOT NULL,
  `uuid_venta_origen` varchar(36) DEFAULT NULL,
  `estatus` enum('Pendiente','Producción','Listo','Entregado','Cancelado') DEFAULT NULL,
  `fecha_pedido` datetime DEFAULT (now()),
  `fecha_actualizacion` datetime DEFAULT (now()),
  PRIMARY KEY (`uuid_pedido`),
  UNIQUE KEY `numero_pedido` (`numero_pedido`),
  KEY `uuid_cliente` (`uuid_cliente`),
  KEY `uuid_venta_origen` (`uuid_venta_origen`),
  KEY `idx_pedido_estatus` (`estatus`),
  KEY `idx_pedido_fecha` (`fecha_pedido`),
  CONSTRAINT `pedidos_cliente_encabezado_ibfk_1` FOREIGN KEY (`uuid_cliente`) REFERENCES `clientes` (`uuid_cliente`),
  CONSTRAINT `pedidos_cliente_encabezado_ibfk_2` FOREIGN KEY (`uuid_venta_origen`) REFERENCES `ventas_encabezado` (`uuid_venta`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pedidos_cliente_encabezado`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `pedidos_cliente_encabezado` WRITE;
/*!40000 ALTER TABLE `pedidos_cliente_encabezado` DISABLE KEYS */;
/*!40000 ALTER TABLE `pedidos_cliente_encabezado` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `pedidos_proveedor_detalle`
--

DROP TABLE IF EXISTS `pedidos_proveedor_detalle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `pedidos_proveedor_detalle` (
  `uuid_detalle_pedido` varchar(36) NOT NULL,
  `uuid_pedido` varchar(36) NOT NULL,
  `uuid_insumo` varchar(36) NOT NULL,
  `cantidad_pedida` decimal(12,4) NOT NULL,
  `cantidad_recibida` decimal(12,4) DEFAULT NULL,
  `costo_unitario_estimado` decimal(12,2) DEFAULT NULL,
  PRIMARY KEY (`uuid_detalle_pedido`),
  KEY `uuid_pedido` (`uuid_pedido`),
  KEY `uuid_insumo` (`uuid_insumo`),
  CONSTRAINT `pedidos_proveedor_detalle_ibfk_1` FOREIGN KEY (`uuid_pedido`) REFERENCES `pedidos_proveedor_encabezado` (`uuid_pedido`),
  CONSTRAINT `pedidos_proveedor_detalle_ibfk_2` FOREIGN KEY (`uuid_insumo`) REFERENCES `insumos` (`uuid_insumo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pedidos_proveedor_detalle`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `pedidos_proveedor_detalle` WRITE;
/*!40000 ALTER TABLE `pedidos_proveedor_detalle` DISABLE KEYS */;
INSERT INTO `pedidos_proveedor_detalle` VALUES
('2384542b-6fd4-4d0e-b8c8-c438b28eaa70','31c3c238-8887-4093-95a2-85dd0b573f0d','3106963b-7eba-4c5f-85a5-0c21d51ff34d',100.0000,0.0000,12.00),
('3d532d35-34ce-499a-9a82-4b4b08fac4f4','fa57def4-f357-4a08-ab56-4bcb0a5b1b7a','4fe663b5-eaa7-45de-8cd4-695152be9da6',5.0000,0.0000,220.00),
('5f3f11d7-7e64-40bf-ade7-56d1bcef3c89','362bdc54-3c62-4bd8-a4ed-d249ed8c4a5f','eb1443ea-070b-404a-a771-17022e20f230',500.0000,0.0000,5.00),
('60df6646-e4c5-45b3-9b60-d4f1ef3ab66a','c92d788f-fe54-4586-97e4-e1c32415ec91','527bde95-e733-4955-98f7-4430cedea805',10.0000,0.0000,150.00);
/*!40000 ALTER TABLE `pedidos_proveedor_detalle` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `pedidos_proveedor_encabezado`
--

DROP TABLE IF EXISTS `pedidos_proveedor_encabezado`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `pedidos_proveedor_encabezado` (
  `uuid_pedido` varchar(36) NOT NULL,
  `folio_pedido` varchar(50) NOT NULL,
  `uuid_proveedor` varchar(36) NOT NULL,
  `uuid_usuario_solicita` varchar(36) NOT NULL,
  `fecha_pedido` datetime DEFAULT (now()),
  `estatus` enum('Pendiente','Aprobado','Parcial','Completado','Cancelado') DEFAULT NULL,
  PRIMARY KEY (`uuid_pedido`),
  UNIQUE KEY `folio_pedido` (`folio_pedido`),
  KEY `uuid_proveedor` (`uuid_proveedor`),
  KEY `uuid_usuario_solicita` (`uuid_usuario_solicita`),
  CONSTRAINT `pedidos_proveedor_encabezado_ibfk_1` FOREIGN KEY (`uuid_proveedor`) REFERENCES `proveedores` (`uuid_proveedor`),
  CONSTRAINT `pedidos_proveedor_encabezado_ibfk_2` FOREIGN KEY (`uuid_usuario_solicita`) REFERENCES `usuarios` (`uuid_usuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pedidos_proveedor_encabezado`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `pedidos_proveedor_encabezado` WRITE;
/*!40000 ALTER TABLE `pedidos_proveedor_encabezado` DISABLE KEYS */;
INSERT INTO `pedidos_proveedor_encabezado` VALUES
('31c3c238-8887-4093-95a2-85dd0b573f0d','PED-INS-ACC-001','87ef0d2a-d32d-4e69-91ce-55c57608756c','4a8f4a27-5ad9-4bfc-8ac6-14886bdfa651','2026-04-13 02:58:16','Completado'),
('362bdc54-3c62-4bd8-a4ed-d249ed8c4a5f','PED-INS-ACC-003','87ef0d2a-d32d-4e69-91ce-55c57608756c','4a8f4a27-5ad9-4bfc-8ac6-14886bdfa651','2026-04-13 02:58:16','Completado'),
('c92d788f-fe54-4586-97e4-e1c32415ec91','PED-INS-TEX-001','8bcc0405-5f72-4af0-854a-eb8a5187c2b7','4a8f4a27-5ad9-4bfc-8ac6-14886bdfa651','2026-04-13 02:58:16','Completado'),
('fa57def4-f357-4a08-ab56-4bcb0a5b1b7a','PED-INS-TEX-002','8bcc0405-5f72-4af0-854a-eb8a5187c2b7','4a8f4a27-5ad9-4bfc-8ac6-14886bdfa651','2026-04-13 02:58:16','Completado');
/*!40000 ALTER TABLE `pedidos_proveedor_encabezado` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `productos_terminados`
--

DROP TABLE IF EXISTS `productos_terminados`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `productos_terminados` (
  `uuid_producto` varchar(36) NOT NULL,
  `uuid_modelo` varchar(36) NOT NULL,
  `uuid_explosion` varchar(36) NOT NULL,
  `sku_especifico` varchar(50) NOT NULL,
  `talla` enum('XSS','XS','S','M','L','XL','XXL','Unica') NOT NULL,
  `precio_venta` decimal(12,2) NOT NULL,
  `stock_fisico_actual` int DEFAULT NULL,
  `stock_minimo_alerta` int DEFAULT NULL,
  `active` tinyint(1) DEFAULT NULL,
  `fecha_creacion` datetime DEFAULT (now()),
  `fecha_actualizacion` datetime DEFAULT (now()),
  PRIMARY KEY (`uuid_producto`),
  UNIQUE KEY `sku_especifico` (`sku_especifico`),
  KEY `idx_producto_modelo` (`uuid_modelo`),
  KEY `idx_producto_explosion` (`uuid_explosion`),
  CONSTRAINT `productos_terminados_ibfk_1` FOREIGN KEY (`uuid_modelo`) REFERENCES `modelos_ropa` (`uuid_modelo`),
  CONSTRAINT `productos_terminados_ibfk_2` FOREIGN KEY (`uuid_explosion`) REFERENCES `explosion_materiales_cabecera` (`uuid_explosion`),
  CONSTRAINT `check_stock_producto_positivo` CHECK ((`stock_fisico_actual` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `productos_terminados`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `productos_terminados` WRITE;
/*!40000 ALTER TABLE `productos_terminados` DISABLE KEYS */;
INSERT INTO `productos_terminados` VALUES
('09de2526-edc6-4d1b-9f10-6241fa9b21f5','2c186a23-664e-4bd3-89ab-4b829a36a619','bf9dfe37-4231-4bec-99da-3fc436095ba7','T-LOG-WHT-XL','XL',450.00,22,0,1,'2026-04-13 02:58:16','2026-04-13 02:58:16'),
('4930ecd3-c783-471a-b1a0-437698440bd9','2c186a23-664e-4bd3-89ab-4b829a36a619','bf9dfe37-4231-4bec-99da-3fc436095ba7','T-LOG-WHT-M','M',450.00,45,0,1,'2026-04-13 02:58:16','2026-04-13 02:58:16'),
('5db8bfe1-35fc-4355-804e-58b33358aa42','2c186a23-664e-4bd3-89ab-4b829a36a619','bf9dfe37-4231-4bec-99da-3fc436095ba7','T-LOG-WHT-L','L',450.00,10,0,1,'2026-04-13 02:58:16','2026-04-13 02:58:16'),
('65cab38b-17a2-40db-a294-7bad793048ea','a928cbe9-d18a-40bc-8bbb-c79c5b66e94c','b19529a2-8d4e-48d8-844a-230f70500667','H-OV-BLK-S','S',1200.00,11,0,1,'2026-04-13 02:58:16','2026-04-13 02:58:16'),
('b83a6654-153d-40de-bf5e-592dd3f2822d','a928cbe9-d18a-40bc-8bbb-c79c5b66e94c','b19529a2-8d4e-48d8-844a-230f70500667','H-OV-BLK-XL','XL',1200.00,20,0,1,'2026-04-13 02:58:16','2026-04-13 02:58:16'),
('c50246d0-890a-49d8-9d68-856694e0ff80','2c186a23-664e-4bd3-89ab-4b829a36a619','bf9dfe37-4231-4bec-99da-3fc436095ba7','T-LOG-WHT-S','S',450.00,31,0,1,'2026-04-13 02:58:16','2026-04-13 02:58:16'),
('df050db0-6adb-4df9-a8e7-7d165910a1c1','a928cbe9-d18a-40bc-8bbb-c79c5b66e94c','b19529a2-8d4e-48d8-844a-230f70500667','H-OV-BLK-M','M',1200.00,24,0,1,'2026-04-13 02:58:16','2026-04-13 02:58:16'),
('f84a2bd9-d76c-4333-8d99-38770be2a17b','a928cbe9-d18a-40bc-8bbb-c79c5b66e94c','b19529a2-8d4e-48d8-844a-230f70500667','H-OV-BLK-L','L',1200.00,40,0,1,'2026-04-13 02:58:16','2026-04-13 02:58:16');
/*!40000 ALTER TABLE `productos_terminados` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `proveedores`
--

DROP TABLE IF EXISTS `proveedores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `proveedores` (
  `uuid_proveedor` varchar(36) NOT NULL,
  `razon_social` varchar(150) NOT NULL,
  `rfc` varchar(20) NOT NULL,
  `contacto_nombre` varchar(100) DEFAULT NULL,
  `fecha_creacion` datetime DEFAULT (now()),
  `fecha_actualizacion` datetime DEFAULT (now()),
  `usuario_creo_uuid` varchar(36) DEFAULT NULL,
  `estatus` tinyint(1) DEFAULT NULL,
  `telefono` varchar(20) NOT NULL,
  `categoria_insumo` varchar(30) NOT NULL,
  PRIMARY KEY (`uuid_proveedor`),
  UNIQUE KEY `razon_social` (`razon_social`),
  UNIQUE KEY `rfc` (`rfc`),
  UNIQUE KEY `telefono` (`telefono`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `proveedores`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `proveedores` WRITE;
/*!40000 ALTER TABLE `proveedores` DISABLE KEYS */;
INSERT INTO `proveedores` VALUES
('27d2c1c5-894d-4cb4-847b-c8ddf7d044f0','Hilos y Avíos del Norte','HIL220301HAN','Roberto','2026-04-13 02:58:16','2026-04-13 02:58:16',NULL,1,'818-200-1010','Otros'),
('87ef0d2a-d32d-4e69-91ce-55c57608756c','Accesorios Industriales','ACC850505XYZ','Carlos','2026-04-13 02:58:16','2026-04-13 02:58:16',NULL,1,'555-300-4000','Otros'),
('8bcc0405-5f72-4af0-854a-eb8a5187c2b7','Textiles Premium S.A.','TEX900101ABC','Elena','2026-04-13 02:58:16','2026-04-13 02:58:16',NULL,1,'555-100-2000','Textiles');
/*!40000 ALTER TABLE `proveedores` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `retazos_inventario`
--

DROP TABLE IF EXISTS `retazos_inventario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `retazos_inventario` (
  `uuid_retazo` varchar(36) NOT NULL,
  `uuid_rollo_origen` varchar(36) NOT NULL,
  `uuid_corte_origen` varchar(36) NOT NULL,
  `metraje` decimal(12,4) NOT NULL,
  `motivo_merma` text,
  `fecha_creacion` datetime DEFAULT (now()),
  PRIMARY KEY (`uuid_retazo`),
  KEY `uuid_rollo_origen` (`uuid_rollo_origen`),
  KEY `uuid_corte_origen` (`uuid_corte_origen`),
  CONSTRAINT `retazos_inventario_ibfk_1` FOREIGN KEY (`uuid_rollo_origen`) REFERENCES `rollos_inventario` (`uuid_rollo`),
  CONSTRAINT `retazos_inventario_ibfk_2` FOREIGN KEY (`uuid_corte_origen`) REFERENCES `ejecucion_corte` (`uuid_corte`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `retazos_inventario`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `retazos_inventario` WRITE;
/*!40000 ALTER TABLE `retazos_inventario` DISABLE KEYS */;
/*!40000 ALTER TABLE `retazos_inventario` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `role`
--

DROP TABLE IF EXISTS `role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `role` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(80) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `role` WRITE;
/*!40000 ALTER TABLE `role` DISABLE KEYS */;
INSERT INTO `role` VALUES
(1,'admin',NULL),
(2,'gerente',NULL),
(3,'produccion',NULL),
(4,'cliente',NULL);
/*!40000 ALTER TABLE `role` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `roles_usuarios`
--

DROP TABLE IF EXISTS `roles_usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles_usuarios` (
  `usuario_id` varchar(36) DEFAULT NULL,
  `role_id` int DEFAULT NULL,
  KEY `usuario_id` (`usuario_id`),
  KEY `role_id` (`role_id`),
  CONSTRAINT `roles_usuarios_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`uuid_usuario`),
  CONSTRAINT `roles_usuarios_ibfk_2` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles_usuarios`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `roles_usuarios` WRITE;
/*!40000 ALTER TABLE `roles_usuarios` DISABLE KEYS */;
INSERT INTO `roles_usuarios` VALUES
('4a8f4a27-5ad9-4bfc-8ac6-14886bdfa651',1),
('85e6e654-8374-4206-b8ed-d33bf5ce697b',3),
('bfcdf757-d0f6-4201-84bc-f19227c562bc',2),
('cfeecc67-0ffa-4531-a877-7d53b7c62b57',3),
('565b7dbe-56da-4422-a121-10225988882d',4),
('ae564347-e661-4e9d-95aa-9f64379afa57',4);
/*!40000 ALTER TABLE `roles_usuarios` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `rollos_inventario`
--

DROP TABLE IF EXISTS `rollos_inventario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `rollos_inventario` (
  `uuid_rollo` varchar(36) NOT NULL,
  `uuid_insumo` varchar(36) NOT NULL,
  `uuid_detalle_compra` varchar(36) NOT NULL,
  `metraje_inicial` decimal(12,4) NOT NULL,
  `metraje_continuo_actual` decimal(12,4) NOT NULL,
  `fecha_creacion` datetime DEFAULT (now()),
  PRIMARY KEY (`uuid_rollo`),
  KEY `uuid_insumo` (`uuid_insumo`),
  KEY `uuid_detalle_compra` (`uuid_detalle_compra`),
  CONSTRAINT `rollos_inventario_ibfk_1` FOREIGN KEY (`uuid_insumo`) REFERENCES `insumos` (`uuid_insumo`),
  CONSTRAINT `rollos_inventario_ibfk_2` FOREIGN KEY (`uuid_detalle_compra`) REFERENCES `compras_detalle` (`uuid_detalle_compra`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rollos_inventario`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `rollos_inventario` WRITE;
/*!40000 ALTER TABLE `rollos_inventario` DISABLE KEYS */;
INSERT INTO `rollos_inventario` VALUES
('00b8e1c6-ac77-4075-a1bd-e4a29d8085b5','527bde95-e733-4955-98f7-4430cedea805','dce3d79e-ee9e-46aa-9445-5cccb445ceb0',100.0000,100.0000,'2026-04-13 02:58:16'),
('0bb4ec2d-328e-49c2-b0fa-3c11580367d9','527bde95-e733-4955-98f7-4430cedea805','dce3d79e-ee9e-46aa-9445-5cccb445ceb0',100.0000,100.0000,'2026-04-13 02:58:16'),
('3a4e0182-6b95-4a20-8328-dfe1cc1ac8ae','4fe663b5-eaa7-45de-8cd4-695152be9da6','01e92299-0626-473a-8f2c-01906635c686',50.0000,23.5000,'2026-04-13 02:58:16'),
('65ed0d89-e104-42e3-8e5a-7a634c0e6c40','527bde95-e733-4955-98f7-4430cedea805','dce3d79e-ee9e-46aa-9445-5cccb445ceb0',100.0000,100.0000,'2026-04-13 02:58:16'),
('740b6d71-3093-454c-b011-ac5347448f82','527bde95-e733-4955-98f7-4430cedea805','dce3d79e-ee9e-46aa-9445-5cccb445ceb0',100.0000,100.0000,'2026-04-13 02:58:16'),
('900c09b9-696f-419d-8cf5-3deb1151b909','4fe663b5-eaa7-45de-8cd4-695152be9da6','01e92299-0626-473a-8f2c-01906635c686',50.0000,50.0000,'2026-04-13 02:58:16'),
('91538209-0b61-45fc-b214-1c2222fcfbd9','527bde95-e733-4955-98f7-4430cedea805','dce3d79e-ee9e-46aa-9445-5cccb445ceb0',100.0000,100.0000,'2026-04-13 02:58:16'),
('a04b2c46-c073-4b09-926a-5b2d4702b57c','4fe663b5-eaa7-45de-8cd4-695152be9da6','01e92299-0626-473a-8f2c-01906635c686',50.0000,50.0000,'2026-04-13 02:58:16'),
('a6603894-f784-48c6-85a5-a24a93816c8c','4fe663b5-eaa7-45de-8cd4-695152be9da6','01e92299-0626-473a-8f2c-01906635c686',50.0000,50.0000,'2026-04-13 02:58:16'),
('a6edd42d-f38e-4f0e-975e-0ecdcc2c62ff','527bde95-e733-4955-98f7-4430cedea805','dce3d79e-ee9e-46aa-9445-5cccb445ceb0',100.0000,100.0000,'2026-04-13 02:58:16'),
('c0a72806-10d1-4910-8bbd-02892327517a','527bde95-e733-4955-98f7-4430cedea805','dce3d79e-ee9e-46aa-9445-5cccb445ceb0',100.0000,100.0000,'2026-04-13 02:58:16'),
('c7f725de-4b65-4d0e-b7d8-2f02d7db78a6','527bde95-e733-4955-98f7-4430cedea805','dce3d79e-ee9e-46aa-9445-5cccb445ceb0',100.0000,100.0000,'2026-04-13 02:58:16'),
('c80e2ca1-8a5a-4387-9881-997f902c2fdf','527bde95-e733-4955-98f7-4430cedea805','dce3d79e-ee9e-46aa-9445-5cccb445ceb0',100.0000,100.0000,'2026-04-13 02:58:16'),
('cf0ca2cb-caca-4a7a-9b05-60c7199c3eca','527bde95-e733-4955-98f7-4430cedea805','dce3d79e-ee9e-46aa-9445-5cccb445ceb0',100.0000,100.0000,'2026-04-13 02:58:16'),
('fd69079e-a6d0-450e-a869-d8e3f04961bb','4fe663b5-eaa7-45de-8cd4-695152be9da6','01e92299-0626-473a-8f2c-01906635c686',50.0000,50.0000,'2026-04-13 02:58:16');
/*!40000 ALTER TABLE `rollos_inventario` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios` (
  `uuid_usuario` varchar(36) NOT NULL,
  `nombre_completo` varchar(150) NOT NULL,
  `email` varchar(120) NOT NULL,
  `password` varchar(255) NOT NULL,
  `active` tinyint(1) DEFAULT NULL,
  `fecha_creacion` datetime DEFAULT (now()),
  `fecha_actualizacion` datetime DEFAULT (now()),
  `fs_uniquifier` varchar(64) NOT NULL,
  `confirmed_at` datetime DEFAULT NULL,
  `tf_primary_method` varchar(64) DEFAULT NULL,
  `tf_totp_secret` varchar(255) DEFAULT NULL,
  `tf_phone_number` varchar(64) DEFAULT NULL,
  `password_changed_at` datetime DEFAULT (now()),
  `mf_recovery_codes` json DEFAULT NULL,
  PRIMARY KEY (`uuid_usuario`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `fs_uniquifier` (`fs_uniquifier`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES
('4a8f4a27-5ad9-4bfc-8ac6-14886bdfa651','Admin Axis','admin@axis.com','$argon2id$v=19$m=65536,t=3,p=4$4Lz3PscYg3DO2fu/V+r9Hw$BzJV/A3aaf+I/SMwZiP9tr4d4xbr5/NVRe1ssAxlSs0',1,'2026-04-13 02:58:15','2026-04-13 03:20:09','ffe53fd589134bc39a431bb63f266ec3','2026-04-13 02:58:16','authenticator','{\"enckey\":{\"c\":14,\"k\":\"JBINF6DAGFNVNOPZ5GSK7HS5DA65JHM4\",\"s\":\"3GN7G7SP5H636V2KRFIQ\",\"t\":\"1\",\"v\":1},\"type\":\"totp\",\"v\":1}',NULL,'2026-04-13 02:58:15',NULL),
('565b7dbe-56da-4422-a121-10225988882d','Juan Cliente','juan@axis.com','$argon2id$v=19$m=65536,t=3,p=4$npOSMgbAWGstpTTG+J+Tsg$Bg5pkeUQh70dO84d+BajU72FiAsk+tZH0sBjCZFwFEg',1,'2026-04-13 02:58:16','2026-04-13 02:58:16','b39b9eacc21d4e57b98424e21b8c08cf','2026-04-13 02:58:16',NULL,NULL,NULL,'2026-04-13 02:58:16',NULL),
('85e6e654-8374-4206-b8ed-d33bf5ce697b','Modista Principal','modista@axis.com','$argon2id$v=19$m=65536,t=3,p=4$Yuw9h7BWSmlNqdW6d84ZAw$wBDIYGXzjlWcUfhWb4VuGDn4i0hFrLzvjHt9TFet0SU',1,'2026-04-13 02:58:15','2026-04-13 02:58:15','d347f135e6a640be88edb84faecce4ae','2026-04-13 02:58:16',NULL,NULL,NULL,'2026-04-13 02:58:15',NULL),
('ae564347-e661-4e9d-95aa-9f64379afa57','Maria Lopez','maria@axis.com','$argon2id$v=19$m=65536,t=3,p=4$MibE+P8fY6yVEiLknJMSog$Y9sIloWfFcU/xldR/XJJWDeEyrR8x3Jc9PrJymqhj5M',1,'2026-04-13 02:58:16','2026-04-13 02:58:16','6763e861b5f54c67b44f70b1acb707bf','2026-04-13 02:58:16',NULL,NULL,NULL,'2026-04-13 02:58:16',NULL),
('bfcdf757-d0f6-4201-84bc-f19227c562bc','Vendedor Axis','ventas@axis.com','$argon2id$v=19$m=65536,t=3,p=4$p5SScs75f+/9n5NSSsm5tw$pnL11DvomAOOr4MOUJhz6SywXZq7kaBXdY6vKCn43Ow',1,'2026-04-13 02:58:16','2026-04-13 02:58:16','22f8db1dadd1474e96d39cacea3c87df','2026-04-13 02:58:16',NULL,NULL,NULL,'2026-04-13 02:58:16',NULL),
('cfeecc67-0ffa-4531-a877-7d53b7c62b57','Comprador Axis','compras@axis.com','$argon2id$v=19$m=65536,t=3,p=4$QsgZQ2jNubcWopRSag1BqA$d2QQ2nyWaXfMGGbZpWe7w1fDar/1Awuc5w3kZYS9nQQ',1,'2026-04-13 02:58:16','2026-04-13 02:58:16','3e179a082c6d46598153dbdcbe4a6a25','2026-04-13 02:58:16',NULL,NULL,NULL,'2026-04-13 02:58:16',NULL);
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `ventas_detalle`
--

DROP TABLE IF EXISTS `ventas_detalle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `ventas_detalle` (
  `uuid_detalle` varchar(36) NOT NULL,
  `uuid_venta` varchar(36) NOT NULL,
  `uuid_producto` varchar(36) NOT NULL,
  `cantidad` int NOT NULL,
  `precio_unitario_historico` decimal(12,2) NOT NULL,
  PRIMARY KEY (`uuid_detalle`),
  KEY `idx_vdetalle_producto` (`uuid_producto`),
  KEY `idx_vdetalle_venta` (`uuid_venta`),
  CONSTRAINT `ventas_detalle_ibfk_1` FOREIGN KEY (`uuid_venta`) REFERENCES `ventas_encabezado` (`uuid_venta`),
  CONSTRAINT `ventas_detalle_ibfk_2` FOREIGN KEY (`uuid_producto`) REFERENCES `productos_terminados` (`uuid_producto`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ventas_detalle`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `ventas_detalle` WRITE;
/*!40000 ALTER TABLE `ventas_detalle` DISABLE KEYS */;
INSERT INTO `ventas_detalle` VALUES
('1a10e895-f44d-4f79-af30-63f70a5db932','86416f3f-f6f0-4038-9115-e607b29b2065','df050db0-6adb-4df9-a8e7-7d165910a1c1',2,1200.00),
('26a529e8-fd35-4570-8b5e-efaf22c0f24f','92185f1f-df42-4ced-8a62-949c6dd3c19b','5db8bfe1-35fc-4355-804e-58b33358aa42',2,450.00),
('d8a705f3-ebd3-4d49-b728-17d5038f4163','92185f1f-df42-4ced-8a62-949c6dd3c19b','df050db0-6adb-4df9-a8e7-7d165910a1c1',1,1200.00);
/*!40000 ALTER TABLE `ventas_detalle` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `ventas_encabezado`
--

DROP TABLE IF EXISTS `ventas_encabezado`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `ventas_encabezado` (
  `uuid_venta` varchar(36) NOT NULL,
  `numero_pedido` varchar(25) NOT NULL,
  `uuid_cliente` varchar(36) NOT NULL,
  `metodo_pago` varchar(50) DEFAULT NULL,
  `estatus_envio` enum('Procesando','Enviado','Entregado','Devuelto','Completado','Pendiente','Cancelado') DEFAULT NULL,
  `fecha_venta` datetime DEFAULT (now()),
  `fecha_actualizacion` datetime DEFAULT (now()),
  PRIMARY KEY (`uuid_venta`),
  UNIQUE KEY `numero_pedido` (`numero_pedido`),
  KEY `uuid_cliente` (`uuid_cliente`),
  KEY `idx_venta_fecha` (`fecha_venta`),
  CONSTRAINT `ventas_encabezado_ibfk_1` FOREIGN KEY (`uuid_cliente`) REFERENCES `clientes` (`uuid_cliente`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ventas_encabezado`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `ventas_encabezado` WRITE;
/*!40000 ALTER TABLE `ventas_encabezado` DISABLE KEYS */;
INSERT INTO `ventas_encabezado` VALUES
('86416f3f-f6f0-4038-9115-e607b29b2065','AX-102','10fb9e73-761a-48f7-81f8-0a80c7b7fae2','Paypal','Procesando','2026-04-13 02:58:16','2026-04-13 02:58:16'),
('92185f1f-df42-4ced-8a62-949c6dd3c19b','AX-101','10fb9e73-761a-48f7-81f8-0a80c7b7fae2','Tarjeta','Entregado','2026-04-13 02:58:16','2026-04-13 02:58:16');
/*!40000 ALTER TABLE `ventas_encabezado` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*M!100616 SET NOTE_VERBOSITY=@OLD_NOTE_VERBOSITY */;

-- Dump completed on 2026-04-13  3:20:37
