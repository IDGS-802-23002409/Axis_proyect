-- Script de Creación de Roles (Versión de Emergencia - Esquema Completo)
-- Autor: Cesar Damian Benal Cruz
-- Fecha: 2026-04-13

-- 1. Crear los roles si no existen
CREATE ROLE IF NOT EXISTS 'admin_rol';
CREATE ROLE IF NOT EXISTS 'gerente_rol';
CREATE ROLE IF NOT EXISTS 'produccion_rol';
CREATE ROLE IF NOT EXISTS 'cliente_rol';

-- ADMIN: Todo
GRANT ALL PRIVILEGES ON flask_db.* TO 'admin_rol';

-- GERENTE: Gestión casi total (Sin DROP)
GRANT SELECT, INSERT, UPDATE, DELETE, EXECUTE ON flask_db.* TO 'gerente_rol';
REVOKE DROP ON flask_db.* FROM 'gerente_rol';

-- PRODUCCION: Permisos sobre todo el esquema para permitir que el app cree tablas si es necesario
-- (Luego se puede restringir a tablas específicas una vez que existan)
GRANT SELECT, INSERT, UPDATE, EXECUTE ON flask_db.* TO 'produccion_rol';

-- CLIENTE: Permisos básicos de consulta e inserción (ventas)
GRANT SELECT, INSERT, EXECUTE ON flask_db.* TO 'cliente_rol';

-- 3. Permitir que flask_user asuma roles
GRANT 'admin_rol', 'gerente_rol', 'produccion_rol', 'cliente_rol' TO 'flask_user'@'%';

-- Activar todos los roles por defecto para que flask_user mantenga sus permisos 
-- y el app pueda limitar el acceso según la sesión usando SET ROLE.
SET DEFAULT ROLE ALL TO 'flask_user'@'%';

FLUSH PRIVILEGES;
