import uuid
from app.utils.database_connection import db
from sqlalchemy import Column, String, Integer, Numeric, DateTime, Enum, ForeignKey, func


class VentaEncabezado(db.Model):
    __tablename__ = 'ventas_encabezado'

    uuid_venta = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    numero_pedido = Column(String(25), unique=True, nullable=False)
    uuid_cliente = Column(String(36), ForeignKey('clientes.uuid_cliente'), nullable=False)
    metodo_pago = Column(String(50))
    estatus_envio = Column(Enum('Procesando', 'Enviado', 'Entregado', 'Devuelto'), default='Procesando')
    fecha_venta = Column(DateTime, server_default=func.now())
    fecha_actualizacion = Column(DateTime, server_default=func.now(), onupdate=func.now())

    cliente = db.relationship('Cliente', backref=db.backref('ventas', lazy=True))

    def __repr__(self):
        return f'<VentaEncabezado {self.numero_pedido}>'


class VentaDetalle(db.Model):
    __tablename__ = 'ventas_detalle'

    uuid_detalle = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    uuid_venta = Column(String(36), ForeignKey('ventas_encabezado.uuid_venta'), nullable=False)
    uuid_producto = Column(String(36), ForeignKey('productos_terminados.uuid_producto'), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_unitario_historico = Column(Numeric(12, 2), nullable=False)

    venta = db.relationship('VentaEncabezado', backref=db.backref('detalles', lazy=True))
    producto = db.relationship('ProductoTerminado', backref=db.backref('ventas_detalle', lazy=True))

    def __repr__(self):
        return f'<VentaDetalle {self.uuid_detalle}>'
