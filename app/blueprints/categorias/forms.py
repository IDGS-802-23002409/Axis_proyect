from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Optional, Length


class CategoriaForm(FlaskForm):
    nombre = StringField(
        "Nombre",
        validators=[
            DataRequired(message="El nombre es obligatorio"),
            Length(max=50, message="Máximo 50 caracteres")
        ]
    )

    descripcion = TextAreaField(
        "Descripción",
        validators=[
            Optional(),
            Length(max=255, message="Máximo 255 caracteres")
        ]
    )

    estatus_visible = BooleanField(
        "Visible",
        default=True
    )

    submit = SubmitField("Guardar")