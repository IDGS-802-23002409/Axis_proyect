import uuid
from app.utils.database_connection import db
from sqlalchemy import Column, String, Numeric, DateTime, Enum, ForeignKey, func, Index

# ── ENUM ─────────────────────────────────────
estatus_compra_enum = Enum(
    'PENDIENTE',
    'RECIBIDO',
    'CANCELADO',
    name='estatus_compra_enum'
)


class CompraEncabezado(db.Model):
    __tablename__ = 'compras_encabezado'

    uuid_compra = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    folio_factura = Column(String(50))
    uuid_proveedor = Column(String(36), ForeignKey('proveedores.uuid_proveedor'), nullable=False)
    uuid_usuario_registro = Column(String(36), ForeignKey('usuarios.uuid_usuario'), nullable=False)
    
    # vínculo con pedido
    uuid_pedido = Column(String(36), ForeignKey('pedidos_proveedor_encabezado.uuid_pedido'), nullable=True)
    
    fecha_compra = Column(DateTime, server_default=func.now())

    # estado de la compra
    estatus = Column(estatus_compra_enum, default='PENDIENTE')

    # relaciones
    proveedor = db.relationship('Proveedor', backref=db.backref('compras', lazy=True))
    usuario_registro = db.relationship('Usuario', backref=db.backref('compras_registradas', lazy=True))
    pedido = db.relationship('PedidoProveedorEncabezado', backref=db.backref('compras', lazy=True))

    # índice para optimizar consultas
    __table_args__ = (
        Index('idx_compra_fecha', 'fecha_compra'),
    )

    def __repr__(self):
        return f'<CompraEncabezado {self.uuid_compra}>'


class CompraDetalle(db.Model):
    __tablename__ = 'compras_detalle'

    uuid_detalle_compra = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    uuid_compra = Column(String(36), ForeignKey('compras_encabezado.uuid_compra'), nullable=False)
    uuid_insumo = Column(String(36), ForeignKey('insumos.uuid_insumo'), nullable=False)

    # datos de compra
    cantidad_comprada = Column(Numeric(12, 4), nullable=False)
    costo_unitario_compra = Column(Numeric(12, 2), nullable=False)

    # relaciones
    compra = db.relationship('CompraEncabezado', backref=db.backref('detalles', lazy=True))
    insumo = db.relationship('Insumo', backref=db.backref('compras_detalle', lazy=True))

    def __repr__(self):
        return f'<CompraDetalle {self.uuid_detalle_compra}>'