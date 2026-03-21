import uuid
from app.utils.database_connection import db
from sqlalchemy import Column, String, Boolean, DateTime, Enum, func


class Usuario(db.Model):
    __tablename__ = 'usuarios'

    uuid_usuario = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    nombre_completo = Column(String(150), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    rol = Column(Enum('Admin', 'Producción', 'Gerente', 'Cliente'), nullable=False)
    estatus = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, server_default=func.now())
    fecha_actualizacion = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f'<Usuario {self.email}>'
