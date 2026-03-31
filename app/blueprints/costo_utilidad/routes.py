from flask import render_template
from app.blueprints.costo_utilidad import costo_utilidad_bp
from flask_security import login_required, roles_required

@costo_utilidad_bp.route('/costo-utilidad', methods=['GET', 'POST'])
@login_required
@roles_required('admin')
def index():
 

    return render_template(
        'produccion/costo_utilidad/index.html'
    )
