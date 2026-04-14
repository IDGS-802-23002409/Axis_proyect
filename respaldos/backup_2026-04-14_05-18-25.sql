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
('1d409b69-d01d-4159-b250-369bd64f1c59','Camisetas','Prendas de cuerpo superior','/static/images/default/default-image.png',1,'2026-04-14 05:17:41','2026-04-14 05:17:41',NULL,NULL),
('3a79ee50-1857-4904-819e-86655e012d38','Accesorios','Gorras y complementos','/static/images/default/default-image.png',1,'2026-04-14 05:17:41','2026-04-14 05:17:41',NULL,NULL),
('6f9f4cad-ff96-4977-8aab-aedc05abe6d1','Shorts','Pantalones cortos','/static/images/default/default-image.png',1,'2026-04-14 05:17:41','2026-04-14 05:17:41',NULL,NULL),
('82109e1a-a626-42f4-ae57-a663eba5559a','Hoodies','Sudaderas urbanas','/static/images/default/default-image.png',1,'2026-04-14 05:17:41','2026-04-14 05:17:41',NULL,NULL),
('939bc74a-7ec0-4b0e-b526-1f509b404732','Pantalones','Prendas inferiores','/static/images/default/default-image.png',1,'2026-04-14 05:17:41','2026-04-14 05:17:41',NULL,NULL),
('c1cc319f-5db7-4653-83ad-9ca95ec398ec','Chaquetas','Abrigos y chamarras','/static/images/default/default-image.png',1,'2026-04-14 05:17:41','2026-04-14 05:17:41',NULL,NULL);
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
('2ef2c1e2-6706-404d-b21e-1cc5f3915521','241f46af-6609-474a-8457-a4ff102e38f2','555-987-6543','Insurgentes Sur 456, CDMX','2026-04-14 05:17:41','2026-04-14 05:17:41',NULL),
('66a5d28d-f4f4-4003-8b46-9cb0d5c60235','ea24a0f4-c26e-40c5-9253-4261a90f8bef','555-123-4567','Av. Reforma 123, CDMX','2026-04-14 05:17:40','2026-04-14 05:17:40',NULL);
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
  `fecha_creacion` datetime DEFAULT (now()),
  `fecha_actualizacion` datetime DEFAULT (now()),
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
('4ba1e1d5-9a06-4d4a-bc19-01ff92911b1c','8669781b-2226-44a5-8bbc-149bca7b8143','6fa71ea2-95f2-4268-b3be-9d5b434e0bbb',5.0000,220.00,'2026-04-14 05:17:41','2026-04-14 05:17:41'),
('65f9aeb8-d802-4dd0-bd7e-a9faf4270072','3dca4cfa-4e85-4b88-bbe8-651ec098dd6f','d34a1441-5bd6-456c-a27e-f7ccd9396b6f',500.0000,5.00,'2026-04-14 05:17:41','2026-04-14 05:17:41'),
('e2e37a1b-ae70-4a14-b5e9-820140f2b562','3a1dc7d5-05e9-4bed-8fb7-72a54c358a7b','9683f566-2d52-42d5-ad2c-d09aad2f6c1e',10.0000,150.00,'2026-04-14 05:17:41','2026-04-14 05:17:41'),
('ea7e339d-0487-4e9c-b75b-4028867c01a7','57e38e01-b330-4466-a925-cd374dc02ce3','b86c4c6e-9e3e-44af-8eae-665e4ada1e43',100.0000,12.00,'2026-04-14 05:17:41','2026-04-14 05:17:41');
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
  `fecha_actualizacion` datetime DEFAULT (now()),
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
('3a1dc7d5-05e9-4bed-8fb7-72a54c358a7b','FAC-INS-TEX-001-99','f9476d8f-02ef-4486-8ec6-71839fb17a86','cb42c028-4deb-48b3-a57b-49c391951b81','686c821b-9b6d-4778-924c-3cff7ee637b8','2026-04-14 05:17:41','2026-04-14 05:17:41','RECIBIDO'),
('3dca4cfa-4e85-4b88-bbe8-651ec098dd6f','FAC-INS-ACC-003-99','a4729e74-4f94-4f47-a9c5-de6395bf5420','cb42c028-4deb-48b3-a57b-49c391951b81','7998623f-4d76-45e5-bf18-fea9e0af7b6e','2026-04-14 05:17:41','2026-04-14 05:17:41','RECIBIDO'),
('57e38e01-b330-4466-a925-cd374dc02ce3','FAC-INS-ACC-001-99','a4729e74-4f94-4f47-a9c5-de6395bf5420','cb42c028-4deb-48b3-a57b-49c391951b81','e2684230-6cca-4339-a594-04336a376553','2026-04-14 05:17:41','2026-04-14 05:17:41','RECIBIDO'),
('8669781b-2226-44a5-8bbc-149bca7b8143','FAC-INS-TEX-002-99','f9476d8f-02ef-4486-8ec6-71839fb17a86','cb42c028-4deb-48b3-a57b-49c391951b81','cf3c0505-c50f-4f4f-b8db-121af6103586','2026-04-14 05:17:41','2026-04-14 05:17:41','RECIBIDO');
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
  `fecha_actualizacion` datetime DEFAULT (now()),
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
('8700dc3c-2440-4c49-ac05-9d532d876725','37986269-3809-48e8-b309-3b0a176318f4','063f0100-5888-473a-bf05-7cd2e8fe7cdd',25.0000,26.5000,10,1.5000,'2026-04-14 05:17:41','2026-04-14 05:17:41','cb42c028-4deb-48b3-a57b-49c391951b81');
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
('796666bd-57b0-475e-8d6c-fa76308b3dbc','3bdd7de8-8ffd-4334-8ee9-d62d8741b499','EMP-002','Jefe de Taller','Producción','2025-04-14 05:17:41','2026-04-14 05:17:40','2026-04-14 05:17:40'),
('a98ce903-f6f9-47e9-a4ae-fbaa9818de57','cb42c028-4deb-48b3-a57b-49c391951b81','EMP-001','Director General','Dirección','2025-04-14 05:17:40','2026-04-14 05:17:40','2026-04-14 05:17:40'),
('e22b0e9d-9064-4e85-832b-7a717890dc97','0f107056-f010-4f27-96c9-5b1256149525','EMP-004','Analista de Suministros','Compras','2025-04-14 05:17:41','2026-04-14 05:17:40','2026-04-14 05:17:40'),
('f19ad1ba-5c7a-43c6-b61e-3fe130d0e398','9a25da8a-8f13-4b20-8560-038e6330f456','EMP-003','Ejecutivo Comercial','Ventas','2025-04-14 05:17:41','2026-04-14 05:17:40','2026-04-14 05:17:40');
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
  `fecha_creacion` datetime DEFAULT (now()),
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
('bd36b3fe-a21e-4ab0-971c-e10527e41339','Corte láser y costura reforzada.','2026-04-14 05:17:41','2026-04-14 05:17:41','cb42c028-4deb-48b3-a57b-49c391951b81','ACTIVO'),
('eda16cbb-b7cc-4989-a17e-b021e7fe9039','Costura plana a dos hilos.','2026-04-14 05:17:41','2026-04-14 05:17:41','cb42c028-4deb-48b3-a57b-49c391951b81','ACTIVO');
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
  `fecha_creacion` datetime DEFAULT (now()),
  `fecha_actualizacion` datetime DEFAULT (now()),
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
('185067ff-0264-430c-b54e-b7c8ed9f4786','bd36b3fe-a21e-4ab0-971c-e10527e41339','b86c4c6e-9e3e-44af-8eae-665e4ada1e43',1.0000,NULL,'2026-04-14 05:17:41','2026-04-14 05:17:41'),
('21925821-5b8a-4878-a19e-17263b3f5251','bd36b3fe-a21e-4ab0-971c-e10527e41339','d34a1441-5bd6-456c-a27e-f7ccd9396b6f',1.0000,NULL,'2026-04-14 05:17:41','2026-04-14 05:17:41'),
('318c84a7-58ba-4aca-be37-65839beafa27','eda16cbb-b7cc-4989-a17e-b021e7fe9039','9683f566-2d52-42d5-ad2c-d09aad2f6c1e',1.2000,NULL,'2026-04-14 05:17:41','2026-04-14 05:17:41'),
('50ded2e7-0359-4d1c-aea0-62104083208c','eda16cbb-b7cc-4989-a17e-b021e7fe9039','d34a1441-5bd6-456c-a27e-f7ccd9396b6f',1.0000,NULL,'2026-04-14 05:17:41','2026-04-14 05:17:41'),
('ed97dc42-65cb-445e-8366-acaf6b92a3af','bd36b3fe-a21e-4ab0-971c-e10527e41339','6fa71ea2-95f2-4268-b3be-9d5b434e0bbb',2.5000,NULL,'2026-04-14 05:17:41','2026-04-14 05:17:41');
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
('368b8aa1-ab0a-441f-a47d-a1fd336ccb9f','INS-ACC-002','Botón Acero Inoxidable','939bc74a-7ec0-4b0e-b526-1f509b404732','PIEZA',1.0000,'PIEZA',0.0000,10.0000,NULL,'2026-04-14 05:17:41','2026-04-14 05:17:41','ACTIVO',NULL),
('6fa71ea2-95f2-4268-b3be-9d5b434e0bbb','INS-TEX-002','Poliéster Gris Roll','82109e1a-a626-42f4-ae57-a663eba5559a','ROLLO',50.0000,'METRO',250.0000,10.0000,NULL,'2026-04-14 05:17:41','2026-04-14 05:17:41','ACTIVO',NULL),
('86ba119e-b2b7-4b03-b7dd-bdeaa1b858c7','INS-TEX-003','Denim Azul 14oz','939bc74a-7ec0-4b0e-b526-1f509b404732','ROLLO',40.0000,'METRO',0.0000,10.0000,NULL,'2026-04-14 05:17:41','2026-04-14 05:17:41','ACTIVO',NULL),
('9683f566-2d52-42d5-ad2c-d09aad2f6c1e','INS-TEX-001','Algodón Negro Roll','1d409b69-d01d-4159-b250-369bd64f1c59','ROLLO',100.0000,'METRO',1000.0000,10.0000,NULL,'2026-04-14 05:17:41','2026-04-14 05:17:41','ACTIVO',NULL),
('b86c4c6e-9e3e-44af-8eae-665e4ada1e43','INS-ACC-001','Cierre Metálico YKK 15cm','c1cc319f-5db7-4653-83ad-9ca95ec398ec','PIEZA',1.0000,'PIEZA',100.0000,10.0000,NULL,'2026-04-14 05:17:41','2026-04-14 05:17:41','ACTIVO',NULL),
('d34a1441-5bd6-456c-a27e-f7ccd9396b6f','INS-ACC-003','Etiqueta Axis Bordada','3a79ee50-1857-4904-819e-86655e012d38','PIEZA',1.0000,'PIEZA',500.0000,10.0000,NULL,'2026-04-14 05:17:41','2026-04-14 05:17:41','ACTIVO',NULL);
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
  `fecha_actualizacion` datetime DEFAULT (now()),
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
('1eec0ea8-0583-4730-a7b0-4bc4cd6396cb','37986269-3809-48e8-b309-3b0a176318f4','d34a1441-5bd6-456c-a27e-f7ccd9396b6f',10.0000,12.0000,'ERROR_OPERARIO','2 etiquetas se dañaron al coser.','2026-04-14 05:17:41','2026-04-14 05:17:41','cb42c028-4deb-48b3-a57b-49c391951b81');
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
('c166ec2b-1862-4452-b4d0-a445fc7a2869','Hoodie Oversight Black','Sudadera pesada con fit urbano.','82109e1a-a626-42f4-ae57-a663eba5559a','/static/images/products/hoodie-black.jpg','2026-04-14 05:17:41','2026-04-14 05:17:41','ACTIVO'),
('e485a914-472a-4a17-875e-787ace4e9174','Axis Logo Tee White','Camiseta 100% algodón alta densidad.','1d409b69-d01d-4159-b250-369bd64f1c59','/static/images/products/tshirt-white.jpg','2026-04-14 05:17:41','2026-04-14 05:17:41','ACTIVO');
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
  `fecha_actualizacion` datetime DEFAULT (now()),
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
('37986269-3809-48e8-b309-3b0a176318f4','ee304c05-f322-4fa6-a6a8-8d2c9c52788a','6bbc2e24-c959-4972-8c92-2568b6eef435',NULL,10,'Terminado','2026-04-14 05:17:41','2026-04-14 05:17:41'),
('7467a944-cde4-40a1-83fa-3e9a2c680d2a','a1ead39f-6c9d-4bf5-9e3a-0119f7b73836',NULL,NULL,30,'Pendiente','2026-04-14 05:17:41','2026-04-14 05:17:41');
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
  `fecha_creacion` datetime DEFAULT (now()),
  `fecha_actualizacion` datetime DEFAULT (now()),
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
  `fecha_creacion` datetime DEFAULT (now()),
  `fecha_actualizacion` datetime DEFAULT (now()),
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
('226eea2f-773d-4063-9014-8b99d23c8ac4','e2684230-6cca-4339-a594-04336a376553','b86c4c6e-9e3e-44af-8eae-665e4ada1e43',100.0000,0.0000,12.00,'2026-04-14 05:17:41','2026-04-14 05:17:41'),
('9b9e7200-56c3-44c3-a426-f51ecd5ff085','686c821b-9b6d-4778-924c-3cff7ee637b8','9683f566-2d52-42d5-ad2c-d09aad2f6c1e',10.0000,0.0000,150.00,'2026-04-14 05:17:41','2026-04-14 05:17:41'),
('a98aa9b2-91a6-4927-a52f-a6d2935c8c9f','7998623f-4d76-45e5-bf18-fea9e0af7b6e','d34a1441-5bd6-456c-a27e-f7ccd9396b6f',500.0000,0.0000,5.00,'2026-04-14 05:17:41','2026-04-14 05:17:41'),
('b487654f-4677-4d41-9834-1c9789f21034','cf3c0505-c50f-4f4f-b8db-121af6103586','6fa71ea2-95f2-4268-b3be-9d5b434e0bbb',5.0000,0.0000,220.00,'2026-04-14 05:17:41','2026-04-14 05:17:41');
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
  `fecha_actualizacion` datetime DEFAULT (now()),
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
('686c821b-9b6d-4778-924c-3cff7ee637b8','PED-INS-TEX-001','f9476d8f-02ef-4486-8ec6-71839fb17a86','cb42c028-4deb-48b3-a57b-49c391951b81','2026-04-14 05:17:41','2026-04-14 05:17:41','Completado'),
('7998623f-4d76-45e5-bf18-fea9e0af7b6e','PED-INS-ACC-003','a4729e74-4f94-4f47-a9c5-de6395bf5420','cb42c028-4deb-48b3-a57b-49c391951b81','2026-04-14 05:17:41','2026-04-14 05:17:41','Completado'),
('cf3c0505-c50f-4f4f-b8db-121af6103586','PED-INS-TEX-002','f9476d8f-02ef-4486-8ec6-71839fb17a86','cb42c028-4deb-48b3-a57b-49c391951b81','2026-04-14 05:17:41','2026-04-14 05:17:41','Completado'),
('e2684230-6cca-4339-a594-04336a376553','PED-INS-ACC-001','a4729e74-4f94-4f47-a9c5-de6395bf5420','cb42c028-4deb-48b3-a57b-49c391951b81','2026-04-14 05:17:41','2026-04-14 05:17:41','Completado');
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
('0dd48e40-dc72-47e2-bcf9-77b6b527cbda','c166ec2b-1862-4452-b4d0-a445fc7a2869','bd36b3fe-a21e-4ab0-971c-e10527e41339','H-OV-BLK-L','L',1200.00,24,0,1,'2026-04-14 05:17:41','2026-04-14 05:17:41'),
('0f52bce7-4a50-496e-aa05-cc950af4f04a','e485a914-472a-4a17-875e-787ace4e9174','eda16cbb-b7cc-4989-a17e-b021e7fe9039','T-LOG-WHT-S','S',450.00,47,0,1,'2026-04-14 05:17:41','2026-04-14 05:17:41'),
('5a0ca62c-b6e5-4f23-935e-aec6eaf695a9','c166ec2b-1862-4452-b4d0-a445fc7a2869','bd36b3fe-a21e-4ab0-971c-e10527e41339','H-OV-BLK-S','S',1200.00,43,0,1,'2026-04-14 05:17:41','2026-04-14 05:17:41'),
('6e308e67-27b2-49b2-8e18-2c63972d7727','c166ec2b-1862-4452-b4d0-a445fc7a2869','bd36b3fe-a21e-4ab0-971c-e10527e41339','H-OV-BLK-XL','XL',1200.00,44,0,1,'2026-04-14 05:17:41','2026-04-14 05:17:41'),
('a1ead39f-6c9d-4bf5-9e3a-0119f7b73836','e485a914-472a-4a17-875e-787ace4e9174','eda16cbb-b7cc-4989-a17e-b021e7fe9039','T-LOG-WHT-L','L',450.00,46,0,1,'2026-04-14 05:17:41','2026-04-14 05:17:41'),
('b6d9fef6-64ed-4f91-858c-b1f39c4c6173','e485a914-472a-4a17-875e-787ace4e9174','eda16cbb-b7cc-4989-a17e-b021e7fe9039','T-LOG-WHT-XL','XL',450.00,24,0,1,'2026-04-14 05:17:41','2026-04-14 05:17:41'),
('ee304c05-f322-4fa6-a6a8-8d2c9c52788a','c166ec2b-1862-4452-b4d0-a445fc7a2869','bd36b3fe-a21e-4ab0-971c-e10527e41339','H-OV-BLK-M','M',1200.00,47,0,1,'2026-04-14 05:17:41','2026-04-14 05:17:41'),
('f9cdb67e-7f17-4d91-a6a2-1631d4864de5','e485a914-472a-4a17-875e-787ace4e9174','eda16cbb-b7cc-4989-a17e-b021e7fe9039','T-LOG-WHT-M','M',450.00,19,0,1,'2026-04-14 05:17:41','2026-04-14 05:17:41');
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
('4b4a6853-e6c7-4c10-986b-b261141c07ad','Hilos y Avíos del Norte','HIL220301HAN','Roberto','2026-04-14 05:17:41','2026-04-14 05:17:41',NULL,1,'818-200-1010','Otros'),
('a4729e74-4f94-4f47-a9c5-de6395bf5420','Accesorios Industriales','ACC850505XYZ','Carlos','2026-04-14 05:17:41','2026-04-14 05:17:41',NULL,1,'555-300-4000','Otros'),
('f9476d8f-02ef-4486-8ec6-71839fb17a86','Textiles Premium S.A.','TEX900101ABC','Elena','2026-04-14 05:17:41','2026-04-14 05:17:41',NULL,1,'555-100-2000','Textiles');
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
  `fecha_actualizacion` datetime DEFAULT (now()),
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
('cb42c028-4deb-48b3-a57b-49c391951b81',1),
('3bdd7de8-8ffd-4334-8ee9-d62d8741b499',3),
('9a25da8a-8f13-4b20-8560-038e6330f456',2),
('0f107056-f010-4f27-96c9-5b1256149525',3),
('ea24a0f4-c26e-40c5-9253-4261a90f8bef',4),
('241f46af-6609-474a-8457-a4ff102e38f2',4);
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
  `fecha_actualizacion` datetime DEFAULT (now()),
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
('063f0100-5888-473a-bf05-7cd2e8fe7cdd','6fa71ea2-95f2-4268-b3be-9d5b434e0bbb','4ba1e1d5-9a06-4d4a-bc19-01ff92911b1c',50.0000,23.5000,'2026-04-14 05:17:41','2026-04-14 05:17:41'),
('0b5dba2e-2568-4e76-9bdb-18846857e18a','9683f566-2d52-42d5-ad2c-d09aad2f6c1e','e2e37a1b-ae70-4a14-b5e9-820140f2b562',100.0000,100.0000,'2026-04-14 05:17:41','2026-04-14 05:17:41'),
('0de1756c-6850-41ad-9093-39a7a90fd46a','6fa71ea2-95f2-4268-b3be-9d5b434e0bbb','4ba1e1d5-9a06-4d4a-bc19-01ff92911b1c',50.0000,50.0000,'2026-04-14 05:17:41','2026-04-14 05:17:41'),
('21858eb7-ee33-46e2-b865-7dff62ec6ec9','6fa71ea2-95f2-4268-b3be-9d5b434e0bbb','4ba1e1d5-9a06-4d4a-bc19-01ff92911b1c',50.0000,50.0000,'2026-04-14 05:17:41','2026-04-14 05:17:41'),
('2239bfbd-a9d4-4a1a-938a-e27a08a0933e','9683f566-2d52-42d5-ad2c-d09aad2f6c1e','e2e37a1b-ae70-4a14-b5e9-820140f2b562',100.0000,100.0000,'2026-04-14 05:17:41','2026-04-14 05:17:41'),
('295f26cb-ab6e-4f55-aa18-e031a90abf25','9683f566-2d52-42d5-ad2c-d09aad2f6c1e','e2e37a1b-ae70-4a14-b5e9-820140f2b562',100.0000,100.0000,'2026-04-14 05:17:41','2026-04-14 05:17:41'),
('2bb9d9f2-889e-4472-a38e-3edce127d0c7','6fa71ea2-95f2-4268-b3be-9d5b434e0bbb','4ba1e1d5-9a06-4d4a-bc19-01ff92911b1c',50.0000,50.0000,'2026-04-14 05:17:41','2026-04-14 05:17:41'),
('306e6950-c6a2-4598-b372-616b84cdeb5d','9683f566-2d52-42d5-ad2c-d09aad2f6c1e','e2e37a1b-ae70-4a14-b5e9-820140f2b562',100.0000,100.0000,'2026-04-14 05:17:41','2026-04-14 05:17:41'),
('52076f85-5416-48dd-b27d-ad7d1f5c736c','9683f566-2d52-42d5-ad2c-d09aad2f6c1e','e2e37a1b-ae70-4a14-b5e9-820140f2b562',100.0000,100.0000,'2026-04-14 05:17:41','2026-04-14 05:17:41'),
('60ad53b9-b13b-4e0d-bf0c-e789eb2c4154','9683f566-2d52-42d5-ad2c-d09aad2f6c1e','e2e37a1b-ae70-4a14-b5e9-820140f2b562',100.0000,100.0000,'2026-04-14 05:17:41','2026-04-14 05:17:41'),
('671876d5-1e8a-4a83-80a1-e334ef5a1d0e','9683f566-2d52-42d5-ad2c-d09aad2f6c1e','e2e37a1b-ae70-4a14-b5e9-820140f2b562',100.0000,100.0000,'2026-04-14 05:17:41','2026-04-14 05:17:41'),
('6c79da94-b5ea-4110-9273-94207ecaa67e','6fa71ea2-95f2-4268-b3be-9d5b434e0bbb','4ba1e1d5-9a06-4d4a-bc19-01ff92911b1c',50.0000,50.0000,'2026-04-14 05:17:41','2026-04-14 05:17:41'),
('c49101ac-27b5-4585-a7d3-3e0bd3ab57ef','9683f566-2d52-42d5-ad2c-d09aad2f6c1e','e2e37a1b-ae70-4a14-b5e9-820140f2b562',100.0000,100.0000,'2026-04-14 05:17:41','2026-04-14 05:17:41'),
('e2b8b983-21c8-48e2-abfb-e8545f4a9d5a','9683f566-2d52-42d5-ad2c-d09aad2f6c1e','e2e37a1b-ae70-4a14-b5e9-820140f2b562',100.0000,100.0000,'2026-04-14 05:17:41','2026-04-14 05:17:41'),
('fa7c40ca-f6f8-471a-b5a7-049a358844a3','9683f566-2d52-42d5-ad2c-d09aad2f6c1e','e2e37a1b-ae70-4a14-b5e9-820140f2b562',100.0000,100.0000,'2026-04-14 05:17:41','2026-04-14 05:17:41');
/*!40000 ALTER TABLE `rollos_inventario` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `security_audit_logs`
--

DROP TABLE IF EXISTS `security_audit_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `security_audit_logs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `uuid_usuario` varchar(36) DEFAULT NULL,
  `nombre_usuario` varchar(150) DEFAULT NULL,
  `rol_usuario` varchar(80) DEFAULT NULL,
  `usuario_bd` varchar(80) DEFAULT NULL,
  `accion` varchar(20) NOT NULL,
  `tabla` varchar(100) NOT NULL,
  `registro_uuid` varchar(36) NOT NULL,
  `valores_anteriores` json DEFAULT NULL,
  `valores_nuevos` json DEFAULT NULL,
  `ip_direccion` varchar(45) DEFAULT NULL,
  `fecha` datetime DEFAULT (now()),
  PRIMARY KEY (`id`),
  KEY `ix_security_audit_logs_registro_uuid` (`registro_uuid`),
  KEY `ix_security_audit_logs_fecha` (`fecha`),
  KEY `ix_security_audit_logs_uuid_usuario` (`uuid_usuario`),
  KEY `ix_security_audit_logs_tabla` (`tabla`)
) ENGINE=InnoDB AUTO_INCREMENT=95 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `security_audit_logs`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `security_audit_logs` WRITE;
/*!40000 ALTER TABLE `security_audit_logs` DISABLE KEYS */;
INSERT INTO `security_audit_logs` VALUES
(1,'Sistema','Sistema','Sistema','default','INSERT','role','N/A',NULL,'{\"id\": null, \"name\": \"admin\", \"description\": null}',NULL,'2026-04-14 05:17:40'),
(2,'Sistema','Sistema','Sistema','default','INSERT','role','N/A',NULL,'{\"id\": null, \"name\": \"gerente\", \"description\": null}',NULL,'2026-04-14 05:17:40'),
(3,'Sistema','Sistema','Sistema','default','INSERT','role','N/A',NULL,'{\"id\": null, \"name\": \"produccion\", \"description\": null}',NULL,'2026-04-14 05:17:40'),
(4,'Sistema','Sistema','Sistema','default','INSERT','role','N/A',NULL,'{\"id\": null, \"name\": \"cliente\", \"description\": null}',NULL,'2026-04-14 05:17:40'),
(5,'Sistema','Sistema','Sistema','default','INSERT','usuarios','N/A',NULL,'{\"email\": \"admin@axis.com\", \"active\": true, \"password\": \"$argon2id$v=19$m=65536,t=3,p=4$ozQGoBSCkLI2RmiNMYYQAg$L5Q5/7wb4Ye7x7zU68kiD+ojenPyDHhT0Fb9TvaM/Bs\", \"confirmed_at\": \"2026-04-14T05:17:40.454210+00:00\", \"uuid_usuario\": null, \"fs_uniquifier\": null, \"fecha_creacion\": null, \"tf_totp_secret\": null, \"nombre_completo\": \"Admin Axis\", \"tf_phone_number\": null, \"mf_recovery_codes\": null, \"tf_primary_method\": null, \"fecha_actualizacion\": null, \"password_changed_at\": null}',NULL,'2026-04-14 05:17:40'),
(6,'Sistema','Sistema','Sistema','default','INSERT','empleados','N/A',NULL,'{\"puesto\": \"Director General\", \"departamento\": \"Dirección\", \"uuid_usuario\": \"cb42c028-4deb-48b3-a57b-49c391951b81\", \"fecha_ingreso\": \"2025-04-14T05:17:40.477899+00:00\", \"uuid_empleado\": null, \"fecha_creacion\": null, \"numero_empleado\": \"EMP-001\", \"fecha_actualizacion\": null}',NULL,'2026-04-14 05:17:40'),
(7,'Sistema','Sistema','Sistema','default','INSERT','usuarios','N/A',NULL,'{\"email\": \"modista@axis.com\", \"active\": true, \"password\": \"$argon2id$v=19$m=65536,t=3,p=4$iRGiVEpJybmXUqq11tobYw$/28lPNikQn3oQMR4+myG0gKO0ToVf7GjnTaC/iKenN8\", \"confirmed_at\": \"2026-04-14T05:17:40.605648+00:00\", \"uuid_usuario\": null, \"fs_uniquifier\": null, \"fecha_creacion\": null, \"tf_totp_secret\": null, \"nombre_completo\": \"Modista Principal\", \"tf_phone_number\": null, \"mf_recovery_codes\": null, \"tf_primary_method\": null, \"fecha_actualizacion\": null, \"password_changed_at\": null}',NULL,'2026-04-14 05:17:40'),
(8,'Sistema','Sistema','Sistema','default','INSERT','empleados','N/A',NULL,'{\"puesto\": \"Jefe de Taller\", \"departamento\": \"Producción\", \"uuid_usuario\": \"3bdd7de8-8ffd-4334-8ee9-d62d8741b499\", \"fecha_ingreso\": \"2025-04-14T05:17:40.615668+00:00\", \"uuid_empleado\": null, \"fecha_creacion\": null, \"numero_empleado\": \"EMP-002\", \"fecha_actualizacion\": null}',NULL,'2026-04-14 05:17:40'),
(9,'Sistema','Sistema','Sistema','default','INSERT','usuarios','N/A',NULL,'{\"email\": \"ventas@axis.com\", \"active\": true, \"password\": \"$argon2id$v=19$m=65536,t=3,p=4$zzknJGQsJUQIQWjNmbOWcg$Yc6wgGYa0Ebbso7orSYbXhceMvTsmlEl4hi5R65dWJc\", \"confirmed_at\": \"2026-04-14T05:17:40.731261+00:00\", \"uuid_usuario\": null, \"fs_uniquifier\": null, \"fecha_creacion\": null, \"tf_totp_secret\": null, \"nombre_completo\": \"Vendedor Axis\", \"tf_phone_number\": null, \"mf_recovery_codes\": null, \"tf_primary_method\": null, \"fecha_actualizacion\": null, \"password_changed_at\": null}',NULL,'2026-04-14 05:17:40'),
(10,'Sistema','Sistema','Sistema','default','INSERT','empleados','N/A',NULL,'{\"puesto\": \"Ejecutivo Comercial\", \"departamento\": \"Ventas\", \"uuid_usuario\": \"9a25da8a-8f13-4b20-8560-038e6330f456\", \"fecha_ingreso\": \"2025-04-14T05:17:40.742708+00:00\", \"uuid_empleado\": null, \"fecha_creacion\": null, \"numero_empleado\": \"EMP-003\", \"fecha_actualizacion\": null}',NULL,'2026-04-14 05:17:40'),
(11,'Sistema','Sistema','Sistema','default','INSERT','usuarios','N/A',NULL,'{\"email\": \"compras@axis.com\", \"active\": true, \"password\": \"$argon2id$v=19$m=65536,t=3,p=4$BOD8n/N+LwXAmFPKGSNEaA$yN6AzzjkCFq2j3ZqHPGI+NjBzbnDFx7AT3fOw1gLW6g\", \"confirmed_at\": \"2026-04-14T05:17:40.852130+00:00\", \"uuid_usuario\": null, \"fs_uniquifier\": null, \"fecha_creacion\": null, \"tf_totp_secret\": null, \"nombre_completo\": \"Comprador Axis\", \"tf_phone_number\": null, \"mf_recovery_codes\": null, \"tf_primary_method\": null, \"fecha_actualizacion\": null, \"password_changed_at\": null}',NULL,'2026-04-14 05:17:40'),
(12,'Sistema','Sistema','Sistema','default','INSERT','empleados','N/A',NULL,'{\"puesto\": \"Analista de Suministros\", \"departamento\": \"Compras\", \"uuid_usuario\": \"0f107056-f010-4f27-96c9-5b1256149525\", \"fecha_ingreso\": \"2025-04-14T05:17:40.861101+00:00\", \"uuid_empleado\": null, \"fecha_creacion\": null, \"numero_empleado\": \"EMP-004\", \"fecha_actualizacion\": null}',NULL,'2026-04-14 05:17:40'),
(13,'Sistema','Sistema','Sistema','default','INSERT','usuarios','N/A',NULL,'{\"email\": \"juan@axis.com\", \"active\": true, \"password\": \"$argon2id$v=19$m=65536,t=3,p=4$7733HkNIyZkT4lxrzfmfMw$8Irvge3nRT6BBETpUwAD0hVHuruRPN8OhzsE0J2ouCU\", \"confirmed_at\": \"2026-04-14T05:17:40.977208+00:00\", \"uuid_usuario\": null, \"fs_uniquifier\": null, \"fecha_creacion\": null, \"tf_totp_secret\": null, \"nombre_completo\": \"Juan Cliente\", \"tf_phone_number\": null, \"mf_recovery_codes\": null, \"tf_primary_method\": null, \"fecha_actualizacion\": null, \"password_changed_at\": null}',NULL,'2026-04-14 05:17:40'),
(14,'Sistema','Sistema','Sistema','default','INSERT','clientes','N/A',NULL,'{\"telefono\": \"555-123-4567\", \"uuid_cliente\": null, \"uuid_usuario\": \"ea24a0f4-c26e-40c5-9253-4261a90f8bef\", \"fecha_creacion\": null, \"direccion_completa\": \"Av. Reforma 123, CDMX\", \"fecha_actualizacion\": null, \"usuario_actualizo_uuid\": null}',NULL,'2026-04-14 05:17:40'),
(15,'Sistema','Sistema','Sistema','default','INSERT','usuarios','N/A',NULL,'{\"email\": \"maria@axis.com\", \"active\": true, \"password\": \"$argon2id$v=19$m=65536,t=3,p=4$zFkrRag1RiillPIeg5BSyg$cg0I4IJxIFupV5dU27/d8oa1oKTo7DU3ccJUhEsf/NU\", \"confirmed_at\": \"2026-04-14T05:17:41.128801+00:00\", \"uuid_usuario\": null, \"fs_uniquifier\": null, \"fecha_creacion\": null, \"tf_totp_secret\": null, \"nombre_completo\": \"Maria Lopez\", \"tf_phone_number\": null, \"mf_recovery_codes\": null, \"tf_primary_method\": null, \"fecha_actualizacion\": null, \"password_changed_at\": null}',NULL,'2026-04-14 05:17:41'),
(16,'Sistema','Sistema','Sistema','default','INSERT','clientes','N/A',NULL,'{\"telefono\": \"555-987-6543\", \"uuid_cliente\": null, \"uuid_usuario\": \"241f46af-6609-474a-8457-a4ff102e38f2\", \"fecha_creacion\": null, \"direccion_completa\": \"Insurgentes Sur 456, CDMX\", \"fecha_actualizacion\": null, \"usuario_actualizo_uuid\": null}',NULL,'2026-04-14 05:17:41'),
(17,'Sistema','Sistema','Sistema','default','INSERT','categorias','N/A',NULL,'{\"nombre\": \"Camisetas\", \"imagen_url\": null, \"descripcion\": \"Prendas de cuerpo superior\", \"fecha_creacion\": null, \"uuid_categoria\": null, \"estatus_visible\": true, \"usuario_creo_uuid\": null, \"fecha_actualizacion\": null, \"usuario_actualizo_uuid\": null}',NULL,'2026-04-14 05:17:41'),
(18,'Sistema','Sistema','Sistema','default','INSERT','categorias','N/A',NULL,'{\"nombre\": \"Pantalones\", \"imagen_url\": null, \"descripcion\": \"Prendas inferiores\", \"fecha_creacion\": null, \"uuid_categoria\": null, \"estatus_visible\": true, \"usuario_creo_uuid\": null, \"fecha_actualizacion\": null, \"usuario_actualizo_uuid\": null}',NULL,'2026-04-14 05:17:41'),
(19,'Sistema','Sistema','Sistema','default','INSERT','categorias','N/A',NULL,'{\"nombre\": \"Hoodies\", \"imagen_url\": null, \"descripcion\": \"Sudaderas urbanas\", \"fecha_creacion\": null, \"uuid_categoria\": null, \"estatus_visible\": true, \"usuario_creo_uuid\": null, \"fecha_actualizacion\": null, \"usuario_actualizo_uuid\": null}',NULL,'2026-04-14 05:17:41'),
(20,'Sistema','Sistema','Sistema','default','INSERT','categorias','N/A',NULL,'{\"nombre\": \"Chaquetas\", \"imagen_url\": null, \"descripcion\": \"Abrigos y chamarras\", \"fecha_creacion\": null, \"uuid_categoria\": null, \"estatus_visible\": true, \"usuario_creo_uuid\": null, \"fecha_actualizacion\": null, \"usuario_actualizo_uuid\": null}',NULL,'2026-04-14 05:17:41'),
(21,'Sistema','Sistema','Sistema','default','INSERT','categorias','N/A',NULL,'{\"nombre\": \"Shorts\", \"imagen_url\": null, \"descripcion\": \"Pantalones cortos\", \"fecha_creacion\": null, \"uuid_categoria\": null, \"estatus_visible\": true, \"usuario_creo_uuid\": null, \"fecha_actualizacion\": null, \"usuario_actualizo_uuid\": null}',NULL,'2026-04-14 05:17:41'),
(22,'Sistema','Sistema','Sistema','default','INSERT','categorias','N/A',NULL,'{\"nombre\": \"Accesorios\", \"imagen_url\": null, \"descripcion\": \"Gorras y complementos\", \"fecha_creacion\": null, \"uuid_categoria\": null, \"estatus_visible\": true, \"usuario_creo_uuid\": null, \"fecha_actualizacion\": null, \"usuario_actualizo_uuid\": null}',NULL,'2026-04-14 05:17:41'),
(23,'Sistema','Sistema','Sistema','default','INSERT','proveedores','N/A',NULL,'{\"rfc\": \"TEX900101ABC\", \"estatus\": null, \"telefono\": \"555-100-2000\", \"razon_social\": \"Textiles Premium S.A.\", \"fecha_creacion\": null, \"uuid_proveedor\": null, \"contacto_nombre\": \"Elena\", \"categoria_insumo\": \"Textiles\", \"usuario_creo_uuid\": null, \"fecha_actualizacion\": null}',NULL,'2026-04-14 05:17:41'),
(24,'Sistema','Sistema','Sistema','default','INSERT','proveedores','N/A',NULL,'{\"rfc\": \"ACC850505XYZ\", \"estatus\": null, \"telefono\": \"555-300-4000\", \"razon_social\": \"Accesorios Industriales\", \"fecha_creacion\": null, \"uuid_proveedor\": null, \"contacto_nombre\": \"Carlos\", \"categoria_insumo\": \"Otros\", \"usuario_creo_uuid\": null, \"fecha_actualizacion\": null}',NULL,'2026-04-14 05:17:41'),
(25,'Sistema','Sistema','Sistema','default','INSERT','proveedores','N/A',NULL,'{\"rfc\": \"HIL220301HAN\", \"estatus\": null, \"telefono\": \"818-200-1010\", \"razon_social\": \"Hilos y Avíos del Norte\", \"fecha_creacion\": null, \"uuid_proveedor\": null, \"contacto_nombre\": \"Roberto\", \"categoria_insumo\": \"Otros\", \"usuario_creo_uuid\": null, \"fecha_actualizacion\": null}',NULL,'2026-04-14 05:17:41'),
(26,'Sistema','Sistema','Sistema','default','INSERT','insumos','N/A',NULL,'{\"sku\": \"INS-TEX-001\", \"ancho\": null, \"nombre\": \"Algodón Negro Roll\", \"estatus\": null, \"uuid_insumo\": null, \"unidad_medida\": \"ROLLO\", \"fecha_creacion\": null, \"uuid_categoria\": \"1d409b69-d01d-4159-b250-369bd64f1c59\", \"contenido_cantidad\": 100.0, \"fecha_actualizacion\": null, \"stock_minimo_alerta\": 10, \"stock_total_acumulado\": 0, \"usuario_actualizo_uuid\": null, \"contenido_unidad_medida\": \"METRO\"}',NULL,'2026-04-14 05:17:41'),
(27,'Sistema','Sistema','Sistema','default','INSERT','insumos','N/A',NULL,'{\"sku\": \"INS-TEX-002\", \"ancho\": null, \"nombre\": \"Poliéster Gris Roll\", \"estatus\": null, \"uuid_insumo\": null, \"unidad_medida\": \"ROLLO\", \"fecha_creacion\": null, \"uuid_categoria\": \"82109e1a-a626-42f4-ae57-a663eba5559a\", \"contenido_cantidad\": 50.0, \"fecha_actualizacion\": null, \"stock_minimo_alerta\": 10, \"stock_total_acumulado\": 0, \"usuario_actualizo_uuid\": null, \"contenido_unidad_medida\": \"METRO\"}',NULL,'2026-04-14 05:17:41'),
(28,'Sistema','Sistema','Sistema','default','INSERT','insumos','N/A',NULL,'{\"sku\": \"INS-TEX-003\", \"ancho\": null, \"nombre\": \"Denim Azul 14oz\", \"estatus\": null, \"uuid_insumo\": null, \"unidad_medida\": \"ROLLO\", \"fecha_creacion\": null, \"uuid_categoria\": \"939bc74a-7ec0-4b0e-b526-1f509b404732\", \"contenido_cantidad\": 40.0, \"fecha_actualizacion\": null, \"stock_minimo_alerta\": 10, \"stock_total_acumulado\": 0, \"usuario_actualizo_uuid\": null, \"contenido_unidad_medida\": \"METRO\"}',NULL,'2026-04-14 05:17:41'),
(29,'Sistema','Sistema','Sistema','default','INSERT','insumos','N/A',NULL,'{\"sku\": \"INS-ACC-001\", \"ancho\": null, \"nombre\": \"Cierre Metálico YKK 15cm\", \"estatus\": null, \"uuid_insumo\": null, \"unidad_medida\": \"PIEZA\", \"fecha_creacion\": null, \"uuid_categoria\": \"c1cc319f-5db7-4653-83ad-9ca95ec398ec\", \"contenido_cantidad\": 1.0, \"fecha_actualizacion\": null, \"stock_minimo_alerta\": 10, \"stock_total_acumulado\": 0, \"usuario_actualizo_uuid\": null, \"contenido_unidad_medida\": \"PIEZA\"}',NULL,'2026-04-14 05:17:41'),
(30,'Sistema','Sistema','Sistema','default','INSERT','insumos','N/A',NULL,'{\"sku\": \"INS-ACC-002\", \"ancho\": null, \"nombre\": \"Botón Acero Inoxidable\", \"estatus\": null, \"uuid_insumo\": null, \"unidad_medida\": \"PIEZA\", \"fecha_creacion\": null, \"uuid_categoria\": \"939bc74a-7ec0-4b0e-b526-1f509b404732\", \"contenido_cantidad\": 1.0, \"fecha_actualizacion\": null, \"stock_minimo_alerta\": 10, \"stock_total_acumulado\": 0, \"usuario_actualizo_uuid\": null, \"contenido_unidad_medida\": \"PIEZA\"}',NULL,'2026-04-14 05:17:41'),
(31,'Sistema','Sistema','Sistema','default','INSERT','insumos','N/A',NULL,'{\"sku\": \"INS-ACC-003\", \"ancho\": null, \"nombre\": \"Etiqueta Axis Bordada\", \"estatus\": null, \"uuid_insumo\": null, \"unidad_medida\": \"PIEZA\", \"fecha_creacion\": null, \"uuid_categoria\": \"3a79ee50-1857-4904-819e-86655e012d38\", \"contenido_cantidad\": 1.0, \"fecha_actualizacion\": null, \"stock_minimo_alerta\": 10, \"stock_total_acumulado\": 0, \"usuario_actualizo_uuid\": null, \"contenido_unidad_medida\": \"PIEZA\"}',NULL,'2026-04-14 05:17:41'),
(32,'Sistema','Sistema','Sistema','default','INSERT','explosion_materiales_cabecera','N/A',NULL,'{\"estatus\": \"ACTIVO\", \"uuid_usuario\": \"cb42c028-4deb-48b3-a57b-49c391951b81\", \"fecha_creacion\": null, \"uuid_explosion\": null, \"fecha_actualizacion\": null, \"instrucciones_proceso\": \"Corte láser y costura reforzada.\"}',NULL,'2026-04-14 05:17:41'),
(33,'Sistema','Sistema','Sistema','default','INSERT','explosion_materiales_detalle','N/A',NULL,'{\"uuid_insumo\": \"6fa71ea2-95f2-4268-b3be-9d5b434e0bbb\", \"uuid_detalle\": null, \"fecha_creacion\": null, \"uuid_explosion\": \"bd36b3fe-a21e-4ab0-971c-e10527e41339\", \"ancho_referencia\": null, \"fecha_actualizacion\": null, \"consumo_teorico_unitario\": 2.5}',NULL,'2026-04-14 05:17:41'),
(34,'Sistema','Sistema','Sistema','default','INSERT','explosion_materiales_detalle','N/A',NULL,'{\"uuid_insumo\": \"b86c4c6e-9e3e-44af-8eae-665e4ada1e43\", \"uuid_detalle\": null, \"fecha_creacion\": null, \"uuid_explosion\": \"bd36b3fe-a21e-4ab0-971c-e10527e41339\", \"ancho_referencia\": null, \"fecha_actualizacion\": null, \"consumo_teorico_unitario\": 1.0}',NULL,'2026-04-14 05:17:41'),
(35,'Sistema','Sistema','Sistema','default','INSERT','explosion_materiales_detalle','N/A',NULL,'{\"uuid_insumo\": \"d34a1441-5bd6-456c-a27e-f7ccd9396b6f\", \"uuid_detalle\": null, \"fecha_creacion\": null, \"uuid_explosion\": \"bd36b3fe-a21e-4ab0-971c-e10527e41339\", \"ancho_referencia\": null, \"fecha_actualizacion\": null, \"consumo_teorico_unitario\": 1.0}',NULL,'2026-04-14 05:17:41'),
(36,'Sistema','Sistema','Sistema','default','INSERT','explosion_materiales_cabecera','N/A',NULL,'{\"estatus\": \"ACTIVO\", \"uuid_usuario\": \"cb42c028-4deb-48b3-a57b-49c391951b81\", \"fecha_creacion\": null, \"uuid_explosion\": null, \"fecha_actualizacion\": null, \"instrucciones_proceso\": \"Costura plana a dos hilos.\"}',NULL,'2026-04-14 05:17:41'),
(37,'Sistema','Sistema','Sistema','default','INSERT','explosion_materiales_detalle','N/A',NULL,'{\"uuid_insumo\": \"9683f566-2d52-42d5-ad2c-d09aad2f6c1e\", \"uuid_detalle\": null, \"fecha_creacion\": null, \"uuid_explosion\": \"eda16cbb-b7cc-4989-a17e-b021e7fe9039\", \"ancho_referencia\": null, \"fecha_actualizacion\": null, \"consumo_teorico_unitario\": 1.2}',NULL,'2026-04-14 05:17:41'),
(38,'Sistema','Sistema','Sistema','default','INSERT','explosion_materiales_detalle','N/A',NULL,'{\"uuid_insumo\": \"d34a1441-5bd6-456c-a27e-f7ccd9396b6f\", \"uuid_detalle\": null, \"fecha_creacion\": null, \"uuid_explosion\": \"eda16cbb-b7cc-4989-a17e-b021e7fe9039\", \"ancho_referencia\": null, \"fecha_actualizacion\": null, \"consumo_teorico_unitario\": 1.0}',NULL,'2026-04-14 05:17:41'),
(39,'Sistema','Sistema','Sistema','default','INSERT','modelos_ropa','N/A',NULL,'{\"estatus\": \"ACTIVO\", \"imagen_url\": \"/static/images/products/hoodie-black.jpg\", \"descripcion\": \"Sudadera pesada con fit urbano.\", \"uuid_modelo\": null, \"nombre_modelo\": \"Hoodie Oversight Black\", \"fecha_creacion\": null, \"uuid_categoria\": \"82109e1a-a626-42f4-ae57-a663eba5559a\", \"fecha_actualizacion\": null}',NULL,'2026-04-14 05:17:41'),
(40,'Sistema','Sistema','Sistema','default','INSERT','productos_terminados','N/A',NULL,'{\"talla\": \"S\", \"active\": null, \"uuid_modelo\": \"c166ec2b-1862-4452-b4d0-a445fc7a2869\", \"precio_venta\": 1200.0, \"uuid_producto\": null, \"fecha_creacion\": null, \"sku_especifico\": \"H-OV-BLK-S\", \"uuid_explosion\": \"bd36b3fe-a21e-4ab0-971c-e10527e41339\", \"fecha_actualizacion\": null, \"stock_fisico_actual\": 43, \"stock_minimo_alerta\": null}',NULL,'2026-04-14 05:17:41'),
(41,'Sistema','Sistema','Sistema','default','INSERT','productos_terminados','N/A',NULL,'{\"talla\": \"M\", \"active\": null, \"uuid_modelo\": \"c166ec2b-1862-4452-b4d0-a445fc7a2869\", \"precio_venta\": 1200.0, \"uuid_producto\": null, \"fecha_creacion\": null, \"sku_especifico\": \"H-OV-BLK-M\", \"uuid_explosion\": \"bd36b3fe-a21e-4ab0-971c-e10527e41339\", \"fecha_actualizacion\": null, \"stock_fisico_actual\": 47, \"stock_minimo_alerta\": null}',NULL,'2026-04-14 05:17:41'),
(42,'Sistema','Sistema','Sistema','default','INSERT','productos_terminados','N/A',NULL,'{\"talla\": \"L\", \"active\": null, \"uuid_modelo\": \"c166ec2b-1862-4452-b4d0-a445fc7a2869\", \"precio_venta\": 1200.0, \"uuid_producto\": null, \"fecha_creacion\": null, \"sku_especifico\": \"H-OV-BLK-L\", \"uuid_explosion\": \"bd36b3fe-a21e-4ab0-971c-e10527e41339\", \"fecha_actualizacion\": null, \"stock_fisico_actual\": 24, \"stock_minimo_alerta\": null}',NULL,'2026-04-14 05:17:41'),
(43,'Sistema','Sistema','Sistema','default','INSERT','productos_terminados','N/A',NULL,'{\"talla\": \"XL\", \"active\": null, \"uuid_modelo\": \"c166ec2b-1862-4452-b4d0-a445fc7a2869\", \"precio_venta\": 1200.0, \"uuid_producto\": null, \"fecha_creacion\": null, \"sku_especifico\": \"H-OV-BLK-XL\", \"uuid_explosion\": \"bd36b3fe-a21e-4ab0-971c-e10527e41339\", \"fecha_actualizacion\": null, \"stock_fisico_actual\": 44, \"stock_minimo_alerta\": null}',NULL,'2026-04-14 05:17:41'),
(44,'Sistema','Sistema','Sistema','default','INSERT','modelos_ropa','N/A',NULL,'{\"estatus\": \"ACTIVO\", \"imagen_url\": \"/static/images/products/tshirt-white.jpg\", \"descripcion\": \"Camiseta 100% algodón alta densidad.\", \"uuid_modelo\": null, \"nombre_modelo\": \"Axis Logo Tee White\", \"fecha_creacion\": null, \"uuid_categoria\": \"1d409b69-d01d-4159-b250-369bd64f1c59\", \"fecha_actualizacion\": null}',NULL,'2026-04-14 05:17:41'),
(45,'Sistema','Sistema','Sistema','default','INSERT','productos_terminados','N/A',NULL,'{\"talla\": \"S\", \"active\": null, \"uuid_modelo\": \"e485a914-472a-4a17-875e-787ace4e9174\", \"precio_venta\": 450.0, \"uuid_producto\": null, \"fecha_creacion\": null, \"sku_especifico\": \"T-LOG-WHT-S\", \"uuid_explosion\": \"eda16cbb-b7cc-4989-a17e-b021e7fe9039\", \"fecha_actualizacion\": null, \"stock_fisico_actual\": 47, \"stock_minimo_alerta\": null}',NULL,'2026-04-14 05:17:41'),
(46,'Sistema','Sistema','Sistema','default','INSERT','productos_terminados','N/A',NULL,'{\"talla\": \"M\", \"active\": null, \"uuid_modelo\": \"e485a914-472a-4a17-875e-787ace4e9174\", \"precio_venta\": 450.0, \"uuid_producto\": null, \"fecha_creacion\": null, \"sku_especifico\": \"T-LOG-WHT-M\", \"uuid_explosion\": \"eda16cbb-b7cc-4989-a17e-b021e7fe9039\", \"fecha_actualizacion\": null, \"stock_fisico_actual\": 19, \"stock_minimo_alerta\": null}',NULL,'2026-04-14 05:17:41'),
(47,'Sistema','Sistema','Sistema','default','INSERT','productos_terminados','N/A',NULL,'{\"talla\": \"L\", \"active\": null, \"uuid_modelo\": \"e485a914-472a-4a17-875e-787ace4e9174\", \"precio_venta\": 450.0, \"uuid_producto\": null, \"fecha_creacion\": null, \"sku_especifico\": \"T-LOG-WHT-L\", \"uuid_explosion\": \"eda16cbb-b7cc-4989-a17e-b021e7fe9039\", \"fecha_actualizacion\": null, \"stock_fisico_actual\": 46, \"stock_minimo_alerta\": null}',NULL,'2026-04-14 05:17:41'),
(48,'Sistema','Sistema','Sistema','default','INSERT','productos_terminados','N/A',NULL,'{\"talla\": \"XL\", \"active\": null, \"uuid_modelo\": \"e485a914-472a-4a17-875e-787ace4e9174\", \"precio_venta\": 450.0, \"uuid_producto\": null, \"fecha_creacion\": null, \"sku_especifico\": \"T-LOG-WHT-XL\", \"uuid_explosion\": \"eda16cbb-b7cc-4989-a17e-b021e7fe9039\", \"fecha_actualizacion\": null, \"stock_fisico_actual\": 24, \"stock_minimo_alerta\": null}',NULL,'2026-04-14 05:17:41'),
(49,'Sistema','Sistema','Sistema','default','INSERT','pedidos_proveedor_encabezado','N/A',NULL,'{\"estatus\": \"Completado\", \"uuid_pedido\": null, \"fecha_pedido\": null, \"folio_pedido\": \"PED-INS-TEX-001\", \"uuid_proveedor\": \"f9476d8f-02ef-4486-8ec6-71839fb17a86\", \"fecha_actualizacion\": null, \"uuid_usuario_solicita\": \"cb42c028-4deb-48b3-a57b-49c391951b81\"}',NULL,'2026-04-14 05:17:41'),
(50,'Sistema','Sistema','Sistema','default','INSERT','pedidos_proveedor_detalle','N/A',NULL,'{\"uuid_insumo\": \"9683f566-2d52-42d5-ad2c-d09aad2f6c1e\", \"uuid_pedido\": \"686c821b-9b6d-4778-924c-3cff7ee637b8\", \"fecha_creacion\": null, \"cantidad_pedida\": 10, \"cantidad_recibida\": null, \"fecha_actualizacion\": null, \"uuid_detalle_pedido\": null, \"costo_unitario_estimado\": 150.0}',NULL,'2026-04-14 05:17:41'),
(51,'Sistema','Sistema','Sistema','default','INSERT','compras_encabezado','N/A',NULL,'{\"estatus\": \"RECIBIDO\", \"uuid_compra\": null, \"uuid_pedido\": \"686c821b-9b6d-4778-924c-3cff7ee637b8\", \"fecha_compra\": null, \"folio_factura\": \"FAC-INS-TEX-001-99\", \"uuid_proveedor\": \"f9476d8f-02ef-4486-8ec6-71839fb17a86\", \"fecha_actualizacion\": null, \"uuid_usuario_registro\": \"cb42c028-4deb-48b3-a57b-49c391951b81\"}',NULL,'2026-04-14 05:17:41'),
(52,'Sistema','Sistema','Sistema','default','INSERT','compras_detalle','N/A',NULL,'{\"uuid_compra\": \"3a1dc7d5-05e9-4bed-8fb7-72a54c358a7b\", \"uuid_insumo\": \"9683f566-2d52-42d5-ad2c-d09aad2f6c1e\", \"fecha_creacion\": null, \"cantidad_comprada\": 10, \"fecha_actualizacion\": null, \"uuid_detalle_compra\": null, \"costo_unitario_compra\": 150.0}',NULL,'2026-04-14 05:17:41'),
(53,'Sistema','Sistema','Sistema','default','INSERT','rollos_inventario','N/A',NULL,'{\"uuid_rollo\": null, \"uuid_insumo\": \"9683f566-2d52-42d5-ad2c-d09aad2f6c1e\", \"fecha_creacion\": null, \"metraje_inicial\": 100.0, \"fecha_actualizacion\": null, \"uuid_detalle_compra\": \"e2e37a1b-ae70-4a14-b5e9-820140f2b562\", \"metraje_continuo_actual\": 100.0}',NULL,'2026-04-14 05:17:41'),
(54,'Sistema','Sistema','Sistema','default','INSERT','rollos_inventario','N/A',NULL,'{\"uuid_rollo\": null, \"uuid_insumo\": \"9683f566-2d52-42d5-ad2c-d09aad2f6c1e\", \"fecha_creacion\": null, \"metraje_inicial\": 100.0, \"fecha_actualizacion\": null, \"uuid_detalle_compra\": \"e2e37a1b-ae70-4a14-b5e9-820140f2b562\", \"metraje_continuo_actual\": 100.0}',NULL,'2026-04-14 05:17:41'),
(55,'Sistema','Sistema','Sistema','default','INSERT','rollos_inventario','N/A',NULL,'{\"uuid_rollo\": null, \"uuid_insumo\": \"9683f566-2d52-42d5-ad2c-d09aad2f6c1e\", \"fecha_creacion\": null, \"metraje_inicial\": 100.0, \"fecha_actualizacion\": null, \"uuid_detalle_compra\": \"e2e37a1b-ae70-4a14-b5e9-820140f2b562\", \"metraje_continuo_actual\": 100.0}',NULL,'2026-04-14 05:17:41'),
(56,'Sistema','Sistema','Sistema','default','INSERT','rollos_inventario','N/A',NULL,'{\"uuid_rollo\": null, \"uuid_insumo\": \"9683f566-2d52-42d5-ad2c-d09aad2f6c1e\", \"fecha_creacion\": null, \"metraje_inicial\": 100.0, \"fecha_actualizacion\": null, \"uuid_detalle_compra\": \"e2e37a1b-ae70-4a14-b5e9-820140f2b562\", \"metraje_continuo_actual\": 100.0}',NULL,'2026-04-14 05:17:41'),
(57,'Sistema','Sistema','Sistema','default','INSERT','rollos_inventario','N/A',NULL,'{\"uuid_rollo\": null, \"uuid_insumo\": \"9683f566-2d52-42d5-ad2c-d09aad2f6c1e\", \"fecha_creacion\": null, \"metraje_inicial\": 100.0, \"fecha_actualizacion\": null, \"uuid_detalle_compra\": \"e2e37a1b-ae70-4a14-b5e9-820140f2b562\", \"metraje_continuo_actual\": 100.0}',NULL,'2026-04-14 05:17:41'),
(58,'Sistema','Sistema','Sistema','default','INSERT','rollos_inventario','N/A',NULL,'{\"uuid_rollo\": null, \"uuid_insumo\": \"9683f566-2d52-42d5-ad2c-d09aad2f6c1e\", \"fecha_creacion\": null, \"metraje_inicial\": 100.0, \"fecha_actualizacion\": null, \"uuid_detalle_compra\": \"e2e37a1b-ae70-4a14-b5e9-820140f2b562\", \"metraje_continuo_actual\": 100.0}',NULL,'2026-04-14 05:17:41'),
(59,'Sistema','Sistema','Sistema','default','INSERT','rollos_inventario','N/A',NULL,'{\"uuid_rollo\": null, \"uuid_insumo\": \"9683f566-2d52-42d5-ad2c-d09aad2f6c1e\", \"fecha_creacion\": null, \"metraje_inicial\": 100.0, \"fecha_actualizacion\": null, \"uuid_detalle_compra\": \"e2e37a1b-ae70-4a14-b5e9-820140f2b562\", \"metraje_continuo_actual\": 100.0}',NULL,'2026-04-14 05:17:41'),
(60,'Sistema','Sistema','Sistema','default','INSERT','rollos_inventario','N/A',NULL,'{\"uuid_rollo\": null, \"uuid_insumo\": \"9683f566-2d52-42d5-ad2c-d09aad2f6c1e\", \"fecha_creacion\": null, \"metraje_inicial\": 100.0, \"fecha_actualizacion\": null, \"uuid_detalle_compra\": \"e2e37a1b-ae70-4a14-b5e9-820140f2b562\", \"metraje_continuo_actual\": 100.0}',NULL,'2026-04-14 05:17:41'),
(61,'Sistema','Sistema','Sistema','default','INSERT','rollos_inventario','N/A',NULL,'{\"uuid_rollo\": null, \"uuid_insumo\": \"9683f566-2d52-42d5-ad2c-d09aad2f6c1e\", \"fecha_creacion\": null, \"metraje_inicial\": 100.0, \"fecha_actualizacion\": null, \"uuid_detalle_compra\": \"e2e37a1b-ae70-4a14-b5e9-820140f2b562\", \"metraje_continuo_actual\": 100.0}',NULL,'2026-04-14 05:17:41'),
(62,'Sistema','Sistema','Sistema','default','INSERT','rollos_inventario','N/A',NULL,'{\"uuid_rollo\": null, \"uuid_insumo\": \"9683f566-2d52-42d5-ad2c-d09aad2f6c1e\", \"fecha_creacion\": null, \"metraje_inicial\": 100.0, \"fecha_actualizacion\": null, \"uuid_detalle_compra\": \"e2e37a1b-ae70-4a14-b5e9-820140f2b562\", \"metraje_continuo_actual\": 100.0}',NULL,'2026-04-14 05:17:41'),
(63,'Sistema','Sistema','Sistema','default','UPDATE','insumos','9683f566-2d52-42d5-ad2c-d09aad2f6c1e','{\"stock_total_acumulado\": 0.0}','{\"stock_total_acumulado\": 1000.0}',NULL,'2026-04-14 05:17:41'),
(64,'Sistema','Sistema','Sistema','default','INSERT','pedidos_proveedor_encabezado','N/A',NULL,'{\"estatus\": \"Completado\", \"uuid_pedido\": null, \"fecha_pedido\": null, \"folio_pedido\": \"PED-INS-TEX-002\", \"uuid_proveedor\": \"f9476d8f-02ef-4486-8ec6-71839fb17a86\", \"fecha_actualizacion\": null, \"uuid_usuario_solicita\": \"cb42c028-4deb-48b3-a57b-49c391951b81\"}',NULL,'2026-04-14 05:17:41'),
(65,'Sistema','Sistema','Sistema','default','INSERT','pedidos_proveedor_detalle','N/A',NULL,'{\"uuid_insumo\": \"6fa71ea2-95f2-4268-b3be-9d5b434e0bbb\", \"uuid_pedido\": \"cf3c0505-c50f-4f4f-b8db-121af6103586\", \"fecha_creacion\": null, \"cantidad_pedida\": 5, \"cantidad_recibida\": null, \"fecha_actualizacion\": null, \"uuid_detalle_pedido\": null, \"costo_unitario_estimado\": 220.0}',NULL,'2026-04-14 05:17:41'),
(66,'Sistema','Sistema','Sistema','default','INSERT','compras_encabezado','N/A',NULL,'{\"estatus\": \"RECIBIDO\", \"uuid_compra\": null, \"uuid_pedido\": \"cf3c0505-c50f-4f4f-b8db-121af6103586\", \"fecha_compra\": null, \"folio_factura\": \"FAC-INS-TEX-002-99\", \"uuid_proveedor\": \"f9476d8f-02ef-4486-8ec6-71839fb17a86\", \"fecha_actualizacion\": null, \"uuid_usuario_registro\": \"cb42c028-4deb-48b3-a57b-49c391951b81\"}',NULL,'2026-04-14 05:17:41'),
(67,'Sistema','Sistema','Sistema','default','INSERT','compras_detalle','N/A',NULL,'{\"uuid_compra\": \"8669781b-2226-44a5-8bbc-149bca7b8143\", \"uuid_insumo\": \"6fa71ea2-95f2-4268-b3be-9d5b434e0bbb\", \"fecha_creacion\": null, \"cantidad_comprada\": 5, \"fecha_actualizacion\": null, \"uuid_detalle_compra\": null, \"costo_unitario_compra\": 220.0}',NULL,'2026-04-14 05:17:41'),
(68,'Sistema','Sistema','Sistema','default','INSERT','rollos_inventario','N/A',NULL,'{\"uuid_rollo\": null, \"uuid_insumo\": \"6fa71ea2-95f2-4268-b3be-9d5b434e0bbb\", \"fecha_creacion\": null, \"metraje_inicial\": 50.0, \"fecha_actualizacion\": null, \"uuid_detalle_compra\": \"4ba1e1d5-9a06-4d4a-bc19-01ff92911b1c\", \"metraje_continuo_actual\": 50.0}',NULL,'2026-04-14 05:17:41'),
(69,'Sistema','Sistema','Sistema','default','INSERT','rollos_inventario','N/A',NULL,'{\"uuid_rollo\": null, \"uuid_insumo\": \"6fa71ea2-95f2-4268-b3be-9d5b434e0bbb\", \"fecha_creacion\": null, \"metraje_inicial\": 50.0, \"fecha_actualizacion\": null, \"uuid_detalle_compra\": \"4ba1e1d5-9a06-4d4a-bc19-01ff92911b1c\", \"metraje_continuo_actual\": 50.0}',NULL,'2026-04-14 05:17:41'),
(70,'Sistema','Sistema','Sistema','default','INSERT','rollos_inventario','N/A',NULL,'{\"uuid_rollo\": null, \"uuid_insumo\": \"6fa71ea2-95f2-4268-b3be-9d5b434e0bbb\", \"fecha_creacion\": null, \"metraje_inicial\": 50.0, \"fecha_actualizacion\": null, \"uuid_detalle_compra\": \"4ba1e1d5-9a06-4d4a-bc19-01ff92911b1c\", \"metraje_continuo_actual\": 50.0}',NULL,'2026-04-14 05:17:41'),
(71,'Sistema','Sistema','Sistema','default','INSERT','rollos_inventario','N/A',NULL,'{\"uuid_rollo\": null, \"uuid_insumo\": \"6fa71ea2-95f2-4268-b3be-9d5b434e0bbb\", \"fecha_creacion\": null, \"metraje_inicial\": 50.0, \"fecha_actualizacion\": null, \"uuid_detalle_compra\": \"4ba1e1d5-9a06-4d4a-bc19-01ff92911b1c\", \"metraje_continuo_actual\": 50.0}',NULL,'2026-04-14 05:17:41'),
(72,'Sistema','Sistema','Sistema','default','INSERT','rollos_inventario','N/A',NULL,'{\"uuid_rollo\": null, \"uuid_insumo\": \"6fa71ea2-95f2-4268-b3be-9d5b434e0bbb\", \"fecha_creacion\": null, \"metraje_inicial\": 50.0, \"fecha_actualizacion\": null, \"uuid_detalle_compra\": \"4ba1e1d5-9a06-4d4a-bc19-01ff92911b1c\", \"metraje_continuo_actual\": 50.0}',NULL,'2026-04-14 05:17:41'),
(73,'Sistema','Sistema','Sistema','default','UPDATE','insumos','6fa71ea2-95f2-4268-b3be-9d5b434e0bbb','{\"stock_total_acumulado\": 0.0}','{\"stock_total_acumulado\": 250.0}',NULL,'2026-04-14 05:17:41'),
(74,'Sistema','Sistema','Sistema','default','INSERT','pedidos_proveedor_encabezado','N/A',NULL,'{\"estatus\": \"Completado\", \"uuid_pedido\": null, \"fecha_pedido\": null, \"folio_pedido\": \"PED-INS-ACC-001\", \"uuid_proveedor\": \"a4729e74-4f94-4f47-a9c5-de6395bf5420\", \"fecha_actualizacion\": null, \"uuid_usuario_solicita\": \"cb42c028-4deb-48b3-a57b-49c391951b81\"}',NULL,'2026-04-14 05:17:41'),
(75,'Sistema','Sistema','Sistema','default','INSERT','pedidos_proveedor_detalle','N/A',NULL,'{\"uuid_insumo\": \"b86c4c6e-9e3e-44af-8eae-665e4ada1e43\", \"uuid_pedido\": \"e2684230-6cca-4339-a594-04336a376553\", \"fecha_creacion\": null, \"cantidad_pedida\": 100, \"cantidad_recibida\": null, \"fecha_actualizacion\": null, \"uuid_detalle_pedido\": null, \"costo_unitario_estimado\": 12.0}',NULL,'2026-04-14 05:17:41'),
(76,'Sistema','Sistema','Sistema','default','INSERT','compras_encabezado','N/A',NULL,'{\"estatus\": \"RECIBIDO\", \"uuid_compra\": null, \"uuid_pedido\": \"e2684230-6cca-4339-a594-04336a376553\", \"fecha_compra\": null, \"folio_factura\": \"FAC-INS-ACC-001-99\", \"uuid_proveedor\": \"a4729e74-4f94-4f47-a9c5-de6395bf5420\", \"fecha_actualizacion\": null, \"uuid_usuario_registro\": \"cb42c028-4deb-48b3-a57b-49c391951b81\"}',NULL,'2026-04-14 05:17:41'),
(77,'Sistema','Sistema','Sistema','default','INSERT','compras_detalle','N/A',NULL,'{\"uuid_compra\": \"57e38e01-b330-4466-a925-cd374dc02ce3\", \"uuid_insumo\": \"b86c4c6e-9e3e-44af-8eae-665e4ada1e43\", \"fecha_creacion\": null, \"cantidad_comprada\": 100, \"fecha_actualizacion\": null, \"uuid_detalle_compra\": null, \"costo_unitario_compra\": 12.0}',NULL,'2026-04-14 05:17:41'),
(78,'Sistema','Sistema','Sistema','default','UPDATE','insumos','b86c4c6e-9e3e-44af-8eae-665e4ada1e43','{\"stock_total_acumulado\": 0.0}','{\"stock_total_acumulado\": 100}',NULL,'2026-04-14 05:17:41'),
(79,'Sistema','Sistema','Sistema','default','INSERT','pedidos_proveedor_encabezado','N/A',NULL,'{\"estatus\": \"Completado\", \"uuid_pedido\": null, \"fecha_pedido\": null, \"folio_pedido\": \"PED-INS-ACC-003\", \"uuid_proveedor\": \"a4729e74-4f94-4f47-a9c5-de6395bf5420\", \"fecha_actualizacion\": null, \"uuid_usuario_solicita\": \"cb42c028-4deb-48b3-a57b-49c391951b81\"}',NULL,'2026-04-14 05:17:41'),
(80,'Sistema','Sistema','Sistema','default','INSERT','pedidos_proveedor_detalle','N/A',NULL,'{\"uuid_insumo\": \"d34a1441-5bd6-456c-a27e-f7ccd9396b6f\", \"uuid_pedido\": \"7998623f-4d76-45e5-bf18-fea9e0af7b6e\", \"fecha_creacion\": null, \"cantidad_pedida\": 500, \"cantidad_recibida\": null, \"fecha_actualizacion\": null, \"uuid_detalle_pedido\": null, \"costo_unitario_estimado\": 5.0}',NULL,'2026-04-14 05:17:41'),
(81,'Sistema','Sistema','Sistema','default','INSERT','compras_encabezado','N/A',NULL,'{\"estatus\": \"RECIBIDO\", \"uuid_compra\": null, \"uuid_pedido\": \"7998623f-4d76-45e5-bf18-fea9e0af7b6e\", \"fecha_compra\": null, \"folio_factura\": \"FAC-INS-ACC-003-99\", \"uuid_proveedor\": \"a4729e74-4f94-4f47-a9c5-de6395bf5420\", \"fecha_actualizacion\": null, \"uuid_usuario_registro\": \"cb42c028-4deb-48b3-a57b-49c391951b81\"}',NULL,'2026-04-14 05:17:41'),
(82,'Sistema','Sistema','Sistema','default','INSERT','compras_detalle','N/A',NULL,'{\"uuid_compra\": \"3dca4cfa-4e85-4b88-bbe8-651ec098dd6f\", \"uuid_insumo\": \"d34a1441-5bd6-456c-a27e-f7ccd9396b6f\", \"fecha_creacion\": null, \"cantidad_comprada\": 500, \"fecha_actualizacion\": null, \"uuid_detalle_compra\": null, \"costo_unitario_compra\": 5.0}',NULL,'2026-04-14 05:17:41'),
(83,'Sistema','Sistema','Sistema','default','UPDATE','insumos','d34a1441-5bd6-456c-a27e-f7ccd9396b6f','{\"stock_total_acumulado\": 0.0}','{\"stock_total_acumulado\": 500}',NULL,'2026-04-14 05:17:41'),
(84,'Sistema','Sistema','Sistema','default','INSERT','ventas_encabezado','N/A',NULL,'{\"uuid_venta\": null, \"fecha_venta\": null, \"metodo_pago\": \"Tarjeta\", \"uuid_cliente\": \"2ef2c1e2-6706-404d-b21e-1cc5f3915521\", \"estatus_envio\": \"Entregado\", \"numero_pedido\": \"AX-101\", \"fecha_actualizacion\": null}',NULL,'2026-04-14 05:17:41'),
(85,'Sistema','Sistema','Sistema','default','INSERT','ventas_detalle','N/A',NULL,'{\"cantidad\": 1, \"uuid_venta\": \"99b47f91-7dd4-4809-9194-0e05d9c9adc9\", \"uuid_detalle\": null, \"uuid_producto\": \"ee304c05-f322-4fa6-a6a8-8d2c9c52788a\", \"fecha_creacion\": null, \"fecha_actualizacion\": null, \"precio_unitario_historico\": 1200.0}',NULL,'2026-04-14 05:17:41'),
(86,'Sistema','Sistema','Sistema','default','INSERT','ventas_detalle','N/A',NULL,'{\"cantidad\": 2, \"uuid_venta\": \"99b47f91-7dd4-4809-9194-0e05d9c9adc9\", \"uuid_detalle\": null, \"uuid_producto\": \"a1ead39f-6c9d-4bf5-9e3a-0119f7b73836\", \"fecha_creacion\": null, \"fecha_actualizacion\": null, \"precio_unitario_historico\": 450.0}',NULL,'2026-04-14 05:17:41'),
(87,'Sistema','Sistema','Sistema','default','INSERT','ventas_encabezado','N/A',NULL,'{\"uuid_venta\": null, \"fecha_venta\": null, \"metodo_pago\": \"Paypal\", \"uuid_cliente\": \"2ef2c1e2-6706-404d-b21e-1cc5f3915521\", \"estatus_envio\": \"Procesando\", \"numero_pedido\": \"AX-102\", \"fecha_actualizacion\": null}',NULL,'2026-04-14 05:17:41'),
(88,'Sistema','Sistema','Sistema','default','INSERT','ventas_detalle','N/A',NULL,'{\"cantidad\": 2, \"uuid_venta\": \"783e1293-dbd5-420c-83d4-f8f89cad5320\", \"uuid_detalle\": null, \"uuid_producto\": \"ee304c05-f322-4fa6-a6a8-8d2c9c52788a\", \"fecha_creacion\": null, \"fecha_actualizacion\": null, \"precio_unitario_historico\": 1200.0}',NULL,'2026-04-14 05:17:41'),
(89,'Sistema','Sistema','Sistema','default','INSERT','ordenes_produccion','N/A',NULL,'{\"estado\": \"Terminado\", \"uuid_op\": null, \"uuid_producto\": \"ee304c05-f322-4fa6-a6a8-8d2c9c52788a\", \"fecha_solicitud\": null, \"uuid_venta_detalle\": \"6bbc2e24-c959-4972-8c92-2568b6eef435\", \"cantidad_a_producir\": 10, \"fecha_actualizacion\": null, \"uuid_pedido_detalle\": null}',NULL,'2026-04-14 05:17:41'),
(90,'Sistema','Sistema','Sistema','default','INSERT','ejecucion_corte','N/A',NULL,'{\"uuid_op\": \"37986269-3809-48e8-b309-3b0a176318f4\", \"uuid_corte\": null, \"fecha_proceso\": null, \"uuid_rollo_used\": \"063f0100-5888-473a-bf05-7cd2e8fe7cdd\", \"usuario_corto_uuid\": \"cb42c028-4deb-48b3-a57b-49c391951b81\", \"fecha_actualizacion\": null, \"merma_real_calculada\": 1.5, \"metros_sacados_bodega\": 26.5, \"prendas_reales_logradas\": 10, \"metros_teoricos_requeridos\": 25.0}',NULL,'2026-04-14 05:17:41'),
(91,'Sistema','Sistema','Sistema','default','INSERT','merma_piezas','N/A',NULL,'{\"motivo\": \"ERROR_OPERARIO\", \"uuid_op\": \"37986269-3809-48e8-b309-3b0a176318f4\", \"uuid_merma\": null, \"uuid_insumo\": \"d34a1441-5bd6-456c-a27e-f7ccd9396b6f\", \"observaciones\": \"2 etiquetas se dañaron al coser.\", \"fecha_registro\": null, \"cantidad_teorica\": 10, \"fecha_actualizacion\": null, \"usuario_registro_uuid\": \"cb42c028-4deb-48b3-a57b-49c391951b81\", \"cantidad_real_consumida\": 12}',NULL,'2026-04-14 05:17:41'),
(92,'Sistema','Sistema','Sistema','default','UPDATE','rollos_inventario','063f0100-5888-473a-bf05-7cd2e8fe7cdd','{\"metraje_continuo_actual\": 50.0}','{\"metraje_continuo_actual\": 23.5}',NULL,'2026-04-14 05:17:41'),
(93,'Sistema','Sistema','Sistema','default','INSERT','ordenes_produccion','N/A',NULL,'{\"estado\": \"Pendiente\", \"uuid_op\": null, \"uuid_producto\": \"a1ead39f-6c9d-4bf5-9e3a-0119f7b73836\", \"fecha_solicitud\": null, \"uuid_venta_detalle\": null, \"cantidad_a_producir\": 30, \"fecha_actualizacion\": null, \"uuid_pedido_detalle\": null}',NULL,'2026-04-14 05:17:41'),
(94,'cb42c028-4deb-48b3-a57b-49c391951b81','Admin Axis','admin','cliente_rol','UPDATE','usuarios','cb42c028-4deb-48b3-a57b-49c391951b81','{\"tf_totp_secret\": null, \"tf_primary_method\": null}','{\"tf_totp_secret\": \"{\\\"enckey\\\":{\\\"c\\\":14,\\\"k\\\":\\\"W4GCDB6VRM3L7APOLEIHNQ4FEG2A3Y6T\\\",\\\"s\\\":\\\"JVE4T6N767PJWU7KLWFQ\\\",\\\"t\\\":\\\"1\\\",\\\"v\\\":1},\\\"type\\\":\\\"totp\\\",\\\"v\\\":1}\", \"tf_primary_method\": \"authenticator\"}','172.18.0.1','2026-04-14 05:18:16');
/*!40000 ALTER TABLE `security_audit_logs` ENABLE KEYS */;
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
('0f107056-f010-4f27-96c9-5b1256149525','Comprador Axis','compras@axis.com','$argon2id$v=19$m=65536,t=3,p=4$BOD8n/N+LwXAmFPKGSNEaA$yN6AzzjkCFq2j3ZqHPGI+NjBzbnDFx7AT3fOw1gLW6g',1,'2026-04-14 05:17:40','2026-04-14 05:17:40','823c04813f90446b8f241b42f5ae577e','2026-04-14 05:17:41',NULL,NULL,NULL,'2026-04-14 05:17:40',NULL),
('241f46af-6609-474a-8457-a4ff102e38f2','Maria Lopez','maria@axis.com','$argon2id$v=19$m=65536,t=3,p=4$zFkrRag1RiillPIeg5BSyg$cg0I4IJxIFupV5dU27/d8oa1oKTo7DU3ccJUhEsf/NU',1,'2026-04-14 05:17:41','2026-04-14 05:17:41','c0fcc6f4061e46a6879c95842ff879df','2026-04-14 05:17:41',NULL,NULL,NULL,'2026-04-14 05:17:41',NULL),
('3bdd7de8-8ffd-4334-8ee9-d62d8741b499','Modista Principal','modista@axis.com','$argon2id$v=19$m=65536,t=3,p=4$iRGiVEpJybmXUqq11tobYw$/28lPNikQn3oQMR4+myG0gKO0ToVf7GjnTaC/iKenN8',1,'2026-04-14 05:17:40','2026-04-14 05:17:40','a1c022e8f8fd4954b76cb79bc330c84a','2026-04-14 05:17:41',NULL,NULL,NULL,'2026-04-14 05:17:40',NULL),
('9a25da8a-8f13-4b20-8560-038e6330f456','Vendedor Axis','ventas@axis.com','$argon2id$v=19$m=65536,t=3,p=4$zzknJGQsJUQIQWjNmbOWcg$Yc6wgGYa0Ebbso7orSYbXhceMvTsmlEl4hi5R65dWJc',1,'2026-04-14 05:17:40','2026-04-14 05:17:40','477f85d3cb5e40a5958a3f3117de4f9c','2026-04-14 05:17:41',NULL,NULL,NULL,'2026-04-14 05:17:40',NULL),
('cb42c028-4deb-48b3-a57b-49c391951b81','Admin Axis','admin@axis.com','$argon2id$v=19$m=65536,t=3,p=4$ozQGoBSCkLI2RmiNMYYQAg$L5Q5/7wb4Ye7x7zU68kiD+ojenPyDHhT0Fb9TvaM/Bs',1,'2026-04-14 05:17:40','2026-04-14 05:18:16','78bd41ceb92c48689f733b6bea6cd84a','2026-04-14 05:17:40','authenticator','{\"enckey\":{\"c\":14,\"k\":\"W4GCDB6VRM3L7APOLEIHNQ4FEG2A3Y6T\",\"s\":\"JVE4T6N767PJWU7KLWFQ\",\"t\":\"1\",\"v\":1},\"type\":\"totp\",\"v\":1}',NULL,'2026-04-14 05:17:40',NULL),
('ea24a0f4-c26e-40c5-9253-4261a90f8bef','Juan Cliente','juan@axis.com','$argon2id$v=19$m=65536,t=3,p=4$7733HkNIyZkT4lxrzfmfMw$8Irvge3nRT6BBETpUwAD0hVHuruRPN8OhzsE0J2ouCU',1,'2026-04-14 05:17:40','2026-04-14 05:17:40','aede777551c647698bf32ce750e7e92e','2026-04-14 05:17:41',NULL,NULL,NULL,'2026-04-14 05:17:40',NULL);
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
  `fecha_creacion` datetime DEFAULT (now()),
  `fecha_actualizacion` datetime DEFAULT (now()),
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
('6bbc2e24-c959-4972-8c92-2568b6eef435','783e1293-dbd5-420c-83d4-f8f89cad5320','ee304c05-f322-4fa6-a6a8-8d2c9c52788a',2,1200.00,'2026-04-14 05:17:41','2026-04-14 05:17:41'),
('a780254b-5a7d-47a7-a339-d5a6c4e07a5e','99b47f91-7dd4-4809-9194-0e05d9c9adc9','a1ead39f-6c9d-4bf5-9e3a-0119f7b73836',2,450.00,'2026-04-14 05:17:41','2026-04-14 05:17:41'),
('aebec02c-2091-409a-90cd-ae48c621876f','99b47f91-7dd4-4809-9194-0e05d9c9adc9','ee304c05-f322-4fa6-a6a8-8d2c9c52788a',1,1200.00,'2026-04-14 05:17:41','2026-04-14 05:17:41');
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
('783e1293-dbd5-420c-83d4-f8f89cad5320','AX-102','2ef2c1e2-6706-404d-b21e-1cc5f3915521','Paypal','Procesando','2026-04-14 05:17:41','2026-04-14 05:17:41'),
('99b47f91-7dd4-4809-9194-0e05d9c9adc9','AX-101','2ef2c1e2-6706-404d-b21e-1cc5f3915521','Tarjeta','Entregado','2026-04-14 05:17:41','2026-04-14 05:17:41');
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

-- Dump completed on 2026-04-14  5:18:25
