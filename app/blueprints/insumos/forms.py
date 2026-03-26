from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SelectField, SubmitField
from wtforms.validators import DataRequired, Optional, NumberRange, Length

class InsumoForm(FlaskForm):
    sku = StringField(
        'SKU',
        validators=[
            Optional(),
            Length(max=50, message="Máximo 50 caracteres")
        ]
    )

    nombre = StringField(
        'Nombre',
        validators=[
            DataRequired(message="El nombre es obligatorio"),
            Length(max=100)
        ]
    )

    uuid_categoria = SelectField(
        'Categoría',
        choices=[],
        coerce=str,
        validators=[Optional()]
    )

    unidad_medida = SelectField(
        'Unidad de Medida',
        choices=[
            ('METRO', 'Metro(s)'),
            ('PIEZA', 'Pieza(s)')
        ],
        validators=[DataRequired(message="La unidad de medida es obligatoria")]
    )

    stock_minimo_alerta = DecimalField(
        'Stock Mínimo',
        default=0,
        validators=[
            DataRequired(message="El stock mínimo es obligatorio"),
            NumberRange(min=0, message="Debe ser mayor o igual a 0")
        ]
    )

    submit = SubmitField('Guardar y salir')
    submit_add = SubmitField('Guardar y continuar')