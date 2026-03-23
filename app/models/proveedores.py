import uuid
from app.utils.database_connection import db
from sqlalchemy import Column, String, DateTime, func


class Proveedor(db.Model):
    __tablename__ = 'proveedores'

    uuid_proveedor = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    razon_social = Column(String(150), nullable=False)
    rfc = Column(String(20), nullable=False)
    contacto_nombre = Column(String(100))
    fecha_creacion = Column(DateTime, server_default=func.now())
    fecha_actualizacion = Column(DateTime, server_default=func.now(), onupdate=func.now())
    usuario_creo_uuid = Column(String(36))

    def __repr__(self):
        return f'<Proveedor {self.razon_social}>'
