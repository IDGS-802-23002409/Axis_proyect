from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField
from wtforms import validators
from app.models.usuarios import Usuario

class EmpleadoForm(FlaskForm):
    uuid_usuario = SelectField('Cuenta de Usuario del Sistema', coerce=str, validators=[
        validators.DataRequired(message="Debe seleccionar una cuenta")
    ])
    
    numero_empleado = StringField('Número de Empleado', [
        validators.DataRequired(message="Requerido"),
        validators.Length(max=50)
    ])
    
    puesto = StringField('Puesto / Cargo', [
        validators.Length(max=100)
    ])
    
    departamento = StringField('Departamento asignado', [
        validators.Length(max=100)
    ])
    
    fecha_ingreso = DateField('Fecha de Ingreso', format='%Y-%m-%d', validators=[
        validators.Optional()
    ])

    def __init__(self, *args, obj=None, **kwargs):
        super().__init__(*args, obj=obj, **kwargs)
        self.obj = obj
        try:
            from app.models.empleados import Empleado
            from app.models.usuarios import Role
            
            # Subconsulta para usuarios ya asignados a un empleado
            usuarios_asignados = db.session.query(Empleado.uuid_usuario)
            if self.obj:
                usuarios_asignados = usuarios_asignados.filter(Empleado.uuid_usuario != self.obj.uuid_usuario)
            
            # Filtro: No deben ser clientes y no deben estar asignados
            usuarios = Usuario.query.filter(
                ~Usuario.roles.any(Role.name == 'cliente'),
                ~Usuario.uuid_usuario.in_(usuarios_asignados)
            ).all()
            
            self.uuid_usuario.choices = [(u.uuid_usuario, f"{u.nombre_completo} ({u.email})") for u in usuarios]
            
            # Si estamos editando, asegurar que el usuario actual esté en las opciones
            if self.obj and self.obj.usuario:
                if (self.obj.uuid_usuario, f"{self.obj.usuario.nombre_completo} ({self.obj.usuario.email})") not in self.uuid_usuario.choices:
                    self.uuid_usuario.choices.insert(0, (self.obj.uuid_usuario, f"{self.obj.usuario.nombre_completo} ({self.obj.usuario.email})"))
                    
        except Exception as e:
            print(f"Error populating user choices: {e}")
            self.uuid_usuario.choices = []

    def validate_uuid_usuario(self, field):
        from app.models.empleados import Empleado
        emp = Empleado.query.filter_by(uuid_usuario=field.data).first()
        if emp and (not self.obj or emp.uuid_empleado != self.obj.uuid_empleado):
            raise validators.ValidationError("Este usuario ya tiene un perfil de empleado asignado.")
