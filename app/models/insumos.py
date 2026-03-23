import uuid
from app.utils.database_connection import db
from sqlalchemy import Column, String, Numeric, DateTime, ForeignKey, func


class Insumo(db.Model):
    __tablename__ = 'insumos'

    uuid_insumo = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    sku = Column(String(50), unique=True)
    nombre = Column(String(100), nullable=False)
    uuid_categoria = Column(String(36), ForeignKey('categorias.uuid_categoria'))
    costo_unitario_individual = Column(Numeric(12, 4), nullable=False, default=0)
    stock_total_acumulado = Column(Numeric(12, 4), default=0)
    stock_minimo_alerta = Column(Numeric(12, 4), default=0)
    fecha_creacion = Column(DateTime, server_default=func.now())
    fecha_actualizacion = Column(DateTime, server_default=func.now(), onupdate=func.now())
    usuario_actualizo_uuid = Column(String(36))

    categoria = db.relationship('Categoria', backref=db.backref('insumos', lazy=True))

    def __repr__(self):
        return f'<Insumo {self.nombre}>'
