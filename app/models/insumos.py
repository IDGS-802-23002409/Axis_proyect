import uuid
from app.utils.database_connection import db
from sqlalchemy import Column, String, Numeric, DateTime, ForeignKey, func, Enum, CheckConstraint

# ── ENUMS ────────────────────────────────────

# cómo se compra el insumo
unidad_compra_enum = Enum(
    'ROLLO',
    'PIEZA',
    name='unidad_compra_enum'
)

# unidad real de uso
unidad_base_enum = Enum(
    'METRO',
    'PIEZA',
    name='unidad_base_enum'
)

# estado del insumo
estatus_enum = Enum(
    'ACTIVO',
    'INACTIVO',
    name='estatus_insumo_enum'
)


class Insumo(db.Model):
    __tablename__ = 'insumos'

    # ── Constraints ───────────────────────────
    __table_args__ = (
        CheckConstraint('stock_total_acumulado >= 0', name='check_stock_insumo_positivo'),
    )

    # ── Identificador ─────────────────────────
    uuid_insumo = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    sku = Column(String(50), unique=True)
    nombre = Column(String(100), nullable=False)
    uuid_categoria = Column(String(36), ForeignKey('categorias.uuid_categoria'))

    # ── Configuración de unidades ─────────────

    # cómo se compra
    unidad_medida = Column(unidad_compra_enum, nullable=False)

    # contenido por unidad de compra
    contenido_cantidad = Column(Numeric(12, 4), nullable=False)

    # unidad base
    contenido_unidad_medida = Column(unidad_base_enum, nullable=False)

    # ── Inventario ────────────────────────────

    stock_total_acumulado = Column(Numeric(12, 4), default=0)
    stock_minimo_alerta = Column(Numeric(12, 4), default=0)

    # ancho para rollos
    ancho = Column(Numeric(5, 2), nullable=True)

    fecha_creacion = Column(DateTime, server_default=func.now())
    fecha_actualizacion = Column(DateTime, server_default=func.now(), onupdate=func.now())

    estatus = Column(estatus_enum, default='ACTIVO')
    usuario_actualizo_uuid = Column(String(36))

    # ── Relaciones ────────────────────────────
    categoria = db.relationship('Categoria', backref=db.backref('insumos', lazy=True))

    def __repr__(self):
        return f'<Insumo {self.nombre}>'