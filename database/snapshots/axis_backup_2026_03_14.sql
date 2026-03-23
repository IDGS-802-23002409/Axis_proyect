/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19-12.1.2-MariaDB, for Win64 (AMD64)
--
-- Host: localhost    Database: axis_db
-- ------------------------------------------------------
-- Server version	12.1.2-MariaDB-log

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
-- Table structure for table `consumos_por_ancho`
--

DROP TABLE IF EXISTS `consumos_por_ancho`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `consumos_por_ancho` (
  `uuid_consumo` char(36) NOT NULL,
  `uuid_ficha` char(36) NOT NULL,
  `uuid_insumo` char(36) NOT NULL,
  `ancho_referencia` decimal(5,2) NOT NULL,
  `consumo_teorico_unitario` decimal(12,4) NOT NULL,
  `fecha_creacion` datetime DEFAULT current_timestamp(),
  `fecha_actualizacion` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `usuario_creo_uuid` char(36) DEFAULT NULL,
  `usuario_actualizo_uuid` char(36) DEFAULT NULL,
  PRIMARY KEY (`uuid_consumo`),
  KEY `uuid_ficha` (`uuid_ficha`),
  KEY `uuid_insumo` (`uuid_insumo`),
  CONSTRAINT `1` FOREIGN KEY (`uuid_ficha`) REFERENCES `fichas_tecnicas` (`uuid_ficha`),
  CONSTRAINT `2` FOREIGN KEY (`uuid_insumo`) REFERENCES `insumos` (`uuid_insumo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `consumos_por_ancho`
--

LOCK TABLES `consumos_por_ancho` WRITE;
/*!40000 ALTER TABLE `consumos_por_ancho` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `consumos_por_ancho` VALUES
('73c1adf3-2027-11f1-9b2d-14ac60e52fb2','73b35e27-2027-11f1-9b2d-14ac60e52fb2','7372e6bf-2027-11f1-9b2d-14ac60e52fb2',1.50,1.4500,'2026-03-14 22:28:44','2026-03-14 22:28:44',NULL,NULL),
('73c1b571-2027-11f1-9b2d-14ac60e52fb2','73b35e27-2027-11f1-9b2d-14ac60e52fb2','7372e6bf-2027-11f1-9b2d-14ac60e52fb2',1.60,1.3500,'2026-03-14 22:28:44','2026-03-14 22:28:44',NULL,NULL),
('73c1b708-2027-11f1-9b2d-14ac60e52fb2','73b90ae7-2027-11f1-9b2d-14ac60e52fb2','7379dcac-2027-11f1-9b2d-14ac60e52fb2',1.60,1.1000,'2026-03-14 22:28:44','2026-03-14 22:28:44',NULL,NULL);
/*!40000 ALTER TABLE `consumos_por_ancho` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `egresos_caja`
--

DROP TABLE IF EXISTS `egresos_caja`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `egresos_caja` (
  `uuid_egreso` char(36) NOT NULL,
  `monto` decimal(12,2) NOT NULL,
  `descripcion` varchar(255) NOT NULL,
  `fecha_creacion` datetime DEFAULT current_timestamp(),
  `fecha_actualizacion` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `usuario_creo_uuid` char(36) DEFAULT NULL,
  `usuario_actualizo_uuid` char(36) DEFAULT NULL,
  PRIMARY KEY (`uuid_egreso`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `egresos_caja`
--

LOCK TABLES `egresos_caja` WRITE;
/*!40000 ALTER TABLE `egresos_caja` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `egresos_caja` VALUES
('73ee2973-2027-11f1-9b2d-14ac60e52fb2',50.00,'Compra de artículos de limpieza','2026-03-14 22:28:44','2026-03-14 22:28:44',NULL,NULL),
('73ee3819-2027-11f1-9b2d-14ac60e52fb2',200.00,'Pago reparación de máquina de coser','2026-03-14 22:28:44','2026-03-14 22:28:44',NULL,NULL);
/*!40000 ALTER TABLE `egresos_caja` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `ejecucion_corte`
--

DROP TABLE IF EXISTS `ejecucion_corte`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `ejecucion_corte` (
  `uuid_corte` char(36) NOT NULL,
  `uuid_op` char(36) NOT NULL,
  `uuid_rollo_usado` char(36) NOT NULL,
  `metros_entregados` decimal(12,4) NOT NULL,
  `metros_devueltos` decimal(12,4) NOT NULL,
  `prendas_finales_reales` int(11) NOT NULL,
  `uuid_motivo_variabilidad` char(36) DEFAULT NULL,
  `fecha_creacion` datetime DEFAULT current_timestamp(),
  `fecha_actualizacion` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `usuario_creo_uuid` char(36) DEFAULT NULL,
  `usuario_actualizo_uuid` char(36) DEFAULT NULL,
  PRIMARY KEY (`uuid_corte`),
  KEY `uuid_op` (`uuid_op`),
  KEY `uuid_rollo_usado` (`uuid_rollo_usado`),
  KEY `uuid_motivo_variabilidad` (`uuid_motivo_variabilidad`),
  CONSTRAINT `1` FOREIGN KEY (`uuid_op`) REFERENCES `ordenes_produccion` (`uuid_op`),
  CONSTRAINT `2` FOREIGN KEY (`uuid_rollo_usado`) REFERENCES `rollos_inventario` (`uuid_rollo`),
  CONSTRAINT `3` FOREIGN KEY (`uuid_motivo_variabilidad`) REFERENCES `motivos_desviacion` (`uuid_motivo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ejecucion_corte`
--

LOCK TABLES `ejecucion_corte` WRITE;
/*!40000 ALTER TABLE `ejecucion_corte` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `ejecucion_corte` VALUES
('73d66561-2027-11f1-9b2d-14ac60e52fb2','73c6cbcd-2027-11f1-9b2d-14ac60e52fb2','7386cc8b-2027-11f1-9b2d-14ac60e52fb2',15.0000,0.5000,10,'7343f22c-2027-11f1-9b2d-14ac60e52fb2','2026-03-14 22:28:44','2026-03-14 22:28:44',NULL,NULL);
/*!40000 ALTER TABLE `ejecucion_corte` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `fichas_tecnicas`
--

DROP TABLE IF EXISTS `fichas_tecnicas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `fichas_tecnicas` (
  `uuid_ficha` char(36) NOT NULL,
  `uuid_producto` char(36) NOT NULL,
  `instrucciones_corte` text DEFAULT NULL,
  `fecha_creacion` datetime DEFAULT current_timestamp(),
  `fecha_actualizacion` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `usuario_creo_uuid` char(36) DEFAULT NULL,
  `usuario_actualizo_uuid` char(36) DEFAULT NULL,
  PRIMARY KEY (`uuid_ficha`),
  KEY `uuid_producto` (`uuid_producto`),
  CONSTRAINT `1` FOREIGN KEY (`uuid_producto`) REFERENCES `productos_terminados` (`uuid_producto`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fichas_tecnicas`
--

LOCK TABLES `fichas_tecnicas` WRITE;
/*!40000 ALTER TABLE `fichas_tecnicas` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `fichas_tecnicas` VALUES
('73b35e27-2027-11f1-9b2d-14ac60e52fb2','73a24e16-2027-11f1-9b2d-14ac60e52fb2','Corte en sentido de la urdimbre, dejar 2cm de costura.','2026-03-14 22:28:44','2026-03-14 22:28:44',NULL,NULL),
('73b90ae7-2027-11f1-9b2d-14ac60e52fb2','73a7bc3a-2027-11f1-9b2d-14ac60e52fb2','Corte con cuidado en cuellos y puños.','2026-03-14 22:28:44','2026-03-14 22:28:44',NULL,NULL);
/*!40000 ALTER TABLE `fichas_tecnicas` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `insumos`
--

DROP TABLE IF EXISTS `insumos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `insumos` (
  `uuid_insumo` char(36) NOT NULL,
  `sku` varchar(50) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `unidad_medida_base` varchar(20) NOT NULL,
  `fecha_creacion` datetime DEFAULT current_timestamp(),
  `fecha_actualizacion` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `usuario_creo_uuid` char(36) DEFAULT NULL,
  `usuario_actualizo_uuid` char(36) DEFAULT NULL,
  PRIMARY KEY (`uuid_insumo`),
  UNIQUE KEY `sku` (`sku`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `insumos`
--

LOCK TABLES `insumos` WRITE;
/*!40000 ALTER TABLE `insumos` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `insumos` VALUES
('7372e6bf-2027-11f1-9b2d-14ac60e52fb2','INS-MEZ-001','Mezclilla Stretch 12oz','Metros','2026-03-14 22:28:43','2026-03-14 22:28:43',NULL,NULL),
('7379dcac-2027-11f1-9b2d-14ac60e52fb2','INS-ALG-502','Algodón Pima Blanco','Metros','2026-03-14 22:28:43','2026-03-14 22:28:43',NULL,NULL),
('738101df-2027-11f1-9b2d-14ac60e52fb2','INS-BOT-001','Botón Metálico 20mm','Piezas','2026-03-14 22:28:43','2026-03-14 22:28:43',NULL,NULL);
/*!40000 ALTER TABLE `insumos` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `motivos_desviacion`
--

DROP TABLE IF EXISTS `motivos_desviacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `motivos_desviacion` (
  `uuid_motivo` char(36) NOT NULL,
  `descripcion` varchar(100) NOT NULL,
  `fecha_creacion` datetime DEFAULT current_timestamp(),
  `fecha_actualizacion` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `usuario_creo_uuid` char(36) DEFAULT NULL,
  `usuario_actualizo_uuid` char(36) DEFAULT NULL,
  PRIMARY KEY (`uuid_motivo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `motivos_desviacion`
--

LOCK TABLES `motivos_desviacion` WRITE;
/*!40000 ALTER TABLE `motivos_desviacion` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `motivos_desviacion` VALUES
('7343b7e9-2027-11f1-9b2d-14ac60e52fb2','Defecto de fábrica en tela','2026-03-14 22:28:43','2026-03-14 22:28:43',NULL,NULL),
('7343cb00-2027-11f1-9b2d-14ac60e52fb2','Error en trazo de corte','2026-03-14 22:28:43','2026-03-14 22:28:43',NULL,NULL),
('7343f12f-2027-11f1-9b2d-14ac60e52fb2','Variación de ancho real vs ficha','2026-03-14 22:28:43','2026-03-14 22:28:43',NULL,NULL),
('7343f1e2-2027-11f1-9b2d-14ac60e52fb2','Muestra adicional para cliente','2026-03-14 22:28:43','2026-03-14 22:28:43',NULL,NULL),
('7343f22c-2027-11f1-9b2d-14ac60e52fb2','Sin desviación (Normal)','2026-03-14 22:28:43','2026-03-14 22:28:43',NULL,NULL);
/*!40000 ALTER TABLE `motivos_desviacion` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `ordenes_produccion`
--

DROP TABLE IF EXISTS `ordenes_produccion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `ordenes_produccion` (
  `uuid_op` char(36) NOT NULL,
  `uuid_producto` char(36) NOT NULL,
  `prendas_solicitadas` int(11) NOT NULL,
  `estado` varchar(20) DEFAULT 'Pendiente',
  `fecha_creacion` datetime DEFAULT current_timestamp(),
  `fecha_actualizacion` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `usuario_creo_uuid` char(36) DEFAULT NULL,
  `usuario_actualizo_uuid` char(36) DEFAULT NULL,
  PRIMARY KEY (`uuid_op`),
  KEY `uuid_producto` (`uuid_producto`),
  CONSTRAINT `1` FOREIGN KEY (`uuid_producto`) REFERENCES `productos_terminados` (`uuid_producto`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ordenes_produccion`
--

LOCK TABLES `ordenes_produccion` WRITE;
/*!40000 ALTER TABLE `ordenes_produccion` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `ordenes_produccion` VALUES
('73c6cbcd-2027-11f1-9b2d-14ac60e52fb2','73a24e16-2027-11f1-9b2d-14ac60e52fb2',10,'Terminado','2026-03-14 22:28:44','2026-03-14 22:28:44',NULL,NULL),
('73cb41d0-2027-11f1-9b2d-14ac60e52fb2','73a24e16-2027-11f1-9b2d-14ac60e52fb2',20,'Corte','2026-03-14 22:28:44','2026-03-14 22:28:44',NULL,NULL),
('73cf3cb4-2027-11f1-9b2d-14ac60e52fb2','73a7bc3a-2027-11f1-9b2d-14ac60e52fb2',50,'Pendiente','2026-03-14 22:28:44','2026-03-14 22:28:44',NULL,NULL);
/*!40000 ALTER TABLE `ordenes_produccion` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `productos_terminados`
--

DROP TABLE IF EXISTS `productos_terminados`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `productos_terminados` (
  `uuid_producto` char(36) NOT NULL,
  `codigo_estilo` varchar(50) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `precio_venta_actual` decimal(12,2) NOT NULL,
  `stock_fisico` int(11) DEFAULT 0,
  `fecha_creacion` datetime DEFAULT current_timestamp(),
  `fecha_actualizacion` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `usuario_creo_uuid` char(36) DEFAULT NULL,
  `usuario_actualizo_uuid` char(36) DEFAULT NULL,
  PRIMARY KEY (`uuid_producto`),
  UNIQUE KEY `codigo_estilo` (`codigo_estilo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `productos_terminados`
--

LOCK TABLES `productos_terminados` WRITE;
/*!40000 ALTER TABLE `productos_terminados` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `productos_terminados` VALUES
('73a24e16-2027-11f1-9b2d-14ac60e52fb2','EST-JEAN-01','Pantalón Jean Clásico',450.00,50,'2026-03-14 22:28:44','2026-03-14 22:28:44',NULL,NULL),
('73a7bc3a-2027-11f1-9b2d-14ac60e52fb2','EST-CAM-05','Camisa Algodón Casual',320.00,30,'2026-03-14 22:28:44','2026-03-14 22:28:44',NULL,NULL),
('73adf0ca-2027-11f1-9b2d-14ac60e52fb2','EST-SHOR-02','Short Verano Denim',280.00,15,'2026-03-14 22:28:44','2026-03-14 22:28:44',NULL,NULL);
/*!40000 ALTER TABLE `productos_terminados` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `proveedores`
--

DROP TABLE IF EXISTS `proveedores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `proveedores` (
  `uuid_proveedor` char(36) NOT NULL,
  `razon_social` varchar(150) NOT NULL,
  `rfc_id_fiscal` varchar(20) NOT NULL,
  `contacto_nombre` varchar(100) DEFAULT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `categoria_insumo` varchar(50) DEFAULT NULL,
  `fecha_creacion` datetime DEFAULT current_timestamp(),
  `fecha_actualizacion` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `usuario_creo_uuid` char(36) DEFAULT NULL,
  `usuario_actualizo_uuid` char(36) DEFAULT NULL,
  PRIMARY KEY (`uuid_proveedor`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `proveedores`
--

LOCK TABLES `proveedores` WRITE;
/*!40000 ALTER TABLE `proveedores` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `proveedores` VALUES
('735e9e0d-2027-11f1-9b2d-14ac60e52fb2','Textiles Globales S.A.','TEXG900101ABC','Juan Pérez',NULL,'Telas','2026-03-14 22:28:43','2026-03-14 22:28:43',NULL,NULL),
('73646224-2027-11f1-9b2d-14ac60e52fb2','Avíos y Botones S.A.','AVIO850505XYZ','María García',NULL,'Accesorios','2026-03-14 22:28:43','2026-03-14 22:28:43',NULL,NULL),
('7364646d-2027-11f1-9b2d-14ac60e52fb2','Hilos de Calidad','HILO701010HIL','Roberto Gómez',NULL,'Hilos','2026-03-14 22:28:43','2026-03-14 22:28:43',NULL,NULL);
/*!40000 ALTER TABLE `proveedores` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `rollos_inventario`
--

DROP TABLE IF EXISTS `rollos_inventario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `rollos_inventario` (
  `uuid_rollo` char(36) NOT NULL,
  `uuid_insumo` char(36) NOT NULL,
  `uuid_proveedor` char(36) NOT NULL,
  `metraje_inicial` decimal(12,4) NOT NULL,
  `metraje_actual` decimal(12,4) NOT NULL,
  `ancho_real_recibido` decimal(5,2) NOT NULL,
  `fecha_creacion` datetime DEFAULT current_timestamp(),
  `fecha_actualizacion` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `usuario_creo_uuid` char(36) DEFAULT NULL,
  `usuario_actualizo_uuid` char(36) DEFAULT NULL,
  PRIMARY KEY (`uuid_rollo`),
  KEY `uuid_insumo` (`uuid_insumo`),
  KEY `uuid_proveedor` (`uuid_proveedor`),
  CONSTRAINT `1` FOREIGN KEY (`uuid_insumo`) REFERENCES `insumos` (`uuid_insumo`),
  CONSTRAINT `2` FOREIGN KEY (`uuid_proveedor`) REFERENCES `proveedores` (`uuid_proveedor`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rollos_inventario`
--

LOCK TABLES `rollos_inventario` WRITE;
/*!40000 ALTER TABLE `rollos_inventario` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `rollos_inventario` VALUES
('7386cc8b-2027-11f1-9b2d-14ac60e52fb2','7372e6bf-2027-11f1-9b2d-14ac60e52fb2','735e9e0d-2027-11f1-9b2d-14ac60e52fb2',100.0000,85.5000,1.50,'2026-03-14 22:28:44','2026-03-14 22:28:44',NULL,NULL),
('73975794-2027-11f1-9b2d-14ac60e52fb2','7372e6bf-2027-11f1-9b2d-14ac60e52fb2','735e9e0d-2027-11f1-9b2d-14ac60e52fb2',120.0000,120.0000,1.55,'2026-03-14 22:28:44','2026-03-14 22:28:44',NULL,NULL),
('739c64fe-2027-11f1-9b2d-14ac60e52fb2','7379dcac-2027-11f1-9b2d-14ac60e52fb2','735e9e0d-2027-11f1-9b2d-14ac60e52fb2',50.0000,50.0000,1.60,'2026-03-14 22:28:44','2026-03-14 22:28:44',NULL,NULL);
/*!40000 ALTER TABLE `rollos_inventario` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios` (
  `uuid_usuario` char(36) NOT NULL,
  `nombre_completo` varchar(150) NOT NULL,
  `email` varchar(120) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `rol` varchar(50) NOT NULL,
  `intentos_fallidos` int(11) DEFAULT 0,
  `estatus` tinyint(1) DEFAULT 1,
  `fecha_creacion` datetime DEFAULT current_timestamp(),
  `fecha_actualizacion` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `usuario_creo_uuid` char(36) DEFAULT NULL,
  `usuario_actualizo_uuid` char(36) DEFAULT NULL,
  PRIMARY KEY (`uuid_usuario`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `usuarios` VALUES
('734a1a2b-2027-11f1-9b2d-14ac60e52fb2','Administrador Sistema','admin@axis.com','hash_admin_123','Admin',0,1,'2026-03-14 22:28:43','2026-03-14 22:28:43',NULL,NULL),
('7350b23c-2027-11f1-9b2d-14ac60e52fb2','Jefe de Producción','produccion@axis.com','hash_prod_123','Producción',0,1,'2026-03-14 22:28:43','2026-03-14 22:28:43',NULL,NULL),
('73549fd6-2027-11f1-9b2d-14ac60e52fb2','Ventas Mostrador 1','ventas@axis.com','hash_ventas_123','Cliente',0,1,'2026-03-14 22:28:43','2026-03-14 22:28:43',NULL,NULL),
('73597601-2027-11f1-9b2d-14ac60e52fb2','Gerencia General','gerente@axis.com','hash_gerente_123','Gerente',0,1,'2026-03-14 22:28:43','2026-03-14 22:28:43',NULL,NULL);
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `ventas_detalle`
--

DROP TABLE IF EXISTS `ventas_detalle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `ventas_detalle` (
  `uuid_detalle` char(36) NOT NULL,
  `uuid_venta` char(36) NOT NULL,
  `uuid_producto` char(36) NOT NULL,
  `cantidad` int(11) NOT NULL,
  `precio_unitario_venta` decimal(12,2) NOT NULL,
  `fecha_creacion` datetime DEFAULT current_timestamp(),
  `fecha_actualizacion` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `usuario_creo_uuid` char(36) DEFAULT NULL,
  `usuario_actualizo_uuid` char(36) DEFAULT NULL,
  PRIMARY KEY (`uuid_detalle`),
  KEY `uuid_venta` (`uuid_venta`),
  KEY `uuid_producto` (`uuid_producto`),
  CONSTRAINT `1` FOREIGN KEY (`uuid_venta`) REFERENCES `ventas_encabezado` (`uuid_venta`),
  CONSTRAINT `2` FOREIGN KEY (`uuid_producto`) REFERENCES `productos_terminados` (`uuid_producto`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ventas_detalle`
--

LOCK TABLES `ventas_detalle` WRITE;
/*!40000 ALTER TABLE `ventas_detalle` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `ventas_detalle` VALUES
('73ea1b7e-2027-11f1-9b2d-14ac60e52fb2','73dad66f-2027-11f1-9b2d-14ac60e52fb2','73a24e16-2027-11f1-9b2d-14ac60e52fb2',2,450.00,'2026-03-14 22:28:44','2026-03-14 22:28:44',NULL,NULL),
('73ea255a-2027-11f1-9b2d-14ac60e52fb2','73df9866-2027-11f1-9b2d-14ac60e52fb2','73a24e16-2027-11f1-9b2d-14ac60e52fb2',2,450.00,'2026-03-14 22:28:44','2026-03-14 22:28:44',NULL,NULL),
('73ea278c-2027-11f1-9b2d-14ac60e52fb2','73df9866-2027-11f1-9b2d-14ac60e52fb2','73a7bc3a-2027-11f1-9b2d-14ac60e52fb2',1,320.00,'2026-03-14 22:28:44','2026-03-14 22:28:44',NULL,NULL);
/*!40000 ALTER TABLE `ventas_detalle` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `ventas_encabezado`
--

DROP TABLE IF EXISTS `ventas_encabezado`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `ventas_encabezado` (
  `uuid_venta` char(36) NOT NULL,
  `numero_ticket` varchar(25) NOT NULL,
  `uuid_vendedor` char(36) NOT NULL,
  `total_pago` decimal(12,2) NOT NULL,
  `metodo_pago` varchar(50) NOT NULL,
  `tipo_entrega` varchar(20) NOT NULL,
  `fecha_creacion` datetime DEFAULT current_timestamp(),
  `fecha_actualizacion` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `usuario_creo_uuid` char(36) DEFAULT NULL,
  `usuario_actualizo_uuid` char(36) DEFAULT NULL,
  PRIMARY KEY (`uuid_venta`),
  UNIQUE KEY `numero_ticket` (`numero_ticket`),
  KEY `uuid_vendedor` (`uuid_vendedor`),
  CONSTRAINT `1` FOREIGN KEY (`uuid_vendedor`) REFERENCES `usuarios` (`uuid_usuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ventas_encabezado`
--

LOCK TABLES `ventas_encabezado` WRITE;
/*!40000 ALTER TABLE `ventas_encabezado` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `ventas_encabezado` VALUES
('73dad66f-2027-11f1-9b2d-14ac60e52fb2','T-000001','73549fd6-2027-11f1-9b2d-14ac60e52fb2',900.00,'Efectivo','Mostrador','2026-03-14 22:28:44','2026-03-14 22:28:44',NULL,NULL),
('73df9866-2027-11f1-9b2d-14ac60e52fb2','T-000002','73549fd6-2027-11f1-9b2d-14ac60e52fb2',1220.00,'Tarjeta','Online','2026-03-14 22:28:44','2026-03-14 22:28:44',NULL,NULL);
/*!40000 ALTER TABLE `ventas_encabezado` ENABLE KEYS */;
UNLOCK TABLES;
commit;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*M!100616 SET NOTE_VERBOSITY=@OLD_NOTE_VERBOSITY */;

-- Dump completed on 2026-03-14 22:42:05
