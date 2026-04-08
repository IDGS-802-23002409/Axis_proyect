## 1. Módulos de Gestión (CRUD)
El sistema debe permitir las operaciones básicas de creación, lectura, actualización y borrado para los siguientes catálogos esenciales:

* **Producto:** Bienes finales destinados a la venta.
* **Insumo / Materia Prima:** Elementos base para la producción.
* **Proveedores:** Entidades que abastecen los insumos.
* **Clientes:** Destinatarios finales de los productos.
* **Empleados:** Personal que opera el sistema y los procesos.
* **Explosión de Insumos (Recetas):** Relación técnica que define qué insumos y en qué cantidad componen cada producto.

---

## 2. Operativa y Transaccionalidad
La lógica de negocio debe garantizar la integridad de los datos en los siguientes procesos:

### A. Ventas y Pedidos
* **Venta de Producto:** Salida de inventario de productos existentes.
* **Levantamiento de Pedidos de Clientes:** * Debe permitir la **reserva** de producto terminado.
    * En caso de no haber stock, debe disparar la **Generación de una Orden de Producción**.

### B. Abastecimiento y Compras
* **Compras:** Registro de entrada de insumos.
* **Conversión de Unidades:** Manejo de equivalencias entre presentaciones de compra y unidades de uso (ej. comprar por bulto, usar por gramo).
* **Gestión de Pedidos a Proveedor:** * Relacionar compras con pedidos previos.
    * Verificación de discrepancias entre lo solicitado y lo realmente abastecido.

### C. Producción
* **Órdenes de Producción:** Seguimiento detallado mediante estatus (ej. *Pendiente*, *En preparación*, *Terminado*, etc.).

---

## 3. Tareas Administrativas y de Gestión
Implementaciones técnicas a nivel de base de datos y sistema:

### Seguridad y Disponibilidad
* **Manejo de Sesiones:** Control de acceso mediante **Roles de BD**. La conexión desde la aplicación debe reflejar el usuario/rol que está operando.
* **Respaldos (Backup):** Capacidad de realizar copias de seguridad (preferentemente integradas en la interfaz del sistema).
* **Restauración (Recovery):** Capacidad de recuperar la base de datos a partir de un respaldo.

### Optimización e Integridad
* **Índices:** Aplicación estratégica para mejorar el rendimiento de las consultas frecuentes.
* **Integridad Referencial y ACID:** Uso estricto de transacciones para asegurar que las operaciones se completen correctamente o se reviertan ante fallos.
* **Manejo de Errores:** Control de excepciones (ej. alertas por existencia insuficiente de insumos o productos).
* **Mermas:** Registro de pérdida de inventario (insumos o productos).

---

## 4. Dashboard e Indicadores (KPIs)
Visualización de datos críticos para la toma de decisiones:

| Indicador | Descripción / Alcance |
| :--- | :--- |
| **Producto más vendido** | Por unidades y por monto total (Filtros: semanal y mensual). |
| **Costo y Utilidad** | Cálculo basado en el precio de venta vs. costo promedio de insumos del último mes. |
| **Reportes** | Generación y exportación de documentos con datos relevantes para la gerencia. |

---

### Notas de Implementación Sugeridas
> [!IMPORTANT]
> Recuerden que para el cumplimiento de **ACID**, es vital el uso de `BEGIN TRANSACTION`, `COMMIT` y `ROLLBACK` en sus procedimientos almacenados, especialmente en los módulos de ventas y explosión de insumos.