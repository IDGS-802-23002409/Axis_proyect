import uuid
from app.utils.database_connection import db
from sqlalchemy import Column, String, Integer, Numeric, DateTime, Enum, Text, ForeignKey, func


class ModeloRopa(db.Model):
    __tablename__ = 'modelos_ropa'

    uuid_modelo = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    nombre_modelo = Column(String(100), nullable=False)
    descripcion = Column(Text)
    uuid_categoria = Column(String(36), ForeignKey('categorias.uuid_categoria'), nullable=False)
    fecha_creacion = Column(DateTime, server_default=func.now())
    fecha_actualizacion = Column(DateTime, server_default=func.now(), onupdate=func.now())

    categoria = db.relationship('Categoria', backref=db.backref('modelos', lazy=True))

    def __repr__(self):
        return f'<ModeloRopa {self.nombre_modelo}>'


class ProductoTerminado(db.Model):
    __tablename__ = 'productos_terminados'

    uuid_producto = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    uuid_modelo = Column(String(36), ForeignKey('modelos_ropa.uuid_modelo'), nullable=False)
    sku_especifico = Column(String(50), unique=True, nullable=False)
    talla = Column(Enum('XSS', 'XS', 'S', 'M', 'L', 'XL', 'XXL', 'Unica'), nullable=False)
    precio_venta = Column(Numeric(12, 2), nullable=False)
    stock_fisico_actual = Column(Integer, default=0)
    stock_minimo_alerta = Column(Integer, default=0)
    fecha_creacion = Column(DateTime, server_default=func.now())
    fecha_actualizacion = Column(DateTime, server_default=func.now(), onupdate=func.now())

    modelo = db.relationship('ModeloRopa', backref=db.backref('productos', lazy=True))

    def __repr__(self):
        return f'<ProductoTerminado {self.sku_especifico}>'
