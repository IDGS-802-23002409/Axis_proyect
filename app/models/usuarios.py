import uuid
from app.utils.database_connection import db
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, func, Integer
from sqlalchemy.orm import relationship, backref
from flask_security import UserMixin, RoleMixin

# Tabla intermedia para Roles y Usuarios
roles_usuarios = db.Table(
    'roles_usuarios',
    db.Column('usuario_id', String(36), db.ForeignKey('usuarios.uuid_usuario')),
    db.Column('role_id', Integer(), db.ForeignKey('role.id'))
)

class Role(db.Model, RoleMixin):
    id = Column(Integer(), primary_key=True)
    name = Column(String(80), unique=True) # Admin, Cliente, Produccion, Gerente
    description = Column(String(255))

class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuarios'

    uuid_usuario = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    nombre_completo = Column(String(150), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    active = Column(Boolean(), default=True)
    fecha_creacion = Column(DateTime, server_default=func.now())
    fecha_actualizacion = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Identificador único para sesiones (Seguridad)
    fs_uniquifier = Column(String(64), unique=True, nullable=False, default=lambda: uuid.uuid4().hex)

    # Confirmación de Email
    confirmed_at = Column(DateTime())

    # Two-Factor Authentication (2FA)
    tf_primary_method = Column(String(64), nullable=True)
    tf_totp_secret = Column(String(255), nullable=True)
    tf_phone_number = Column(String(64), nullable=True)

    # Rastreo de cambio de contraseña
    password_changed_at = Column(DateTime(), server_default=func.now())

    # Multi-factor recovery codes
    mf_recovery_codes = Column(db.JSON, nullable=True)

    # Relaciones
    roles = db.relationship('Role', secondary=roles_usuarios,
                          backref=db.backref('usuarios', lazy='dynamic'))
    

    # Flask-Security necesita un 'id' property
    @property
    def id(self):
        return self.uuid_usuario

    def __repr__(self):
        return f'<Usuario {self.email}>'
