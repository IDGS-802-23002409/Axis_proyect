from flask_wtf import FlaskForm
from wtforms import SelectField, DateField, SubmitField
from wtforms.validators import Optional


class InventarioForm(FlaskForm):

    uuid_insumo = SelectField(
        "Insumo",
        choices=[],
        coerce=str,   # 🔥 IMPORTANTE
        validators=[Optional()]
    )

    tipo_movimiento = SelectField(
        "Tipo",
        choices=[
            ("", "Todos"),
            ("ENTRADA", "Entradas"),
            ("SALIDA", "Salidas")
        ],
        validators=[Optional()]
    )

    subtipo = SelectField(
        "Subtipo",
        choices=[
            ("", "Todos"),
            ("COMPRA", "Compras"),
            ("CONSUMO", "Consumo"),
            ("MERMA", "Merma")
        ],
        validators=[Optional()]
    )

    fecha_inicio = DateField(
        "Fecha inicio",
        format="%Y-%m-%d",
        validators=[Optional()]
    )

    fecha_fin = DateField(
        "Fecha fin",
        format="%Y-%m-%d",
        validators=[Optional()]
    )

    submit = SubmitField("Filtrar")