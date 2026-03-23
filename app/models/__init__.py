# Import all models so SQLAlchemy registers them when db.create_all() is called.
from app.models.categorias import Categoria  # noqa: F401
from app.models.usuarios import Usuario  # noqa: F401
from app.models.clientes import Cliente  # noqa: F401
from app.models.proveedores import Proveedor  # noqa: F401
from app.models.insumos import Insumo  # noqa: F401
from app.models.compras import CompraEncabezado, CompraDetalle  # noqa: F401
from app.models.inventario import RolloInventario, RetazoInventario  # noqa: F401
from app.models.modelos_productos import ModeloRopa, ProductoTerminado  # noqa: F401
from app.models.explosion_materiales import ExplosionMaterialesCabecera, ExplosionMaterialesDetalle  # noqa: F401
from app.models.produccion import OrdenProduccion, EjecucionCorte  # noqa: F401
from app.models.ventas import VentaEncabezado, VentaDetalle  # noqa: F401
