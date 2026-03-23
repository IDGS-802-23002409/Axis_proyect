# Axis ERP

ERP para una empresa de ropa llamada **Axis**. Administra insumos, producción, inventario de rollos, explosión de materiales y venta al público general.

Stack: **Flask 3 · SQLAlchemy 2 · Flask-Migrate (Alembic) · MySQL 8 · Docker**

---

## Requisitos previos

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado y corriendo
- (Opcional para desarrollo local) Python 3.12+

---

## 1. Configuración inicial

Copia el archivo de ejemplo y llena tus variables:

```bash
cp example.env .env
```

El `.env` ya viene con los valores que coinciden con `docker-compose.yml`:

```env
DB_HOST=mysql
DB_PORT=3306
DB_NAME=flask_db
DB_USER=flask_user
DB_PASSWORD=flask_password
FLASK_ENV=development
SECRET_KEY=change_this_secret_key_in_production
```

---

## 2. Levantar el entorno

```bash
# Primera vez (o cuando cambies requirements.txt / Dockerfile)
docker-compose up --build

# Veces posteriores
docker-compose up
```

Servicios disponibles:

| Servicio    | URL                        |
|-------------|----------------------------|
| Flask API   | http://localhost:3030      |
| phpMyAdmin  | http://localhost:8080      |
| MySQL       | localhost:3331             |

Para detener:

```bash
docker-compose down
```

Para detener **y borrar la base de datos** (volumen):

```bash
docker-compose down -v
```

---

## 3. Migraciones de base de datos (Flask-Migrate)

Todos los comandos se ejecutan **dentro del contenedor Flask** con `docker exec`.

### Primera vez en el proyecto (solo se hace una vez)

```bash
docker exec -it flask_app flask db init
```

Esto crea la carpeta `migrations/` en la raíz del proyecto. **Commitea esta carpeta** al repositorio.

### Crear tablas iniciales (primer migrate)

```bash
docker exec -it flask_app flask db migrate -m "initial schema"
docker exec -it flask_app flask db upgrade
```

### Después de modificar un modelo

1. Edita el archivo de modelo en `app/models/`
2. Genera el script de migración:

```bash
docker exec -it flask_app flask db migrate -m "describe el cambio"
```

3. Aplica el cambio a la base de datos:

```bash
docker exec -it flask_app flask db upgrade
```

### Revertir la última migración

```bash
docker exec -it flask_app flask db downgrade
```

### Ver el historial de migraciones

```bash
docker exec -it flask_app flask db history
docker exec -it flask_app flask db current
```

---

## 4. Estructura del proyecto

```
Axis_proyect/
│
├── app/
│   ├── __init__.py
│   ├── app.py                  # Factory create_app() + Migrate init
│   ├── blueprints/             # Blueprints por módulo (Auth, Ventas, etc.)
│   ├── models/                 # Modelos SQLAlchemy (uno por módulo)
│   │   ├── __init__.py         # Importa todos los modelos
│   │   ├── categorias.py
│   │   ├── usuarios.py
│   │   ├── clientes.py
│   │   ├── proveedores.py
│   │   ├── insumos.py
│   │   ├── compras.py
│   │   ├── inventario.py
│   │   ├── modelos_productos.py
│   │   ├── explosion_materiales.py
│   │   ├── produccion.py
│   │   └── ventas.py
│   ├── static/
│   └── templates/
│       └── utils/
│           ├── config.py           # Lee variables del .env
│           └── database_connection.py  # Instancia de SQLAlchemy (db)
│
├── migrations/                 # Generado por `flask db init` (committear)
├── database/
│   └── snapshots/              # Backups manuales de la BD
│
├── main.py                     # Punto de entrada
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env                        # Variables locales (NO committear)
└── example.env                 # Plantilla del .env (sí committear)
```

---

## 6. Desarrollo local (sin Docker)

Si prefieres correr Flask directamente en tu máquina (requiere MySQL accesible):

```bash
pip install -r requirements.txt
# Ajusta DB_HOST=localhost en tu .env
python main.py
```

---

## 7. Variables de entorno

| Variable      | Descripción                              | Default (docker)  |
|---------------|------------------------------------------|-------------------|
| `DB_HOST`     | Host de MySQL                            | `mysql`           |
| `DB_PORT`     | Puerto de MySQL                          | `3306`            |
| `DB_NAME`     | Nombre de la base de datos               | `flask_db`        |
| `DB_USER`     | Usuario de MySQL                         | `flask_user`      |
| `DB_PASSWORD` | Contraseña de MySQL                      | `flask_password`  |
| `FLASK_ENV`   | `development` o `production`             | `development`     |
| `SECRET_KEY`  | Clave secreta para sesiones y tokens     | *(cambiar)*       |
