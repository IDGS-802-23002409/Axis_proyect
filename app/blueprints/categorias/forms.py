from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, BooleanField, SubmitField, SelectField
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

    tipo = SelectField(
        "Tipo",
        choices=[("Insumo", "Insumo"), ("Prenda", "Prenda")],
        validators=[DataRequired(message="Selecciona un tipo")],
        coerce=str,
        default="Insumo",
    )

    imagen = FileField(
        "Imagen de categoría",
        validators=[
            Optional(),
            FileAllowed(['jpg', 'jpeg', 'png', 'webp'], 'Solo se permiten imágenes: jpg, png, webp')
        ]
    )

    estatus_visible = BooleanField(
        "Visible",
        default=True
    )

    submit = SubmitField("Guardar")