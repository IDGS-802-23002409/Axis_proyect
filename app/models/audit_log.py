import uuid
from app.utils.database_connection import db
from sqlalchemy import Column, String, Integer, DateTime, Text, func

class SecurityAuditLog(db.Model):
    __tablename__ = 'security_audit_logs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid_usuario = Column(String(36), index=True, nullable=True) 
    nombre_usuario = Column(String(150), nullable=True)
    rol_usuario = Column(String(80), nullable=True) 
    usuario_bd = Column(String(80), nullable=True) # El usuario/rol de la base de datos
    
    accion = Column(String(20), nullable=False) 
    tabla = Column(String(100), nullable=False, index=True)
    registro_uuid = Column(String(36), nullable=False, index=True)
    
    valores_anteriores = Column(db.JSON, nullable=True)
    valores_nuevos = Column(db.JSON, nullable=True)
    
    ip_direccion = Column(String(45), nullable=True) 
    fecha = Column(DateTime, server_default=func.now(), index=True)

    def __repr__(self):
        return f'<SecurityAuditLog {self.accion} on {self.tabla} by {self.uuid_usuario}>'
