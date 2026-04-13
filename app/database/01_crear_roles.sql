-- Script de Creación de Roles (Versión de Emergencia - Esquema Completo)
-- Autor: Cesar Damian Benal Cruz
-- Fecha: 2026-04-13

-- 1. Crear los roles si no existen
CREATE ROLE IF NOT EXISTS 'admin_rol';
CREATE ROLE IF NOT EXISTS 'gerente_rol';
CREATE ROLE IF NOT EXISTS 'produccion_rol';
CREATE ROLE IF NOT EXISTS 'cliente_rol';
CREATE ROLE IF NOT EXISTS 'respaldo_rol';

-- 2. Asignación de Privilegios

-- ADMIN: Todo (Root a nivel aplicación)
GRANT ALL PRIVILEGES ON flask_db.* TO 'admin_rol';
GRANT 'admin_rol' TO 'flask_user'@'%';

-- GERENTE: Gestión casi total (Sin DROP)
GRANT SELECT, INSERT, UPDATE, DELETE, EXECUTE ON flask_db.* TO 'gerente_rol';
REVOKE DROP ON flask_db.* FROM 'gerente_rol';

-- PRODUCCION: Permisos operativos
GRANT SELECT, INSERT, UPDATE, EXECUTE ON flask_db.* TO 'produccion_rol';

-- CLIENTE: Permisos básicos de consulta e inserción (ventas)
GRANT SELECT, INSERT, EXECUTE ON flask_db.* TO 'cliente_rol';

-- RESPALDO: Rol dedicado para backup y restauración
-- Permisos para backup (mysqldump)
GRANT SELECT, LOCK TABLES, SHOW VIEW, TRIGGER ON flask_db.* TO 'respaldo_rol';
-- Permisos para restauración (mysql < backup.sql)
GRANT INSERT, UPDATE, DELETE, CREATE, DROP, REFERENCES, INDEX, ALTER, CREATE VIEW, SHOW VIEW, TRIGGER, EVENT ON flask_db.* TO 'respaldo_rol';

-- 3. Crear usuario dedicado de backup
CREATE USER IF NOT EXISTS 'backup_user'@'%' IDENTIFIED BY 'backup_password';
GRANT 'respaldo_rol' TO 'backup_user'@'%';
SET DEFAULT ROLE 'respaldo_rol' TO 'backup_user'@'%';

-- 4. Permitir que flask_user asuma los roles operativos
GRANT 'gerente_rol', 'produccion_rol', 'cliente_rol', 'admin_rol' TO 'flask_user'@'%';

-- Permisos básicos para que flask_user pueda autenticar (SELECT en tablas de usuarios/roles)
GRANT SELECT ON flask_db.usuarios TO 'flask_user'@'%';
GRANT SELECT ON flask_db.role TO 'flask_user'@'%';
GRANT SELECT ON flask_db.roles_usuarios TO 'flask_user'@'%';

-- Establecer cliente_rol como rol por defecto para que la aplicación pueda iniciar
-- (leer esquemas, procedimientos, etc.) sin crashear.
-- Al iniciar sesión, el app cambiará al rol específico usando SET ROLE.
ALTER USER 'flask_user'@'%' DEFAULT ROLE 'cliente_rol';

FLUSH PRIVILEGES;
