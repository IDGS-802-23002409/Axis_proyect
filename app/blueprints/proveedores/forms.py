from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class ProveedorForm(FlaskForm):
    razon_social = StringField('Razón Social', validators=[DataRequired(), Length(max=150)])
    rfc = StringField('RFC / ID Fiscal', validators=[DataRequired(), Length(max=20)])
    contacto_nombre = StringField('Nombre de Contacto', validators=[Length(max=100)])
    telefono = StringField('Teléfono', validators=[Length(max=20)])
    categoria_insumo = StringField('Categoría de Insumo', validators=[Length(max=100)])
    submit = SubmitField('Guardar Proveedor')