from sqlalchemy import event
from flask import request, has_request_context
from flask_security import current_user
from app.models.audit_log import SecurityAuditLog
from app.utils.database_connection import db
import json
from decimal import Decimal
from datetime import datetime, date

def object_to_dict(obj):
    """Convierte un objeto SQLAlchemy a un diccionario serializable."""
    d = {}
    for column in obj.__table__.columns:
        val = getattr(obj, column.name)
        if isinstance(val, Decimal):
            val = float(val)
        elif isinstance(val, datetime):
            val = val.isoformat()
        elif isinstance(val, date):
            val = val.isoformat()
        d[column.name] = val
    return d

def get_current_user_info():
    """Obtiene información del usuario actual fuera o dentro de un request context."""
    if not has_request_context():
        return 'Sistema', 'Sistema', 'Sistema'
    
    if current_user and current_user.is_authenticated:
        roles = ", ".join([r.name for r in current_user.roles])
        return str(current_user.uuid_usuario), current_user.nombre_completo, roles
    
    return 'Anonimo', 'Anonimo', 'Anonimo'

def get_db_user_info():
    """Obtiene el rol de base de datos activo en g.db_role."""
    from flask import g
    if has_request_context() and hasattr(g, 'db_role'):
        return g.db_role
    return 'default'

def get_remote_addr():
    if has_request_context():
        return request.remote_addr
    return None

def capture_audit_log(session, flush_context, instances):
    """
    Listener para capturar cambios en el flush de la sesión.
    """
    if any(isinstance(obj, SecurityAuditLog) for obj in session.new):
        return

    user_uuid, user_name, user_role = get_current_user_info()
    db_user = get_db_user_info()
    ip = get_remote_addr()

    for obj in session.new:
        if not hasattr(obj, '__table__'): continue
        
        reg_uuid = None
        for col in obj.__table__.primary_key:
            if 'uuid' in col.name:
                reg_uuid = getattr(obj, col.name)
                break
        
        log = SecurityAuditLog(
            uuid_usuario=user_uuid,
            nombre_usuario=user_name,
            rol_usuario=user_role,
            usuario_bd=db_user,
            accion='INSERT',
            tabla=obj.__tablename__,
            registro_uuid=str(reg_uuid) if reg_uuid else 'N/A',
            valores_nuevos=object_to_dict(obj),
            ip_direccion=ip
        )
        db.session.add(log)

    for obj in session.dirty:
        if not hasattr(obj, '__table__'): continue
        
        state = db.inspect(obj)
        changes_old = {}
        changes_new = {}
        
        for attr in state.attrs:
            # Solo procesar atributos que son columnas reales, no relaciones
            if attr.key not in obj.__table__.columns:
                continue

            hist = attr.load_history()
            if not hist.has_changes():
                continue
            
            old_val = hist.deleted[0] if hist.deleted else None
            new_val = hist.added[0] if hist.added else None
            
            def serialize(val):
                if isinstance(val, Decimal): return float(val)
                if isinstance(val, datetime): return val.isoformat()
                if isinstance(val, date): return val.isoformat()
                if hasattr(val, '__table__'): return str(val)
                return val

            changes_old[attr.key] = serialize(old_val)
            changes_new[attr.key] = serialize(new_val)

        if not changes_new: continue

        reg_uuid = None
        for col in obj.__table__.primary_key:
            if 'uuid' in col.name:
                reg_uuid = getattr(obj, col.name)
                break

        log = SecurityAuditLog(
            uuid_usuario=user_uuid,
            nombre_usuario=user_name,
            rol_usuario=user_role,
            usuario_bd=db_user,
            accion='UPDATE',
            tabla=obj.__tablename__,
            registro_uuid=str(reg_uuid) if reg_uuid else 'N/A',
            valores_anteriores=changes_old,
            valores_nuevos=changes_new,
            ip_direccion=ip
        )
        db.session.add(log)

    for obj in session.deleted:
        if not hasattr(obj, '__table__'): continue
        
        reg_uuid = None
        for col in obj.__table__.primary_key:
            if 'uuid' in col.name:
                reg_uuid = getattr(obj, col.name)
                break

        log = SecurityAuditLog(
            uuid_usuario=user_uuid,
            nombre_usuario=user_name,
            rol_usuario=user_role,
            usuario_bd=db_user,
            accion='DELETE',
            tabla=obj.__tablename__,
            registro_uuid=str(reg_uuid) if reg_uuid else 'N/A',
            valores_anteriores=object_to_dict(obj),
            ip_direccion=ip
        )
        db.session.add(log)

def register_audit_listeners():
    event.listen(db.session, 'before_flush', capture_audit_log)
