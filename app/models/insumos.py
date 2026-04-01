import uuid
from app.utils.database_connection import db
from sqlalchemy import Column, String, Numeric, DateTime, ForeignKey, func, Enum,CheckConstraint

#  cómo se compra el insumo (presentación comercial)
unidad_compra_enum = Enum(
    'ROLLO',
    'PIEZA', 
    name='unidad_compra_enum'
)

#  unidad real en la que se usa o consume el insumo
unidad_base_enum = Enum(
    'METRO',  # Para telas, hilos, etc.
    'PIEZA',  # Para botones, agujas, etc.
    name='unidad_base_enum'
)

# Estado del insumo
estatus_enum = Enum(
    'ACTIVO',
    'INACTIVO',
    name='estatus_insumo_enum'
)

class Insumo(db.Model):
    __tablename__ = 'insumos'

    __table_args__ = (
        CheckConstraint('stock_total_acumulado >= 0', name='check_stock_no_negativo'),
    )


    # Identificador único
    uuid_insumo = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    sku = Column(String(50), unique=True)
    nombre = Column(String(100), nullable=False)
    uuid_categoria = Column(String(36), ForeignKey('categorias.uuid_categoria'))

    # 
    #  CONFIGURACIÓN DE UNIDADES 
    # 

    #  Cómo compras el insumo (presentación)
    # Ejemplo:
    # - Tela → ROLLO
    # - Botones → CAJA
    unidad_medida = Column(unidad_compra_enum, nullable=False)

    # Cuánto contiene UNA unidad de compra
    # Ejemplo:
    # - 1 rollo de tela = 50 metros
    # - 1 boton en pieza
    contenido_cantidad = Column(Numeric(12, 4), nullable=False)

    #  En qué unidad se mide ese contenido
    # Ejemplo:
    # - Tela → METRO
    # - Botones → PIEZA
    contenido_unidad_medida = Column(unidad_base_enum, nullable=False)

    # 
    # INVENTARIO REAL
    # 

    #  Stock total SIEMPRE en unidad base (nunca en cajas o rollos)
    # Ejemplo:
    # - Compras 3 rollos de tela de 50m → stock = 150 METROS
    
    stock_total_acumulado = Column(Numeric(12, 4), default=0)

    #  Alerta mínima de inventario
    stock_minimo_alerta = Column(Numeric(12, 4), default=0)

# ancho para rollo inventario
    ancho = Column(Numeric(5, 2), nullable=True)

    fecha_creacion = Column(DateTime, server_default=func.now())
    fecha_actualizacion = Column(DateTime, server_default=func.now(), onupdate=func.now())
    estatus = Column(estatus_enum, default='ACTIVO')
    usuario_actualizo_uuid = Column(String(36))
    categoria = db.relationship('Categoria', backref=db.backref('insumos', lazy=True))

    def __repr__(self):
        return f'<Insumo {self.nombre}>'