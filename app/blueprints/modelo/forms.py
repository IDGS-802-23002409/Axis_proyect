from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length
from app.models.categorias import Categoria  # Importa tu modelo de categorías

class ModeloForm(FlaskForm):
    nombre_modelo = StringField(
        'Nombre del Modelo',
        validators=[DataRequired(message="El nombre es obligatorio"), Length(max=100)]
    )
    descripcion = TextAreaField(
        'Descripción',
        validators=[Length(max=500)]
    )
    uuid_categoria = SelectField(
        'Categoría',
        coerce=str,
        validators=[DataRequired(message="Debe seleccionar una categoría")]
    )
    submit = SubmitField('Guardar')

    def __init__(self, *args, **kwargs):
        super(ModeloForm, self).__init__(*args, **kwargs)
        # Cargar solo categorías visibles
        categorias = Categoria.query.filter_by(estatus_visible=True).all()
        # Ajusta para usar el nombre correcto del campo en tu modelo
        self.uuid_categoria.choices = [(c.uuid_categoria, c.nombre) for c in categorias]