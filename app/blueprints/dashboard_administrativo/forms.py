from flask_wtf import FlaskForm
from wtforms import DateField, SelectField
from wtforms.validators import Optional

class DashboardFilterForm(FlaskForm):
    fecha_inicio = DateField('Desde', validators=[Optional()])
    fecha_fin = DateField('Hasta', validators=[Optional()])
    categoria = SelectField('Categoría', choices=[('all', 'Todas')], validators=[Optional()])