import uuid
from app.utils.database_connection import db
from sqlalchemy import (
    CheckConstraint, Column, String, Integer, Numeric,
    DateTime, Enum, ForeignKey, Text, func, Index
)


# ─────────────────────────────────────────────
# ORDEN DE PRODUCCIÓN
# ─────────────────────────────────────────────
class OrdenProduccion(db.Model):
    __tablename__ = 'ordenes_produccion'

    uuid_op = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    uuid_producto = Column(String(36), ForeignKey('productos_terminados.uuid_producto'), nullable=False)
    uuid_venta = Column(String(36), ForeignKey('ventas_encabezado.uuid_venta'), nullable=True)
    uuid_venta_detalle = Column(String(36), ForeignKey('ventas_detalle.uuid_detalle'), nullable=True)
    uuid_pedido_detalle = Column(String(36), ForeignKey('pedidos_cliente_detalle.uuid_detalle_pedido'), nullable=True)
    cantidad_a_producir = Column(Integer, nullable=False)
    estado = Column(Enum('Pendiente', 'En Corte', 'Confección', 'Terminado'), default='Pendiente')
    fecha_solicitud = Column(DateTime, server_default=func.now())
    fecha_actualizacion = Column(DateTime, server_default=func.now(), onupdate=func.now())

    producto = db.relationship('ProductoTerminado', backref=db.backref('ordenes_produccion', lazy=True))
    venta = db.relationship('VentaEncabezado', backref=db.backref('ordenes_produccion', lazy=True))
    venta_detalle = db.relationship('VentaDetalle', backref=db.backref('ordenes_produccion', lazy=True))
    pedido_detalle = db.relationship('PedidoClienteDetalle', backref=db.backref('ordenes_produccion', lazy=True))

    __table_args__ = (
        Index('idx_op_estado', 'estado'),
        Index('idx_op_producto', 'uuid_producto'),
    )

    def __repr__(self):
        return f'<OrdenProduccion {self.uuid_op}>'


# ─────────────────────────────────────────────
# EJECUCIÓN DE CORTE (cabecera agregada por OP + insumo)
# uuid_rollo_used fue reemplazado por EjecucionCorteRollo (tabla pivot)
# ─────────────────────────────────────────────
class EjecucionCorte(db.Model):
    __tablename__ = 'ejecucion_corte'

    uuid_corte = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    uuid_op = Column(String(36), ForeignKey('ordenes_produccion.uuid_op'), nullable=False)

    # Totales agresados para este corte (suma de todos los rollos usados)
    metros_teoricos_requeridos = Column(Numeric(12, 4), nullable=False)
    metros_sacados_bodega = Column(Numeric(12, 4), nullable=False)
    prendas_reales_logradas = Column(Integer, nullable=False)

    fecha_proceso = Column(DateTime, server_default=func.now())
    fecha_actualizacion = Column(DateTime, server_default=func.now(), onupdate=func.now())
    usuario_corto_uuid = Column(String(36))

    orden_produccion = db.relationship(
        'OrdenProduccion',
        backref=db.backref('ejecuciones_corte', lazy=True)
    )
    # Relación one-to-many hacia los rollos específicos usados
    rollos_usados = db.relationship(
        'EjecucionCorteRollo',
        backref='ejecucion',
        lazy=True,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f'<EjecucionCorte {self.uuid_corte}>'


# ─────────────────────────────────────────────
# TRAZABILIDAD DE ROLLOS POR CORTE (tabla pivot)
# Registra qué rollo específico aportó cuántos metros a cada corte
# ─────────────────────────────────────────────
class EjecucionCorteRollo(db.Model):
    __tablename__ = 'ejecucion_corte_rollo'

    uuid = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    uuid_corte = Column(String(36), ForeignKey('ejecucion_corte.uuid_corte'), nullable=False)
    uuid_rollo = Column(String(36), ForeignKey('rollos_inventario.uuid_rollo'), nullable=False)
    uuid_insumo = Column(String(36), ForeignKey('insumos.uuid_insumo'), nullable=True)
    metros_usados = Column(Numeric(12, 4), nullable=False)
    fecha_creacion = Column(DateTime, server_default=func.now())

    rollo = db.relationship("RolloInventario", backref="usos_en_corte")
    insumo = db.relationship("Insumo", backref="usos_en_corte")

    def __repr__(self):
        return f'<EjecucionCorteRollo corte={self.uuid_corte} rollo={self.uuid_rollo} metros={self.metros_usados}>'


# ─────────────────────────────────────────────
# MERMA DE PIEZAS
# ─────────────────────────────────────────────
motivo_merma_pieza_enum = Enum(
    'DEFECTO_PROVEEDOR',
    'DAÑO_EN_PROCESO',
    'ERROR_OPERARIO',
    'MUESTRA_PRUEBA',
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

    uuid_merma = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    uuid_op = Column(String(36), ForeignKey('ordenes_produccion.uuid_op'), nullable=False)
    uuid_insumo = Column(String(36), ForeignKey('insumos.uuid_insumo'), nullable=False)
    cantidad_teorica = Column(Numeric(12, 4), nullable=False)
    cantidad_real_consumida = Column(Numeric(12, 4), nullable=False)
    motivo = Column(motivo_merma_pieza_enum, nullable=True)
    observaciones = Column(Text, nullable=True)
    fecha_registro = Column(DateTime, server_default=func.now())
    fecha_actualizacion = Column(DateTime, server_default=func.now(), onupdate=func.now())
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
