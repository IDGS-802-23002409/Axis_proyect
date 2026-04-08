from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class RecetaForm(FlaskForm):
    # Removed nombre_producto as it's not present in DB
    instrucciones_proceso = TextAreaField(
        "Instrucciones de la Receta",
        validators=[
            DataRequired(message="Agrega las instrucciones de la receta"),
            Length(min=1, max=5000, message="Debe tener entre 10 y 5000 caracteres")
        ],
        render_kw={"rows": 6, "placeholder": "Describe paso a paso la receta..."}
    )

    submit = SubmitField("Guardar")