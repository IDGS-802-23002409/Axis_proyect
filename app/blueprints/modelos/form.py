from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField
from flask_wtf.file import FileField, FileAllowed
from wtforms import validators
from app.models.categorias import Categoria

class ModeloForm(FlaskForm):
    nombre_modelo = StringField('Nombre del modelo', [
        validators.DataRequired(message="El nombre es requerido"),
        validators.Length(min=3, max=100, message="Debe tener entre 3 y 100 caracteres")
    ])

    descripcion = TextAreaField('Descripción detallada', [
        validators.Optional()
    ])

    uuid_categoria = SelectField('Categoría', coerce=str, validators=[
        validators.DataRequired(message="La categoría es obligatoria")
    ])

    imagen = FileField('Imagen del producto', validators=[
        FileAllowed(['jpg', 'png', 'jpeg', 'webp'], 'Solo imágenes (jpg, png, jpeg, webp)')
    ])

    def __init__(self, *args, obj=None, **kwargs):
        super().__init__(*args, obj=obj, **kwargs)
        self.obj = obj
        try:
            # Poblamos el select desde la bd
            categorias = Categoria.query.all()
            self.uuid_categoria.choices = [(c.uuid_categoria, c.nombre_categoria) for c in categorias]
        except Exception as e:
            self.uuid_categoria.choices = []
