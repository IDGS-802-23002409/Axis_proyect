from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, ValidationError
from app.models.proveedores import Proveedor
import re
from flask import request

# Delimitación de mi forms
class ProveedorForm(FlaskForm):
    razon_social = StringField('Razón Social', validators=[
        DataRequired(message="La razón social es obligatoria"),
        Length(max=150)
    ])
    rfc = StringField('RFC', validators=[
        DataRequired(message="El RFC es obligatorio"),
        Length(min=12, max=13, message="El RFC debe tener entre 12 y 13 caracteres")
    ])
    contacto_nombre = StringField('Nombre de Contacto', validators=[
        DataRequired(message="El nombre es obligatorio"),
        Length(max=100)
        ])
    estatus = BooleanField('Activo')
    telefono = StringField('Teléfono', validators=[
        DataRequired(message="El teléfono es obligatorio"),
        Length(max=15, message="El campo no puede tener más de 10 dígitos numéricos") 
    ])    
    categoria_insumo = StringField('Categoría de Insumo', validators=[Length(max=100)])
    submit = SubmitField('Guardar Proveedor') 

def validate_razon_social(self, field):
        uid = request.view_args.get('uid')
        check = Proveedor.query.filter_by(razon_social=field.data.upper()).first()
        
        # Solo lanza error si lo encuentra Y no es el mismo que estamos editando
        if check and check.uuid_proveedor != uid:
            raise ValidationError('Esta razón social ya está registrada en el sistema.')
        
def validate_telefono(self, field):
        if field.data:
            uid = request.view_args.get('uid')
            dato_limpio = re.sub(r'\D', '', str(field.data))
            
            # Validación de Unicidad acoplada
            check = Proveedor.query.filter_by(telefono=dato_limpio).first()
            if check and check.uuid_proveedor != uid:
                raise ValidationError('Este número de teléfono ya está en uso.')
            
            if not str(field.data).replace("-", "").replace(" ", "").isdigit():
                raise ValidationError('Solo se permiten números.')
            if len(dato_limpio) != 10:
                raise ValidationError('Deben ser exactamente 10 dígitos.')
                
def validate_rfc(self, field):
        if field.data:
            uid = request.view_args.get('uid')
            
            check = Proveedor.query.filter_by(rfc=field.data.upper()).first()
            if check and check.uuid_proveedor != uid:
                raise ValidationError('Este RFC ya pertenece a otro proveedor.')
            
            pattern = r'^[A-Z&Ñ]{3,4}\d{6}[A-Z0-9]{3}$'
            if not re.match(pattern, field.data.upper()):
                raise ValidationError('El formato del RFC es inválido (Ej: ABC123456XYZ)')