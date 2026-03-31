import uuid
from app.utils.database_connection import db
from sqlalchemy import Column, String, Numeric, DateTime, Enum, ForeignKey, func
from sqlalchemy import Enum


import uuid
from app.utils.database_connection import db
from sqlalchemy import Column, String, DateTime, Enum, ForeignKey, func

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
    fecha_compra = Column(DateTime, server_default=func.now())

    # Estado de la compra
    # PENDIENTE → aún no entra al inventario
    # RECIBIDO → ya afecta el stock
    # CANCELADO → no afecta nada
    estatus = Column(estatus_compra_enum, default='PENDIENTE')
    proveedor = db.relationship('Proveedor', backref=db.backref('compras', lazy=True))
    usuario_registro = db.relationship('Usuario', backref=db.backref('compras_registradas', lazy=True))
    def __repr__(self):
        return f'<CompraEncabezado {self.uuid_compra}>'


class CompraDetalle(db.Model):
    __tablename__ = 'compras_detalle'

    uuid_detalle_compra = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    uuid_compra = Column(String(36), ForeignKey('compras_encabezado.uuid_compra'), nullable=False)
    uuid_insumo = Column(String(36), ForeignKey('insumos.uuid_insumo'), nullable=False)

    # 
    #  DATOS DE COMPRA
    # -------------------

    # Cantidad comprada en UNIDAD DE COMPRA
    # Ejemplo:
    # - 3 rollos
    # 
    cantidad_comprada = Column(Numeric(12, 4), nullable=False)

    #  Costo por unidad de compra
    # Ejemplo:
    # - $500 por rollo
    
    costo_unitario_compra = Column(Numeric(12, 2), nullable=False)
    compra = db.relationship('CompraEncabezado', backref=db.backref('detalles', lazy=True))
    insumo = db.relationship('Insumo', backref=db.backref('compras_detalle', lazy=True))

    def __repr__(self):
        return f'<CompraDetalle {self.uuid_detalle_compra}>'