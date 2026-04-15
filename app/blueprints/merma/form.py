from flask_wtf import FlaskForm
from wtforms import (
    SelectField,
    DecimalField,
    TextAreaField,
    BooleanField
)
from wtforms.validators import DataRequired, NumberRange, Optional


class MermaForm(FlaskForm):
    """Formulario base para registro de merma."""

    # ─────────────────────────────
    # CLASIFICACIÓN
    # ─────────────────────────────
    tipo_merma = SelectField(
        "Tipo de Merma",
        choices=[
            ("TELA", "Tela"),
            ("INSUMO", "Insumo"),
            ("PRODUCTO", "Producto")
        ],
        validators=[DataRequired()]
    )

    tipo_evento = SelectField(
        "Tipo de Evento",
        choices=[
            ("DESPERDICIO_TOTAL", "Desperdicio Total"),
            ("DESPERDICIO_PARCIAL", "Desperdicio Parcial"),
            ("DEFECTO_CALIDAD", "Defecto de Calidad"),
            ("ERROR_OPERARIO", "Error de Operario"),
            ("DANIO_ACCIDENTAL", "Daño Accidental"),
            ("DEFECTO_ORIGEN", "Defecto de Origen"),
            ("AJUSTE_INVENTARIO", "Ajuste de Inventario")
        ],
        validators=[DataRequired()]
    )

    motivo = SelectField(
        "Motivo",
        choices=[
            ("CORTE_INCORRECTO", "Corte Incorrecto"),
            ("TELA_DEFECTUOSA", "Tela Defectuosa"),
            ("COSTURA_INCORRECTA", "Costura Incorrecta"),
            ("MANCHA", "Mancha"),
            ("ROTURA", "Rotura"),
            ("MEDIDA_ERRONEA", "Medida Errónea"),
            ("PRUEBA_MUESTRA", "Prueba / Muestra"),
            ("MAL_USO_MAQUINA", "Mal Uso de Máquina"),
            ("OTRO", "Otro")
        ],
        validators=[Optional()]
    )

    # ─────────────────────────────
    # RELACIONES (Para CRUD manual)
    # ─────────────────────────────
    uuid_insumo = SelectField("Insumo", choices=[], validators=[Optional()])
    uuid_rollo = SelectField("Rollo", choices=[], validators=[Optional()])
    uuid_producto = SelectField("Producto Terminado", choices=[], validators=[Optional()])

    # ─────────────────────────────
    # DATO REAL (Usado para registros individuales)
    # ─────────────────────────────
    cantidad = DecimalField(
        "Cantidad",
        places=4,
        validators=[
            Optional(),
            NumberRange(min=0)
        ]
    )

    es_total = BooleanField("Merma Total", default=True)

    observaciones = TextAreaField(
        "Observaciones",
        validators=[Optional()]
    )