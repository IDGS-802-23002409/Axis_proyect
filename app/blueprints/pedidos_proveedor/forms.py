from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FieldList, FormField, DecimalField, SubmitField
from wtforms.validators import DataRequired, Optional

class PedidoProveedorForm(FlaskForm):
    folio_pedido = StringField('Folio del Pedido', validators=[DataRequired()])
    uuid_proveedor = SelectField('Proveedor', coerce=str, validators=[DataRequired()])
    estatus = SelectField('Estatus Inicial', choices=[
        ('Pendiente', 'Pendiente'),
        ('Aprobado', 'Aprobado')
    ], validators=[DataRequired()])
    submit = SubmitField('Guardar Pedido')
