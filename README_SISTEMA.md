# Documentación del Sistema: Roles y Respaldos - Axis Proyect

Este documento detalla el funcionamiento técnico, archivos involucrados y flujos de los sistemas de control de acceso (roles) y gestión de respaldos.

---

## 1. Sistema de Roles (RBAC & Database Segregation)

El sistema de roles está diseñado con una arquitectura de "Múltiples Capas de Aplicación", lo que permite que las restricciones no solo vivan en el código, sino que se hereden directamente a la base de datos MySQL.

### Archivos Involucrados
- **`app/database/01_crear_roles.sql`**: Define los roles de base de datos (`admin_rol`, `gerente_rol`, etc.) y sus permisos específicos (GRANT/REVOKE).
- **`app/models/usuarios.py`**: Contiene los modelos `Usuario` y `Role` utilizados por Flask-Security.
- **`app/utils/database_connection.py`**: Gestiona la creación de motores de base de datos específicos por rol.
- **`app/app.py`**: Configura los `SQLALCHEMY_BINDS` y el middleware que cambia la conexión dinámicamente.

### Flujo de Implementación
1. **Autenticación (Flask-Security)**: El usuario inicia sesión y se cargan sus roles de aplicación desde la tabla `roles_usuarios`.
2. **Mapeo de Rol (`before_request`)**: En cada petición, el middleware `set_db_role_g` identifica el rol del usuario actual y lo asigna al objeto global `g.db_role`.
3. **Segregación de Base de Datos**: El middleware `set_db_bind` detecta el rol en `g` y cambia el "bind" (la conexión activa) de `db.session` al motor configurado con sus credenciales específicas:
   - **Admin**: Acceso total.
   - **Gerente**: Acceso total excepto `DROP`.
   - **Producción**: Acceso a lectura/escritura pero no eliminación.
   - **Cliente**: Acceso limitado a lectura y ejecución de procedimientos específicos.

### Roles de Base de Datos (MySQL)
| Rol | Usuario de BD | Permisos Principales |
| :--- | :--- | :--- |
| `admin_rol` | `admin_db_user` | `ALL PRIVILEGES` en `flask_db` y `staging`. |
| `gerente_rol` | `gerente_db_user` | `SELECT, INSERT, UPDATE, DELETE`. No puede usar `DROP`. |
| `produccion_rol`| `produccion_db_user` | `SELECT, INSERT, UPDATE`. No puede eliminar registros. |
| `cliente_rol` | `cliente_db_user` | `SELECT, INSERT, EXECUTE`. Restringido a catálogo y pedidos. |
| `backup_rol` | `backup_db_user` | Permisos globales de lectura y gestión de tablas para respaldos. |

---

## 2. Sistema de Respaldos (Backups & Restores)

El sistema de respaldos utiliza una metodología de **Restauración Incremental Conservadora**, lo que garantiza que la recuperación de datos nunca borre información nueva que ya exista en producción.

### Archivos Involucrados
- **`app/blueprints/respaldos/routes.py`**: Define las rutas web para generar, descargar y restaurar respaldos.
- **`app/utils/backup_commands.py`**: Contiene la lógica central de sincronización `sync_databases`.
- **`app/templates/produccion/respaldos.html`**: Interfaz de usuario para la administración.
- **`respaldos/`**: Directorio raíz donde se almacenan los archivos `.sql` generados.

### Flujo de Trabajo (Workflows)

#### Generación de Respaldo
1. El usuario administrador solicita un respaldo desde la interfaz.
2. El sistema ejecuta un comando `mysqldump` utilizando el usuario `backup_db_user`.
3. Se genera un archivo `.sql` con marca de tiempo en la carpeta `/respaldos`.

#### Restauración Incremental (Paso a Paso)
Este es el proceso más crítico y seguro del sistema:
1. **Carga en Staging**: El archivo `.sql` seleccionado se restaura primero en una base de datos secundaria llamada `flask_db_staging`. Esto permite analizar los datos sin afectar la base de datos viva.
2. **Sincronización de Datos**: El sistema compara tabla por tabla entre `Staging` y `Producción`.
3. **Lógica Conservadora**:
   - Si un registro existe en Staging pero NO en Producción, se **INSERTA** (recupera datos borrados).
   - Si un registro existe en ambos, se **ACTUALIZA** solo si el de Staging es más reciente (comparando `fecha_actualizacion`).
   - **CRÍTICO**: El sistema **NUNCA ejecuta DELETE** en Producción durante una restauración. Los datos creados después del respaldo se conservan intactos.

### Características de Seguridad
- **Usuario Aislado**: Los respaldos se realizan con `backup_db_user`, que tiene permisos de `LOCK TABLES` y `PROCESS` pero está limitado a las bases de datos de la aplicación.
- **Staging Isolation**: El uso de una BD intermedia evita errores de sintaxis o corrupción directa en la base de datos principal durante el proceso de recuperación.
- **Audit Logs**: Cada operación de respaldo y restauración queda registrada en los logs del sistema (`backup_axis`).
