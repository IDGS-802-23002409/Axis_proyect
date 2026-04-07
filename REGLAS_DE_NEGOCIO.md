---

## 1. Descripción del Sistema
Sistema web integral para la administración de un taller de confección. Gestiona el ciclo completo desde el abastecimiento de insumos hasta la venta final, controlando inventarios, órdenes de producción por talla/modelo y mermas. Destaca por su capacidad de calcular la **utilidad real** mediante el costo histórico de insumos y consumos reales.

---

## 2. Reglas de Negocio

### Proceso de Ventas
* **Requisitos de Cliente:** Para finalizar una compra, es obligatorio iniciar sesión. Si el cliente no tiene dirección o teléfono registrados, el sistema solicitará estos datos antes del pago para evitar "compras fantasma".
* **Gestión de Stock y Tiempos:**
    * Si hay stock: Envío habitual.
    * Si **no** hay stock: La compra procede, pero se añaden **5 días adicionales** al tiempo de entrega para preparación.
* **Restricciones:** El carrito tiene un límite máximo de **100 productos totales**.
* **Política de Inventario "Express":** Si un pedido supera el stock disponible (ej. pedido de 80, stock de 40), el sistema **no toma las prendas existentes**. Crea una orden de producción desde cero para preservar el stock para ventas pequeñas (menos de 10 artículos) y mantener el stock mínimo.

### Proceso de Compras y Abastecimiento
* **Flujo de Insumos:** Solo se abastece mediante pedidos formales al proveedor. El estatus cambia de *Pendiente* a *Recibido* tras la validación física.
* **Política de Recepción:** No se aceptará ningún material que no coincida exactamente con lo solicitado (productos extra, unidades o cantidades distintas).
* **Unidades de Medida:**
    * **Insumos generales:** Se manejan exclusivamente por piezas.
    * **Telas:** Se compran por rollo (cada rollo es una unidad en el sistema). El metraje debe ser exacto (tolerancia de **5 cm**); de lo contrario, el rollo es rechazado.

### Roles y Control de Acceso
| Rol | Permisos |
| :--- | :--- |
| **Admin** | Acceso total al sistema. |
| **Gerente** | Acceso total, excepto al módulo de Usuarios. |
| **Producción** | Acceso a Órdenes de Producción, Stocks, Inventario, Recetas y Modelos. |
| **Cliente** | Rol restringido únicamente para realizar compras. |

* **Registro de Personal:** Los empleados de producción no pueden registrarse públicamente. Deben ser creados por un Admin en el módulo 'Usuarios' y posteriormente asignados en la gestión de empleados.

### Levantamiento y Atención de Pedidos
* **Generación de Pedidos:** Al comprar, si hay stock suficiente, el pedido se marca como **Completado**.
* **Derivación a Producción:** Si el stock es insuficiente, el pedido queda como **Pendiente** y se envía automáticamente al área de producción para su fabricación.

### Registro y Atención de Órdenes de Producción
* **Explosión de Materiales (Recetas):** Es obligatorio tener una receta para crear una orden. Las recetas se manejan por **lotes** (ej. una receta de 1 lote produce 10 unidades).
* **Reserva de Materiales:** El sistema valida y descuenta el inventario desde el inicio de la orden para evitar sobreuso.
* **Gestión de Insumos según Tipo:**
    * **Tipo Pieza:** Descuento directo del stock total.
    * **Tipo Rollo (Tela):** Se asigna el metraje exacto según receta. El consumo excedente se registra como **merma de corte**.
* **Flujo de Estados:** Pendiente $\rightarrow$ En Corte $\rightarrow$ Confección $\rightarrow$ Terminado. La actualización de estados es **manual**, responsabilidad del encargado de producción.

### Cálculo de Costo y Utilidad
El sistema utiliza el costo real y mermas históricas para determinar la rentabilidad.

#### Fórmulas de Costeo
1.  **Costo Promedio de Insumos:**
    $$costo\_promedio = \frac{\sum (cantidad \times costo\_unitario)}{\sum (unidades\_base\_compradas)}$$
    *(Basado en las últimas 5 compras)*.

2.  **Cálculo de Consumo Real (Ajustado por Merma):**
    * Insumos METRO: $consumo\_real = consumo\_teorico \times (1 + merma\_tela)$
    * Insumos PIEZA: $consumo\_real = consumo\_teorico \times (1 + merma\_pieza)$

3.  **Utilidad y Precio:**
    * **Utilidad %:** $\frac{precio\_actual - costo\_mp}{costo\_mp} \times 100$
    * **Precio Ajustado:** $costo\_mp \times (1 + \frac{margen}{100})$

---



---

### Cancelaciones y Mermas
* **Ventas:** No hay devoluciones. El cliente solo puede cancelar si el estatus es *Pendiente*. Si se cancela, el producto se termina de fabricar y se integra al stock.
* **Mermas (Insumos Pieza):** Se calcula como $cantidad\_real - cantidad\_teorica$. Si es positiva, el stock se ajusta automáticamente ($stock = stock - merma$).
* **Retazos (Insumos Metro):** Los fragmentos de tela se descuentan del rollo y del stock general. Si el retazo es defectuoso, se suma a la `merma_real_calculada`.
* **Restricción de Seguridad:** No se pueden eliminar registros de mermas o retazos si la orden de producción ya está en estado **Terminado**.