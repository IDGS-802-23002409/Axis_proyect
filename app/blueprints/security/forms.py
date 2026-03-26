from flask_security.forms import ConfirmRegisterForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length


class ExtendedRegisterForm(ConfirmRegisterForm):
    """Formulario extendido de registro con nombre completo."""
    nombre_completo = StringField(
        'Nombre Completo',
        validators=[
            DataRequired(message='El nombre completo es obligatorio.'),
            Length(min=3, max=150, message='El nombre debe tener entre 3 y 150 caracteres.')
        ]
    )
