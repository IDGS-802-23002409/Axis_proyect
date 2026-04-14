-- Script de Creación de Roles y Usuarios (Versión Final de Segregación)
-- Autor: Axis Team
-- Fecha: 2026-04-14

-- 1. Crear los roles si no existen
CREATE ROLE IF NOT EXISTS 'admin_rol';
CREATE ROLE IF NOT EXISTS 'gerente_rol';
CREATE ROLE IF NOT EXISTS 'produccion_rol';
CREATE ROLE IF NOT EXISTS 'cliente_rol';
CREATE ROLE IF NOT EXISTS 'backup_rol';

-- 2. Privilegios de Roles
GRANT ALL PRIVILEGES ON flask_db.* TO 'admin_rol';
GRANT SELECT, INSERT, UPDATE, DELETE, EXECUTE ON flask_db.* TO 'gerente_rol';
REVOKE DROP ON flask_db.* FROM 'gerente_rol';
GRANT SELECT, INSERT, UPDATE, EXECUTE ON flask_db.* TO 'produccion_rol';
GRANT SELECT, INSERT, EXECUTE ON flask_db.* TO 'cliente_rol';
GRANT SELECT, LOCK TABLES, SHOW VIEW, EVENT, TRIGGER, PROCESS ON *.* TO 'backup_rol';
GRANT INSERT, UPDATE, DELETE, CREATE, DROP, ALTER, INDEX, REFERENCES ON flask_db.* TO 'backup_rol';
GRANT INSERT, UPDATE, DELETE, CREATE, DROP, ALTER, INDEX, REFERENCES ON flask_db_staging.* TO 'backup_rol';
GRANT ALL PRIVILEGES ON flask_db_staging.* TO 'admin_rol';
CREATE DATABASE IF NOT EXISTS flask_db_staging;

-- 3. Usuarios de BD específicos
-- Nota: Las contraseñas se sincronizan con el .env
CREATE USER IF NOT EXISTS 'admin_db_user'@'%' IDENTIFIED BY 'admin_password';
CREATE USER IF NOT EXISTS 'gerente_db_user'@'%' IDENTIFIED BY 'gerente_password';
CREATE USER IF NOT EXISTS 'produccion_db_user'@'%' IDENTIFIED BY 'produccion_password';
CREATE USER IF NOT EXISTS 'cliente_db_user'@'%' IDENTIFIED BY 'cliente_password';
CREATE USER IF NOT EXISTS 'backup_db_user'@'%' IDENTIFIED BY 'backup_password';

-- El usuario base (flask_user) DEBE tener permisos totales para la inicialización (CREATE/DROP tables/SPs)
GRANT ALL PRIVILEGES ON flask_db.* TO 'flask_user'@'%';

-- 4. Asignar roles a los usuarios
GRANT 'admin_rol' TO 'admin_db_user'@'%';
GRANT 'gerente_rol' TO 'gerente_db_user'@'%';
GRANT 'produccion_rol' TO 'produccion_db_user'@'%';
GRANT 'cliente_rol' TO 'cliente_db_user'@'%';
GRANT 'backup_rol' TO 'backup_db_user'@'%';

-- 5. Activar roles por defecto para todos
SET DEFAULT ROLE ALL TO 
    'admin_db_user'@'%', 
    'gerente_db_user'@'%', 
    'produccion_db_user'@'%', 
    'cliente_db_user'@'%', 
    'backup_db_user'@'%';

FLUSH PRIVILEGES;
