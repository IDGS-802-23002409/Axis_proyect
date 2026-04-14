import uuid
from app.utils.database_connection import db
from sqlalchemy import Column, String, Integer, Numeric, DateTime, Enum, ForeignKey, func, Index

class PedidoClienteEncabezado(db.Model):
    __tablename__ = 'pedidos_cliente_encabezado'

    uuid_pedido = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    numero_pedido = Column(String(25), unique=True, nullable=False)
    uuid_cliente = Column(String(36), ForeignKey('clientes.uuid_cliente'), nullable=False)
    uuid_venta_origen = Column(String(36), ForeignKey('ventas_encabezado.uuid_venta'), nullable=True)
    estatus = Column(Enum('Pendiente', 'Producción', 'Listo', 'Entregado', 'Cancelado'), default='Pendiente')
    fecha_pedido = Column(DateTime, server_default=func.now())
    fecha_actualizacion = Column(DateTime, server_default=func.now(), onupdate=func.now())

    cliente = db.relationship('Cliente', backref=db.backref('pedidos_cliente', lazy=True))
    venta_origen = db.relationship('VentaEncabezado', backref=db.backref('pedidos_vinculados', lazy=True))

    __table_args__ = (
        Index('idx_pedido_fecha', 'fecha_pedido'),
        Index('idx_pedido_estatus', 'estatus'),
    )

    def __repr__(self):
        return f'<PedidoClienteEncabezado {self.numero_pedido}>'


class PedidoClienteDetalle(db.Model):
    __tablename__ = 'pedidos_cliente_detalle'

    uuid_detalle_pedido = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    uuid_pedido = Column(String(36), ForeignKey('pedidos_cliente_encabezado.uuid_pedido'), nullable=False)
    uuid_producto = Column(String(36), ForeignKey('productos_terminados.uuid_producto'), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_unitario_historico = Column(Numeric(12, 2), nullable=False)
    estatus_item = Column(Enum('Pendiente', 'En Producción', 'Terminado'), default='Pendiente')
    fecha_creacion = Column(DateTime, server_default=func.now())
    fecha_actualizacion = Column(DateTime, server_default=func.now(), onupdate=func.now())

    pedido = db.relationship('PedidoClienteEncabezado', backref=db.backref('detalles', lazy=True, cascade="all, delete-orphan"))
    producto = db.relationship('ProductoTerminado', backref=db.backref('pedidos_detalle', lazy=True))

    def __repr__(self):
        return f'<PedidoClienteDetalle {self.uuid_detalle_pedido}>'
