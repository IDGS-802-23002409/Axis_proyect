from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length
from wtforms import DecimalField
from wtforms.validators import NumberRange

class CompraEncabezadoForm(FlaskForm):

    folio_factura = StringField(
        'Folio de Factura',
        validators=[
            DataRequired(message="El folio es obligatorio"),
            Length(max=50)
        ]
    )

    uuid_proveedor = SelectField(
        'Proveedor',
        validators=[DataRequired(message="Selecciona un proveedor")],
        coerce=str
    )

    uuid_usuario_registro = SelectField(
        'Usuario',
        validators=[DataRequired(message="Selecciona un usuario")],
        coerce=str
    )

    estatus = SelectField(
        'Estatus',
        choices=[
            ('PENDIENTE', 'Pendiente'),
            ('RECIBIDO', 'Recibido'),
            ('CANCELADO', 'Cancelado')
        ],
        default='PENDIENTE'
    )

    submit = SubmitField('Guardar Compra')



class CompraDetalleForm(FlaskForm):

    uuid_insumo = SelectField(
        'Insumo',
        validators=[DataRequired(message="Selecciona un insumo")],
        coerce=str
    )

    cantidad_comprada = DecimalField(
        'Cantidad',
        validators=[
            DataRequired(message="La cantidad es obligatoria"),
            NumberRange(min=0.0001, message="Debe ser mayor a 0")
        ],
        places=4
    )

    costo_unitario_compra = DecimalField(
        'Costo Unitario',
        validators=[
            DataRequired(message="El costo es obligatorio"),
            NumberRange(min=0, message="No puede ser negativo")
        ],
        places=2
    )

    submit = SubmitField('Agregar Producto')