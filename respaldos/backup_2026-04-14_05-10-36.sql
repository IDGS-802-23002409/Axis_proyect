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
('2cb3d1e2-e62c-4438-865e-704b35c133e1','Pantalones','Prendas inferiores','/static/images/default/default-image.png',1,'2026-04-14 05:09:34','2026-04-14 05:09:34',NULL,NULL),
('301661d9-207f-429d-a91d-6419ebd40d76','Shorts','Pantalones cortos','/static/images/default/default-image.png',1,'2026-04-14 05:09:34','2026-04-14 05:09:34',NULL,NULL),
('562156c6-6dec-48aa-9fa4-f307df5cfde9','Camisetas','Prendas de cuerpo superior','/static/images/default/default-image.png',1,'2026-04-14 05:09:34','2026-04-14 05:09:34',NULL,NULL),
('6bfb63ec-4450-4c16-bc4d-9aef01d14345','Chaquetas','Abrigos y chamarras','/static/images/default/default-image.png',1,'2026-04-14 05:09:34','2026-04-14 05:09:34',NULL,NULL),
('f3a20cb5-362c-4bce-99da-bccc55fc1138','Hoodies','Sudaderas urbanas','/static/images/default/default-image.png',1,'2026-04-14 05:09:34','2026-04-14 05:09:34',NULL,NULL),
('fd2f22d5-276e-4816-b57d-3a9b8655e01f','Accesorios','Gorras y complementos','/static/images/default/default-image.png',1,'2026-04-14 05:09:34','2026-04-14 05:09:34',NULL,NULL);
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
('2754c910-75f9-4447-9d4a-f783061f40a9','323c5471-f959-41fb-97ff-ad12ed417cc2','555-123-4567','Av. Reforma 123, CDMX','2026-04-14 05:09:34','2026-04-14 05:09:34',NULL),
('2d3026b3-62b8-49fc-a017-e6748693dcc9','cf4dc48f-ad19-49a6-9ab7-b8ad690bb982','555-987-6543','Insurgentes Sur 456, CDMX','2026-04-14 05:09:34','2026-04-14 05:09:34',NULL);
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
('0187cb82-5341-42da-b424-df19ac92e452','923dfcf2-579d-4137-b6bc-02aabaa1a628','c8bf5828-7c54-4c8f-a310-1232856eef44',500.0000,5.00,'2026-04-14 05:09:34','2026-04-14 05:09:34'),
('8c53f951-8e26-4b46-9d1e-b5d0d6d5b0dc','11bcad79-3ca3-45b3-9155-ee03039ef625','759dfd9f-9a35-4a0a-a89e-c5dc3ddc7c01',100.0000,12.00,'2026-04-14 05:09:34','2026-04-14 05:09:34'),
('bc04bc8b-515b-4700-b76b-1c14263ac25f','4c2f113f-2a97-4dd3-8205-fd1c59c89bef','81be855e-62f4-425a-ba74-c310706e8681',5.0000,220.00,'2026-04-14 05:09:34','2026-04-14 05:09:34'),
('f560f7e8-1226-42bf-9086-567ea16c53f9','bbbd1709-94e4-428f-90ed-c27a4cec2934','1dc7710a-a247-46cd-9161-bcc95669f98d',10.0000,150.00,'2026-04-14 05:09:34','2026-04-14 05:09:34');
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
('11bcad79-3ca3-45b3-9155-ee03039ef625','FAC-INS-ACC-001-99','0922ee6f-efb2-4957-baa5-8130029f941c','1344d2d6-c82e-467a-8c50-6364a778f0bb','9ac877ce-f3cc-4bd4-94fa-dcd01730f4e4','2026-04-14 05:09:34','2026-04-14 05:09:34','RECIBIDO'),
('4c2f113f-2a97-4dd3-8205-fd1c59c89bef','FAC-INS-TEX-002-99','44481cff-8dc3-4545-b241-d06ca6ecb46f','1344d2d6-c82e-467a-8c50-6364a778f0bb','41019023-3ff3-416d-94e4-06ff58325b9f','2026-04-14 05:09:34','2026-04-14 05:09:34','RECIBIDO'),
('923dfcf2-579d-4137-b6bc-02aabaa1a628','FAC-INS-ACC-003-99','0922ee6f-efb2-4957-baa5-8130029f941c','1344d2d6-c82e-467a-8c50-6364a778f0bb','d2022988-8d1d-4075-8cf0-422bf5d5d02c','2026-04-14 05:09:34','2026-04-14 05:09:34','RECIBIDO'),
('bbbd1709-94e4-428f-90ed-c27a4cec2934','FAC-INS-TEX-001-99','44481cff-8dc3-4545-b241-d06ca6ecb46f','1344d2d6-c82e-467a-8c50-6364a778f0bb','67b0b371-4854-4f30-ad5b-603bb3c8aa94','2026-04-14 05:09:34','2026-04-14 05:09:34','RECIBIDO');
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
('a23f0a43-50ce-4b8f-9846-4fe9dee764b6','20a8923a-056b-49e5-97f8-aed360fc7d81','2187a50d-698d-414e-bf66-04350ee86bb6',25.0000,26.5000,10,1.5000,'2026-04-14 05:09:34','2026-04-14 05:09:34','1344d2d6-c82e-467a-8c50-6364a778f0bb');
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
('072d3404-3512-4352-9052-075fb9f69a98','1a8fb32d-2298-4076-96ca-28300138f462','EMP-002','Jefe de Taller','Producción','2025-04-14 05:09:34','2026-04-14 05:09:33','2026-04-14 05:09:33'),
('304ed500-2430-4529-92dc-14c3334f612e','b935683e-5e64-4cae-9e2f-94fb896af4b9','EMP-003','Ejecutivo Comercial','Ventas','2025-04-14 05:09:34','2026-04-14 05:09:33','2026-04-14 05:09:33'),
('58fbf17b-c63b-4dd5-aefa-1a17fc1def59','262dcc8c-d33e-4fdb-8d6d-91ecbae6f45d','EMP-004','Analista de Suministros','Compras','2025-04-14 05:09:34','2026-04-14 05:09:33','2026-04-14 05:09:33'),
('6fc7f2b2-b2fa-4eed-8d0f-5ec96b61530c','1344d2d6-c82e-467a-8c50-6364a778f0bb','EMP-001','Director General','Dirección','2025-04-14 05:09:34','2026-04-14 05:09:33','2026-04-14 05:09:33');
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
('580539c8-022c-45d6-ab11-2f82bc766025','Corte láser y costura reforzada.','2026-04-14 05:09:34','2026-04-14 05:09:34','1344d2d6-c82e-467a-8c50-6364a778f0bb','ACTIVO'),
('654f98f0-96a1-4b05-80b4-0a1ec066416c','Costura plana a dos hilos.','2026-04-14 05:09:34','2026-04-14 05:09:34','1344d2d6-c82e-467a-8c50-6364a778f0bb','ACTIVO');
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
('036a044d-5702-45b9-a748-dfba5adae08d','580539c8-022c-45d6-ab11-2f82bc766025','759dfd9f-9a35-4a0a-a89e-c5dc3ddc7c01',1.0000,NULL,'2026-04-14 05:09:34','2026-04-14 05:09:34'),
('437e561f-5f72-4ee5-872e-d661f30bafb7','654f98f0-96a1-4b05-80b4-0a1ec066416c','1dc7710a-a247-46cd-9161-bcc95669f98d',1.2000,NULL,'2026-04-14 05:09:34','2026-04-14 05:09:34'),
('bd74b1c8-bbc0-4803-a31e-7945b57c034a','580539c8-022c-45d6-ab11-2f82bc766025','c8bf5828-7c54-4c8f-a310-1232856eef44',1.0000,NULL,'2026-04-14 05:09:34','2026-04-14 05:09:34'),
('c1e2b15c-a577-4255-8c2f-d0043a5aed56','580539c8-022c-45d6-ab11-2f82bc766025','81be855e-62f4-425a-ba74-c310706e8681',2.5000,NULL,'2026-04-14 05:09:34','2026-04-14 05:09:34'),
('f02561dd-d60e-4558-86bf-0924f0f0ad56','654f98f0-96a1-4b05-80b4-0a1ec066416c','c8bf5828-7c54-4c8f-a310-1232856eef44',1.0000,NULL,'2026-04-14 05:09:34','2026-04-14 05:09:34');
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
('1dc7710a-a247-46cd-9161-bcc95669f98d','INS-TEX-001','Algodón Negro Roll','562156c6-6dec-48aa-9fa4-f307df5cfde9','ROLLO',100.0000,'METRO',1000.0000,10.0000,NULL,'2026-04-14 05:09:34','2026-04-14 05:09:34','ACTIVO',NULL),
('759dfd9f-9a35-4a0a-a89e-c5dc3ddc7c01','INS-ACC-001','Cierre Metálico YKK 15cm','6bfb63ec-4450-4c16-bc4d-9aef01d14345','PIEZA',1.0000,'PIEZA',100.0000,10.0000,NULL,'2026-04-14 05:09:34','2026-04-14 05:09:34','ACTIVO',NULL),
('77e3ee46-0f97-4c64-9cfa-f2fca2e969db','INS-ACC-002','Botón Acero Inoxidable','2cb3d1e2-e62c-4438-865e-704b35c133e1','PIEZA',1.0000,'PIEZA',0.0000,10.0000,NULL,'2026-04-14 05:09:34','2026-04-14 05:09:34','ACTIVO',NULL),
('81be855e-62f4-425a-ba74-c310706e8681','INS-TEX-002','Poliéster Gris Roll','f3a20cb5-362c-4bce-99da-bccc55fc1138','ROLLO',50.0000,'METRO',250.0000,10.0000,NULL,'2026-04-14 05:09:34','2026-04-14 05:09:34','ACTIVO',NULL),
('86b2ec79-3f9f-4e06-85e7-84b52151dc32','INS-TEX-003','Denim Azul 14oz','2cb3d1e2-e62c-4438-865e-704b35c133e1','ROLLO',40.0000,'METRO',0.0000,10.0000,NULL,'2026-04-14 05:09:34','2026-04-14 05:09:34','ACTIVO',NULL),
('c8bf5828-7c54-4c8f-a310-1232856eef44','INS-ACC-003','Etiqueta Axis Bordada','fd2f22d5-276e-4816-b57d-3a9b8655e01f','PIEZA',1.0000,'PIEZA',500.0000,10.0000,NULL,'2026-04-14 05:09:34','2026-04-14 05:09:34','ACTIVO',NULL);
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
('8fa6772c-2d07-474a-af56-4606b38793bd','20a8923a-056b-49e5-97f8-aed360fc7d81','c8bf5828-7c54-4c8f-a310-1232856eef44',10.0000,12.0000,'ERROR_OPERARIO','2 etiquetas se dañaron al coser.','2026-04-14 05:09:34','2026-04-14 05:09:34','1344d2d6-c82e-467a-8c50-6364a778f0bb');
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
('1a5ce75b-75cf-473c-87a3-e5f45583d85f','Axis Logo Tee White','Camiseta 100% algodón alta densidad.','562156c6-6dec-48aa-9fa4-f307df5cfde9','/static/images/products/tshirt-white.jpg','2026-04-14 05:09:34','2026-04-14 05:09:34','ACTIVO'),
('bc9172fc-242e-4eb8-8a49-ada987487d5a','Hoodie Oversight Black','Sudadera pesada con fit urbano.','f3a20cb5-362c-4bce-99da-bccc55fc1138','/static/images/products/hoodie-black.jpg','2026-04-14 05:09:34','2026-04-14 05:09:34','ACTIVO');
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
('20a8923a-056b-49e5-97f8-aed360fc7d81','db29c2f4-e7ae-4dbd-8d10-d5045bd1dcdf','8965c7ce-da97-490d-8fe0-2ad7e928ba7d',NULL,10,'Terminado','2026-04-14 05:09:34','2026-04-14 05:09:34'),
('77f10ca9-1afe-4808-947f-c85b68236eea','107d538b-e93e-425d-9c72-ee545ba509d3',NULL,NULL,30,'Pendiente','2026-04-14 05:09:34','2026-04-14 05:09:34');
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
('0d21fe77-14f4-4943-9ef9-81504a581c17','d2022988-8d1d-4075-8cf0-422bf5d5d02c','c8bf5828-7c54-4c8f-a310-1232856eef44',500.0000,0.0000,5.00,'2026-04-14 05:09:34','2026-04-14 05:09:34'),
('ba7a81d7-33b7-42a6-8360-c6670f5130e1','67b0b371-4854-4f30-ad5b-603bb3c8aa94','1dc7710a-a247-46cd-9161-bcc95669f98d',10.0000,0.0000,150.00,'2026-04-14 05:09:34','2026-04-14 05:09:34'),
('ed942ac1-0176-46b3-bb85-7d0b0a87b776','9ac877ce-f3cc-4bd4-94fa-dcd01730f4e4','759dfd9f-9a35-4a0a-a89e-c5dc3ddc7c01',100.0000,0.0000,12.00,'2026-04-14 05:09:34','2026-04-14 05:09:34'),
('f7018fc4-5cf7-41de-aada-01fc8c830bd1','41019023-3ff3-416d-94e4-06ff58325b9f','81be855e-62f4-425a-ba74-c310706e8681',5.0000,0.0000,220.00,'2026-04-14 05:09:34','2026-04-14 05:09:34');
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
('41019023-3ff3-416d-94e4-06ff58325b9f','PED-INS-TEX-002','44481cff-8dc3-4545-b241-d06ca6ecb46f','1344d2d6-c82e-467a-8c50-6364a778f0bb','2026-04-14 05:09:34','2026-04-14 05:09:34','Completado'),
('67b0b371-4854-4f30-ad5b-603bb3c8aa94','PED-INS-TEX-001','44481cff-8dc3-4545-b241-d06ca6ecb46f','1344d2d6-c82e-467a-8c50-6364a778f0bb','2026-04-14 05:09:34','2026-04-14 05:09:34','Completado'),
('9ac877ce-f3cc-4bd4-94fa-dcd01730f4e4','PED-INS-ACC-001','0922ee6f-efb2-4957-baa5-8130029f941c','1344d2d6-c82e-467a-8c50-6364a778f0bb','2026-04-14 05:09:34','2026-04-14 05:09:34','Completado'),
('d2022988-8d1d-4075-8cf0-422bf5d5d02c','PED-INS-ACC-003','0922ee6f-efb2-4957-baa5-8130029f941c','1344d2d6-c82e-467a-8c50-6364a778f0bb','2026-04-14 05:09:34','2026-04-14 05:09:34','Completado');
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
('107d538b-e93e-425d-9c72-ee545ba509d3','1a5ce75b-75cf-473c-87a3-e5f45583d85f','654f98f0-96a1-4b05-80b4-0a1ec066416c','T-LOG-WHT-L','L',450.00,35,0,1,'2026-04-14 05:09:34','2026-04-14 05:09:34'),
('325baf1a-7ff1-4a3d-8ebc-123e6f2860fc','bc9172fc-242e-4eb8-8a49-ada987487d5a','580539c8-022c-45d6-ab11-2f82bc766025','H-OV-BLK-XL','XL',1200.00,19,0,1,'2026-04-14 05:09:34','2026-04-14 05:09:34'),
('5336ef5a-4ff4-4621-8f76-0935ef3989dc','bc9172fc-242e-4eb8-8a49-ada987487d5a','580539c8-022c-45d6-ab11-2f82bc766025','H-OV-BLK-S','S',1200.00,35,0,1,'2026-04-14 05:09:34','2026-04-14 05:09:34'),
('7e8c998b-78a5-4562-a789-b1552aa97b8f','1a5ce75b-75cf-473c-87a3-e5f45583d85f','654f98f0-96a1-4b05-80b4-0a1ec066416c','T-LOG-WHT-S','S',450.00,27,0,1,'2026-04-14 05:09:34','2026-04-14 05:09:34'),
('afb16534-def7-41f3-b21f-a6b518678301','bc9172fc-242e-4eb8-8a49-ada987487d5a','580539c8-022c-45d6-ab11-2f82bc766025','H-OV-BLK-L','L',1200.00,17,0,1,'2026-04-14 05:09:34','2026-04-14 05:09:34'),
('bacce444-c7f5-4afd-ac77-a6fdde2356a1','1a5ce75b-75cf-473c-87a3-e5f45583d85f','654f98f0-96a1-4b05-80b4-0a1ec066416c','T-LOG-WHT-M','M',450.00,42,0,1,'2026-04-14 05:09:34','2026-04-14 05:09:34'),
('db29c2f4-e7ae-4dbd-8d10-d5045bd1dcdf','bc9172fc-242e-4eb8-8a49-ada987487d5a','580539c8-022c-45d6-ab11-2f82bc766025','H-OV-BLK-M','M',1200.00,43,0,1,'2026-04-14 05:09:34','2026-04-14 05:09:34'),
('e1861c91-1bbb-4166-8e30-9efbeb1a7267','1a5ce75b-75cf-473c-87a3-e5f45583d85f','654f98f0-96a1-4b05-80b4-0a1ec066416c','T-LOG-WHT-XL','XL',450.00,34,0,1,'2026-04-14 05:09:34','2026-04-14 05:09:34');
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
('0922ee6f-efb2-4957-baa5-8130029f941c','Accesorios Industriales','ACC850505XYZ','Carlos','2026-04-14 05:09:34','2026-04-14 05:09:34',NULL,1,'555-300-4000','Otros'),
('44481cff-8dc3-4545-b241-d06ca6ecb46f','Textiles Premium S.A.','TEX900101ABC','Elena','2026-04-14 05:09:34','2026-04-14 05:09:34',NULL,1,'555-100-2000','Textiles'),
('e46fdafc-929e-49e6-81b0-53d1e815efd3','Hilos y Avíos del Norte','HIL220301HAN','Roberto','2026-04-14 05:09:34','2026-04-14 05:09:34',NULL,1,'818-200-1010','Otros');
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
('1344d2d6-c82e-467a-8c50-6364a778f0bb',1),
('1a8fb32d-2298-4076-96ca-28300138f462',3),
('b935683e-5e64-4cae-9e2f-94fb896af4b9',2),
('262dcc8c-d33e-4fdb-8d6d-91ecbae6f45d',3),
('323c5471-f959-41fb-97ff-ad12ed417cc2',4),
('cf4dc48f-ad19-49a6-9ab7-b8ad690bb982',4);
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
('2187a50d-698d-414e-bf66-04350ee86bb6','81be855e-62f4-425a-ba74-c310706e8681','bc04bc8b-515b-4700-b76b-1c14263ac25f',50.0000,23.5000,'2026-04-14 05:09:34','2026-04-14 05:09:34'),
('23a42c19-916e-446a-adfb-87c14ff271ee','1dc7710a-a247-46cd-9161-bcc95669f98d','f560f7e8-1226-42bf-9086-567ea16c53f9',100.0000,100.0000,'2026-04-14 05:09:34','2026-04-14 05:09:34'),
('27df8680-a65f-4291-b939-eca9baa11eaa','1dc7710a-a247-46cd-9161-bcc95669f98d','f560f7e8-1226-42bf-9086-567ea16c53f9',100.0000,100.0000,'2026-04-14 05:09:34','2026-04-14 05:09:34'),
('2997fdb9-60cb-49b6-b867-3732ac1fe719','1dc7710a-a247-46cd-9161-bcc95669f98d','f560f7e8-1226-42bf-9086-567ea16c53f9',100.0000,100.0000,'2026-04-14 05:09:34','2026-04-14 05:09:34'),
('2f7a4f04-4bd8-4f73-a26d-2eeed5b91249','81be855e-62f4-425a-ba74-c310706e8681','bc04bc8b-515b-4700-b76b-1c14263ac25f',50.0000,50.0000,'2026-04-14 05:09:34','2026-04-14 05:09:34'),
('5315f108-ad5c-45af-9a3c-565688d75cb9','1dc7710a-a247-46cd-9161-bcc95669f98d','f560f7e8-1226-42bf-9086-567ea16c53f9',100.0000,100.0000,'2026-04-14 05:09:34','2026-04-14 05:09:34'),
('53e20517-0aa3-4081-9df7-8c423e34c17e','1dc7710a-a247-46cd-9161-bcc95669f98d','f560f7e8-1226-42bf-9086-567ea16c53f9',100.0000,100.0000,'2026-04-14 05:09:34','2026-04-14 05:09:34'),
('567ed234-218b-44c7-9d2a-108a1c9542b5','1dc7710a-a247-46cd-9161-bcc95669f98d','f560f7e8-1226-42bf-9086-567ea16c53f9',100.0000,100.0000,'2026-04-14 05:09:34','2026-04-14 05:09:34'),
('7011ccd4-9dba-489c-8f0c-955bbe9d1869','1dc7710a-a247-46cd-9161-bcc95669f98d','f560f7e8-1226-42bf-9086-567ea16c53f9',100.0000,100.0000,'2026-04-14 05:09:34','2026-04-14 05:09:34'),
('854fb4e6-b5f8-4c64-b6a6-3b7a06aa9da8','81be855e-62f4-425a-ba74-c310706e8681','bc04bc8b-515b-4700-b76b-1c14263ac25f',50.0000,50.0000,'2026-04-14 05:09:34','2026-04-14 05:09:34'),
('89def0ff-d1c1-406d-9f1d-620899ee39c4','1dc7710a-a247-46cd-9161-bcc95669f98d','f560f7e8-1226-42bf-9086-567ea16c53f9',100.0000,100.0000,'2026-04-14 05:09:34','2026-04-14 05:09:34'),
('dc3331f9-b6ce-4d88-baae-41f453ebe933','1dc7710a-a247-46cd-9161-bcc95669f98d','f560f7e8-1226-42bf-9086-567ea16c53f9',100.0000,100.0000,'2026-04-14 05:09:34','2026-04-14 05:09:34'),
('e9fc43d3-9e4e-4cdf-8f10-f3c7fce6617f','81be855e-62f4-425a-ba74-c310706e8681','bc04bc8b-515b-4700-b76b-1c14263ac25f',50.0000,50.0000,'2026-04-14 05:09:34','2026-04-14 05:09:34'),
('f1947449-b6a7-4cb7-8c74-29e9bbdce4d5','1dc7710a-a247-46cd-9161-bcc95669f98d','f560f7e8-1226-42bf-9086-567ea16c53f9',100.0000,100.0000,'2026-04-14 05:09:34','2026-04-14 05:09:34'),
('f49fb385-69cc-4bf3-94e7-f8bec0738b25','81be855e-62f4-425a-ba74-c310706e8681','bc04bc8b-515b-4700-b76b-1c14263ac25f',50.0000,50.0000,'2026-04-14 05:09:34','2026-04-14 05:09:34');
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
  KEY `ix_security_audit_logs_tabla` (`tabla`),
  KEY `ix_security_audit_logs_uuid_usuario` (`uuid_usuario`),
  KEY `ix_security_audit_logs_fecha` (`fecha`)
) ENGINE=InnoDB AUTO_INCREMENT=95 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `security_audit_logs`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `security_audit_logs` WRITE;
/*!40000 ALTER TABLE `security_audit_logs` DISABLE KEYS */;
INSERT INTO `security_audit_logs` VALUES
(1,'Sistema','Sistema','Sistema','default','INSERT','role','N/A',NULL,'{\"id\": null, \"name\": \"admin\", \"description\": null}',NULL,'2026-04-14 05:09:33'),
(2,'Sistema','Sistema','Sistema','default','INSERT','role','N/A',NULL,'{\"id\": null, \"name\": \"gerente\", \"description\": null}',NULL,'2026-04-14 05:09:33'),
(3,'Sistema','Sistema','Sistema','default','INSERT','role','N/A',NULL,'{\"id\": null, \"name\": \"produccion\", \"description\": null}',NULL,'2026-04-14 05:09:33'),
(4,'Sistema','Sistema','Sistema','default','INSERT','role','N/A',NULL,'{\"id\": null, \"name\": \"cliente\", \"description\": null}',NULL,'2026-04-14 05:09:33'),
(5,'Sistema','Sistema','Sistema','default','INSERT','usuarios','N/A',NULL,'{\"email\": \"admin@axis.com\", \"active\": true, \"password\": \"$argon2id$v=19$m=65536,t=3,p=4$+l/Ludfau9day3nP+Z8Twg$87CCDRTWBfiTnjWXeyZHamtBMwQMl6oHNfN7lsjE3VQ\", \"confirmed_at\": \"2026-04-14T05:09:33.551703+00:00\", \"uuid_usuario\": null, \"fs_uniquifier\": null, \"fecha_creacion\": null, \"tf_totp_secret\": null, \"nombre_completo\": \"Admin Axis\", \"tf_phone_number\": null, \"mf_recovery_codes\": null, \"tf_primary_method\": null, \"fecha_actualizacion\": null, \"password_changed_at\": null}',NULL,'2026-04-14 05:09:33'),
(6,'Sistema','Sistema','Sistema','default','INSERT','empleados','N/A',NULL,'{\"puesto\": \"Director General\", \"departamento\": \"Dirección\", \"uuid_usuario\": \"1344d2d6-c82e-467a-8c50-6364a778f0bb\", \"fecha_ingreso\": \"2025-04-14T05:09:33.571192+00:00\", \"uuid_empleado\": null, \"fecha_creacion\": null, \"numero_empleado\": \"EMP-001\", \"fecha_actualizacion\": null}',NULL,'2026-04-14 05:09:33'),
(7,'Sistema','Sistema','Sistema','default','INSERT','usuarios','N/A',NULL,'{\"email\": \"modista@axis.com\", \"active\": true, \"password\": \"$argon2id$v=19$m=65536,t=3,p=4$KmXsXUupFaK0FuIc49y7Nw$hu8yyfSHD2LoAr4L54RJTMRBpfWQqkFx/bO0OM/TqgE\", \"confirmed_at\": \"2026-04-14T05:09:33.680043+00:00\", \"uuid_usuario\": null, \"fs_uniquifier\": null, \"fecha_creacion\": null, \"tf_totp_secret\": null, \"nombre_completo\": \"Modista Principal\", \"tf_phone_number\": null, \"mf_recovery_codes\": null, \"tf_primary_method\": null, \"fecha_actualizacion\": null, \"password_changed_at\": null}',NULL,'2026-04-14 05:09:33'),
(8,'Sistema','Sistema','Sistema','default','INSERT','empleados','N/A',NULL,'{\"puesto\": \"Jefe de Taller\", \"departamento\": \"Producción\", \"uuid_usuario\": \"1a8fb32d-2298-4076-96ca-28300138f462\", \"fecha_ingreso\": \"2025-04-14T05:09:33.691370+00:00\", \"uuid_empleado\": null, \"fecha_creacion\": null, \"numero_empleado\": \"EMP-002\", \"fecha_actualizacion\": null}',NULL,'2026-04-14 05:09:33'),
(9,'Sistema','Sistema','Sistema','default','INSERT','usuarios','N/A',NULL,'{\"email\": \"ventas@axis.com\", \"active\": true, \"password\": \"$argon2id$v=19$m=65536,t=3,p=4$vpdyDiFEqBWidG5trVUK4Q$rv4b7Uxgsz9gh4mLickQX/v8WQV3O2kmte9kTlxEnVA\", \"confirmed_at\": \"2026-04-14T05:09:33.804281+00:00\", \"uuid_usuario\": null, \"fs_uniquifier\": null, \"fecha_creacion\": null, \"tf_totp_secret\": null, \"nombre_completo\": \"Vendedor Axis\", \"tf_phone_number\": null, \"mf_recovery_codes\": null, \"tf_primary_method\": null, \"fecha_actualizacion\": null, \"password_changed_at\": null}',NULL,'2026-04-14 05:09:33'),
(10,'Sistema','Sistema','Sistema','default','INSERT','empleados','N/A',NULL,'{\"puesto\": \"Ejecutivo Comercial\", \"departamento\": \"Ventas\", \"uuid_usuario\": \"b935683e-5e64-4cae-9e2f-94fb896af4b9\", \"fecha_ingreso\": \"2025-04-14T05:09:33.814875+00:00\", \"uuid_empleado\": null, \"fecha_creacion\": null, \"numero_empleado\": \"EMP-003\", \"fecha_actualizacion\": null}',NULL,'2026-04-14 05:09:33'),
(11,'Sistema','Sistema','Sistema','default','INSERT','usuarios','N/A',NULL,'{\"email\": \"compras@axis.com\", \"active\": true, \"password\": \"$argon2id$v=19$m=65536,t=3,p=4$Z+zde4/Rek/J+T9HyNm7Nw$Qz8bxcWPS7Hpgl/aTsbdNoNjw5Aw58Bmo2K37uSITb0\", \"confirmed_at\": \"2026-04-14T05:09:33.914407+00:00\", \"uuid_usuario\": null, \"fs_uniquifier\": null, \"fecha_creacion\": null, \"tf_totp_secret\": null, \"nombre_completo\": \"Comprador Axis\", \"tf_phone_number\": null, \"mf_recovery_codes\": null, \"tf_primary_method\": null, \"fecha_actualizacion\": null, \"password_changed_at\": null}',NULL,'2026-04-14 05:09:33'),
(12,'Sistema','Sistema','Sistema','default','INSERT','empleados','N/A',NULL,'{\"puesto\": \"Analista de Suministros\", \"departamento\": \"Compras\", \"uuid_usuario\": \"262dcc8c-d33e-4fdb-8d6d-91ecbae6f45d\", \"fecha_ingreso\": \"2025-04-14T05:09:33.922767+00:00\", \"uuid_empleado\": null, \"fecha_creacion\": null, \"numero_empleado\": \"EMP-004\", \"fecha_actualizacion\": null}',NULL,'2026-04-14 05:09:33'),
(13,'Sistema','Sistema','Sistema','default','INSERT','usuarios','N/A',NULL,'{\"email\": \"juan@axis.com\", \"active\": true, \"password\": \"$argon2id$v=19$m=65536,t=3,p=4$itGac85Zaw2hNOZcq/XeGw$eGDs71zgBAlT1/Wzka9JB1TK4aFiVONIW5wjqgVQ6DQ\", \"confirmed_at\": \"2026-04-14T05:09:34.027164+00:00\", \"uuid_usuario\": null, \"fs_uniquifier\": null, \"fecha_creacion\": null, \"tf_totp_secret\": null, \"nombre_completo\": \"Juan Cliente\", \"tf_phone_number\": null, \"mf_recovery_codes\": null, \"tf_primary_method\": null, \"fecha_actualizacion\": null, \"password_changed_at\": null}',NULL,'2026-04-14 05:09:34'),
(14,'Sistema','Sistema','Sistema','default','INSERT','clientes','N/A',NULL,'{\"telefono\": \"555-123-4567\", \"uuid_cliente\": null, \"uuid_usuario\": \"323c5471-f959-41fb-97ff-ad12ed417cc2\", \"fecha_creacion\": null, \"direccion_completa\": \"Av. Reforma 123, CDMX\", \"fecha_actualizacion\": null, \"usuario_actualizo_uuid\": null}',NULL,'2026-04-14 05:09:34'),
(15,'Sistema','Sistema','Sistema','default','INSERT','usuarios','N/A',NULL,'{\"email\": \"maria@axis.com\", \"active\": true, \"password\": \"$argon2id$v=19$m=65536,t=3,p=4$sDZmbG2tVarVWotRaq3VGg$P8ClmMmO/C3cNX6ClnXUzfwM5d38H3AdKJGqpaDssfU\", \"confirmed_at\": \"2026-04-14T05:09:34.147518+00:00\", \"uuid_usuario\": null, \"fs_uniquifier\": null, \"fecha_creacion\": null, \"tf_totp_secret\": null, \"nombre_completo\": \"Maria Lopez\", \"tf_phone_number\": null, \"mf_recovery_codes\": null, \"tf_primary_method\": null, \"fecha_actualizacion\": null, \"password_changed_at\": null}',NULL,'2026-04-14 05:09:34'),
(16,'Sistema','Sistema','Sistema','default','INSERT','clientes','N/A',NULL,'{\"telefono\": \"555-987-6543\", \"uuid_cliente\": null, \"uuid_usuario\": \"cf4dc48f-ad19-49a6-9ab7-b8ad690bb982\", \"fecha_creacion\": null, \"direccion_completa\": \"Insurgentes Sur 456, CDMX\", \"fecha_actualizacion\": null, \"usuario_actualizo_uuid\": null}',NULL,'2026-04-14 05:09:34'),
(17,'Sistema','Sistema','Sistema','default','INSERT','categorias','N/A',NULL,'{\"nombre\": \"Camisetas\", \"imagen_url\": null, \"descripcion\": \"Prendas de cuerpo superior\", \"fecha_creacion\": null, \"uuid_categoria\": null, \"estatus_visible\": true, \"usuario_creo_uuid\": null, \"fecha_actualizacion\": null, \"usuario_actualizo_uuid\": null}',NULL,'2026-04-14 05:09:34'),
(18,'Sistema','Sistema','Sistema','default','INSERT','categorias','N/A',NULL,'{\"nombre\": \"Pantalones\", \"imagen_url\": null, \"descripcion\": \"Prendas inferiores\", \"fecha_creacion\": null, \"uuid_categoria\": null, \"estatus_visible\": true, \"usuario_creo_uuid\": null, \"fecha_actualizacion\": null, \"usuario_actualizo_uuid\": null}',NULL,'2026-04-14 05:09:34'),
(19,'Sistema','Sistema','Sistema','default','INSERT','categorias','N/A',NULL,'{\"nombre\": \"Hoodies\", \"imagen_url\": null, \"descripcion\": \"Sudaderas urbanas\", \"fecha_creacion\": null, \"uuid_categoria\": null, \"estatus_visible\": true, \"usuario_creo_uuid\": null, \"fecha_actualizacion\": null, \"usuario_actualizo_uuid\": null}',NULL,'2026-04-14 05:09:34'),
(20,'Sistema','Sistema','Sistema','default','INSERT','categorias','N/A',NULL,'{\"nombre\": \"Chaquetas\", \"imagen_url\": null, \"descripcion\": \"Abrigos y chamarras\", \"fecha_creacion\": null, \"uuid_categoria\": null, \"estatus_visible\": true, \"usuario_creo_uuid\": null, \"fecha_actualizacion\": null, \"usuario_actualizo_uuid\": null}',NULL,'2026-04-14 05:09:34'),
(21,'Sistema','Sistema','Sistema','default','INSERT','categorias','N/A',NULL,'{\"nombre\": \"Shorts\", \"imagen_url\": null, \"descripcion\": \"Pantalones cortos\", \"fecha_creacion\": null, \"uuid_categoria\": null, \"estatus_visible\": true, \"usuario_creo_uuid\": null, \"fecha_actualizacion\": null, \"usuario_actualizo_uuid\": null}',NULL,'2026-04-14 05:09:34'),
(22,'Sistema','Sistema','Sistema','default','INSERT','categorias','N/A',NULL,'{\"nombre\": \"Accesorios\", \"imagen_url\": null, \"descripcion\": \"Gorras y complementos\", \"fecha_creacion\": null, \"uuid_categoria\": null, \"estatus_visible\": true, \"usuario_creo_uuid\": null, \"fecha_actualizacion\": null, \"usuario_actualizo_uuid\": null}',NULL,'2026-04-14 05:09:34'),
(23,'Sistema','Sistema','Sistema','default','INSERT','proveedores','N/A',NULL,'{\"rfc\": \"TEX900101ABC\", \"estatus\": null, \"telefono\": \"555-100-2000\", \"razon_social\": \"Textiles Premium S.A.\", \"fecha_creacion\": null, \"uuid_proveedor\": null, \"contacto_nombre\": \"Elena\", \"categoria_insumo\": \"Textiles\", \"usuario_creo_uuid\": null, \"fecha_actualizacion\": null}',NULL,'2026-04-14 05:09:34'),
(24,'Sistema','Sistema','Sistema','default','INSERT','proveedores','N/A',NULL,'{\"rfc\": \"ACC850505XYZ\", \"estatus\": null, \"telefono\": \"555-300-4000\", \"razon_social\": \"Accesorios Industriales\", \"fecha_creacion\": null, \"uuid_proveedor\": null, \"contacto_nombre\": \"Carlos\", \"categoria_insumo\": \"Otros\", \"usuario_creo_uuid\": null, \"fecha_actualizacion\": null}',NULL,'2026-04-14 05:09:34'),
(25,'Sistema','Sistema','Sistema','default','INSERT','proveedores','N/A',NULL,'{\"rfc\": \"HIL220301HAN\", \"estatus\": null, \"telefono\": \"818-200-1010\", \"razon_social\": \"Hilos y Avíos del Norte\", \"fecha_creacion\": null, \"uuid_proveedor\": null, \"contacto_nombre\": \"Roberto\", \"categoria_insumo\": \"Otros\", \"usuario_creo_uuid\": null, \"fecha_actualizacion\": null}',NULL,'2026-04-14 05:09:34'),
(26,'Sistema','Sistema','Sistema','default','INSERT','insumos','N/A',NULL,'{\"sku\": \"INS-TEX-001\", \"ancho\": null, \"nombre\": \"Algodón Negro Roll\", \"estatus\": null, \"uuid_insumo\": null, \"unidad_medida\": \"ROLLO\", \"fecha_creacion\": null, \"uuid_categoria\": \"562156c6-6dec-48aa-9fa4-f307df5cfde9\", \"contenido_cantidad\": 100.0, \"fecha_actualizacion\": null, \"stock_minimo_alerta\": 10, \"stock_total_acumulado\": 0, \"usuario_actualizo_uuid\": null, \"contenido_unidad_medida\": \"METRO\"}',NULL,'2026-04-14 05:09:34'),
(27,'Sistema','Sistema','Sistema','default','INSERT','insumos','N/A',NULL,'{\"sku\": \"INS-TEX-002\", \"ancho\": null, \"nombre\": \"Poliéster Gris Roll\", \"estatus\": null, \"uuid_insumo\": null, \"unidad_medida\": \"ROLLO\", \"fecha_creacion\": null, \"uuid_categoria\": \"f3a20cb5-362c-4bce-99da-bccc55fc1138\", \"contenido_cantidad\": 50.0, \"fecha_actualizacion\": null, \"stock_minimo_alerta\": 10, \"stock_total_acumulado\": 0, \"usuario_actualizo_uuid\": null, \"contenido_unidad_medida\": \"METRO\"}',NULL,'2026-04-14 05:09:34'),
(28,'Sistema','Sistema','Sistema','default','INSERT','insumos','N/A',NULL,'{\"sku\": \"INS-TEX-003\", \"ancho\": null, \"nombre\": \"Denim Azul 14oz\", \"estatus\": null, \"uuid_insumo\": null, \"unidad_medida\": \"ROLLO\", \"fecha_creacion\": null, \"uuid_categoria\": \"2cb3d1e2-e62c-4438-865e-704b35c133e1\", \"contenido_cantidad\": 40.0, \"fecha_actualizacion\": null, \"stock_minimo_alerta\": 10, \"stock_total_acumulado\": 0, \"usuario_actualizo_uuid\": null, \"contenido_unidad_medida\": \"METRO\"}',NULL,'2026-04-14 05:09:34'),
(29,'Sistema','Sistema','Sistema','default','INSERT','insumos','N/A',NULL,'{\"sku\": \"INS-ACC-001\", \"ancho\": null, \"nombre\": \"Cierre Metálico YKK 15cm\", \"estatus\": null, \"uuid_insumo\": null, \"unidad_medida\": \"PIEZA\", \"fecha_creacion\": null, \"uuid_categoria\": \"6bfb63ec-4450-4c16-bc4d-9aef01d14345\", \"contenido_cantidad\": 1.0, \"fecha_actualizacion\": null, \"stock_minimo_alerta\": 10, \"stock_total_acumulado\": 0, \"usuario_actualizo_uuid\": null, \"contenido_unidad_medida\": \"PIEZA\"}',NULL,'2026-04-14 05:09:34'),
(30,'Sistema','Sistema','Sistema','default','INSERT','insumos','N/A',NULL,'{\"sku\": \"INS-ACC-002\", \"ancho\": null, \"nombre\": \"Botón Acero Inoxidable\", \"estatus\": null, \"uuid_insumo\": null, \"unidad_medida\": \"PIEZA\", \"fecha_creacion\": null, \"uuid_categoria\": \"2cb3d1e2-e62c-4438-865e-704b35c133e1\", \"contenido_cantidad\": 1.0, \"fecha_actualizacion\": null, \"stock_minimo_alerta\": 10, \"stock_total_acumulado\": 0, \"usuario_actualizo_uuid\": null, \"contenido_unidad_medida\": \"PIEZA\"}',NULL,'2026-04-14 05:09:34'),
(31,'Sistema','Sistema','Sistema','default','INSERT','insumos','N/A',NULL,'{\"sku\": \"INS-ACC-003\", \"ancho\": null, \"nombre\": \"Etiqueta Axis Bordada\", \"estatus\": null, \"uuid_insumo\": null, \"unidad_medida\": \"PIEZA\", \"fecha_creacion\": null, \"uuid_categoria\": \"fd2f22d5-276e-4816-b57d-3a9b8655e01f\", \"contenido_cantidad\": 1.0, \"fecha_actualizacion\": null, \"stock_minimo_alerta\": 10, \"stock_total_acumulado\": 0, \"usuario_actualizo_uuid\": null, \"contenido_unidad_medida\": \"PIEZA\"}',NULL,'2026-04-14 05:09:34'),
(32,'Sistema','Sistema','Sistema','default','INSERT','explosion_materiales_cabecera','N/A',NULL,'{\"estatus\": \"ACTIVO\", \"uuid_usuario\": \"1344d2d6-c82e-467a-8c50-6364a778f0bb\", \"fecha_creacion\": null, \"uuid_explosion\": null, \"fecha_actualizacion\": null, \"instrucciones_proceso\": \"Corte láser y costura reforzada.\"}',NULL,'2026-04-14 05:09:34'),
(33,'Sistema','Sistema','Sistema','default','INSERT','explosion_materiales_detalle','N/A',NULL,'{\"uuid_insumo\": \"81be855e-62f4-425a-ba74-c310706e8681\", \"uuid_detalle\": null, \"fecha_creacion\": null, \"uuid_explosion\": \"580539c8-022c-45d6-ab11-2f82bc766025\", \"ancho_referencia\": null, \"fecha_actualizacion\": null, \"consumo_teorico_unitario\": 2.5}',NULL,'2026-04-14 05:09:34'),
(34,'Sistema','Sistema','Sistema','default','INSERT','explosion_materiales_detalle','N/A',NULL,'{\"uuid_insumo\": \"759dfd9f-9a35-4a0a-a89e-c5dc3ddc7c01\", \"uuid_detalle\": null, \"fecha_creacion\": null, \"uuid_explosion\": \"580539c8-022c-45d6-ab11-2f82bc766025\", \"ancho_referencia\": null, \"fecha_actualizacion\": null, \"consumo_teorico_unitario\": 1.0}',NULL,'2026-04-14 05:09:34'),
(35,'Sistema','Sistema','Sistema','default','INSERT','explosion_materiales_detalle','N/A',NULL,'{\"uuid_insumo\": \"c8bf5828-7c54-4c8f-a310-1232856eef44\", \"uuid_detalle\": null, \"fecha_creacion\": null, \"uuid_explosion\": \"580539c8-022c-45d6-ab11-2f82bc766025\", \"ancho_referencia\": null, \"fecha_actualizacion\": null, \"consumo_teorico_unitario\": 1.0}',NULL,'2026-04-14 05:09:34'),
(36,'Sistema','Sistema','Sistema','default','INSERT','explosion_materiales_cabecera','N/A',NULL,'{\"estatus\": \"ACTIVO\", \"uuid_usuario\": \"1344d2d6-c82e-467a-8c50-6364a778f0bb\", \"fecha_creacion\": null, \"uuid_explosion\": null, \"fecha_actualizacion\": null, \"instrucciones_proceso\": \"Costura plana a dos hilos.\"}',NULL,'2026-04-14 05:09:34'),
(37,'Sistema','Sistema','Sistema','default','INSERT','explosion_materiales_detalle','N/A',NULL,'{\"uuid_insumo\": \"1dc7710a-a247-46cd-9161-bcc95669f98d\", \"uuid_detalle\": null, \"fecha_creacion\": null, \"uuid_explosion\": \"654f98f0-96a1-4b05-80b4-0a1ec066416c\", \"ancho_referencia\": null, \"fecha_actualizacion\": null, \"consumo_teorico_unitario\": 1.2}',NULL,'2026-04-14 05:09:34'),
(38,'Sistema','Sistema','Sistema','default','INSERT','explosion_materiales_detalle','N/A',NULL,'{\"uuid_insumo\": \"c8bf5828-7c54-4c8f-a310-1232856eef44\", \"uuid_detalle\": null, \"fecha_creacion\": null, \"uuid_explosion\": \"654f98f0-96a1-4b05-80b4-0a1ec066416c\", \"ancho_referencia\": null, \"fecha_actualizacion\": null, \"consumo_teorico_unitario\": 1.0}',NULL,'2026-04-14 05:09:34'),
(39,'Sistema','Sistema','Sistema','default','INSERT','modelos_ropa','N/A',NULL,'{\"estatus\": \"ACTIVO\", \"imagen_url\": \"/static/images/products/hoodie-black.jpg\", \"descripcion\": \"Sudadera pesada con fit urbano.\", \"uuid_modelo\": null, \"nombre_modelo\": \"Hoodie Oversight Black\", \"fecha_creacion\": null, \"uuid_categoria\": \"f3a20cb5-362c-4bce-99da-bccc55fc1138\", \"fecha_actualizacion\": null}',NULL,'2026-04-14 05:09:34'),
(40,'Sistema','Sistema','Sistema','default','INSERT','productos_terminados','N/A',NULL,'{\"talla\": \"S\", \"active\": null, \"uuid_modelo\": \"bc9172fc-242e-4eb8-8a49-ada987487d5a\", \"precio_venta\": 1200.0, \"uuid_producto\": null, \"fecha_creacion\": null, \"sku_especifico\": \"H-OV-BLK-S\", \"uuid_explosion\": \"580539c8-022c-45d6-ab11-2f82bc766025\", \"fecha_actualizacion\": null, \"stock_fisico_actual\": 35, \"stock_minimo_alerta\": null}',NULL,'2026-04-14 05:09:34'),
(41,'Sistema','Sistema','Sistema','default','INSERT','productos_terminados','N/A',NULL,'{\"talla\": \"M\", \"active\": null, \"uuid_modelo\": \"bc9172fc-242e-4eb8-8a49-ada987487d5a\", \"precio_venta\": 1200.0, \"uuid_producto\": null, \"fecha_creacion\": null, \"sku_especifico\": \"H-OV-BLK-M\", \"uuid_explosion\": \"580539c8-022c-45d6-ab11-2f82bc766025\", \"fecha_actualizacion\": null, \"stock_fisico_actual\": 43, \"stock_minimo_alerta\": null}',NULL,'2026-04-14 05:09:34'),
(42,'Sistema','Sistema','Sistema','default','INSERT','productos_terminados','N/A',NULL,'{\"talla\": \"L\", \"active\": null, \"uuid_modelo\": \"bc9172fc-242e-4eb8-8a49-ada987487d5a\", \"precio_venta\": 1200.0, \"uuid_producto\": null, \"fecha_creacion\": null, \"sku_especifico\": \"H-OV-BLK-L\", \"uuid_explosion\": \"580539c8-022c-45d6-ab11-2f82bc766025\", \"fecha_actualizacion\": null, \"stock_fisico_actual\": 17, \"stock_minimo_alerta\": null}',NULL,'2026-04-14 05:09:34'),
(43,'Sistema','Sistema','Sistema','default','INSERT','productos_terminados','N/A',NULL,'{\"talla\": \"XL\", \"active\": null, \"uuid_modelo\": \"bc9172fc-242e-4eb8-8a49-ada987487d5a\", \"precio_venta\": 1200.0, \"uuid_producto\": null, \"fecha_creacion\": null, \"sku_especifico\": \"H-OV-BLK-XL\", \"uuid_explosion\": \"580539c8-022c-45d6-ab11-2f82bc766025\", \"fecha_actualizacion\": null, \"stock_fisico_actual\": 19, \"stock_minimo_alerta\": null}',NULL,'2026-04-14 05:09:34'),
(44,'Sistema','Sistema','Sistema','default','INSERT','modelos_ropa','N/A',NULL,'{\"estatus\": \"ACTIVO\", \"imagen_url\": \"/static/images/products/tshirt-white.jpg\", \"descripcion\": \"Camiseta 100% algodón alta densidad.\", \"uuid_modelo\": null, \"nombre_modelo\": \"Axis Logo Tee White\", \"fecha_creacion\": null, \"uuid_categoria\": \"562156c6-6dec-48aa-9fa4-f307df5cfde9\", \"fecha_actualizacion\": null}',NULL,'2026-04-14 05:09:34'),
(45,'Sistema','Sistema','Sistema','default','INSERT','productos_terminados','N/A',NULL,'{\"talla\": \"S\", \"active\": null, \"uuid_modelo\": \"1a5ce75b-75cf-473c-87a3-e5f45583d85f\", \"precio_venta\": 450.0, \"uuid_producto\": null, \"fecha_creacion\": null, \"sku_especifico\": \"T-LOG-WHT-S\", \"uuid_explosion\": \"654f98f0-96a1-4b05-80b4-0a1ec066416c\", \"fecha_actualizacion\": null, \"stock_fisico_actual\": 27, \"stock_minimo_alerta\": null}',NULL,'2026-04-14 05:09:34'),
(46,'Sistema','Sistema','Sistema','default','INSERT','productos_terminados','N/A',NULL,'{\"talla\": \"M\", \"active\": null, \"uuid_modelo\": \"1a5ce75b-75cf-473c-87a3-e5f45583d85f\", \"precio_venta\": 450.0, \"uuid_producto\": null, \"fecha_creacion\": null, \"sku_especifico\": \"T-LOG-WHT-M\", \"uuid_explosion\": \"654f98f0-96a1-4b05-80b4-0a1ec066416c\", \"fecha_actualizacion\": null, \"stock_fisico_actual\": 42, \"stock_minimo_alerta\": null}',NULL,'2026-04-14 05:09:34'),
(47,'Sistema','Sistema','Sistema','default','INSERT','productos_terminados','N/A',NULL,'{\"talla\": \"L\", \"active\": null, \"uuid_modelo\": \"1a5ce75b-75cf-473c-87a3-e5f45583d85f\", \"precio_venta\": 450.0, \"uuid_producto\": null, \"fecha_creacion\": null, \"sku_especifico\": \"T-LOG-WHT-L\", \"uuid_explosion\": \"654f98f0-96a1-4b05-80b4-0a1ec066416c\", \"fecha_actualizacion\": null, \"stock_fisico_actual\": 35, \"stock_minimo_alerta\": null}',NULL,'2026-04-14 05:09:34'),
(48,'Sistema','Sistema','Sistema','default','INSERT','productos_terminados','N/A',NULL,'{\"talla\": \"XL\", \"active\": null, \"uuid_modelo\": \"1a5ce75b-75cf-473c-87a3-e5f45583d85f\", \"precio_venta\": 450.0, \"uuid_producto\": null, \"fecha_creacion\": null, \"sku_especifico\": \"T-LOG-WHT-XL\", \"uuid_explosion\": \"654f98f0-96a1-4b05-80b4-0a1ec066416c\", \"fecha_actualizacion\": null, \"stock_fisico_actual\": 34, \"stock_minimo_alerta\": null}',NULL,'2026-04-14 05:09:34'),
(49,'Sistema','Sistema','Sistema','default','INSERT','pedidos_proveedor_encabezado','N/A',NULL,'{\"estatus\": \"Completado\", \"uuid_pedido\": null, \"fecha_pedido\": null, \"folio_pedido\": \"PED-INS-TEX-001\", \"uuid_proveedor\": \"44481cff-8dc3-4545-b241-d06ca6ecb46f\", \"fecha_actualizacion\": null, \"uuid_usuario_solicita\": \"1344d2d6-c82e-467a-8c50-6364a778f0bb\"}',NULL,'2026-04-14 05:09:34'),
(50,'Sistema','Sistema','Sistema','default','INSERT','pedidos_proveedor_detalle','N/A',NULL,'{\"uuid_insumo\": \"1dc7710a-a247-46cd-9161-bcc95669f98d\", \"uuid_pedido\": \"67b0b371-4854-4f30-ad5b-603bb3c8aa94\", \"fecha_creacion\": null, \"cantidad_pedida\": 10, \"cantidad_recibida\": null, \"fecha_actualizacion\": null, \"uuid_detalle_pedido\": null, \"costo_unitario_estimado\": 150.0}',NULL,'2026-04-14 05:09:34'),
(51,'Sistema','Sistema','Sistema','default','INSERT','compras_encabezado','N/A',NULL,'{\"estatus\": \"RECIBIDO\", \"uuid_compra\": null, \"uuid_pedido\": \"67b0b371-4854-4f30-ad5b-603bb3c8aa94\", \"fecha_compra\": null, \"folio_factura\": \"FAC-INS-TEX-001-99\", \"uuid_proveedor\": \"44481cff-8dc3-4545-b241-d06ca6ecb46f\", \"fecha_actualizacion\": null, \"uuid_usuario_registro\": \"1344d2d6-c82e-467a-8c50-6364a778f0bb\"}',NULL,'2026-04-14 05:09:34'),
(52,'Sistema','Sistema','Sistema','default','INSERT','compras_detalle','N/A',NULL,'{\"uuid_compra\": \"bbbd1709-94e4-428f-90ed-c27a4cec2934\", \"uuid_insumo\": \"1dc7710a-a247-46cd-9161-bcc95669f98d\", \"fecha_creacion\": null, \"cantidad_comprada\": 10, \"fecha_actualizacion\": null, \"uuid_detalle_compra\": null, \"costo_unitario_compra\": 150.0}',NULL,'2026-04-14 05:09:34'),
(53,'Sistema','Sistema','Sistema','default','INSERT','rollos_inventario','N/A',NULL,'{\"uuid_rollo\": null, \"uuid_insumo\": \"1dc7710a-a247-46cd-9161-bcc95669f98d\", \"fecha_creacion\": null, \"metraje_inicial\": 100.0, \"fecha_actualizacion\": null, \"uuid_detalle_compra\": \"f560f7e8-1226-42bf-9086-567ea16c53f9\", \"metraje_continuo_actual\": 100.0}',NULL,'2026-04-14 05:09:34'),
(54,'Sistema','Sistema','Sistema','default','INSERT','rollos_inventario','N/A',NULL,'{\"uuid_rollo\": null, \"uuid_insumo\": \"1dc7710a-a247-46cd-9161-bcc95669f98d\", \"fecha_creacion\": null, \"metraje_inicial\": 100.0, \"fecha_actualizacion\": null, \"uuid_detalle_compra\": \"f560f7e8-1226-42bf-9086-567ea16c53f9\", \"metraje_continuo_actual\": 100.0}',NULL,'2026-04-14 05:09:34'),
(55,'Sistema','Sistema','Sistema','default','INSERT','rollos_inventario','N/A',NULL,'{\"uuid_rollo\": null, \"uuid_insumo\": \"1dc7710a-a247-46cd-9161-bcc95669f98d\", \"fecha_creacion\": null, \"metraje_inicial\": 100.0, \"fecha_actualizacion\": null, \"uuid_detalle_compra\": \"f560f7e8-1226-42bf-9086-567ea16c53f9\", \"metraje_continuo_actual\": 100.0}',NULL,'2026-04-14 05:09:34'),
(56,'Sistema','Sistema','Sistema','default','INSERT','rollos_inventario','N/A',NULL,'{\"uuid_rollo\": null, \"uuid_insumo\": \"1dc7710a-a247-46cd-9161-bcc95669f98d\", \"fecha_creacion\": null, \"metraje_inicial\": 100.0, \"fecha_actualizacion\": null, \"uuid_detalle_compra\": \"f560f7e8-1226-42bf-9086-567ea16c53f9\", \"metraje_continuo_actual\": 100.0}',NULL,'2026-04-14 05:09:34'),
(57,'Sistema','Sistema','Sistema','default','INSERT','rollos_inventario','N/A',NULL,'{\"uuid_rollo\": null, \"uuid_insumo\": \"1dc7710a-a247-46cd-9161-bcc95669f98d\", \"fecha_creacion\": null, \"metraje_inicial\": 100.0, \"fecha_actualizacion\": null, \"uuid_detalle_compra\": \"f560f7e8-1226-42bf-9086-567ea16c53f9\", \"metraje_continuo_actual\": 100.0}',NULL,'2026-04-14 05:09:34'),
(58,'Sistema','Sistema','Sistema','default','INSERT','rollos_inventario','N/A',NULL,'{\"uuid_rollo\": null, \"uuid_insumo\": \"1dc7710a-a247-46cd-9161-bcc95669f98d\", \"fecha_creacion\": null, \"metraje_inicial\": 100.0, \"fecha_actualizacion\": null, \"uuid_detalle_compra\": \"f560f7e8-1226-42bf-9086-567ea16c53f9\", \"metraje_continuo_actual\": 100.0}',NULL,'2026-04-14 05:09:34'),
(59,'Sistema','Sistema','Sistema','default','INSERT','rollos_inventario','N/A',NULL,'{\"uuid_rollo\": null, \"uuid_insumo\": \"1dc7710a-a247-46cd-9161-bcc95669f98d\", \"fecha_creacion\": null, \"metraje_inicial\": 100.0, \"fecha_actualizacion\": null, \"uuid_detalle_compra\": \"f560f7e8-1226-42bf-9086-567ea16c53f9\", \"metraje_continuo_actual\": 100.0}',NULL,'2026-04-14 05:09:34'),
(60,'Sistema','Sistema','Sistema','default','INSERT','rollos_inventario','N/A',NULL,'{\"uuid_rollo\": null, \"uuid_insumo\": \"1dc7710a-a247-46cd-9161-bcc95669f98d\", \"fecha_creacion\": null, \"metraje_inicial\": 100.0, \"fecha_actualizacion\": null, \"uuid_detalle_compra\": \"f560f7e8-1226-42bf-9086-567ea16c53f9\", \"metraje_continuo_actual\": 100.0}',NULL,'2026-04-14 05:09:34'),
(61,'Sistema','Sistema','Sistema','default','INSERT','rollos_inventario','N/A',NULL,'{\"uuid_rollo\": null, \"uuid_insumo\": \"1dc7710a-a247-46cd-9161-bcc95669f98d\", \"fecha_creacion\": null, \"metraje_inicial\": 100.0, \"fecha_actualizacion\": null, \"uuid_detalle_compra\": \"f560f7e8-1226-42bf-9086-567ea16c53f9\", \"metraje_continuo_actual\": 100.0}',NULL,'2026-04-14 05:09:34'),
(62,'Sistema','Sistema','Sistema','default','INSERT','rollos_inventario','N/A',NULL,'{\"uuid_rollo\": null, \"uuid_insumo\": \"1dc7710a-a247-46cd-9161-bcc95669f98d\", \"fecha_creacion\": null, \"metraje_inicial\": 100.0, \"fecha_actualizacion\": null, \"uuid_detalle_compra\": \"f560f7e8-1226-42bf-9086-567ea16c53f9\", \"metraje_continuo_actual\": 100.0}',NULL,'2026-04-14 05:09:34'),
(63,'Sistema','Sistema','Sistema','default','UPDATE','insumos','1dc7710a-a247-46cd-9161-bcc95669f98d','{\"stock_total_acumulado\": 0.0}','{\"stock_total_acumulado\": 1000.0}',NULL,'2026-04-14 05:09:34'),
(64,'Sistema','Sistema','Sistema','default','INSERT','pedidos_proveedor_encabezado','N/A',NULL,'{\"estatus\": \"Completado\", \"uuid_pedido\": null, \"fecha_pedido\": null, \"folio_pedido\": \"PED-INS-TEX-002\", \"uuid_proveedor\": \"44481cff-8dc3-4545-b241-d06ca6ecb46f\", \"fecha_actualizacion\": null, \"uuid_usuario_solicita\": \"1344d2d6-c82e-467a-8c50-6364a778f0bb\"}',NULL,'2026-04-14 05:09:34'),
(65,'Sistema','Sistema','Sistema','default','INSERT','pedidos_proveedor_detalle','N/A',NULL,'{\"uuid_insumo\": \"81be855e-62f4-425a-ba74-c310706e8681\", \"uuid_pedido\": \"41019023-3ff3-416d-94e4-06ff58325b9f\", \"fecha_creacion\": null, \"cantidad_pedida\": 5, \"cantidad_recibida\": null, \"fecha_actualizacion\": null, \"uuid_detalle_pedido\": null, \"costo_unitario_estimado\": 220.0}',NULL,'2026-04-14 05:09:34'),
(66,'Sistema','Sistema','Sistema','default','INSERT','compras_encabezado','N/A',NULL,'{\"estatus\": \"RECIBIDO\", \"uuid_compra\": null, \"uuid_pedido\": \"41019023-3ff3-416d-94e4-06ff58325b9f\", \"fecha_compra\": null, \"folio_factura\": \"FAC-INS-TEX-002-99\", \"uuid_proveedor\": \"44481cff-8dc3-4545-b241-d06ca6ecb46f\", \"fecha_actualizacion\": null, \"uuid_usuario_registro\": \"1344d2d6-c82e-467a-8c50-6364a778f0bb\"}',NULL,'2026-04-14 05:09:34'),
(67,'Sistema','Sistema','Sistema','default','INSERT','compras_detalle','N/A',NULL,'{\"uuid_compra\": \"4c2f113f-2a97-4dd3-8205-fd1c59c89bef\", \"uuid_insumo\": \"81be855e-62f4-425a-ba74-c310706e8681\", \"fecha_creacion\": null, \"cantidad_comprada\": 5, \"fecha_actualizacion\": null, \"uuid_detalle_compra\": null, \"costo_unitario_compra\": 220.0}',NULL,'2026-04-14 05:09:34'),
(68,'Sistema','Sistema','Sistema','default','INSERT','rollos_inventario','N/A',NULL,'{\"uuid_rollo\": null, \"uuid_insumo\": \"81be855e-62f4-425a-ba74-c310706e8681\", \"fecha_creacion\": null, \"metraje_inicial\": 50.0, \"fecha_actualizacion\": null, \"uuid_detalle_compra\": \"bc04bc8b-515b-4700-b76b-1c14263ac25f\", \"metraje_continuo_actual\": 50.0}',NULL,'2026-04-14 05:09:34'),
(69,'Sistema','Sistema','Sistema','default','INSERT','rollos_inventario','N/A',NULL,'{\"uuid_rollo\": null, \"uuid_insumo\": \"81be855e-62f4-425a-ba74-c310706e8681\", \"fecha_creacion\": null, \"metraje_inicial\": 50.0, \"fecha_actualizacion\": null, \"uuid_detalle_compra\": \"bc04bc8b-515b-4700-b76b-1c14263ac25f\", \"metraje_continuo_actual\": 50.0}',NULL,'2026-04-14 05:09:34'),
(70,'Sistema','Sistema','Sistema','default','INSERT','rollos_inventario','N/A',NULL,'{\"uuid_rollo\": null, \"uuid_insumo\": \"81be855e-62f4-425a-ba74-c310706e8681\", \"fecha_creacion\": null, \"metraje_inicial\": 50.0, \"fecha_actualizacion\": null, \"uuid_detalle_compra\": \"bc04bc8b-515b-4700-b76b-1c14263ac25f\", \"metraje_continuo_actual\": 50.0}',NULL,'2026-04-14 05:09:34'),
(71,'Sistema','Sistema','Sistema','default','INSERT','rollos_inventario','N/A',NULL,'{\"uuid_rollo\": null, \"uuid_insumo\": \"81be855e-62f4-425a-ba74-c310706e8681\", \"fecha_creacion\": null, \"metraje_inicial\": 50.0, \"fecha_actualizacion\": null, \"uuid_detalle_compra\": \"bc04bc8b-515b-4700-b76b-1c14263ac25f\", \"metraje_continuo_actual\": 50.0}',NULL,'2026-04-14 05:09:34'),
(72,'Sistema','Sistema','Sistema','default','INSERT','rollos_inventario','N/A',NULL,'{\"uuid_rollo\": null, \"uuid_insumo\": \"81be855e-62f4-425a-ba74-c310706e8681\", \"fecha_creacion\": null, \"metraje_inicial\": 50.0, \"fecha_actualizacion\": null, \"uuid_detalle_compra\": \"bc04bc8b-515b-4700-b76b-1c14263ac25f\", \"metraje_continuo_actual\": 50.0}',NULL,'2026-04-14 05:09:34'),
(73,'Sistema','Sistema','Sistema','default','UPDATE','insumos','81be855e-62f4-425a-ba74-c310706e8681','{\"stock_total_acumulado\": 0.0}','{\"stock_total_acumulado\": 250.0}',NULL,'2026-04-14 05:09:34'),
(74,'Sistema','Sistema','Sistema','default','INSERT','pedidos_proveedor_encabezado','N/A',NULL,'{\"estatus\": \"Completado\", \"uuid_pedido\": null, \"fecha_pedido\": null, \"folio_pedido\": \"PED-INS-ACC-001\", \"uuid_proveedor\": \"0922ee6f-efb2-4957-baa5-8130029f941c\", \"fecha_actualizacion\": null, \"uuid_usuario_solicita\": \"1344d2d6-c82e-467a-8c50-6364a778f0bb\"}',NULL,'2026-04-14 05:09:34'),
(75,'Sistema','Sistema','Sistema','default','INSERT','pedidos_proveedor_detalle','N/A',NULL,'{\"uuid_insumo\": \"759dfd9f-9a35-4a0a-a89e-c5dc3ddc7c01\", \"uuid_pedido\": \"9ac877ce-f3cc-4bd4-94fa-dcd01730f4e4\", \"fecha_creacion\": null, \"cantidad_pedida\": 100, \"cantidad_recibida\": null, \"fecha_actualizacion\": null, \"uuid_detalle_pedido\": null, \"costo_unitario_estimado\": 12.0}',NULL,'2026-04-14 05:09:34'),
(76,'Sistema','Sistema','Sistema','default','INSERT','compras_encabezado','N/A',NULL,'{\"estatus\": \"RECIBIDO\", \"uuid_compra\": null, \"uuid_pedido\": \"9ac877ce-f3cc-4bd4-94fa-dcd01730f4e4\", \"fecha_compra\": null, \"folio_factura\": \"FAC-INS-ACC-001-99\", \"uuid_proveedor\": \"0922ee6f-efb2-4957-baa5-8130029f941c\", \"fecha_actualizacion\": null, \"uuid_usuario_registro\": \"1344d2d6-c82e-467a-8c50-6364a778f0bb\"}',NULL,'2026-04-14 05:09:34'),
(77,'Sistema','Sistema','Sistema','default','INSERT','compras_detalle','N/A',NULL,'{\"uuid_compra\": \"11bcad79-3ca3-45b3-9155-ee03039ef625\", \"uuid_insumo\": \"759dfd9f-9a35-4a0a-a89e-c5dc3ddc7c01\", \"fecha_creacion\": null, \"cantidad_comprada\": 100, \"fecha_actualizacion\": null, \"uuid_detalle_compra\": null, \"costo_unitario_compra\": 12.0}',NULL,'2026-04-14 05:09:34'),
(78,'Sistema','Sistema','Sistema','default','UPDATE','insumos','759dfd9f-9a35-4a0a-a89e-c5dc3ddc7c01','{\"stock_total_acumulado\": 0.0}','{\"stock_total_acumulado\": 100}',NULL,'2026-04-14 05:09:34'),
(79,'Sistema','Sistema','Sistema','default','INSERT','pedidos_proveedor_encabezado','N/A',NULL,'{\"estatus\": \"Completado\", \"uuid_pedido\": null, \"fecha_pedido\": null, \"folio_pedido\": \"PED-INS-ACC-003\", \"uuid_proveedor\": \"0922ee6f-efb2-4957-baa5-8130029f941c\", \"fecha_actualizacion\": null, \"uuid_usuario_solicita\": \"1344d2d6-c82e-467a-8c50-6364a778f0bb\"}',NULL,'2026-04-14 05:09:34'),
(80,'Sistema','Sistema','Sistema','default','INSERT','pedidos_proveedor_detalle','N/A',NULL,'{\"uuid_insumo\": \"c8bf5828-7c54-4c8f-a310-1232856eef44\", \"uuid_pedido\": \"d2022988-8d1d-4075-8cf0-422bf5d5d02c\", \"fecha_creacion\": null, \"cantidad_pedida\": 500, \"cantidad_recibida\": null, \"fecha_actualizacion\": null, \"uuid_detalle_pedido\": null, \"costo_unitario_estimado\": 5.0}',NULL,'2026-04-14 05:09:34'),
(81,'Sistema','Sistema','Sistema','default','INSERT','compras_encabezado','N/A',NULL,'{\"estatus\": \"RECIBIDO\", \"uuid_compra\": null, \"uuid_pedido\": \"d2022988-8d1d-4075-8cf0-422bf5d5d02c\", \"fecha_compra\": null, \"folio_factura\": \"FAC-INS-ACC-003-99\", \"uuid_proveedor\": \"0922ee6f-efb2-4957-baa5-8130029f941c\", \"fecha_actualizacion\": null, \"uuid_usuario_registro\": \"1344d2d6-c82e-467a-8c50-6364a778f0bb\"}',NULL,'2026-04-14 05:09:34'),
(82,'Sistema','Sistema','Sistema','default','INSERT','compras_detalle','N/A',NULL,'{\"uuid_compra\": \"923dfcf2-579d-4137-b6bc-02aabaa1a628\", \"uuid_insumo\": \"c8bf5828-7c54-4c8f-a310-1232856eef44\", \"fecha_creacion\": null, \"cantidad_comprada\": 500, \"fecha_actualizacion\": null, \"uuid_detalle_compra\": null, \"costo_unitario_compra\": 5.0}',NULL,'2026-04-14 05:09:34'),
(83,'Sistema','Sistema','Sistema','default','UPDATE','insumos','c8bf5828-7c54-4c8f-a310-1232856eef44','{\"stock_total_acumulado\": 0.0}','{\"stock_total_acumulado\": 500}',NULL,'2026-04-14 05:09:34'),
(84,'Sistema','Sistema','Sistema','default','INSERT','ventas_encabezado','N/A',NULL,'{\"uuid_venta\": null, \"fecha_venta\": null, \"metodo_pago\": \"Tarjeta\", \"uuid_cliente\": \"2754c910-75f9-4447-9d4a-f783061f40a9\", \"estatus_envio\": \"Entregado\", \"numero_pedido\": \"AX-101\", \"fecha_actualizacion\": null}',NULL,'2026-04-14 05:09:34'),
(85,'Sistema','Sistema','Sistema','default','INSERT','ventas_detalle','N/A',NULL,'{\"cantidad\": 1, \"uuid_venta\": \"9611f585-7630-436b-b35e-9dcf1713ab3d\", \"uuid_detalle\": null, \"uuid_producto\": \"db29c2f4-e7ae-4dbd-8d10-d5045bd1dcdf\", \"fecha_creacion\": null, \"fecha_actualizacion\": null, \"precio_unitario_historico\": 1200.0}',NULL,'2026-04-14 05:09:34'),
(86,'Sistema','Sistema','Sistema','default','INSERT','ventas_detalle','N/A',NULL,'{\"cantidad\": 2, \"uuid_venta\": \"9611f585-7630-436b-b35e-9dcf1713ab3d\", \"uuid_detalle\": null, \"uuid_producto\": \"107d538b-e93e-425d-9c72-ee545ba509d3\", \"fecha_creacion\": null, \"fecha_actualizacion\": null, \"precio_unitario_historico\": 450.0}',NULL,'2026-04-14 05:09:34'),
(87,'Sistema','Sistema','Sistema','default','INSERT','ventas_encabezado','N/A',NULL,'{\"uuid_venta\": null, \"fecha_venta\": null, \"metodo_pago\": \"Paypal\", \"uuid_cliente\": \"2754c910-75f9-4447-9d4a-f783061f40a9\", \"estatus_envio\": \"Procesando\", \"numero_pedido\": \"AX-102\", \"fecha_actualizacion\": null}',NULL,'2026-04-14 05:09:34'),
(88,'Sistema','Sistema','Sistema','default','INSERT','ventas_detalle','N/A',NULL,'{\"cantidad\": 2, \"uuid_venta\": \"4affbf8f-5c8a-4875-a20d-7ef68cfca739\", \"uuid_detalle\": null, \"uuid_producto\": \"db29c2f4-e7ae-4dbd-8d10-d5045bd1dcdf\", \"fecha_creacion\": null, \"fecha_actualizacion\": null, \"precio_unitario_historico\": 1200.0}',NULL,'2026-04-14 05:09:34'),
(89,'Sistema','Sistema','Sistema','default','INSERT','ordenes_produccion','N/A',NULL,'{\"estado\": \"Terminado\", \"uuid_op\": null, \"uuid_producto\": \"db29c2f4-e7ae-4dbd-8d10-d5045bd1dcdf\", \"fecha_solicitud\": null, \"uuid_venta_detalle\": \"8965c7ce-da97-490d-8fe0-2ad7e928ba7d\", \"cantidad_a_producir\": 10, \"fecha_actualizacion\": null, \"uuid_pedido_detalle\": null}',NULL,'2026-04-14 05:09:34'),
(90,'Sistema','Sistema','Sistema','default','INSERT','ejecucion_corte','N/A',NULL,'{\"uuid_op\": \"20a8923a-056b-49e5-97f8-aed360fc7d81\", \"uuid_corte\": null, \"fecha_proceso\": null, \"uuid_rollo_used\": \"2187a50d-698d-414e-bf66-04350ee86bb6\", \"usuario_corto_uuid\": \"1344d2d6-c82e-467a-8c50-6364a778f0bb\", \"fecha_actualizacion\": null, \"merma_real_calculada\": 1.5, \"metros_sacados_bodega\": 26.5, \"prendas_reales_logradas\": 10, \"metros_teoricos_requeridos\": 25.0}',NULL,'2026-04-14 05:09:34'),
(91,'Sistema','Sistema','Sistema','default','INSERT','merma_piezas','N/A',NULL,'{\"motivo\": \"ERROR_OPERARIO\", \"uuid_op\": \"20a8923a-056b-49e5-97f8-aed360fc7d81\", \"uuid_merma\": null, \"uuid_insumo\": \"c8bf5828-7c54-4c8f-a310-1232856eef44\", \"observaciones\": \"2 etiquetas se dañaron al coser.\", \"fecha_registro\": null, \"cantidad_teorica\": 10, \"fecha_actualizacion\": null, \"usuario_registro_uuid\": \"1344d2d6-c82e-467a-8c50-6364a778f0bb\", \"cantidad_real_consumida\": 12}',NULL,'2026-04-14 05:09:34'),
(92,'Sistema','Sistema','Sistema','default','UPDATE','rollos_inventario','2187a50d-698d-414e-bf66-04350ee86bb6','{\"metraje_continuo_actual\": 50.0}','{\"metraje_continuo_actual\": 23.5}',NULL,'2026-04-14 05:09:34'),
(93,'Sistema','Sistema','Sistema','default','INSERT','ordenes_produccion','N/A',NULL,'{\"estado\": \"Pendiente\", \"uuid_op\": null, \"uuid_producto\": \"107d538b-e93e-425d-9c72-ee545ba509d3\", \"fecha_solicitud\": null, \"uuid_venta_detalle\": null, \"cantidad_a_producir\": 30, \"fecha_actualizacion\": null, \"uuid_pedido_detalle\": null}',NULL,'2026-04-14 05:09:34'),
(94,'1344d2d6-c82e-467a-8c50-6364a778f0bb','Admin Axis','admin','cliente_rol','UPDATE','usuarios','1344d2d6-c82e-467a-8c50-6364a778f0bb','{\"tf_totp_secret\": null, \"tf_primary_method\": null}','{\"tf_totp_secret\": \"{\\\"enckey\\\":{\\\"c\\\":14,\\\"k\\\":\\\"TTO4Y57AMIK5SIF7ND7GOWZQVW4E76MJ\\\",\\\"s\\\":\\\"6OPBGQRIEWCFBCRRMZWA\\\",\\\"t\\\":\\\"1\\\",\\\"v\\\":1},\\\"type\\\":\\\"totp\\\",\\\"v\\\":1}\", \"tf_primary_method\": \"authenticator\"}','172.18.0.1','2026-04-14 05:10:28');
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
('1344d2d6-c82e-467a-8c50-6364a778f0bb','Admin Axis','admin@axis.com','$argon2id$v=19$m=65536,t=3,p=4$+l/Ludfau9day3nP+Z8Twg$87CCDRTWBfiTnjWXeyZHamtBMwQMl6oHNfN7lsjE3VQ',1,'2026-04-14 05:09:33','2026-04-14 05:10:28','7503db8daa894b178a9551ce8c1b4e18','2026-04-14 05:09:34','authenticator','{\"enckey\":{\"c\":14,\"k\":\"TTO4Y57AMIK5SIF7ND7GOWZQVW4E76MJ\",\"s\":\"6OPBGQRIEWCFBCRRMZWA\",\"t\":\"1\",\"v\":1},\"type\":\"totp\",\"v\":1}',NULL,'2026-04-14 05:09:33',NULL),
('1a8fb32d-2298-4076-96ca-28300138f462','Modista Principal','modista@axis.com','$argon2id$v=19$m=65536,t=3,p=4$KmXsXUupFaK0FuIc49y7Nw$hu8yyfSHD2LoAr4L54RJTMRBpfWQqkFx/bO0OM/TqgE',1,'2026-04-14 05:09:33','2026-04-14 05:09:33','27b7754b330942f49e9338156186b1de','2026-04-14 05:09:34',NULL,NULL,NULL,'2026-04-14 05:09:33',NULL),
('262dcc8c-d33e-4fdb-8d6d-91ecbae6f45d','Comprador Axis','compras@axis.com','$argon2id$v=19$m=65536,t=3,p=4$Z+zde4/Rek/J+T9HyNm7Nw$Qz8bxcWPS7Hpgl/aTsbdNoNjw5Aw58Bmo2K37uSITb0',1,'2026-04-14 05:09:33','2026-04-14 05:09:33','8ec2d77b64d64072871acee868a636dd','2026-04-14 05:09:34',NULL,NULL,NULL,'2026-04-14 05:09:33',NULL),
('323c5471-f959-41fb-97ff-ad12ed417cc2','Juan Cliente','juan@axis.com','$argon2id$v=19$m=65536,t=3,p=4$itGac85Zaw2hNOZcq/XeGw$eGDs71zgBAlT1/Wzka9JB1TK4aFiVONIW5wjqgVQ6DQ',1,'2026-04-14 05:09:34','2026-04-14 05:09:34','4e3b43461e4849ba89a580774875e27e','2026-04-14 05:09:34',NULL,NULL,NULL,'2026-04-14 05:09:34',NULL),
('b935683e-5e64-4cae-9e2f-94fb896af4b9','Vendedor Axis','ventas@axis.com','$argon2id$v=19$m=65536,t=3,p=4$vpdyDiFEqBWidG5trVUK4Q$rv4b7Uxgsz9gh4mLickQX/v8WQV3O2kmte9kTlxEnVA',1,'2026-04-14 05:09:33','2026-04-14 05:09:33','12c3440df4b84643a5fc524fdfbabdbe','2026-04-14 05:09:34',NULL,NULL,NULL,'2026-04-14 05:09:33',NULL),
('cf4dc48f-ad19-49a6-9ab7-b8ad690bb982','Maria Lopez','maria@axis.com','$argon2id$v=19$m=65536,t=3,p=4$sDZmbG2tVarVWotRaq3VGg$P8ClmMmO/C3cNX6ClnXUzfwM5d38H3AdKJGqpaDssfU',1,'2026-04-14 05:09:34','2026-04-14 05:09:34','e2a50eca7e6645fa97262954882ba446','2026-04-14 05:09:34',NULL,NULL,NULL,'2026-04-14 05:09:34',NULL);
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
('8965c7ce-da97-490d-8fe0-2ad7e928ba7d','9611f585-7630-436b-b35e-9dcf1713ab3d','107d538b-e93e-425d-9c72-ee545ba509d3',2,450.00,'2026-04-14 05:09:34','2026-04-14 05:09:34'),
('be6976a4-2b99-4f24-b7bd-417c931a169a','9611f585-7630-436b-b35e-9dcf1713ab3d','db29c2f4-e7ae-4dbd-8d10-d5045bd1dcdf',1,1200.00,'2026-04-14 05:09:34','2026-04-14 05:09:34'),
('d01a0dbf-ec80-4584-8e3a-a8819274676b','4affbf8f-5c8a-4875-a20d-7ef68cfca739','db29c2f4-e7ae-4dbd-8d10-d5045bd1dcdf',2,1200.00,'2026-04-14 05:09:34','2026-04-14 05:09:34');
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
('4affbf8f-5c8a-4875-a20d-7ef68cfca739','AX-102','2754c910-75f9-4447-9d4a-f783061f40a9','Paypal','Procesando','2026-04-14 05:09:34','2026-04-14 05:09:34'),
('9611f585-7630-436b-b35e-9dcf1713ab3d','AX-101','2754c910-75f9-4447-9d4a-f783061f40a9','Tarjeta','Entregado','2026-04-14 05:09:34','2026-04-14 05:09:34');
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

-- Dump completed on 2026-04-14  5:10:36
