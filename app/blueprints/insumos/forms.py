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

    #  UNIDAD DE COMPRA (ANTES era unidad_medida mal definida)
    unidad_medida = SelectField(
        'Unidad de compra',
        choices=[
            ('CAJA', 'Caja'),
            ('ROLLO', 'Rollo')
        ],
        validators=[DataRequired(message="La unidad de compra es obligatoria")]
    )

    #  CONTENIDO DE ESA UNIDAD
    contenido_cantidad = DecimalField(
        'Cantidad por unidad de compra',
        places=4,
        validators=[
            DataRequired(message="La cantidad es obligatoria"),
            NumberRange(min=0, message="Debe ser mayor a 0")
        ]
    )

    #  UNIDAD BASE (en qué realmente se mide)
    contenido_unidad_medida = SelectField(
        'Unidad base',
        choices=[
            ('METRO', 'Metro(s)'),
            ('PIEZA', 'Pieza(s)')
        ],
        validators=[DataRequired(message="La unidad base es obligatoria")]
    )

    #  STOCK MÍNIMO
    stock_minimo_alerta = DecimalField(
        'Stock mínimo',
        default=0,
        places=4,
        validators=[
            DataRequired(message="El stock mínimo es obligatorio"),
            NumberRange(min=0, message="Debe ser mayor o igual a 0")
        ]
    )

    submit = SubmitField('Guardar y salir')
    submit_add = SubmitField('Guardar y continuar')