from wtforms import Form, StringField, PasswordField, SelectField, RadioField, EmailField
from wtforms import validators
from app.models.usuarios import Usuario

class UserForm(Form):

    nombre_completo = StringField('Nombre completo', [
        validators.DataRequired(message="El nombre es requerido"),
        validators.Length(min=3, max=150, message="Debe tener entre 3 y 150 caracteres")
    ])

    email = EmailField('Correo electrónico', [
        validators.DataRequired(message="El correo es requerido"),
        validators.Email(message="Correo inválido"),
        validators.Length(max=120)
    ])

    password = PasswordField('Contraseña', [
        validators.Optional(),
        validators.Length(min=8, message="Mínimo 8 caracteres")
    ])

    rol = SelectField('Rol', choices=[
        ('Admin', 'Admin'),
        ('Producción', 'Producción'),
        ('Gerente', 'Gerente'),
        ('Cliente', 'Cliente')
    ], validators=[
        validators.DataRequired(message="El rol es requerido")
    ])

    estatus = RadioField('Estatus', choices=[
        (True, 'Activo'),
        (False, 'Inactivo')
    ], coerce=bool, default=True)

def __init__(self, *args, obj=None, **kwargs):
    super().__init__(*args, **kwargs)
    self.obj = obj

def validate_email(self, field):
    user = Usuario.query.filter_by(email=field.data).first()

    if user and (not self.obj or user.uuid_usuario != self.obj.uuid_usuario):
        raise validators.ValidationError("Este correo ya está registrado")
    
def validate_password(self, field):
    if not self.obj and not field.data:
        raise validators.ValidationError("La contraseña es requerida")