import uuid
from app.utils.database_connection import db
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, func


class Cliente(db.Model):
    __tablename__ = 'clientes'

    uuid_cliente = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    uuid_usuario = Column(String(36), ForeignKey('usuarios.uuid_usuario'), unique=True, nullable=False)
    telefono = Column(String(20))
    direccion_completa = Column(Text)
    fecha_creacion = Column(DateTime, server_default=func.now())
    fecha_actualizacion = Column(DateTime, server_default=func.now(), onupdate=func.now())
    usuario_actualizo_uuid = Column(String(36))

    usuario = db.relationship('Usuario', backref=db.backref('cliente', uselist=False))

    def __repr__(self):
        return f'<Cliente {self.uuid_cliente}>'
