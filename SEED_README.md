# Script de Seeding de Datos

Este script `seed.py` genera datos de prueba para la base de datos del proyecto Axis.

## Requisitos

- Docker y Docker Compose instalados y ejecutándose.
- La base de datos MySQL corriendo en Docker (puerto 3331 en host).
- Dependencias instaladas: `pip install -r requirements.txt`

## Uso

1. Asegúrate de que los contenedores de Docker estén corriendo:
   ```bash
   docker-compose up -d
   ```

2. Ejecuta el script:
   ```bash
   python seed.py
   ```

## Descripción

El script crea al menos 10 registros por tabla/modelo, usando datos generados con Faker para simular información realista.

- **Roles**: Admin, Cliente, Producción
- **Usuarios**: 15 usuarios con roles asignados
- **Clientes**: Asociados a usuarios clientes
- **Categorías**: 10 categorías de ropa
- **Proveedores**: 10 proveedores
- **Insumos**: 15 insumos con SKUs
- **Modelos de Ropa**: 12 modelos
- **Productos Terminados**: Múltiples productos por modelo con tallas
- **Explosión de Materiales**: Detalles de materiales para productos
- **Compras**: 10 compras con detalles
- **Inventario**: Rollos de inventario
- **Producción**: Órdenes y ejecuciones de corte
- **Ventas**: 10 ventas con detalles

Todas las relaciones de clave foránea se respetan.

## Notas

- Las contraseñas de usuarios son 'password123' (hasheadas).
- Algunos campos opcionales pueden estar vacíos.
- Ejecuta solo en entornos de desarrollo/prueba.