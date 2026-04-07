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
            from app.models.clientes import Cliente
            from app.models.usuarios import Role

            # Subconsulta para usuarios ya asignados a un cliente
            usuarios_asignados = db.session.query(Cliente.uuid_usuario)
            if self.obj:
                usuarios_asignados = usuarios_asignados.filter(Cliente.uuid_usuario != self.obj.uuid_usuario)
            
            # Filtro: Solo deben ser clientes y no deben estar asignados
            usuarios = Usuario.query.filter(
                Usuario.roles.any(Role.name == 'cliente'),
                ~Usuario.uuid_usuario.in_(usuarios_asignados)
            ).all()
            
            self.uuid_usuario.choices = [(u.uuid_usuario, f"{u.nombre_completo} ({u.email})") for u in usuarios]

            # Si estamos editando, asegurar que el usuario actual esté en las opciones
            if self.obj and self.obj.usuario:
                if (self.obj.uuid_usuario, f"{self.obj.usuario.nombre_completo} ({self.obj.usuario.email})") not in self.uuid_usuario.choices:
                    self.uuid_usuario.choices.insert(0, (self.obj.uuid_usuario, f"{self.obj.usuario.nombre_completo} ({self.obj.usuario.email})"))

        except Exception as e:
            print(f"Error populating user choices in ClienteForm: {e}")
            self.uuid_usuario.choices = []

    def validate_uuid_usuario(self, field):
        from app.models.clientes import Cliente
        cli = Cliente.query.filter_by(uuid_usuario=field.data).first()
        if cli and (not self.obj or cli.uuid_cliente != self.obj.uuid_cliente):
            raise validators.ValidationError("Este usuario ya tiene un perfil de cliente asignado.")
