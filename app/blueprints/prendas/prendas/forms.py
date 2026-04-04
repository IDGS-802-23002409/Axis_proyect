from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, IntegerField, SelectField, HiddenField
from wtforms.validators import DataRequired, NumberRange, Length, Optional


TALLAS = [
    ('XSS', 'XSS'), ('XS', 'XS'), ('S', 'S'), ('M', 'M'),
    ('L', 'L'), ('XL', 'XL'), ('XXL', 'XXL'), ('Unica', 'Única'),
]


class PrendaForm(FlaskForm):
    """Alta y edición de ProductoTerminado."""
    uuid_modelo = SelectField(
        'Modelo',
        validators=[DataRequired(message='Selecciona un modelo.')],
    )
    talla = SelectField(
        'Talla',
        choices=TALLAS,
        validators=[DataRequired()],
    )
    sku_especifico = StringField(
        'SKU Específico',
        validators=[DataRequired(), Length(max=50)],
    )
    precio_venta = DecimalField(
        'Precio de Venta',
        places=2,
        validators=[DataRequired(), NumberRange(min=0.01, message='El precio debe ser mayor a 0.')],
    )
    costo_confeccion = DecimalField(
        'Costo de Confección',
        places=2,
        default=0.00,
        validators=[Optional(), NumberRange(min=0)],
    )
    merma_estimada_pct = DecimalField(
        'Merma Estimada (%)',
        places=2,
        default=0.00,
        validators=[Optional(), NumberRange(min=0, max=100)],
    )
    stock_minimo_alerta = IntegerField(
        'Stock Mínimo de Alerta',
        default=0,
        validators=[Optional(), NumberRange(min=0)],
    )


class AjustePrecioForm(FlaskForm):
    """Formulario mínimo para actualizar solo el precio de venta."""
    precio_venta = DecimalField(
        'Precio de Venta',
        places=2,
        validators=[DataRequired(), NumberRange(min=0.01)],
    )


class BomLineaForm(FlaskForm):
    """Añadir/editar una línea en la receta (BOM) de una prenda."""
    uuid_insumo = SelectField(
        'Insumo',
        validators=[DataRequired(message='Selecciona un insumo.')],
    )
    cantidad_requerida = DecimalField(
        'Cantidad',
        places=4,
        validators=[DataRequired(), NumberRange(min=0.0001)],
    )
    unidad_medida = SelectField(
        'Unidad',
        choices=[
            ('m', 'Metros'), ('kg', 'Kilogramos'),
            ('ud', 'Unidades'), ('ml', 'Mililitros'),
        ],
        validators=[DataRequired()],
    )
    uuid_linea = HiddenField()  # poblado en edición