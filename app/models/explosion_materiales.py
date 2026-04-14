import uuid
from app.utils.database_connection import db
from sqlalchemy import Column, String, Integer, Numeric, DateTime, Text, Enum, ForeignKey, func, Index


class ExplosionMaterialesCabecera(db.Model):
    __tablename__ = 'explosion_materiales_cabecera'

    uuid_explosion = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    nombre_receta = Column(String(100), nullable=False)
    instrucciones_proceso = Column(Text)
    uuid_categoria = Column(String(36), ForeignKey('categorias.uuid_categoria'), nullable=False)
    talla = Column(Enum('XSS', 'XS', 'S', 'M', 'L', 'XL', 'XXL', 'Unica'), nullable=False)
    fecha_creacion = Column(DateTime, server_default=func.now())
    fecha_actualizacion = Column(DateTime, server_default=func.now(), onupdate=func.now())
    uuid_usuario = Column(String(36), nullable=False)
    categoria = db.relationship('Categoria', backref=db.backref('modelos', lazy=True))
    # NUEVO CAMPO ESTATUS
    estatus = Column(
        Enum('ACTIVO', 'INACTIVO', name='estatus_receta'),
        default='ACTIVO',
        nullable=False
    )

# relacion al reves porque producto apunta a la receta no al reves ocupas tener la receta antes que un prod terminado
   # producto = db.relationship('ProductoTerminado', backref=db.backref('explosion', uselist=False))

    def __repr__(self):
        return f'<ExplosionMaterialesCabecera {self.uuid_explosion}>'


class ExplosionMaterialesDetalle(db.Model):
    __tablename__ = 'explosion_materiales_detalle'

    uuid_detalle = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    uuid_explosion = Column(String(36), ForeignKey('explosion_materiales_cabecera.uuid_explosion'), nullable=False)
    uuid_insumo = Column(String(36), ForeignKey('insumos.uuid_insumo'), nullable=False)
    consumo_teorico_unitario = Column(Numeric(12, 4), nullable=False)
    ancho_referencia = Column(Numeric(5, 2))
    fecha_creacion = Column(DateTime, server_default=func.now())
    fecha_actualizacion = Column(DateTime, server_default=func.now(), onupdate=func.now())

    explosion = db.relationship('ExplosionMaterialesCabecera', backref=db.backref('detalles', lazy=True))
    insumo = db.relationship('Insumo', backref=db.backref('explosion_detalles', lazy=True))

    __table_args__ = (
        Index('idx_expdet_explosion', 'uuid_explosion'),
        Index('idx_expdet_insumo', 'uuid_insumo'),
    )

    def __repr__(self):
        return f'<ExplosionMaterialesDetalle {self.uuid_detalle}>'
