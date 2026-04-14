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
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

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
('073963aa-24a4-4b8c-8876-3557a2211f39','Hoodies','Sudaderas urbanas','/static/images/default/default-image.png',1,'2026-04-14 04:55:30','2026-04-14 04:55:30',NULL,NULL),
('4e048a20-99b4-49e8-8f4a-d7709ec6a062','Accesorios','Gorras y complementos','/static/images/default/default-image.png',1,'2026-04-14 04:55:30','2026-04-14 04:55:30',NULL,NULL),
('a78d4490-68c1-4e9e-9775-36d1228fac0c','Shorts','Pantalones cortos','/static/images/default/default-image.png',1,'2026-04-14 04:55:30','2026-04-14 04:55:30',NULL,NULL),
('b2396e2e-035b-477a-b60c-d3810816a349','Chaquetas','Abrigos y chamarras','/static/images/default/default-image.png',1,'2026-04-14 04:55:30','2026-04-14 04:55:30',NULL,NULL),
('ba68917d-e5b1-44b0-ac75-0adb53dded2e','Pantalones','Prendas inferiores','/static/images/default/default-image.png',1,'2026-04-14 04:55:30','2026-04-14 04:55:30',NULL,NULL),
('e5dd9b05-252e-44df-88f1-ee738f59001b','Camisetas','Prendas de cuerpo superior','/static/images/default/default-image.png',1,'2026-04-14 04:55:30','2026-04-14 04:55:30',NULL,NULL);
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
('93375c12-04fa-411f-8cab-5006e6290962','faed6acb-b63a-4c73-86f0-a776d1fc75ba','555-987-6543','Insurgentes Sur 456, CDMX','2026-04-14 04:55:30','2026-04-14 04:55:30',NULL),
('bcb1c893-c604-4c27-8e97-ef6a19ec2704','8b808a74-bd51-4403-95ad-8224d074e2a7','555-123-4567','Av. Reforma 123, CDMX','2026-04-14 04:55:30','2026-04-14 04:55:30',NULL);
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
  KEY `idx_cdetalle_insumo` (`uuid_insumo`),
  KEY `idx_cdetalle_compra` (`uuid_compra`),
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
('88f75ee7-a8f1-4a19-85fc-89de07a328ad','fc4d4731-e144-465f-ba2f-c931eccea5a6','34109c8f-4699-4511-9b39-bbcf39a5974a',10.0000,150.00,'2026-04-14 04:55:30','2026-04-14 04:55:30'),
('bfb879ff-b0cc-40a8-aea9-9cd085b66e61','524f8034-8910-4fc9-846c-ad8eb9de6124','9854bf3d-b35c-4c91-ab30-6beb4aaa1cdf',5.0000,220.00,'2026-04-14 04:55:30','2026-04-14 04:55:30'),
('c15d1787-e6b7-4367-ab43-8bc209f26fd9','6a0c762b-734b-4552-98fb-186284aa4b2e','20c47043-787d-4906-b3fe-df10df306130',100.0000,12.00,'2026-04-14 04:55:30','2026-04-14 04:55:30'),
('f3f8a233-d0fd-44f6-accd-0d78dc3e7a24','34a7ad59-9ca0-4cbf-8c56-3d087103edeb','5d01eda0-e3ed-4700-bf3b-3fc24ec47132',500.0000,5.00,'2026-04-14 04:55:30','2026-04-14 04:55:30');
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
('34a7ad59-9ca0-4cbf-8c56-3d087103edeb','FAC-INS-ACC-003-99','da7fe9dc-8e3f-4877-aeae-b1ad5d9a71af','178cb120-83ad-4de7-8423-e9fd0e20005b','59eb30f9-ca5a-4609-bf1d-3c823b908de2','2026-04-14 04:55:30','2026-04-14 04:55:30','RECIBIDO'),
('524f8034-8910-4fc9-846c-ad8eb9de6124','FAC-INS-TEX-002-99','d2ca2750-faa7-4345-841c-5ed3dd1b7abc','178cb120-83ad-4de7-8423-e9fd0e20005b','a6dfc1a0-7f74-4080-88dd-cce7e5eeaf45','2026-04-14 04:55:30','2026-04-14 04:55:30','RECIBIDO'),
('6a0c762b-734b-4552-98fb-186284aa4b2e','FAC-INS-ACC-001-99','da7fe9dc-8e3f-4877-aeae-b1ad5d9a71af','178cb120-83ad-4de7-8423-e9fd0e20005b','429b2bf3-f8bc-4b77-bd09-03b7d4ffba54','2026-04-14 04:55:30','2026-04-14 04:55:30','RECIBIDO'),
('fc4d4731-e144-465f-ba2f-c931eccea5a6','FAC-INS-TEX-001-99','d2ca2750-faa7-4345-841c-5ed3dd1b7abc','178cb120-83ad-4de7-8423-e9fd0e20005b','2da30220-ecd5-492f-8f99-4b7d48d98398','2026-04-14 04:55:30','2026-04-14 04:55:30','RECIBIDO');
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
('429d45e0-8926-4958-a1c1-08bcb4967939','7edb9659-a52d-4fa4-8871-d0420f50e18f','05dacdc6-d12d-4adc-82de-779cfe2bd979',25.0000,26.5000,10,1.5000,'2026-04-14 04:55:30','2026-04-14 04:55:30','178cb120-83ad-4de7-8423-e9fd0e20005b');
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
('1879c936-eab3-433a-82b1-dec237c8162f','f7b4d7a8-9108-4a32-8ae0-4f35cd686ef2','EMP-004','Analista de Suministros','Compras','2025-04-14 04:55:30','2026-04-14 04:55:29','2026-04-14 04:55:29'),
('91c01d45-c95f-4cb6-b893-5cdc3c5c4931','178cb120-83ad-4de7-8423-e9fd0e20005b','EMP-001','Director General','Dirección','2025-04-14 04:55:30','2026-04-14 04:55:29','2026-04-14 04:55:29'),
('b045dd61-4865-4526-8f52-48fd48bffe63','5252f29e-fb61-4bc3-bb0c-de06ab13b612','EMP-002','Jefe de Taller','Producción','2025-04-14 04:55:30','2026-04-14 04:55:29','2026-04-14 04:55:29'),
('cf2f5e12-81be-4ad7-a363-e279dbe46b65','521e2399-deb7-49b5-a258-ead0ddab6a10','EMP-003','Ejecutivo Comercial','Ventas','2025-04-14 04:55:30','2026-04-14 04:55:29','2026-04-14 04:55:29');
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
('7b8752bb-4bd3-4445-80ab-a7977deb2f73','Costura plana a dos hilos.','2026-04-14 04:55:30','2026-04-14 04:55:30','178cb120-83ad-4de7-8423-e9fd0e20005b','ACTIVO'),
('fe7beb8d-8eee-4fc5-a5ff-568d76ba543b','Corte láser y costura reforzada.','2026-04-14 04:55:30','2026-04-14 04:55:30','178cb120-83ad-4de7-8423-e9fd0e20005b','ACTIVO');
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
  KEY `idx_expdet_explosion` (`uuid_explosion`),
  KEY `idx_expdet_insumo` (`uuid_insumo`),
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
('05b6c89c-f10f-42c0-82ea-adf51a14340a','fe7beb8d-8eee-4fc5-a5ff-568d76ba543b','9854bf3d-b35c-4c91-ab30-6beb4aaa1cdf',2.5000,NULL,'2026-04-14 04:55:30','2026-04-14 04:55:30'),
('31900322-3a6a-430d-9428-48e63be7dae8','fe7beb8d-8eee-4fc5-a5ff-568d76ba543b','5d01eda0-e3ed-4700-bf3b-3fc24ec47132',1.0000,NULL,'2026-04-14 04:55:30','2026-04-14 04:55:30'),
('5ea6fd52-d8ba-44d3-b4ac-a6446e2224b8','fe7beb8d-8eee-4fc5-a5ff-568d76ba543b','20c47043-787d-4906-b3fe-df10df306130',1.0000,NULL,'2026-04-14 04:55:30','2026-04-14 04:55:30'),
('8d7ac729-1d3b-4674-90c0-2181109d921d','7b8752bb-4bd3-4445-80ab-a7977deb2f73','5d01eda0-e3ed-4700-bf3b-3fc24ec47132',1.0000,NULL,'2026-04-14 04:55:30','2026-04-14 04:55:30'),
('9abcce8b-5d75-4432-979b-523a251d0932','7b8752bb-4bd3-4445-80ab-a7977deb2f73','34109c8f-4699-4511-9b39-bbcf39a5974a',1.2000,NULL,'2026-04-14 04:55:30','2026-04-14 04:55:30');
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
('20c47043-787d-4906-b3fe-df10df306130','INS-ACC-001','Cierre Metálico YKK 15cm','b2396e2e-035b-477a-b60c-d3810816a349','PIEZA',1.0000,'PIEZA',100.0000,10.0000,NULL,'2026-04-14 04:55:30','2026-04-14 04:55:30','ACTIVO',NULL),
('34109c8f-4699-4511-9b39-bbcf39a5974a','INS-TEX-001','Algodón Negro Roll','e5dd9b05-252e-44df-88f1-ee738f59001b','ROLLO',100.0000,'METRO',1000.0000,10.0000,NULL,'2026-04-14 04:55:30','2026-04-14 04:55:30','ACTIVO',NULL),
('3e93bf3d-ad7a-448e-8203-844d0fe58b2e','INS-TEX-003','Denim Azul 14oz','ba68917d-e5b1-44b0-ac75-0adb53dded2e','ROLLO',40.0000,'METRO',0.0000,10.0000,NULL,'2026-04-14 04:55:30','2026-04-14 04:55:30','ACTIVO',NULL),
('4331e68e-8bd2-4f2f-9b41-287ae273e33e','INS-ACC-002','Botón Acero Inoxidable','ba68917d-e5b1-44b0-ac75-0adb53dded2e','PIEZA',1.0000,'PIEZA',0.0000,10.0000,NULL,'2026-04-14 04:55:30','2026-04-14 04:55:30','ACTIVO',NULL),
('5d01eda0-e3ed-4700-bf3b-3fc24ec47132','INS-ACC-003','Etiqueta Axis Bordada','4e048a20-99b4-49e8-8f4a-d7709ec6a062','PIEZA',1.0000,'PIEZA',500.0000,10.0000,NULL,'2026-04-14 04:55:30','2026-04-14 04:55:30','ACTIVO',NULL),
('9854bf3d-b35c-4c91-ab30-6beb4aaa1cdf','INS-TEX-002','Poliéster Gris Roll','073963aa-24a4-4b8c-8876-3557a2211f39','ROLLO',50.0000,'METRO',250.0000,10.0000,NULL,'2026-04-14 04:55:30','2026-04-14 04:55:30','ACTIVO',NULL);
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
('e4cf7dd3-45a0-48c5-a4d2-124ff7a55871','7edb9659-a52d-4fa4-8871-d0420f50e18f','5d01eda0-e3ed-4700-bf3b-3fc24ec47132',10.0000,12.0000,'ERROR_OPERARIO','2 etiquetas se dañaron al coser.','2026-04-14 04:55:30','2026-04-14 04:55:30','178cb120-83ad-4de7-8423-e9fd0e20005b');
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
('60cf1584-3d1e-4ec4-8219-04ee9c61557d','Axis Logo Tee White','Camiseta 100% algodón alta densidad.','e5dd9b05-252e-44df-88f1-ee738f59001b','/static/images/products/tshirt-white.jpg','2026-04-14 04:55:30','2026-04-14 04:55:30','ACTIVO'),
('a3a8cfb0-b285-4908-8d34-28cce917ccfb','Hoodie Oversight Black','Sudadera pesada con fit urbano.','073963aa-24a4-4b8c-8876-3557a2211f39','/static/images/products/hoodie-black.jpg','2026-04-14 04:55:30','2026-04-14 04:55:30','ACTIVO');
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
  KEY `idx_op_estado` (`estado`),
  KEY `idx_op_producto` (`uuid_producto`),
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
('04cff0fa-1a92-4ece-8a6c-e5daef7afe51','bb188f69-0812-4f2c-9a8b-4e685916cf5c',NULL,NULL,30,'Pendiente','2026-04-14 04:55:30','2026-04-14 04:55:30'),
('7edb9659-a52d-4fa4-8871-d0420f50e18f','06fde997-e181-4304-b63e-5e5e7a5daec6','8a3cab16-5016-43bc-a5cc-cf5706cdd3eb',NULL,10,'Terminado','2026-04-14 04:55:30','2026-04-14 04:55:30');
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
  KEY `idx_pedido_fecha` (`fecha_pedido`),
  KEY `idx_pedido_estatus` (`estatus`),
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
('305b72eb-0ced-4f1d-bd90-21f54a6a9750','a6dfc1a0-7f74-4080-88dd-cce7e5eeaf45','9854bf3d-b35c-4c91-ab30-6beb4aaa1cdf',5.0000,0.0000,220.00,'2026-04-14 04:55:30','2026-04-14 04:55:30'),
('3f98ec09-c3d0-4ed3-b355-5d40d291d8df','59eb30f9-ca5a-4609-bf1d-3c823b908de2','5d01eda0-e3ed-4700-bf3b-3fc24ec47132',500.0000,0.0000,5.00,'2026-04-14 04:55:30','2026-04-14 04:55:30'),
('59ba5386-c760-4d57-96c2-4e521f41160d','2da30220-ecd5-492f-8f99-4b7d48d98398','34109c8f-4699-4511-9b39-bbcf39a5974a',10.0000,0.0000,150.00,'2026-04-14 04:55:30','2026-04-14 04:55:30'),
('7349c348-c288-436b-b1dc-e445bcd455f9','429b2bf3-f8bc-4b77-bd09-03b7d4ffba54','20c47043-787d-4906-b3fe-df10df306130',100.0000,0.0000,12.00,'2026-04-14 04:55:30','2026-04-14 04:55:30');
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
('2da30220-ecd5-492f-8f99-4b7d48d98398','PED-INS-TEX-001','d2ca2750-faa7-4345-841c-5ed3dd1b7abc','178cb120-83ad-4de7-8423-e9fd0e20005b','2026-04-14 04:55:30','2026-04-14 04:55:30','Completado'),
('429b2bf3-f8bc-4b77-bd09-03b7d4ffba54','PED-INS-ACC-001','da7fe9dc-8e3f-4877-aeae-b1ad5d9a71af','178cb120-83ad-4de7-8423-e9fd0e20005b','2026-04-14 04:55:30','2026-04-14 04:55:30','Completado'),
('59eb30f9-ca5a-4609-bf1d-3c823b908de2','PED-INS-ACC-003','da7fe9dc-8e3f-4877-aeae-b1ad5d9a71af','178cb120-83ad-4de7-8423-e9fd0e20005b','2026-04-14 04:55:30','2026-04-14 04:55:30','Completado'),
('a6dfc1a0-7f74-4080-88dd-cce7e5eeaf45','PED-INS-TEX-002','d2ca2750-faa7-4345-841c-5ed3dd1b7abc','178cb120-83ad-4de7-8423-e9fd0e20005b','2026-04-14 04:55:30','2026-04-14 04:55:30','Completado');
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
('06fde997-e181-4304-b63e-5e5e7a5daec6','a3a8cfb0-b285-4908-8d34-28cce917ccfb','7b8752bb-4bd3-4445-80ab-a7977deb2f73','H-OV-BLK-M','M',1200.00,10,0,1,'2026-04-14 04:55:30','2026-04-14 04:55:30'),
('1a8c7e1e-3aea-4727-89a6-93a9898cac68','60cf1584-3d1e-4ec4-8219-04ee9c61557d','fe7beb8d-8eee-4fc5-a5ff-568d76ba543b','T-LOG-WHT-M','M',450.00,47,0,1,'2026-04-14 04:55:30','2026-04-14 04:55:30'),
('6fb49cbc-a71f-4c0b-8f22-147fbf03532e','60cf1584-3d1e-4ec4-8219-04ee9c61557d','fe7beb8d-8eee-4fc5-a5ff-568d76ba543b','T-LOG-WHT-XL','XL',450.00,23,0,1,'2026-04-14 04:55:30','2026-04-14 04:55:30'),
('950616be-2616-4930-a8e1-19cb72cbf94d','60cf1584-3d1e-4ec4-8219-04ee9c61557d','fe7beb8d-8eee-4fc5-a5ff-568d76ba543b','T-LOG-WHT-S','S',450.00,49,0,1,'2026-04-14 04:55:30','2026-04-14 04:55:30'),
('95566812-b658-431f-adb0-b2e4a6b58d91','a3a8cfb0-b285-4908-8d34-28cce917ccfb','7b8752bb-4bd3-4445-80ab-a7977deb2f73','H-OV-BLK-XL','XL',1200.00,17,0,1,'2026-04-14 04:55:30','2026-04-14 04:55:30'),
('b0e60f60-27e1-4f3f-9d8f-1b5736d0ae4e','a3a8cfb0-b285-4908-8d34-28cce917ccfb','7b8752bb-4bd3-4445-80ab-a7977deb2f73','H-OV-BLK-S','S',1200.00,28,0,1,'2026-04-14 04:55:30','2026-04-14 04:55:30'),
('bb188f69-0812-4f2c-9a8b-4e685916cf5c','60cf1584-3d1e-4ec4-8219-04ee9c61557d','fe7beb8d-8eee-4fc5-a5ff-568d76ba543b','T-LOG-WHT-L','L',450.00,47,0,1,'2026-04-14 04:55:30','2026-04-14 04:55:30'),
('f729fc68-7502-4e9f-afde-acf515beb2f0','a3a8cfb0-b285-4908-8d34-28cce917ccfb','7b8752bb-4bd3-4445-80ab-a7977deb2f73','H-OV-BLK-L','L',1200.00,32,0,1,'2026-04-14 04:55:30','2026-04-14 04:55:30');
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
('d2ca2750-faa7-4345-841c-5ed3dd1b7abc','Textiles Premium S.A.','TEX900101ABC','Elena','2026-04-14 04:55:30','2026-04-14 04:55:30',NULL,1,'555-100-2000','Textiles'),
('da7fe9dc-8e3f-4877-aeae-b1ad5d9a71af','Accesorios Industriales','ACC850505XYZ','Carlos','2026-04-14 04:55:30','2026-04-14 04:55:30',NULL,1,'555-300-4000','Otros'),
('e5512d0b-cbc8-4bf3-b22f-31c782bb4cc0','Hilos y Avíos del Norte','HIL220301HAN','Roberto','2026-04-14 04:55:30','2026-04-14 04:55:30',NULL,1,'818-200-1010','Otros');
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
('0bb11562-a91c-421e-8eeb-2c5093c86635',1),
('178cb120-83ad-4de7-8423-e9fd0e20005b',1),
('5252f29e-fb61-4bc3-bb0c-de06ab13b612',3),
('521e2399-deb7-49b5-a258-ead0ddab6a10',2),
('f7b4d7a8-9108-4a32-8ae0-4f35cd686ef2',3),
('8b808a74-bd51-4403-95ad-8224d074e2a7',4),
('faed6acb-b63a-4c73-86f0-a776d1fc75ba',4);
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
('05dacdc6-d12d-4adc-82de-779cfe2bd979','9854bf3d-b35c-4c91-ab30-6beb4aaa1cdf','bfb879ff-b0cc-40a8-aea9-9cd085b66e61',50.0000,23.5000,'2026-04-14 04:55:30','2026-04-14 04:55:30'),
('122e224f-c106-4e41-afeb-c66fc13e0695','34109c8f-4699-4511-9b39-bbcf39a5974a','88f75ee7-a8f1-4a19-85fc-89de07a328ad',100.0000,100.0000,'2026-04-14 04:55:30','2026-04-14 04:55:30'),
('339addff-18f3-4260-a81b-d18076953579','9854bf3d-b35c-4c91-ab30-6beb4aaa1cdf','bfb879ff-b0cc-40a8-aea9-9cd085b66e61',50.0000,50.0000,'2026-04-14 04:55:30','2026-04-14 04:55:30'),
('396bdf14-8c91-4f28-bda4-a9f855daae98','34109c8f-4699-4511-9b39-bbcf39a5974a','88f75ee7-a8f1-4a19-85fc-89de07a328ad',100.0000,100.0000,'2026-04-14 04:55:30','2026-04-14 04:55:30'),
('8ab435a7-60e5-4150-aa5a-96c9bf344543','34109c8f-4699-4511-9b39-bbcf39a5974a','88f75ee7-a8f1-4a19-85fc-89de07a328ad',100.0000,100.0000,'2026-04-14 04:55:30','2026-04-14 04:55:30'),
('9505f706-acff-45dc-a7c4-0d97eae0057a','34109c8f-4699-4511-9b39-bbcf39a5974a','88f75ee7-a8f1-4a19-85fc-89de07a328ad',100.0000,100.0000,'2026-04-14 04:55:30','2026-04-14 04:55:30'),
('9d28035b-beb6-49e2-8659-38ab8d05520f','9854bf3d-b35c-4c91-ab30-6beb4aaa1cdf','bfb879ff-b0cc-40a8-aea9-9cd085b66e61',50.0000,50.0000,'2026-04-14 04:55:30','2026-04-14 04:55:30'),
('b1ab7e9d-4e39-43be-b1c9-9ea86edb60be','34109c8f-4699-4511-9b39-bbcf39a5974a','88f75ee7-a8f1-4a19-85fc-89de07a328ad',100.0000,100.0000,'2026-04-14 04:55:30','2026-04-14 04:55:30'),
('c2c032c4-bfcd-4f50-871c-c423a51b4b65','9854bf3d-b35c-4c91-ab30-6beb4aaa1cdf','bfb879ff-b0cc-40a8-aea9-9cd085b66e61',50.0000,50.0000,'2026-04-14 04:55:30','2026-04-14 04:55:30'),
('c8e71926-6c64-432b-bb93-e91fc9f0c66c','34109c8f-4699-4511-9b39-bbcf39a5974a','88f75ee7-a8f1-4a19-85fc-89de07a328ad',100.0000,100.0000,'2026-04-14 04:55:30','2026-04-14 04:55:30'),
('cac048e2-2a77-4d01-8548-0e358ec7296a','34109c8f-4699-4511-9b39-bbcf39a5974a','88f75ee7-a8f1-4a19-85fc-89de07a328ad',100.0000,100.0000,'2026-04-14 04:55:30','2026-04-14 04:55:30'),
('d37ae7bc-f859-43c7-bcbb-8c6ae2d4d3ad','34109c8f-4699-4511-9b39-bbcf39a5974a','88f75ee7-a8f1-4a19-85fc-89de07a328ad',100.0000,100.0000,'2026-04-14 04:55:30','2026-04-14 04:55:30'),
('ec7a9501-9882-4f81-a06f-bf59f9a2c239','9854bf3d-b35c-4c91-ab30-6beb4aaa1cdf','bfb879ff-b0cc-40a8-aea9-9cd085b66e61',50.0000,50.0000,'2026-04-14 04:55:30','2026-04-14 04:55:30'),
('fb0966e9-8b66-426b-861f-fd59b68964e6','34109c8f-4699-4511-9b39-bbcf39a5974a','88f75ee7-a8f1-4a19-85fc-89de07a328ad',100.0000,100.0000,'2026-04-14 04:55:30','2026-04-14 04:55:30'),
('fd78d6ab-dcb8-4075-9b70-f90f9b90e022','34109c8f-4699-4511-9b39-bbcf39a5974a','88f75ee7-a8f1-4a19-85fc-89de07a328ad',100.0000,100.0000,'2026-04-14 04:55:30','2026-04-14 04:55:30');
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
  KEY `ix_security_audit_logs_tabla` (`tabla`),
  KEY `ix_security_audit_logs_uuid_usuario` (`uuid_usuario`),
  KEY `ix_security_audit_logs_registro_uuid` (`registro_uuid`),
  KEY `ix_security_audit_logs_fecha` (`fecha`)
) ENGINE=InnoDB AUTO_INCREMENT=98 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `security_audit_logs`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `security_audit_logs` WRITE;
/*!40000 ALTER TABLE `security_audit_logs` DISABLE KEYS */;
INSERT INTO `security_audit_logs` VALUES
(1,'Sistema','Sistema','Sistema','default','INSERT','role','N/A',NULL,'{\"id\": null, \"name\": \"admin\", \"description\": null}',NULL,'2026-04-14 04:51:38'),
(2,'Sistema','Sistema','Sistema','default','INSERT','role','N/A',NULL,'{\"id\": null, \"name\": \"gerente\", \"description\": null}',NULL,'2026-04-14 04:51:38'),
(3,'Sistema','Sistema','Sistema','default','INSERT','role','N/A',NULL,'{\"id\": null, \"name\": \"produccion\", \"description\": null}',NULL,'2026-04-14 04:51:38'),
(4,'Sistema','Sistema','Sistema','default','INSERT','role','N/A',NULL,'{\"id\": null, \"name\": \"cliente\", \"description\": null}',NULL,'2026-04-14 04:51:38'),
(7,'Sistema','Sistema','Sistema','default','INSERT','usuarios','N/A',NULL,'{\"email\": \"hguzmanp.1@gmail.com\", \"active\": true, \"password\": \"$argon2id$v=19$m=65536,t=3,p=4$QAhB6B0jREjJ2Vsr5XzvvQ$S3bfVK1tUemXIthTOLywYBApLq/QM9qb7MlyEr8YMw0\", \"confirmed_at\": null, \"uuid_usuario\": null, \"fs_uniquifier\": \"c7b4564344684db4bac0cddbfc2a3450\", \"fecha_creacion\": null, \"tf_totp_secret\": null, \"nombre_completo\": \"Administrador Axis\", \"tf_phone_number\": null, \"mf_recovery_codes\": null, \"tf_primary_method\": null, \"fecha_actualizacion\": null, \"password_changed_at\": null}',NULL,'2026-04-14 04:55:17'),
(8,'Sistema','Sistema','Sistema','default','INSERT','usuarios','N/A',NULL,'{\"email\": \"admin@axis.com\", \"active\": true, \"password\": \"$argon2id$v=19$m=65536,t=3,p=4$1poTgnDu3ZtzjvF+TwmBMA$hczpYHMn4POxaNFHWEx0b/pjqwPYcMlmTPt9o0ccslo\", \"confirmed_at\": \"2026-04-14T04:55:29.481606+00:00\", \"uuid_usuario\": null, \"fs_uniquifier\": null, \"fecha_creacion\": null, \"tf_totp_secret\": null, \"nombre_completo\": \"Admin Axis\", \"tf_phone_number\": null, \"mf_recovery_codes\": null, \"tf_primary_method\": null, \"fecha_actualizacion\": null, \"password_changed_at\": null}',NULL,'2026-04-14 04:55:29'),
(9,'Sistema','Sistema','Sistema','default','INSERT','empleados','N/A',NULL,'{\"puesto\": \"Director General\", \"departamento\": \"Dirección\", \"uuid_usuario\": \"178cb120-83ad-4de7-8423-e9fd0e20005b\", \"fecha_ingreso\": \"2025-04-14T04:55:29.509799+00:00\", \"uuid_empleado\": null, \"fecha_creacion\": null, \"numero_empleado\": \"EMP-001\", \"fecha_actualizacion\": null}',NULL,'2026-04-14 04:55:29'),
(10,'Sistema','Sistema','Sistema','default','INSERT','usuarios','N/A',NULL,'{\"email\": \"modista@axis.com\", \"active\": true, \"password\": \"$argon2id$v=19$m=65536,t=3,p=4$ttY6B+C89/5fq/W+d44xJg$lU3JO2VDa8qvCL1BXJyHpxIHXMLHbFRPkRvjdy9bLF8\", \"confirmed_at\": \"2026-04-14T04:55:29.628104+00:00\", \"uuid_usuario\": null, \"fs_uniquifier\": null, \"fecha_creacion\": null, \"tf_totp_secret\": null, \"nombre_completo\": \"Modista Principal\", \"tf_phone_number\": null, \"mf_recovery_codes\": null, \"tf_primary_method\": null, \"fecha_actualizacion\": null, \"password_changed_at\": null}',NULL,'2026-04-14 04:55:29'),
(11,'Sistema','Sistema','Sistema','default','INSERT','empleados','N/A',NULL,'{\"puesto\": \"Jefe de Taller\", \"departamento\": \"Producción\", \"uuid_usuario\": \"5252f29e-fb61-4bc3-bb0c-de06ab13b612\", \"fecha_ingreso\": \"2025-04-14T04:55:29.637158+00:00\", \"uuid_empleado\": null, \"fecha_creacion\": null, \"numero_empleado\": \"EMP-002\", \"fecha_actualizacion\": null}',NULL,'2026-04-14 04:55:29'),
(12,'Sistema','Sistema','Sistema','default','INSERT','usuarios','N/A',NULL,'{\"email\": \"ventas@axis.com\", \"active\": true, \"password\": \"$argon2id$v=19$m=65536,t=3,p=4$5LwXAkDIOYfw3jvnnFOqdQ$lkhTYfzhKkkbcrVs4Fu6qO0c4csOYpJSLBnVIcVCtmU\", \"confirmed_at\": \"2026-04-14T04:55:29.748771+00:00\", \"uuid_usuario\": null, \"fs_uniquifier\": null, \"fecha_creacion\": null, \"tf_totp_secret\": null, \"nombre_completo\": \"Vendedor Axis\", \"tf_phone_number\": null, \"mf_recovery_codes\": null, \"tf_primary_method\": null, \"fecha_actualizacion\": null, \"password_changed_at\": null}',NULL,'2026-04-14 04:55:29'),
(13,'Sistema','Sistema','Sistema','default','INSERT','empleados','N/A',NULL,'{\"puesto\": \"Ejecutivo Comercial\", \"departamento\": \"Ventas\", \"uuid_usuario\": \"521e2399-deb7-49b5-a258-ead0ddab6a10\", \"fecha_ingreso\": \"2025-04-14T04:55:29.760654+00:00\", \"uuid_empleado\": null, \"fecha_creacion\": null, \"numero_empleado\": \"EMP-003\", \"fecha_actualizacion\": null}',NULL,'2026-04-14 04:55:29'),
(14,'Sistema','Sistema','Sistema','default','INSERT','usuarios','N/A',NULL,'{\"email\": \"compras@axis.com\", \"active\": true, \"password\": \"$argon2id$v=19$m=65536,t=3,p=4$uhciJATgHIPQOqf0PmcMAQ$06tgwaHreqfn7GRi+sA8Hk3XS+F2UBp4+7M2EKRqGmk\", \"confirmed_at\": \"2026-04-14T04:55:29.871698+00:00\", \"uuid_usuario\": null, \"fs_uniquifier\": null, \"fecha_creacion\": null, \"tf_totp_secret\": null, \"nombre_completo\": \"Comprador Axis\", \"tf_phone_number\": null, \"mf_recovery_codes\": null, \"tf_primary_method\": null, \"fecha_actualizacion\": null, \"password_changed_at\": null}',NULL,'2026-04-14 04:55:29'),
(15,'Sistema','Sistema','Sistema','default','INSERT','empleados','N/A',NULL,'{\"puesto\": \"Analista de Suministros\", \"departamento\": \"Compras\", \"uuid_usuario\": \"f7b4d7a8-9108-4a32-8ae0-4f35cd686ef2\", \"fecha_ingreso\": \"2025-04-14T04:55:29.879825+00:00\", \"uuid_empleado\": null, \"fecha_creacion\": null, \"numero_empleado\": \"EMP-004\", \"fecha_actualizacion\": null}',NULL,'2026-04-14 04:55:29'),
(16,'Sistema','Sistema','Sistema','default','INSERT','usuarios','N/A',NULL,'{\"email\": \"juan@axis.com\", \"active\": true, \"password\": \"$argon2id$v=19$m=65536,t=3,p=4$Ywwh5JzTGuOcM2aM8b63Ng$rdOFLhFnoc7sqDTNUZ7Z3f9TjRpetHFcm2DfTkvN6F0\", \"confirmed_at\": \"2026-04-14T04:55:29.991874+00:00\", \"uuid_usuario\": null, \"fs_uniquifier\": null, \"fecha_creacion\": null, \"tf_totp_secret\": null, \"nombre_completo\": \"Juan Cliente\", \"tf_phone_number\": null, \"mf_recovery_codes\": null, \"tf_primary_method\": null, \"fecha_actualizacion\": null, \"password_changed_at\": null}',NULL,'2026-04-14 04:55:29'),
(17,'Sistema','Sistema','Sistema','default','INSERT','clientes','N/A',NULL,'{\"telefono\": \"555-123-4567\", \"uuid_cliente\": null, \"uuid_usuario\": \"8b808a74-bd51-4403-95ad-8224d074e2a7\", \"fecha_creacion\": null, \"direccion_completa\": \"Av. Reforma 123, CDMX\", \"fecha_actualizacion\": null, \"usuario_actualizo_uuid\": null}',NULL,'2026-04-14 04:55:30'),
(18,'Sistema','Sistema','Sistema','default','INSERT','usuarios','N/A',NULL,'{\"email\": \"maria@axis.com\", \"active\": true, \"password\": \"$argon2id$v=19$m=65536,t=3,p=4$rtUa4xxDqJVSyhnDGOP8Xw$cwQ18LXnQt8Loc0MZn1h2D0vTqO1zyWYTXHwXpikOQA\", \"confirmed_at\": \"2026-04-14T04:55:30.122972+00:00\", \"uuid_usuario\": null, \"fs_uniquifier\": null, \"fecha_creacion\": null, \"tf_totp_secret\": null, \"nombre_completo\": \"Maria Lopez\", \"tf_phone_number\": null, \"mf_recovery_codes\": null, \"tf_primary_method\": null, \"fecha_actualizacion\": null, \"password_changed_at\": null}',NULL,'2026-04-14 04:55:30'),
(19,'Sistema','Sistema','Sistema','default','INSERT','clientes','N/A',NULL,'{\"telefono\": \"555-987-6543\", \"uuid_cliente\": null, \"uuid_usuario\": \"faed6acb-b63a-4c73-86f0-a776d1fc75ba\", \"fecha_creacion\": null, \"direccion_completa\": \"Insurgentes Sur 456, CDMX\", \"fecha_actualizacion\": null, \"usuario_actualizo_uuid\": null}',NULL,'2026-04-14 04:55:30'),
(20,'Sistema','Sistema','Sistema','default','INSERT','categorias','N/A',NULL,'{\"nombre\": \"Camisetas\", \"imagen_url\": null, \"descripcion\": \"Prendas de cuerpo superior\", \"fecha_creacion\": null, \"uuid_categoria\": null, \"estatus_visible\": true, \"usuario_creo_uuid\": null, \"fecha_actualizacion\": null, \"usuario_actualizo_uuid\": null}',NULL,'2026-04-14 04:55:30'),
(21,'Sistema','Sistema','Sistema','default','INSERT','categorias','N/A',NULL,'{\"nombre\": \"Pantalones\", \"imagen_url\": null, \"descripcion\": \"Prendas inferiores\", \"fecha_creacion\": null, \"uuid_categoria\": null, \"estatus_visible\": true, \"usuario_creo_uuid\": null, \"fecha_actualizacion\": null, \"usuario_actualizo_uuid\": null}',NULL,'2026-04-14 04:55:30'),
(22,'Sistema','Sistema','Sistema','default','INSERT','categorias','N/A',NULL,'{\"nombre\": \"Hoodies\", \"imagen_url\": null, \"descripcion\": \"Sudaderas urbanas\", \"fecha_creacion\": null, \"uuid_categoria\": null, \"estatus_visible\": true, \"usuario_creo_uuid\": null, \"fecha_actualizacion\": null, \"usuario_actualizo_uuid\": null}',NULL,'2026-04-14 04:55:30'),
(23,'Sistema','Sistema','Sistema','default','INSERT','categorias','N/A',NULL,'{\"nombre\": \"Chaquetas\", \"imagen_url\": null, \"descripcion\": \"Abrigos y chamarras\", \"fecha_creacion\": null, \"uuid_categoria\": null, \"estatus_visible\": true, \"usuario_creo_uuid\": null, \"fecha_actualizacion\": null, \"usuario_actualizo_uuid\": null}',NULL,'2026-04-14 04:55:30'),
(24,'Sistema','Sistema','Sistema','default','INSERT','categorias','N/A',NULL,'{\"nombre\": \"Shorts\", \"imagen_url\": null, \"descripcion\": \"Pantalones cortos\", \"fecha_creacion\": null, \"uuid_categoria\": null, \"estatus_visible\": true, \"usuario_creo_uuid\": null, \"fecha_actualizacion\": null, \"usuario_actualizo_uuid\": null}',NULL,'2026-04-14 04:55:30'),
(25,'Sistema','Sistema','Sistema','default','INSERT','categorias','N/A',NULL,'{\"nombre\": \"Accesorios\", \"imagen_url\": null, \"descripcion\": \"Gorras y complementos\", \"fecha_creacion\": null, \"uuid_categoria\": null, \"estatus_visible\": true, \"usuario_creo_uuid\": null, \"fecha_actualizacion\": null, \"usuario_actualizo_uuid\": null}',NULL,'2026-04-14 04:55:30'),
(26,'Sistema','Sistema','Sistema','default','INSERT','proveedores','N/A',NULL,'{\"rfc\": \"TEX900101ABC\", \"estatus\": null, \"telefono\": \"555-100-2000\", \"razon_social\": \"Textiles Premium S.A.\", \"fecha_creacion\": null, \"uuid_proveedor\": null, \"contacto_nombre\": \"Elena\", \"categoria_insumo\": \"Textiles\", \"usuario_creo_uuid\": null, \"fecha_actualizacion\": null}',NULL,'2026-04-14 04:55:30'),
(27,'Sistema','Sistema','Sistema','default','INSERT','proveedores','N/A',NULL,'{\"rfc\": \"ACC850505XYZ\", \"estatus\": null, \"telefono\": \"555-300-4000\", \"razon_social\": \"Accesorios Industriales\", \"fecha_creacion\": null, \"uuid_proveedor\": null, \"contacto_nombre\": \"Carlos\", \"categoria_insumo\": \"Otros\", \"usuario_creo_uuid\": null, \"fecha_actualizacion\": null}',NULL,'2026-04-14 04:55:30'),
(28,'Sistema','Sistema','Sistema','default','INSERT','proveedores','N/A',NULL,'{\"rfc\": \"HIL220301HAN\", \"estatus\": null, \"telefono\": \"818-200-1010\", \"razon_social\": \"Hilos y Avíos del Norte\", \"fecha_creacion\": null, \"uuid_proveedor\": null, \"contacto_nombre\": \"Roberto\", \"categoria_insumo\": \"Otros\", \"usuario_creo_uuid\": null, \"fecha_actualizacion\": null}',NULL,'2026-04-14 04:55:30'),
(29,'Sistema','Sistema','Sistema','default','INSERT','insumos','N/A',NULL,'{\"sku\": \"INS-TEX-001\", \"ancho\": null, \"nombre\": \"Algodón Negro Roll\", \"estatus\": null, \"uuid_insumo\": null, \"unidad_medida\": \"ROLLO\", \"fecha_creacion\": null, \"uuid_categoria\": \"e5dd9b05-252e-44df-88f1-ee738f59001b\", \"contenido_cantidad\": 100.0, \"fecha_actualizacion\": null, \"stock_minimo_alerta\": 10, \"stock_total_acumulado\": 0, \"usuario_actualizo_uuid\": null, \"contenido_unidad_medida\": \"METRO\"}',NULL,'2026-04-14 04:55:30'),
(30,'Sistema','Sistema','Sistema','default','INSERT','insumos','N/A',NULL,'{\"sku\": \"INS-TEX-002\", \"ancho\": null, \"nombre\": \"Poliéster Gris Roll\", \"estatus\": null, \"uuid_insumo\": null, \"unidad_medida\": \"ROLLO\", \"fecha_creacion\": null, \"uuid_categoria\": \"073963aa-24a4-4b8c-8876-3557a2211f39\", \"contenido_cantidad\": 50.0, \"fecha_actualizacion\": null, \"stock_minimo_alerta\": 10, \"stock_total_acumulado\": 0, \"usuario_actualizo_uuid\": null, \"contenido_unidad_medida\": \"METRO\"}',NULL,'2026-04-14 04:55:30'),
(31,'Sistema','Sistema','Sistema','default','INSERT','insumos','N/A',NULL,'{\"sku\": \"INS-TEX-003\", \"ancho\": null, \"nombre\": \"Denim Azul 14oz\", \"estatus\": null, \"uuid_insumo\": null, \"unidad_medida\": \"ROLLO\", \"fecha_creacion\": null, \"uuid_categoria\": \"ba68917d-e5b1-44b0-ac75-0adb53dded2e\", \"contenido_cantidad\": 40.0, \"fecha_actualizacion\": null, \"stock_minimo_alerta\": 10, \"stock_total_acumulado\": 0, \"usuario_actualizo_uuid\": null, \"contenido_unidad_medida\": \"METRO\"}',NULL,'2026-04-14 04:55:30'),
(32,'Sistema','Sistema','Sistema','default','INSERT','insumos','N/A',NULL,'{\"sku\": \"INS-ACC-001\", \"ancho\": null, \"nombre\": \"Cierre Metálico YKK 15cm\", \"estatus\": null, \"uuid_insumo\": null, \"unidad_medida\": \"PIEZA\", \"fecha_creacion\": null, \"uuid_categoria\": \"b2396e2e-035b-477a-b60c-d3810816a349\", \"contenido_cantidad\": 1.0, \"fecha_actualizacion\": null, \"stock_minimo_alerta\": 10, \"stock_total_acumulado\": 0, \"usuario_actualizo_uuid\": null, \"contenido_unidad_medida\": \"PIEZA\"}',NULL,'2026-04-14 04:55:30'),
(33,'Sistema','Sistema','Sistema','default','INSERT','insumos','N/A',NULL,'{\"sku\": \"INS-ACC-002\", \"ancho\": null, \"nombre\": \"Botón Acero Inoxidable\", \"estatus\": null, \"uuid_insumo\": null, \"unidad_medida\": \"PIEZA\", \"fecha_creacion\": null, \"uuid_categoria\": \"ba68917d-e5b1-44b0-ac75-0adb53dded2e\", \"contenido_cantidad\": 1.0, \"fecha_actualizacion\": null, \"stock_minimo_alerta\": 10, \"stock_total_acumulado\": 0, \"usuario_actualizo_uuid\": null, \"contenido_unidad_medida\": \"PIEZA\"}',NULL,'2026-04-14 04:55:30'),
(34,'Sistema','Sistema','Sistema','default','INSERT','insumos','N/A',NULL,'{\"sku\": \"INS-ACC-003\", \"ancho\": null, \"nombre\": \"Etiqueta Axis Bordada\", \"estatus\": null, \"uuid_insumo\": null, \"unidad_medida\": \"PIEZA\", \"fecha_creacion\": null, \"uuid_categoria\": \"4e048a20-99b4-49e8-8f4a-d7709ec6a062\", \"contenido_cantidad\": 1.0, \"fecha_actualizacion\": null, \"stock_minimo_alerta\": 10, \"stock_total_acumulado\": 0, \"usuario_actualizo_uuid\": null, \"contenido_unidad_medida\": \"PIEZA\"}',NULL,'2026-04-14 04:55:30'),
(35,'Sistema','Sistema','Sistema','default','INSERT','explosion_materiales_cabecera','N/A',NULL,'{\"estatus\": \"ACTIVO\", \"uuid_usuario\": \"178cb120-83ad-4de7-8423-e9fd0e20005b\", \"fecha_creacion\": null, \"uuid_explosion\": null, \"fecha_actualizacion\": null, \"instrucciones_proceso\": \"Corte láser y costura reforzada.\"}',NULL,'2026-04-14 04:55:30'),
(36,'Sistema','Sistema','Sistema','default','INSERT','explosion_materiales_detalle','N/A',NULL,'{\"uuid_insumo\": \"9854bf3d-b35c-4c91-ab30-6beb4aaa1cdf\", \"uuid_detalle\": null, \"fecha_creacion\": null, \"uuid_explosion\": \"fe7beb8d-8eee-4fc5-a5ff-568d76ba543b\", \"ancho_referencia\": null, \"fecha_actualizacion\": null, \"consumo_teorico_unitario\": 2.5}',NULL,'2026-04-14 04:55:30'),
(37,'Sistema','Sistema','Sistema','default','INSERT','explosion_materiales_detalle','N/A',NULL,'{\"uuid_insumo\": \"20c47043-787d-4906-b3fe-df10df306130\", \"uuid_detalle\": null, \"fecha_creacion\": null, \"uuid_explosion\": \"fe7beb8d-8eee-4fc5-a5ff-568d76ba543b\", \"ancho_referencia\": null, \"fecha_actualizacion\": null, \"consumo_teorico_unitario\": 1.0}',NULL,'2026-04-14 04:55:30'),
(38,'Sistema','Sistema','Sistema','default','INSERT','explosion_materiales_detalle','N/A',NULL,'{\"uuid_insumo\": \"5d01eda0-e3ed-4700-bf3b-3fc24ec47132\", \"uuid_detalle\": null, \"fecha_creacion\": null, \"uuid_explosion\": \"fe7beb8d-8eee-4fc5-a5ff-568d76ba543b\", \"ancho_referencia\": null, \"fecha_actualizacion\": null, \"consumo_teorico_unitario\": 1.0}',NULL,'2026-04-14 04:55:30'),
(39,'Sistema','Sistema','Sistema','default','INSERT','explosion_materiales_cabecera','N/A',NULL,'{\"estatus\": \"ACTIVO\", \"uuid_usuario\": \"178cb120-83ad-4de7-8423-e9fd0e20005b\", \"fecha_creacion\": null, \"uuid_explosion\": null, \"fecha_actualizacion\": null, \"instrucciones_proceso\": \"Costura plana a dos hilos.\"}',NULL,'2026-04-14 04:55:30'),
(40,'Sistema','Sistema','Sistema','default','INSERT','explosion_materiales_detalle','N/A',NULL,'{\"uuid_insumo\": \"34109c8f-4699-4511-9b39-bbcf39a5974a\", \"uuid_detalle\": null, \"fecha_creacion\": null, \"uuid_explosion\": \"7b8752bb-4bd3-4445-80ab-a7977deb2f73\", \"ancho_referencia\": null, \"fecha_actualizacion\": null, \"consumo_teorico_unitario\": 1.2}',NULL,'2026-04-14 04:55:30'),
(41,'Sistema','Sistema','Sistema','default','INSERT','explosion_materiales_detalle','N/A',NULL,'{\"uuid_insumo\": \"5d01eda0-e3ed-4700-bf3b-3fc24ec47132\", \"uuid_detalle\": null, \"fecha_creacion\": null, \"uuid_explosion\": \"7b8752bb-4bd3-4445-80ab-a7977deb2f73\", \"ancho_referencia\": null, \"fecha_actualizacion\": null, \"consumo_teorico_unitario\": 1.0}',NULL,'2026-04-14 04:55:30'),
(42,'Sistema','Sistema','Sistema','default','INSERT','modelos_ropa','N/A',NULL,'{\"estatus\": \"ACTIVO\", \"imagen_url\": \"/static/images/products/hoodie-black.jpg\", \"descripcion\": \"Sudadera pesada con fit urbano.\", \"uuid_modelo\": null, \"nombre_modelo\": \"Hoodie Oversight Black\", \"fecha_creacion\": null, \"uuid_categoria\": \"073963aa-24a4-4b8c-8876-3557a2211f39\", \"fecha_actualizacion\": null}',NULL,'2026-04-14 04:55:30'),
(43,'Sistema','Sistema','Sistema','default','INSERT','productos_terminados','N/A',NULL,'{\"talla\": \"S\", \"active\": null, \"uuid_modelo\": \"a3a8cfb0-b285-4908-8d34-28cce917ccfb\", \"precio_venta\": 1200.0, \"uuid_producto\": null, \"fecha_creacion\": null, \"sku_especifico\": \"H-OV-BLK-S\", \"uuid_explosion\": \"7b8752bb-4bd3-4445-80ab-a7977deb2f73\", \"fecha_actualizacion\": null, \"stock_fisico_actual\": 28, \"stock_minimo_alerta\": null}',NULL,'2026-04-14 04:55:30'),
(44,'Sistema','Sistema','Sistema','default','INSERT','productos_terminados','N/A',NULL,'{\"talla\": \"M\", \"active\": null, \"uuid_modelo\": \"a3a8cfb0-b285-4908-8d34-28cce917ccfb\", \"precio_venta\": 1200.0, \"uuid_producto\": null, \"fecha_creacion\": null, \"sku_especifico\": \"H-OV-BLK-M\", \"uuid_explosion\": \"7b8752bb-4bd3-4445-80ab-a7977deb2f73\", \"fecha_actualizacion\": null, \"stock_fisico_actual\": 10, \"stock_minimo_alerta\": null}',NULL,'2026-04-14 04:55:30'),
(45,'Sistema','Sistema','Sistema','default','INSERT','productos_terminados','N/A',NULL,'{\"talla\": \"L\", \"active\": null, \"uuid_modelo\": \"a3a8cfb0-b285-4908-8d34-28cce917ccfb\", \"precio_venta\": 1200.0, \"uuid_producto\": null, \"fecha_creacion\": null, \"sku_especifico\": \"H-OV-BLK-L\", \"uuid_explosion\": \"7b8752bb-4bd3-4445-80ab-a7977deb2f73\", \"fecha_actualizacion\": null, \"stock_fisico_actual\": 32, \"stock_minimo_alerta\": null}',NULL,'2026-04-14 04:55:30'),
(46,'Sistema','Sistema','Sistema','default','INSERT','productos_terminados','N/A',NULL,'{\"talla\": \"XL\", \"active\": null, \"uuid_modelo\": \"a3a8cfb0-b285-4908-8d34-28cce917ccfb\", \"precio_venta\": 1200.0, \"uuid_producto\": null, \"fecha_creacion\": null, \"sku_especifico\": \"H-OV-BLK-XL\", \"uuid_explosion\": \"7b8752bb-4bd3-4445-80ab-a7977deb2f73\", \"fecha_actualizacion\": null, \"stock_fisico_actual\": 17, \"stock_minimo_alerta\": null}',NULL,'2026-04-14 04:55:30'),
(47,'Sistema','Sistema','Sistema','default','INSERT','modelos_ropa','N/A',NULL,'{\"estatus\": \"ACTIVO\", \"imagen_url\": \"/static/images/products/tshirt-white.jpg\", \"descripcion\": \"Camiseta 100% algodón alta densidad.\", \"uuid_modelo\": null, \"nombre_modelo\": \"Axis Logo Tee White\", \"fecha_creacion\": null, \"uuid_categoria\": \"e5dd9b05-252e-44df-88f1-ee738f59001b\", \"fecha_actualizacion\": null}',NULL,'2026-04-14 04:55:30'),
(48,'Sistema','Sistema','Sistema','default','INSERT','productos_terminados','N/A',NULL,'{\"talla\": \"S\", \"active\": null, \"uuid_modelo\": \"60cf1584-3d1e-4ec4-8219-04ee9c61557d\", \"precio_venta\": 450.0, \"uuid_producto\": null, \"fecha_creacion\": null, \"sku_especifico\": \"T-LOG-WHT-S\", \"uuid_explosion\": \"fe7beb8d-8eee-4fc5-a5ff-568d76ba543b\", \"fecha_actualizacion\": null, \"stock_fisico_actual\": 49, \"stock_minimo_alerta\": null}',NULL,'2026-04-14 04:55:30'),
(49,'Sistema','Sistema','Sistema','default','INSERT','productos_terminados','N/A',NULL,'{\"talla\": \"M\", \"active\": null, \"uuid_modelo\": \"60cf1584-3d1e-4ec4-8219-04ee9c61557d\", \"precio_venta\": 450.0, \"uuid_producto\": null, \"fecha_creacion\": null, \"sku_especifico\": \"T-LOG-WHT-M\", \"uuid_explosion\": \"fe7beb8d-8eee-4fc5-a5ff-568d76ba543b\", \"fecha_actualizacion\": null, \"stock_fisico_actual\": 47, \"stock_minimo_alerta\": null}',NULL,'2026-04-14 04:55:30'),
(50,'Sistema','Sistema','Sistema','default','INSERT','productos_terminados','N/A',NULL,'{\"talla\": \"L\", \"active\": null, \"uuid_modelo\": \"60cf1584-3d1e-4ec4-8219-04ee9c61557d\", \"precio_venta\": 450.0, \"uuid_producto\": null, \"fecha_creacion\": null, \"sku_especifico\": \"T-LOG-WHT-L\", \"uuid_explosion\": \"fe7beb8d-8eee-4fc5-a5ff-568d76ba543b\", \"fecha_actualizacion\": null, \"stock_fisico_actual\": 47, \"stock_minimo_alerta\": null}',NULL,'2026-04-14 04:55:30'),
(51,'Sistema','Sistema','Sistema','default','INSERT','productos_terminados','N/A',NULL,'{\"talla\": \"XL\", \"active\": null, \"uuid_modelo\": \"60cf1584-3d1e-4ec4-8219-04ee9c61557d\", \"precio_venta\": 450.0, \"uuid_producto\": null, \"fecha_creacion\": null, \"sku_especifico\": \"T-LOG-WHT-XL\", \"uuid_explosion\": \"fe7beb8d-8eee-4fc5-a5ff-568d76ba543b\", \"fecha_actualizacion\": null, \"stock_fisico_actual\": 23, \"stock_minimo_alerta\": null}',NULL,'2026-04-14 04:55:30'),
(52,'Sistema','Sistema','Sistema','default','INSERT','pedidos_proveedor_encabezado','N/A',NULL,'{\"estatus\": \"Completado\", \"uuid_pedido\": null, \"fecha_pedido\": null, \"folio_pedido\": \"PED-INS-TEX-001\", \"uuid_proveedor\": \"d2ca2750-faa7-4345-841c-5ed3dd1b7abc\", \"fecha_actualizacion\": null, \"uuid_usuario_solicita\": \"178cb120-83ad-4de7-8423-e9fd0e20005b\"}',NULL,'2026-04-14 04:55:30'),
(53,'Sistema','Sistema','Sistema','default','INSERT','pedidos_proveedor_detalle','N/A',NULL,'{\"uuid_insumo\": \"34109c8f-4699-4511-9b39-bbcf39a5974a\", \"uuid_pedido\": \"2da30220-ecd5-492f-8f99-4b7d48d98398\", \"fecha_creacion\": null, \"cantidad_pedida\": 10, \"cantidad_recibida\": null, \"fecha_actualizacion\": null, \"uuid_detalle_pedido\": null, \"costo_unitario_estimado\": 150.0}',NULL,'2026-04-14 04:55:30'),
(54,'Sistema','Sistema','Sistema','default','INSERT','compras_encabezado','N/A',NULL,'{\"estatus\": \"RECIBIDO\", \"uuid_compra\": null, \"uuid_pedido\": \"2da30220-ecd5-492f-8f99-4b7d48d98398\", \"fecha_compra\": null, \"folio_factura\": \"FAC-INS-TEX-001-99\", \"uuid_proveedor\": \"d2ca2750-faa7-4345-841c-5ed3dd1b7abc\", \"fecha_actualizacion\": null, \"uuid_usuario_registro\": \"178cb120-83ad-4de7-8423-e9fd0e20005b\"}',NULL,'2026-04-14 04:55:30'),
(55,'Sistema','Sistema','Sistema','default','INSERT','compras_detalle','N/A',NULL,'{\"uuid_compra\": \"fc4d4731-e144-465f-ba2f-c931eccea5a6\", \"uuid_insumo\": \"34109c8f-4699-4511-9b39-bbcf39a5974a\", \"fecha_creacion\": null, \"cantidad_comprada\": 10, \"fecha_actualizacion\": null, \"uuid_detalle_compra\": null, \"costo_unitario_compra\": 150.0}',NULL,'2026-04-14 04:55:30'),
(56,'Sistema','Sistema','Sistema','default','INSERT','rollos_inventario','N/A',NULL,'{\"uuid_rollo\": null, \"uuid_insumo\": \"34109c8f-4699-4511-9b39-bbcf39a5974a\", \"fecha_creacion\": null, \"metraje_inicial\": 100.0, \"fecha_actualizacion\": null, \"uuid_detalle_compra\": \"88f75ee7-a8f1-4a19-85fc-89de07a328ad\", \"metraje_continuo_actual\": 100.0}',NULL,'2026-04-14 04:55:30'),
(57,'Sistema','Sistema','Sistema','default','INSERT','rollos_inventario','N/A',NULL,'{\"uuid_rollo\": null, \"uuid_insumo\": \"34109c8f-4699-4511-9b39-bbcf39a5974a\", \"fecha_creacion\": null, \"metraje_inicial\": 100.0, \"fecha_actualizacion\": null, \"uuid_detalle_compra\": \"88f75ee7-a8f1-4a19-85fc-89de07a328ad\", \"metraje_continuo_actual\": 100.0}',NULL,'2026-04-14 04:55:30'),
(58,'Sistema','Sistema','Sistema','default','INSERT','rollos_inventario','N/A',NULL,'{\"uuid_rollo\": null, \"uuid_insumo\": \"34109c8f-4699-4511-9b39-bbcf39a5974a\", \"fecha_creacion\": null, \"metraje_inicial\": 100.0, \"fecha_actualizacion\": null, \"uuid_detalle_compra\": \"88f75ee7-a8f1-4a19-85fc-89de07a328ad\", \"metraje_continuo_actual\": 100.0}',NULL,'2026-04-14 04:55:30'),
(59,'Sistema','Sistema','Sistema','default','INSERT','rollos_inventario','N/A',NULL,'{\"uuid_rollo\": null, \"uuid_insumo\": \"34109c8f-4699-4511-9b39-bbcf39a5974a\", \"fecha_creacion\": null, \"metraje_inicial\": 100.0, \"fecha_actualizacion\": null, \"uuid_detalle_compra\": \"88f75ee7-a8f1-4a19-85fc-89de07a328ad\", \"metraje_continuo_actual\": 100.0}',NULL,'2026-04-14 04:55:30'),
(60,'Sistema','Sistema','Sistema','default','INSERT','rollos_inventario','N/A',NULL,'{\"uuid_rollo\": null, \"uuid_insumo\": \"34109c8f-4699-4511-9b39-bbcf39a5974a\", \"fecha_creacion\": null, \"metraje_inicial\": 100.0, \"fecha_actualizacion\": null, \"uuid_detalle_compra\": \"88f75ee7-a8f1-4a19-85fc-89de07a328ad\", \"metraje_continuo_actual\": 100.0}',NULL,'2026-04-14 04:55:30'),
(61,'Sistema','Sistema','Sistema','default','INSERT','rollos_inventario','N/A',NULL,'{\"uuid_rollo\": null, \"uuid_insumo\": \"34109c8f-4699-4511-9b39-bbcf39a5974a\", \"fecha_creacion\": null, \"metraje_inicial\": 100.0, \"fecha_actualizacion\": null, \"uuid_detalle_compra\": \"88f75ee7-a8f1-4a19-85fc-89de07a328ad\", \"metraje_continuo_actual\": 100.0}',NULL,'2026-04-14 04:55:30'),
(62,'Sistema','Sistema','Sistema','default','INSERT','rollos_inventario','N/A',NULL,'{\"uuid_rollo\": null, \"uuid_insumo\": \"34109c8f-4699-4511-9b39-bbcf39a5974a\", \"fecha_creacion\": null, \"metraje_inicial\": 100.0, \"fecha_actualizacion\": null, \"uuid_detalle_compra\": \"88f75ee7-a8f1-4a19-85fc-89de07a328ad\", \"metraje_continuo_actual\": 100.0}',NULL,'2026-04-14 04:55:30'),
(63,'Sistema','Sistema','Sistema','default','INSERT','rollos_inventario','N/A',NULL,'{\"uuid_rollo\": null, \"uuid_insumo\": \"34109c8f-4699-4511-9b39-bbcf39a5974a\", \"fecha_creacion\": null, \"metraje_inicial\": 100.0, \"fecha_actualizacion\": null, \"uuid_detalle_compra\": \"88f75ee7-a8f1-4a19-85fc-89de07a328ad\", \"metraje_continuo_actual\": 100.0}',NULL,'2026-04-14 04:55:30'),
(64,'Sistema','Sistema','Sistema','default','INSERT','rollos_inventario','N/A',NULL,'{\"uuid_rollo\": null, \"uuid_insumo\": \"34109c8f-4699-4511-9b39-bbcf39a5974a\", \"fecha_creacion\": null, \"metraje_inicial\": 100.0, \"fecha_actualizacion\": null, \"uuid_detalle_compra\": \"88f75ee7-a8f1-4a19-85fc-89de07a328ad\", \"metraje_continuo_actual\": 100.0}',NULL,'2026-04-14 04:55:30'),
(65,'Sistema','Sistema','Sistema','default','INSERT','rollos_inventario','N/A',NULL,'{\"uuid_rollo\": null, \"uuid_insumo\": \"34109c8f-4699-4511-9b39-bbcf39a5974a\", \"fecha_creacion\": null, \"metraje_inicial\": 100.0, \"fecha_actualizacion\": null, \"uuid_detalle_compra\": \"88f75ee7-a8f1-4a19-85fc-89de07a328ad\", \"metraje_continuo_actual\": 100.0}',NULL,'2026-04-14 04:55:30'),
(66,'Sistema','Sistema','Sistema','default','UPDATE','insumos','34109c8f-4699-4511-9b39-bbcf39a5974a','{\"stock_total_acumulado\": 0.0}','{\"stock_total_acumulado\": 1000.0}',NULL,'2026-04-14 04:55:30'),
(67,'Sistema','Sistema','Sistema','default','INSERT','pedidos_proveedor_encabezado','N/A',NULL,'{\"estatus\": \"Completado\", \"uuid_pedido\": null, \"fecha_pedido\": null, \"folio_pedido\": \"PED-INS-TEX-002\", \"uuid_proveedor\": \"d2ca2750-faa7-4345-841c-5ed3dd1b7abc\", \"fecha_actualizacion\": null, \"uuid_usuario_solicita\": \"178cb120-83ad-4de7-8423-e9fd0e20005b\"}',NULL,'2026-04-14 04:55:30'),
(68,'Sistema','Sistema','Sistema','default','INSERT','pedidos_proveedor_detalle','N/A',NULL,'{\"uuid_insumo\": \"9854bf3d-b35c-4c91-ab30-6beb4aaa1cdf\", \"uuid_pedido\": \"a6dfc1a0-7f74-4080-88dd-cce7e5eeaf45\", \"fecha_creacion\": null, \"cantidad_pedida\": 5, \"cantidad_recibida\": null, \"fecha_actualizacion\": null, \"uuid_detalle_pedido\": null, \"costo_unitario_estimado\": 220.0}',NULL,'2026-04-14 04:55:30'),
(69,'Sistema','Sistema','Sistema','default','INSERT','compras_encabezado','N/A',NULL,'{\"estatus\": \"RECIBIDO\", \"uuid_compra\": null, \"uuid_pedido\": \"a6dfc1a0-7f74-4080-88dd-cce7e5eeaf45\", \"fecha_compra\": null, \"folio_factura\": \"FAC-INS-TEX-002-99\", \"uuid_proveedor\": \"d2ca2750-faa7-4345-841c-5ed3dd1b7abc\", \"fecha_actualizacion\": null, \"uuid_usuario_registro\": \"178cb120-83ad-4de7-8423-e9fd0e20005b\"}',NULL,'2026-04-14 04:55:30'),
(70,'Sistema','Sistema','Sistema','default','INSERT','compras_detalle','N/A',NULL,'{\"uuid_compra\": \"524f8034-8910-4fc9-846c-ad8eb9de6124\", \"uuid_insumo\": \"9854bf3d-b35c-4c91-ab30-6beb4aaa1cdf\", \"fecha_creacion\": null, \"cantidad_comprada\": 5, \"fecha_actualizacion\": null, \"uuid_detalle_compra\": null, \"costo_unitario_compra\": 220.0}',NULL,'2026-04-14 04:55:30'),
(71,'Sistema','Sistema','Sistema','default','INSERT','rollos_inventario','N/A',NULL,'{\"uuid_rollo\": null, \"uuid_insumo\": \"9854bf3d-b35c-4c91-ab30-6beb4aaa1cdf\", \"fecha_creacion\": null, \"metraje_inicial\": 50.0, \"fecha_actualizacion\": null, \"uuid_detalle_compra\": \"bfb879ff-b0cc-40a8-aea9-9cd085b66e61\", \"metraje_continuo_actual\": 50.0}',NULL,'2026-04-14 04:55:30'),
(72,'Sistema','Sistema','Sistema','default','INSERT','rollos_inventario','N/A',NULL,'{\"uuid_rollo\": null, \"uuid_insumo\": \"9854bf3d-b35c-4c91-ab30-6beb4aaa1cdf\", \"fecha_creacion\": null, \"metraje_inicial\": 50.0, \"fecha_actualizacion\": null, \"uuid_detalle_compra\": \"bfb879ff-b0cc-40a8-aea9-9cd085b66e61\", \"metraje_continuo_actual\": 50.0}',NULL,'2026-04-14 04:55:30'),
(73,'Sistema','Sistema','Sistema','default','INSERT','rollos_inventario','N/A',NULL,'{\"uuid_rollo\": null, \"uuid_insumo\": \"9854bf3d-b35c-4c91-ab30-6beb4aaa1cdf\", \"fecha_creacion\": null, \"metraje_inicial\": 50.0, \"fecha_actualizacion\": null, \"uuid_detalle_compra\": \"bfb879ff-b0cc-40a8-aea9-9cd085b66e61\", \"metraje_continuo_actual\": 50.0}',NULL,'2026-04-14 04:55:30'),
(74,'Sistema','Sistema','Sistema','default','INSERT','rollos_inventario','N/A',NULL,'{\"uuid_rollo\": null, \"uuid_insumo\": \"9854bf3d-b35c-4c91-ab30-6beb4aaa1cdf\", \"fecha_creacion\": null, \"metraje_inicial\": 50.0, \"fecha_actualizacion\": null, \"uuid_detalle_compra\": \"bfb879ff-b0cc-40a8-aea9-9cd085b66e61\", \"metraje_continuo_actual\": 50.0}',NULL,'2026-04-14 04:55:30'),
(75,'Sistema','Sistema','Sistema','default','INSERT','rollos_inventario','N/A',NULL,'{\"uuid_rollo\": null, \"uuid_insumo\": \"9854bf3d-b35c-4c91-ab30-6beb4aaa1cdf\", \"fecha_creacion\": null, \"metraje_inicial\": 50.0, \"fecha_actualizacion\": null, \"uuid_detalle_compra\": \"bfb879ff-b0cc-40a8-aea9-9cd085b66e61\", \"metraje_continuo_actual\": 50.0}',NULL,'2026-04-14 04:55:30'),
(76,'Sistema','Sistema','Sistema','default','UPDATE','insumos','9854bf3d-b35c-4c91-ab30-6beb4aaa1cdf','{\"stock_total_acumulado\": 0.0}','{\"stock_total_acumulado\": 250.0}',NULL,'2026-04-14 04:55:30'),
(77,'Sistema','Sistema','Sistema','default','INSERT','pedidos_proveedor_encabezado','N/A',NULL,'{\"estatus\": \"Completado\", \"uuid_pedido\": null, \"fecha_pedido\": null, \"folio_pedido\": \"PED-INS-ACC-001\", \"uuid_proveedor\": \"da7fe9dc-8e3f-4877-aeae-b1ad5d9a71af\", \"fecha_actualizacion\": null, \"uuid_usuario_solicita\": \"178cb120-83ad-4de7-8423-e9fd0e20005b\"}',NULL,'2026-04-14 04:55:30'),
(78,'Sistema','Sistema','Sistema','default','INSERT','pedidos_proveedor_detalle','N/A',NULL,'{\"uuid_insumo\": \"20c47043-787d-4906-b3fe-df10df306130\", \"uuid_pedido\": \"429b2bf3-f8bc-4b77-bd09-03b7d4ffba54\", \"fecha_creacion\": null, \"cantidad_pedida\": 100, \"cantidad_recibida\": null, \"fecha_actualizacion\": null, \"uuid_detalle_pedido\": null, \"costo_unitario_estimado\": 12.0}',NULL,'2026-04-14 04:55:30'),
(79,'Sistema','Sistema','Sistema','default','INSERT','compras_encabezado','N/A',NULL,'{\"estatus\": \"RECIBIDO\", \"uuid_compra\": null, \"uuid_pedido\": \"429b2bf3-f8bc-4b77-bd09-03b7d4ffba54\", \"fecha_compra\": null, \"folio_factura\": \"FAC-INS-ACC-001-99\", \"uuid_proveedor\": \"da7fe9dc-8e3f-4877-aeae-b1ad5d9a71af\", \"fecha_actualizacion\": null, \"uuid_usuario_registro\": \"178cb120-83ad-4de7-8423-e9fd0e20005b\"}',NULL,'2026-04-14 04:55:30'),
(80,'Sistema','Sistema','Sistema','default','INSERT','compras_detalle','N/A',NULL,'{\"uuid_compra\": \"6a0c762b-734b-4552-98fb-186284aa4b2e\", \"uuid_insumo\": \"20c47043-787d-4906-b3fe-df10df306130\", \"fecha_creacion\": null, \"cantidad_comprada\": 100, \"fecha_actualizacion\": null, \"uuid_detalle_compra\": null, \"costo_unitario_compra\": 12.0}',NULL,'2026-04-14 04:55:30'),
(81,'Sistema','Sistema','Sistema','default','UPDATE','insumos','20c47043-787d-4906-b3fe-df10df306130','{\"stock_total_acumulado\": 0.0}','{\"stock_total_acumulado\": 100}',NULL,'2026-04-14 04:55:30'),
(82,'Sistema','Sistema','Sistema','default','INSERT','pedidos_proveedor_encabezado','N/A',NULL,'{\"estatus\": \"Completado\", \"uuid_pedido\": null, \"fecha_pedido\": null, \"folio_pedido\": \"PED-INS-ACC-003\", \"uuid_proveedor\": \"da7fe9dc-8e3f-4877-aeae-b1ad5d9a71af\", \"fecha_actualizacion\": null, \"uuid_usuario_solicita\": \"178cb120-83ad-4de7-8423-e9fd0e20005b\"}',NULL,'2026-04-14 04:55:30'),
(83,'Sistema','Sistema','Sistema','default','INSERT','pedidos_proveedor_detalle','N/A',NULL,'{\"uuid_insumo\": \"5d01eda0-e3ed-4700-bf3b-3fc24ec47132\", \"uuid_pedido\": \"59eb30f9-ca5a-4609-bf1d-3c823b908de2\", \"fecha_creacion\": null, \"cantidad_pedida\": 500, \"cantidad_recibida\": null, \"fecha_actualizacion\": null, \"uuid_detalle_pedido\": null, \"costo_unitario_estimado\": 5.0}',NULL,'2026-04-14 04:55:30'),
(84,'Sistema','Sistema','Sistema','default','INSERT','compras_encabezado','N/A',NULL,'{\"estatus\": \"RECIBIDO\", \"uuid_compra\": null, \"uuid_pedido\": \"59eb30f9-ca5a-4609-bf1d-3c823b908de2\", \"fecha_compra\": null, \"folio_factura\": \"FAC-INS-ACC-003-99\", \"uuid_proveedor\": \"da7fe9dc-8e3f-4877-aeae-b1ad5d9a71af\", \"fecha_actualizacion\": null, \"uuid_usuario_registro\": \"178cb120-83ad-4de7-8423-e9fd0e20005b\"}',NULL,'2026-04-14 04:55:30'),
(85,'Sistema','Sistema','Sistema','default','INSERT','compras_detalle','N/A',NULL,'{\"uuid_compra\": \"34a7ad59-9ca0-4cbf-8c56-3d087103edeb\", \"uuid_insumo\": \"5d01eda0-e3ed-4700-bf3b-3fc24ec47132\", \"fecha_creacion\": null, \"cantidad_comprada\": 500, \"fecha_actualizacion\": null, \"uuid_detalle_compra\": null, \"costo_unitario_compra\": 5.0}',NULL,'2026-04-14 04:55:30'),
(86,'Sistema','Sistema','Sistema','default','UPDATE','insumos','5d01eda0-e3ed-4700-bf3b-3fc24ec47132','{\"stock_total_acumulado\": 0.0}','{\"stock_total_acumulado\": 500}',NULL,'2026-04-14 04:55:30'),
(87,'Sistema','Sistema','Sistema','default','INSERT','ventas_encabezado','N/A',NULL,'{\"uuid_venta\": null, \"fecha_venta\": null, \"metodo_pago\": \"Tarjeta\", \"uuid_cliente\": \"93375c12-04fa-411f-8cab-5006e6290962\", \"estatus_envio\": \"Entregado\", \"numero_pedido\": \"AX-101\", \"fecha_actualizacion\": null}',NULL,'2026-04-14 04:55:30'),
(88,'Sistema','Sistema','Sistema','default','INSERT','ventas_detalle','N/A',NULL,'{\"cantidad\": 1, \"uuid_venta\": \"801cc793-c048-4e38-8c66-a0bdb0d920e7\", \"uuid_detalle\": null, \"uuid_producto\": \"06fde997-e181-4304-b63e-5e5e7a5daec6\", \"fecha_creacion\": null, \"fecha_actualizacion\": null, \"precio_unitario_historico\": 1200.0}',NULL,'2026-04-14 04:55:30'),
(89,'Sistema','Sistema','Sistema','default','INSERT','ventas_detalle','N/A',NULL,'{\"cantidad\": 2, \"uuid_venta\": \"801cc793-c048-4e38-8c66-a0bdb0d920e7\", \"uuid_detalle\": null, \"uuid_producto\": \"bb188f69-0812-4f2c-9a8b-4e685916cf5c\", \"fecha_creacion\": null, \"fecha_actualizacion\": null, \"precio_unitario_historico\": 450.0}',NULL,'2026-04-14 04:55:30'),
(90,'Sistema','Sistema','Sistema','default','INSERT','ventas_encabezado','N/A',NULL,'{\"uuid_venta\": null, \"fecha_venta\": null, \"metodo_pago\": \"Paypal\", \"uuid_cliente\": \"93375c12-04fa-411f-8cab-5006e6290962\", \"estatus_envio\": \"Procesando\", \"numero_pedido\": \"AX-102\", \"fecha_actualizacion\": null}',NULL,'2026-04-14 04:55:30'),
(91,'Sistema','Sistema','Sistema','default','INSERT','ventas_detalle','N/A',NULL,'{\"cantidad\": 2, \"uuid_venta\": \"bec85b91-cf16-4f66-8cf5-b671c364818b\", \"uuid_detalle\": null, \"uuid_producto\": \"06fde997-e181-4304-b63e-5e5e7a5daec6\", \"fecha_creacion\": null, \"fecha_actualizacion\": null, \"precio_unitario_historico\": 1200.0}',NULL,'2026-04-14 04:55:30'),
(92,'Sistema','Sistema','Sistema','default','INSERT','ordenes_produccion','N/A',NULL,'{\"estado\": \"Terminado\", \"uuid_op\": null, \"uuid_producto\": \"06fde997-e181-4304-b63e-5e5e7a5daec6\", \"fecha_solicitud\": null, \"uuid_venta_detalle\": \"8a3cab16-5016-43bc-a5cc-cf5706cdd3eb\", \"cantidad_a_producir\": 10, \"fecha_actualizacion\": null, \"uuid_pedido_detalle\": null}',NULL,'2026-04-14 04:55:30'),
(93,'Sistema','Sistema','Sistema','default','INSERT','ejecucion_corte','N/A',NULL,'{\"uuid_op\": \"7edb9659-a52d-4fa4-8871-d0420f50e18f\", \"uuid_corte\": null, \"fecha_proceso\": null, \"uuid_rollo_used\": \"05dacdc6-d12d-4adc-82de-779cfe2bd979\", \"usuario_corto_uuid\": \"178cb120-83ad-4de7-8423-e9fd0e20005b\", \"fecha_actualizacion\": null, \"merma_real_calculada\": 1.5, \"metros_sacados_bodega\": 26.5, \"prendas_reales_logradas\": 10, \"metros_teoricos_requeridos\": 25.0}',NULL,'2026-04-14 04:55:30'),
(94,'Sistema','Sistema','Sistema','default','INSERT','merma_piezas','N/A',NULL,'{\"motivo\": \"ERROR_OPERARIO\", \"uuid_op\": \"7edb9659-a52d-4fa4-8871-d0420f50e18f\", \"uuid_merma\": null, \"uuid_insumo\": \"5d01eda0-e3ed-4700-bf3b-3fc24ec47132\", \"observaciones\": \"2 etiquetas se dañaron al coser.\", \"fecha_registro\": null, \"cantidad_teorica\": 10, \"fecha_actualizacion\": null, \"usuario_registro_uuid\": \"178cb120-83ad-4de7-8423-e9fd0e20005b\", \"cantidad_real_consumida\": 12}',NULL,'2026-04-14 04:55:30'),
(95,'Sistema','Sistema','Sistema','default','UPDATE','rollos_inventario','05dacdc6-d12d-4adc-82de-779cfe2bd979','{\"metraje_continuo_actual\": 50.0}','{\"metraje_continuo_actual\": 23.5}',NULL,'2026-04-14 04:55:30'),
(96,'Sistema','Sistema','Sistema','default','INSERT','ordenes_produccion','N/A',NULL,'{\"estado\": \"Pendiente\", \"uuid_op\": null, \"uuid_producto\": \"bb188f69-0812-4f2c-9a8b-4e685916cf5c\", \"fecha_solicitud\": null, \"uuid_venta_detalle\": null, \"cantidad_a_producir\": 30, \"fecha_actualizacion\": null, \"uuid_pedido_detalle\": null}',NULL,'2026-04-14 04:55:30'),
(97,'178cb120-83ad-4de7-8423-e9fd0e20005b','Admin Axis','admin','cliente_rol','UPDATE','usuarios','178cb120-83ad-4de7-8423-e9fd0e20005b','{\"tf_totp_secret\": null, \"tf_primary_method\": null}','{\"tf_totp_secret\": \"{\\\"enckey\\\":{\\\"c\\\":14,\\\"k\\\":\\\"YLL6LEHO6XUDWXIFXJ2P2I2RSEYAQRWF\\\",\\\"s\\\":\\\"XTL7V7677O77P7T7J6UQ\\\",\\\"t\\\":\\\"1\\\",\\\"v\\\":1},\\\"type\\\":\\\"totp\\\",\\\"v\\\":1}\", \"tf_primary_method\": \"authenticator\"}','172.18.0.1','2026-04-14 04:57:10');
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
('0bb11562-a91c-421e-8eeb-2c5093c86635','Administrador Axis','hguzmanp.1@gmail.com','$argon2id$v=19$m=65536,t=3,p=4$QAhB6B0jREjJ2Vsr5XzvvQ$S3bfVK1tUemXIthTOLywYBApLq/QM9qb7MlyEr8YMw0',1,'2026-04-14 04:55:17','2026-04-14 04:55:17','c7b4564344684db4bac0cddbfc2a3450',NULL,NULL,NULL,NULL,'2026-04-14 04:55:17',NULL),
('178cb120-83ad-4de7-8423-e9fd0e20005b','Admin Axis','admin@axis.com','$argon2id$v=19$m=65536,t=3,p=4$1poTgnDu3ZtzjvF+TwmBMA$hczpYHMn4POxaNFHWEx0b/pjqwPYcMlmTPt9o0ccslo',1,'2026-04-14 04:55:29','2026-04-14 04:57:10','7ea54de6f26e4c23a0dc5161b99fd3d5','2026-04-14 04:55:29','authenticator','{\"enckey\":{\"c\":14,\"k\":\"YLL6LEHO6XUDWXIFXJ2P2I2RSEYAQRWF\",\"s\":\"XTL7V7677O77P7T7J6UQ\",\"t\":\"1\",\"v\":1},\"type\":\"totp\",\"v\":1}',NULL,'2026-04-14 04:55:29',NULL),
('521e2399-deb7-49b5-a258-ead0ddab6a10','Vendedor Axis','ventas@axis.com','$argon2id$v=19$m=65536,t=3,p=4$5LwXAkDIOYfw3jvnnFOqdQ$lkhTYfzhKkkbcrVs4Fu6qO0c4csOYpJSLBnVIcVCtmU',1,'2026-04-14 04:55:29','2026-04-14 04:55:29','70c3209e8d1a4be8a584cd55e595f752','2026-04-14 04:55:30',NULL,NULL,NULL,'2026-04-14 04:55:29',NULL),
('5252f29e-fb61-4bc3-bb0c-de06ab13b612','Modista Principal','modista@axis.com','$argon2id$v=19$m=65536,t=3,p=4$ttY6B+C89/5fq/W+d44xJg$lU3JO2VDa8qvCL1BXJyHpxIHXMLHbFRPkRvjdy9bLF8',1,'2026-04-14 04:55:29','2026-04-14 04:55:29','22fa95ff882748e08d919c93615bc834','2026-04-14 04:55:30',NULL,NULL,NULL,'2026-04-14 04:55:29',NULL),
('8b808a74-bd51-4403-95ad-8224d074e2a7','Juan Cliente','juan@axis.com','$argon2id$v=19$m=65536,t=3,p=4$Ywwh5JzTGuOcM2aM8b63Ng$rdOFLhFnoc7sqDTNUZ7Z3f9TjRpetHFcm2DfTkvN6F0',1,'2026-04-14 04:55:29','2026-04-14 04:55:29','79d848de78b848a297cba3fdda02c3ff','2026-04-14 04:55:30',NULL,NULL,NULL,'2026-04-14 04:55:29',NULL),
('f7b4d7a8-9108-4a32-8ae0-4f35cd686ef2','Comprador Axis','compras@axis.com','$argon2id$v=19$m=65536,t=3,p=4$uhciJATgHIPQOqf0PmcMAQ$06tgwaHreqfn7GRi+sA8Hk3XS+F2UBp4+7M2EKRqGmk',1,'2026-04-14 04:55:29','2026-04-14 04:55:29','7ebd9d4a662f48b4be35b1b2ee1fd9d4','2026-04-14 04:55:30',NULL,NULL,NULL,'2026-04-14 04:55:29',NULL),
('faed6acb-b63a-4c73-86f0-a776d1fc75ba','Maria Lopez','maria@axis.com','$argon2id$v=19$m=65536,t=3,p=4$rtUa4xxDqJVSyhnDGOP8Xw$cwQ18LXnQt8Loc0MZn1h2D0vTqO1zyWYTXHwXpikOQA',1,'2026-04-14 04:55:30','2026-04-14 04:55:30','a0bb93806cdc4b2988239ccd87157513','2026-04-14 04:55:30',NULL,NULL,NULL,'2026-04-14 04:55:30',NULL);
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
('78aa41a1-a6f0-41e9-987e-955fbc4be763','801cc793-c048-4e38-8c66-a0bdb0d920e7','06fde997-e181-4304-b63e-5e5e7a5daec6',1,1200.00,'2026-04-14 04:55:30','2026-04-14 04:55:30'),
('8a3cab16-5016-43bc-a5cc-cf5706cdd3eb','bec85b91-cf16-4f66-8cf5-b671c364818b','06fde997-e181-4304-b63e-5e5e7a5daec6',2,1200.00,'2026-04-14 04:55:30','2026-04-14 04:55:30'),
('a0be0029-5eff-4303-9cc8-074be993033d','801cc793-c048-4e38-8c66-a0bdb0d920e7','bb188f69-0812-4f2c-9a8b-4e685916cf5c',2,450.00,'2026-04-14 04:55:30','2026-04-14 04:55:30');
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
('801cc793-c048-4e38-8c66-a0bdb0d920e7','AX-101','93375c12-04fa-411f-8cab-5006e6290962','Tarjeta','Entregado','2026-04-14 04:55:30','2026-04-14 04:55:30'),
('bec85b91-cf16-4f66-8cf5-b671c364818b','AX-102','93375c12-04fa-411f-8cab-5006e6290962','Paypal','Procesando','2026-04-14 04:55:30','2026-04-14 04:55:30');
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

-- Dump completed on 2026-04-14  4:57:23
