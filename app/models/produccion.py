import uuid
from app.utils.database_connection import db
from sqlalchemy import CheckConstraint, Column, String, Integer, Numeric, DateTime, Enum, ForeignKey, Text, func


class OrdenProduccion(db.Model):
    __tablename__ = 'ordenes_produccion'

    uuid_op = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    uuid_producto = Column(String(36), ForeignKey('productos_terminados.uuid_producto'), nullable=False)
    # NUEVO: Relación con el pedido específico del cliente
    uuid_venta_detalle = Column(String(36), ForeignKey('ventas_detalle.uuid_detalle'), nullable=True) 
    cantidad_a_producir = Column(Integer, nullable=False)
    estado = Column(Enum('Pendiente', 'En Corte', 'Confección', 'Terminado'), default='Pendiente')
    fecha_solicitud = Column(DateTime, server_default=func.now())
    producto = db.relationship('ProductoTerminado', backref=db.backref('ordenes_produccion', lazy=True))
    venta_detalle = db.relationship('VentaDetalle', backref=db.backref('orden_produccion', uselist=False))

    def __repr__(self):
        return f'<OrdenProduccion {self.uuid_op}>'


class EjecucionCorte(db.Model):
    __tablename__ = 'ejecucion_corte'

    uuid_corte = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    uuid_op = Column(String(36), ForeignKey('ordenes_produccion.uuid_op'), nullable=False)
    uuid_rollo_used = Column(String(36), ForeignKey('rollos_inventario.uuid_rollo'), nullable=False)
    
    # Lo que el sistema calculó que se ocupaba (Explosión * Cantidad)
    metros_teoricos_requeridos = Column(Numeric(12, 4), nullable=False) 
    # Lo que el cortador sacó físicamente del rollo
    metros_sacados_bodega = Column(Numeric(12, 4), nullable=False) 
    prendas_reales_logradas = Column(Integer, nullable=False)
    merma_real_calculada = Column(Numeric(12, 4), nullable=False)
    fecha_proceso = Column(DateTime, server_default=func.now())
    usuario_corto_uuid = Column(String(36))
    orden_produccion = db.relationship('OrdenProduccion', backref=db.backref('ejecuciones_corte', lazy=True))
    rollo_usado = db.relationship('RolloInventario', backref=db.backref('ejecuciones_corte', lazy=True))
    def __repr__(self):
        return f'<EjecucionCorte {self.uuid_corte}>'

motivo_merma_pieza_enum = Enum(
    'DEFECTO_PROVEEDOR',    # Pieza llegó dañada desde la compra
    'DAÑO_EN_PROCESO',      # Se dañó durante confección o corte
    'ERROR_OPERARIO',       # Error humano al usar el insumo
    'MUESTRA_PRUEBA',       # Se usó como prueba/muestra sin llegar a prenda
    'OTRO',
    name='motivo_merma_pieza_enum'
)
 
 
class MermaPiezas(db.Model):
    """
    Flujo esperado:
        1. Al ejecutar la confección, el operario registra cuántas piezas usó realmente.
        2. El servicio calcula: merma = cantidad_real_consumida - cantidad_teorica
        3. Si merma > 0, se inserta este registro y se descuenta del stock del insumo.
        4. Si merma < 0 (se usaron menos), también se registra como ahorro.
    """
    __tablename__ = 'merma_piezas'
    uuid_merma = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    uuid_op = Column(
        String(36),
        ForeignKey('ordenes_produccion.uuid_op'),
        nullable=False
    )
    uuid_insumo = Column(
        String(36),
        ForeignKey('insumos.uuid_insumo'),
        nullable=False
    )
    # Cantidad que la explosión de materiales indicaba consumir
    # (consumo_teorico_unitario × cantidad_a_producir de la OP)
    cantidad_teorica = Column(Numeric(12, 4), nullable=False)
    cantidad_real_consumida = Column(Numeric(12, 4), nullable=False)
    motivo = Column(motivo_merma_pieza_enum, nullable=True)
    observaciones = Column(Text, nullable=True)
    fecha_registro = Column(DateTime, server_default=func.now())
    usuario_registro_uuid = Column(String(36), nullable=True)
    orden_produccion = db.relationship(
        'OrdenProduccion',
        backref=db.backref('mermas_piezas', lazy=True)
    )
    insumo = db.relationship(
        'Insumo',
        backref=db.backref('mermas_piezas', lazy=True)
    )
    __table_args__ = (
        CheckConstraint('cantidad_teorica > 0', name='check_merma_teorica_positiva'),
        CheckConstraint('cantidad_real_consumida >= 0', name='check_merma_real_no_negativa'),
    )
    
    @property
    def diferencia(self):
        return self.cantidad_real_consumida - self.cantidad_teorica
 
    def __repr__(self):
        return f'<MermaPiezas op={self.uuid_op} insumo={self.uuid_insumo} diff={self.diferencia}>'