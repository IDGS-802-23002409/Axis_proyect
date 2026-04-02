import uuid
from app.utils.database_connection import db
from sqlalchemy import Column, String, Numeric, DateTime, ForeignKey, func


class RolloInventario(db.Model):
    __tablename__ = 'rollos_inventario'

    uuid_rollo = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    uuid_insumo = Column(String(36), ForeignKey('insumos.uuid_insumo'), nullable=False)
    uuid_detalle_compra = Column(String(36), ForeignKey('compras_detalle.uuid_detalle_compra'))
    metraje_inicial = Column(Numeric(12, 4), nullable=False)
    metraje_continuo_actual = Column(Numeric(12, 4), nullable=False)
    ancho_real_recibido = Column(Numeric(5, 2))
    fecha_creacion = Column(DateTime, server_default=func.now())

    insumo = db.relationship('Insumo', backref=db.backref('rollos', lazy=True))
    detalle_compra = db.relationship('CompraDetalle', backref=db.backref('rollos', lazy=True))

    def __repr__(self):
        return f'<RolloInventario {self.uuid_rollo}>'


class RetazoInventario(db.Model):
    __tablename__ = 'retazos_inventario'

    uuid_retazo = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    uuid_rollo_origen = Column(String(36), ForeignKey('rollos_inventario.uuid_rollo'), nullable=False)
    uuid_corte_origen = Column(String(36), ForeignKey('ejecucion_corte.uuid_corte'), nullable=False)
    metraje = Column(Numeric(12, 4), nullable=False)
    motivo_merma = Column(db.Text)
    fecha_creacion = Column(DateTime, server_default=func.now())

    rollo_origen = db.relationship('RolloInventario', backref=db.backref('retazos', lazy=True))

    def __repr__(self):
        return f'<RetazoInventario {self.uuid_retazo}>'
