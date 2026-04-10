from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError, Optional
from app.models.proveedores import Proveedor
import re
from flask import request


def _coerce_uuid_categoria(val):
    if val is None or val == "":
        return None
    return str(val)


class ProveedorForm(FlaskForm):
    razon_social = StringField('Razón Social', validators=[
        DataRequired(message="La razón social es obligatoria"),
        Length(max=150)
    ])
    rfc = StringField('RFC', validators=[
        DataRequired(message="El RFC es obligatorio"),
        Length(min=12, max=13, message="El RFC debe tener entre 12 y 13 caracteres")
    ])
    contacto_nombre = StringField('Nombre de Contacto', validators=[
        DataRequired(message="El nombre es obligatorio"),
        Length(max=100)
    ])
    estatus = BooleanField('Activo')
    telefono = StringField('Teléfono', validators=[
        DataRequired(message="El teléfono es obligatorio"),
        Length(max=15, message="El campo no puede tener más de 10 dígitos numéricos")
    ])
    uuid_categoria = SelectField(
        'Categoría de Insumo',
        choices=[],
        validators=[Optional()],
        coerce=_coerce_uuid_categoria,
    )
    submit = SubmitField('Guardar Proveedor')

    def __init__(self, *args, **kwargs):
        super(ProveedorForm, self).__init__(*args, **kwargs)
        from sqlalchemy import or_
        from app.models.categorias import Categoria
        from app.utils.database_connection import db

        used_uuids = (
            db.session.query(Proveedor.uuid_categoria)
            .filter(Proveedor.uuid_categoria.isnot(None))
            .distinct()
        )
        categorias = (
            Categoria.query.filter(
                Categoria.tipo == "Insumo",
                or_(
                    Categoria.estatus_visible == True,
                    Categoria.uuid_categoria.in_(used_uuids),
                ),
            )
            .order_by(Categoria.nombre)
            .all()
        )
        self.uuid_categoria.choices = [("", "Seleccione una categoría")] + [
            (c.uuid_categoria, c.nombre) for c in categorias
        ]

    def validate_razon_social(self, field):
        uid = request.view_args.get('uid')
        check = Proveedor.query.filter_by(razon_social=field.data.upper()).first()

        if check and check.uuid_proveedor != uid:
            raise ValidationError('Esta razón social ya está registrada en el sistema.')

    def validate_telefono(self, field):
        if field.data:
            uid = request.view_args.get('uid')
            dato_limpio = re.sub(r'\D', '', str(field.data))

            check = Proveedor.query.filter_by(telefono=dato_limpio).first()
            if check and check.uuid_proveedor != uid:
                raise ValidationError('Este número de teléfono ya está en uso.')

            if not str(field.data).replace("-", "").replace(" ", "").isdigit():
                raise ValidationError('Solo se permiten números.')
            if len(dato_limpio) != 10:
                raise ValidationError('Deben ser exactamente 10 dígitos.')

    def validate_rfc(self, field):
        if field.data:
            uid = request.view_args.get('uid')

            check = Proveedor.query.filter_by(rfc=field.data.upper()).first()
            if check and check.uuid_proveedor != uid:
                raise ValidationError('Este RFC ya pertenece a otro proveedor.')

            pattern = r'^[A-Z&Ñ]{3,4}\d{6}[A-Z0-9]{3}$'
            if not re.match(pattern, field.data.upper()):
                raise ValidationError('El formato del RFC es inválido (Ej: ABC123456XYZ)')
