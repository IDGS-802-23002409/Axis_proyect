import uuid
from app.utils.database_connection import db
from sqlalchemy import (
    Column, String, Numeric, DateTime, ForeignKey, Text,
    Boolean, CheckConstraint, func, Index, Enum
)

# ENUMS
TipoMermaEnum = Enum('TELA','INSUMO','PRODUCTO', name='tipo_merma_enum')

ProcesoMermaEnum = Enum('CORTE','CONFECCION','ACABADO','ALMACEN', name='proceso_merma_enum')

TipoEventoMermaEnum = Enum(
    'DESPERDICIO_TOTAL','DESPERDICIO_PARCIAL','DEFECTO_CALIDAD',
    'ERROR_OPERARIO','DANIO_ACCIDENTAL','DEFECTO_ORIGEN','AJUSTE_INVENTARIO',
    name='tipo_evento_merma_enum'
)

MotivoMermaEnum = Enum(
    'CORTE_INCORRECTO','TELA_DEFECTUOSA','COSTURA_INCORRECTA',
    'MANCHA','ROTURA','MEDIDA_ERRONEA','PRUEBA_MUESTRA',
    'MAL_USO_MAQUINA','OTRO',
    name='motivo_merma_enum'
)

class Merma(db.Model):
    __tablename__ = 'mermas'

    uuid_merma = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    tipo_merma = Column(TipoMermaEnum, nullable=False)
    proceso = Column(ProcesoMermaEnum, nullable=False)
    tipo_evento = Column(TipoEventoMermaEnum, nullable=False)
    motivo = Column(MotivoMermaEnum, nullable=True)

    uuid_op = Column(String(36), ForeignKey('ordenes_produccion.uuid_op'), nullable=True)
    uuid_corte = Column(String(36), ForeignKey('ejecucion_corte.uuid_corte'), nullable=True)

    uuid_insumo = Column(String(36), ForeignKey('insumos.uuid_insumo'), nullable=True)
    uuid_rollo = Column(String(36), ForeignKey('rollos_inventario.uuid_rollo'), nullable=True)
    uuid_producto = Column(String(36), ForeignKey('productos_terminados.uuid_producto'), nullable=True)

    #  ÚNICO DATO REAL DE MERMA (ingresado por usuario)
    cantidad = Column(Numeric(12, 4), nullable=False)
    es_total = Column(Boolean, default=True)

    observaciones = Column(Text, nullable=True)

    fecha_creacion = Column(DateTime, server_default=func.now())
    fecha_actualizacion = Column(DateTime, onupdate=func.now())

    usuario_creacion = Column(String(36), nullable=True)
    usuario_actualizacion = Column(String(36), nullable=True)
    usuario_responsable = Column(String(36), nullable=True)

    activo = Column(Boolean, default=True)

    __table_args__ = (

        CheckConstraint('cantidad >= 0', name='check_cantidad_no_negativa'),

        # Debe existir al menos un origen
        CheckConstraint(
            "(uuid_insumo IS NOT NULL) OR (uuid_producto IS NOT NULL) OR (uuid_rollo IS NOT NULL)",
            name='check_merma_tiene_origen'
        ),

        # Si es tela debe existir rollo
        CheckConstraint(
            "(tipo_merma != 'TELA') OR (uuid_rollo IS NOT NULL)",
            name='check_tela_requiere_rollo'
        ),

        # Si es producto debe existir producto
        CheckConstraint(
            "(tipo_merma != 'PRODUCTO') OR (uuid_producto IS NOT NULL)",
            name='check_producto_requerido'
        ),

        # Si hay corte debe haber OP
        CheckConstraint(
            "(uuid_corte IS NULL) OR (uuid_op IS NOT NULL)",
            name='check_corte_op'
        ),

        
    )

    orden_produccion = db.relationship('OrdenProduccion', backref='mermas')
    corte = db.relationship('EjecucionCorte', backref='mermas')
    insumo = db.relationship('Insumo', backref='mermas')
    rollo = db.relationship('RolloInventario', backref='mermas')
    producto = db.relationship('ProductoTerminado', backref='mermas')

    def __repr__(self):
        return f'<Merma tipo={self.tipo_merma} proceso={self.proceso} cantidad={self.cantidad}>'