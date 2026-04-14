import uuid
from app.utils.database_connection import db
from sqlalchemy import Column, String, DateTime, ForeignKey, func, Boolean

class Empleado(db.Model):
    __tablename__ = 'empleados'

    uuid_empleado = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    uuid_usuario = Column(String(36), ForeignKey('usuarios.uuid_usuario'), unique=True, nullable=False)
    numero_empleado = Column(String(50), unique=True)
    puesto = Column(String(100))
    departamento = Column(String(100))
    fecha_ingreso = Column(DateTime)
    fecha_creacion = Column(DateTime, server_default=func.now())
    fecha_actualizacion = Column(DateTime, server_default=func.now(), onupdate=func.now())
    activo = Column(Boolean, default=True, nullable=False)

    usuario = db.relationship('Usuario', backref=db.backref('empleado', uselist=False))

    def __repr__(self):
        return f'<Empleado {self.numero_empleado or self.uuid_empleado}>'
