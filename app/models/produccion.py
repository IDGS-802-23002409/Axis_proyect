import uuid
from app.utils.database_connection import db
from sqlalchemy import Column, String, Integer, Numeric, DateTime, Enum, ForeignKey, func


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
