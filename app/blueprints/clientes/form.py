from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField
from wtforms import validators
from app.models.usuarios import Usuario

class ClienteForm(FlaskForm):
    uuid_usuario = SelectField('Cuenta de Usuario Base', coerce=str, validators=[
        validators.DataRequired()
    ])
    
    telefono = StringField('Teléfono de Contacto', [
        validators.Length(max=20)
    ])
    
    direccion_completa = TextAreaField('Domicilio de Envío/Facturación', [
        validators.Optional()
    ])

    def __init__(self, *args, obj=None, **kwargs):
        super().__init__(*args, obj=obj, **kwargs)
        self.obj = obj
        try:
            usuarios = Usuario.query.all()
            self.uuid_usuario.choices = [(u.uuid_usuario, f"{u.nombre_completo} ({u.email})") for u in usuarios]
        except Exception:
            self.uuid_usuario.choices = []

    def validate_uuid_usuario(self, field):
        from app.models.clientes import Cliente
        cli = Cliente.query.filter_by(uuid_usuario=field.data).first()
        if cli and (not self.obj or cli.uuid_cliente != self.obj.uuid_cliente):
            raise validators.ValidationError("Este usuario ya tiene un perfil de cliente asignado.")
