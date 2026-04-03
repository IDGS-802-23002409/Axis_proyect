from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DecimalField, IntegerField, RadioField
from wtforms import validators
from app.models.modelos_productos import ModeloRopa


class ProductoTerminadoForm(FlaskForm):

    modelo = SelectField('Modelo', coerce=str, validators=[
        validators.DataRequired(message='El modelo es requerido')
    ])

    explosion = SelectField('Receta (Explosión)', coerce=str, validators=[
        validators.DataRequired(message='La receta es requerida')
    ])

    sku_especifico = StringField('SKU específico', [
        validators.DataRequired(message='SKU es requerido'),
        validators.Length(max=50)
    ])

    talla = SelectField('Talla', coerce=str, choices=[
        ('XSS', 'XSS'), ('XS', 'XS'), ('S', 'S'), ('M', 'M'),
        ('L', 'L'), ('XL', 'XL'), ('XXL', 'XXL'), ('Unica', 'Única'),
    ], validators=[validators.DataRequired(message='La talla es requerida')])

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

        modelos = ModeloRopa.query.order_by(ModeloRopa.nombre_modelo).all()
        self.modelo.choices = [(m.uuid_modelo, m.nombre_modelo) for m in modelos]

        from app.models.explosion_materiales import ExplosionMaterialesCabecera
        explosiones = ExplosionMaterialesCabecera.query.filter_by(estatus='ACTIVO').all()
        self.explosion.choices = [(e.uuid_explosion, f"Receta {e.uuid_explosion[:8]}") for e in explosiones]