import uuid
from app.utils.database_connection import db
from sqlalchemy import Boolean, Column, String, Integer, Numeric, DateTime, ForeignKey, UniqueConstraint, func, CheckConstraint, Index

class ProductoTerminado(db.Model):
    __tablename__ = 'productos_terminados'

    uuid_producto = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    uuid_explosion = Column(String(36), ForeignKey('explosion_materiales_cabecera.uuid_explosion'), nullable=False)
    sku_especifico = Column(String(50), unique=True, nullable=False)
    imagen_url = Column(String(255))
    precio_venta = Column(Numeric(12, 2), nullable=False)
    stock_fisico_actual = Column(Integer, default=0)
    stock_minimo_alerta = Column(Integer, default=0)
    active = Column(Boolean(), default=True)
    fecha_creacion = Column(DateTime, server_default=func.now())
    fecha_actualizacion = Column(DateTime, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        CheckConstraint('stock_fisico_actual >= 0', name='check_stock_producto_positivo'),
        Index('idx_producto_explosion', 'uuid_explosion'),
        UniqueConstraint('uuid_explosion', name='uq_producto_explosion'),
    )
    
    explosion = db.relationship(
        'ExplosionMaterialesCabecera',
        backref=db.backref('productos', lazy='selectin')
    )
    def __repr__(self):
        return f'<ProductoTerminado {self.sku_especifico}>'
