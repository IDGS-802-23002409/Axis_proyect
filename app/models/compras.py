import uuid
from app.utils.database_connection import db
from sqlalchemy import Column, String, Numeric, DateTime, Enum, ForeignKey, func


class CompraEncabezado(db.Model):
    __tablename__ = 'compras_encabezado'

    uuid_compra = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    folio_factura = Column(String(50))
    uuid_proveedor = Column(String(36), ForeignKey('proveedores.uuid_proveedor'), nullable=False)
    uuid_usuario_registro = Column(String(36), ForeignKey('usuarios.uuid_usuario'), nullable=False)
    fecha_compra = Column(DateTime, server_default=func.now())
    estatus = Column(Enum('Pendiente', 'Recibido', 'Cancelado'), default='Pendiente')

    proveedor = db.relationship('Proveedor', backref=db.backref('compras', lazy=True))
    usuario_registro = db.relationship('Usuario', backref=db.backref('compras_registradas', lazy=True))

    def __repr__(self):
        return f'<CompraEncabezado {self.uuid_compra}>'


class CompraDetalle(db.Model):
    __tablename__ = 'compras_detalle'

    uuid_detalle_compra = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    uuid_compra = Column(String(36), ForeignKey('compras_encabezado.uuid_compra'), nullable=False)
    uuid_insumo = Column(String(36), ForeignKey('insumos.uuid_insumo'), nullable=False)
    cantidad_comprada = Column(Numeric(12, 4), nullable=False)
    unidad_medida = Column(String(20), nullable=False)
    costo_unitario_compra = Column(Numeric(12, 2), nullable=False)

    compra = db.relationship('CompraEncabezado', backref=db.backref('detalles', lazy=True))
    insumo = db.relationship('Insumo', backref=db.backref('compras_detalle', lazy=True))

    def __repr__(self):
        return f'<CompraDetalle {self.uuid_detalle_compra}>'
