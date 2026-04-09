from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length

class RecetaForm(FlaskForm):
    nombre_receta = StringField(
        "Nombre de la Receta",
        validators=[
            DataRequired(message="El nombre de la receta es requerido"),
            Length(min=3, max=100, message="Debe tener entre 3 y 100 caracteres")
        ],
        render_kw={"placeholder": "Ej: Hoodie Talla M Negro..."}
    )

    talla = SelectField(
        "Talla",
        choices=[
            ('XSS', 'XSS'),
            ('XS', 'XS'),
            ('S', 'S'),
            ('M', 'M'),
            ('L', 'L'),
            ('XL', 'XL'),
            ('XXL', 'XXL'),
            ('Unica', 'Única')
        ],
        validators=[DataRequired(message="Selecciona una talla")],
        render_kw={"placeholder": "Selecciona una talla"}
    )

    uuid_categoria = SelectField(
        "Categoría",
        validators=[DataRequired(message="Selecciona una categoría")],
        coerce=str,
        render_kw={"placeholder": "Selecciona una categoría"}
    )

    instrucciones_proceso = TextAreaField(
        "Instrucciones de la Receta",
        validators=[
            DataRequired(message="Agrega las instrucciones de la receta"),
            Length(min=1, max=5000, message="Debe tener entre 1 y 5000 caracteres")
        ],
        render_kw={"rows": 6, "placeholder": "Describe paso a paso la receta..."}
    )

    submit = SubmitField("Guardar")