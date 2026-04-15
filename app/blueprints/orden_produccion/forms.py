from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Optional


class OrdenProduccionForm(FlaskForm):

    uuid_producto = SelectField(
        'Producto',
        choices=[],  # 
        validators=[DataRequired()],
        coerce=str
    )

    cantidad_a_producir = IntegerField(
        'Cantidad a producir',
        validators=[
            DataRequired(),
            NumberRange(min=1, max=500, message="La cantidad debe estar entre 1 y 500 unidades")
        ]
    )

    uuid_venta_detalle = SelectField(
        'Venta relacionada (opcional)',
        choices=[],  # 
        validators=[Optional()],
        coerce=str
    )

    submit = SubmitField('Guardar')