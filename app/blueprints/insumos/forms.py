from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SelectField, SubmitField
from wtforms.validators import DataRequired, Optional, NumberRange, Length, ValidationError


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

    # UNIDAD DE COMPRA
    unidad_medida = SelectField(
        'Unidad de compra',
        choices=[
            ('PIEZA', 'Pieza'),
            ('ROLLO', 'Rollo')
        ],
        validators=[DataRequired(message="La unidad de compra es obligatoria")]
    )

    # CONTENIDO
    contenido_cantidad = DecimalField(
        'Cantidad por unidad de compra',
        places=4,
        validators=[
            Optional(),
            NumberRange(min=0, message="Debe ser mayor a 0")
        ]
    )

    # UNIDAD BASE
    contenido_unidad_medida = SelectField(
        'Unidad base',
        choices=[
            ('METRO', 'Metro(s)'),
            ('PIEZA', 'Pieza(s)')
        ],
        validators=[Optional()]
    )

    # NUEVO CAMPO: ANCHO
    ancho = DecimalField(
        'Ancho (metros)',
        places=2,
        validators=[
            Optional(),
            NumberRange(min=0, message="Debe ser mayor a 0")
        ]
    )

    # STOCK MÍNIMO
    modo_stock_minimo = SelectField(
        'Definir stock mínimo por',
        choices=[
            ('INTERNO', 'Contenido Interno (Metros/Piezas)'),
            ('COMPRA', 'Unidad de Compra (Rollos/Piezas)')
        ],
        default='INTERNO'
    )

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

    #  VALIDACIÓN PERSONALIZADA
    def validate(self, extra_validators=None):
        if not super().validate(extra_validators):
            return False

        # Si es ROLLO → ancho obligatorio
        if self.unidad_medida.data == "ROLLO":
            if self.ancho.data is None or self.ancho.data <= 0:
                self.ancho.errors.append("El ancho es obligatorio y debe ser mayor a 0 para insumos tipo ROLLO")
                return False

        return True