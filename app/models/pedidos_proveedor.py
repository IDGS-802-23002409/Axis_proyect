import uuid
from app.utils.database_connection import db
from sqlalchemy import Column, String, Numeric, DateTime, Enum, ForeignKey, func

class PedidoProveedorEncabezado(db.Model):
    __tablename__ = 'pedidos_proveedor_encabezado'

    uuid_pedido = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    folio_pedido = Column(String(50), unique=True, nullable=False)
    uuid_proveedor = Column(String(36), ForeignKey('proveedores.uuid_proveedor'), nullable=False)
    uuid_usuario_solicita = Column(String(36), ForeignKey('usuarios.uuid_usuario'), nullable=False)
    fecha_pedido = Column(DateTime, server_default=func.now())
    fecha_actualizacion = Column(DateTime, server_default=func.now(), onupdate=func.now())
    estatus = Column(Enum('Pendiente', 'Aprobado', 'Parcial', 'Completado', 'Cancelado', name='estatus_pedido_enum'), default='Pendiente')

    proveedor = db.relationship('Proveedor', backref=db.backref('pedidos', lazy=True))
    usuario_solicita = db.relationship('Usuario', backref=db.backref('pedidos_solicitados', lazy=True))

    def __repr__(self):
        return f'<PedidoProveedor {self.folio_pedido}>'


class PedidoProveedorDetalle(db.Model):
    __tablename__ = 'pedidos_proveedor_detalle'

    uuid_detalle_pedido = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    uuid_pedido = Column(String(36), ForeignKey('pedidos_proveedor_encabezado.uuid_pedido'), nullable=False)
    uuid_insumo = Column(String(36), ForeignKey('insumos.uuid_insumo'), nullable=False)
    cantidad_pedida = Column(Numeric(12, 4), nullable=False)
    cantidad_recibida = Column(Numeric(12, 4), default=0)
    costo_unitario_estimado = Column(Numeric(12, 2))
    fecha_creacion = Column(DateTime, server_default=func.now())
    fecha_actualizacion = Column(DateTime, server_default=func.now(), onupdate=func.now())

    pedido = db.relationship('PedidoProveedorEncabezado', backref=db.backref('detalles', lazy=True))
    insumo = db.relationship('Insumo', backref=db.backref('pedidos_detalle', lazy=True))

    def __repr__(self):
        return f'<PedidoProveedorDetalle {self.uuid_detalle_pedido}>'
