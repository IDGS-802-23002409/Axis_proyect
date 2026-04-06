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
            # Traer solo usuarios para popular combo (podría filtrarse por admin/produccion)
            usuarios = Usuario.query.all()
            self.uuid_usuario.choices = [(u.uuid_usuario, f"{u.nombre_completo} ({u.email})") for u in usuarios]
        except Exception:
            self.uuid_usuario.choices = []

    def validate_uuid_usuario(self, field):
        from app.models.empleados import Empleado
        emp = Empleado.query.filter_by(uuid_usuario=field.data).first()
        if emp and (not self.obj or emp.uuid_empleado != self.obj.uuid_empleado):
            raise validators.ValidationError("Este usuario ya tiene un perfil de empleado asignado.")
