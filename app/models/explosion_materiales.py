import uuid
from app.utils.database_connection import db
from sqlalchemy import Column, String, Integer, Numeric, DateTime, Text, Enum, ForeignKey, func


class ExplosionMaterialesCabecera(db.Model):
    __tablename__ = 'explosion_materiales_cabecera'

    uuid_explosion = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    uuid_producto = Column(String(36), ForeignKey('productos_terminados.uuid_producto'), unique=True, nullable=False)
    instrucciones_proceso = Column(Text)
    fecha_actualizacion = Column(DateTime, server_default=func.now(), onupdate=func.now())

    producto = db.relationship('ProductoTerminado', backref=db.backref('explosion', uselist=False))

    def __repr__(self):
        return f'<ExplosionMaterialesCabecera {self.uuid_explosion}>'


class ExplosionMaterialesDetalle(db.Model):
    __tablename__ = 'explosion_materiales_detalle'

    uuid_detalle = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    uuid_explosion = Column(String(36), ForeignKey('explosion_materiales_cabecera.uuid_explosion'), nullable=False)
    uuid_insumo = Column(String(36), ForeignKey('insumos.uuid_insumo'), nullable=False)
    consumo_teorico_unitario = Column(Numeric(12, 4), nullable=False)
    ancho_referencia = Column(Numeric(5, 2))

    explosion = db.relationship('ExplosionMaterialesCabecera', backref=db.backref('detalles', lazy=True))
    insumo = db.relationship('Insumo', backref=db.backref('explosion_detalles', lazy=True))

    def __repr__(self):
        return f'<ExplosionMaterialesDetalle {self.uuid_detalle}>'
