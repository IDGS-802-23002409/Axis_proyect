import uuid
from app.utils.database_connection import db
from sqlalchemy import Column, String, Boolean, DateTime, func


class Categoria(db.Model):
    __tablename__ = 'categorias'

    uuid_categoria = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    nombre = Column(String(50), nullable=False)
    descripcion = Column(String(255))
    estatus_visible = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, server_default=func.now())
    fecha_actualizacion = Column(DateTime, server_default=func.now(), onupdate=func.now())
    usuario_creo_uuid = Column(String(36))
    usuario_actualizo_uuid = Column(String(36))

    def __repr__(self):
        return f'<Categoria {self.nombre}>'
