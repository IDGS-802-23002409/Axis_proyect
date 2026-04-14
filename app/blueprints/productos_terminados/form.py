from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DecimalField, IntegerField, RadioField
from flask_wtf.file import FileField, FileAllowed
from wtforms import validators


class ProductoTerminadoForm(FlaskForm):

    explosion = SelectField('Receta (Explosión)', coerce=str, validators=[
        validators.DataRequired(message='La receta es requerida')
    ])

    sku_especifico = StringField('SKU específico', [
        validators.DataRequired(message='SKU es requerido'),
        validators.Length(max=50)
    ])

    imagen = FileField('Imagen del producto', validators=[
    FileAllowed(['jpg', 'png', 'jpeg', 'webp'], 'Solo imágenes (jpg, png, jpeg, webp)')
    ])
    
    precio_venta = DecimalField('Precio de venta', places=2, validators=[
        validators.InputRequired(message='Precio requerido'),
        validators.NumberRange(min=0, message='Precio debe ser >= 0')
    ])

    stock_minimo_alerta = IntegerField('Stock mínimo', validators=[
        validators.Optional(),  
        validators.NumberRange(min=0, message='Stock mínimo debe ser >= 0')
    ])

    active = RadioField('Estatus', choices=[
        (1, 'Activo'),
        (0, 'Inactivo')
    ], coerce=int, default=1)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        from app.models.explosion_materiales import ExplosionMaterialesCabecera
        explosiones = ExplosionMaterialesCabecera.query.filter_by(estatus='ACTIVO').all()
        self.explosion.choices = [(e.uuid_explosion, f"{e.nombre_receta} ({e.talla})") for e in explosiones]