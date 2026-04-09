import os
import uuid
from werkzeug.utils import secure_filename
from flask import flash, redirect, render_template, request, url_for, current_app
from flask_security import login_required
from app.blueprints.modelos import modelos_bp
from app.blueprints.modelos.form import ModeloForm
from app.models.modelos_productos import ModeloRopa
from app.utils.database_connection import db

def get_upload_folder():
    """Garantiza la existencia y retorna la ruta local de las fotos de modelos."""
    upload_folder = os.path.join(current_app.root_path, 'static', 'uploads', 'modelos')
    os.makedirs(upload_folder, exist_ok=True)
    return upload_folder

@modelos_bp.route("/")
@login_required
def index():
    q = request.args.get('q', '').strip()
    # Solo modelos activos en la vista principal
    modelos = ModeloRopa.query.filter_by(estatus='ACTIVO')
    
    if q:
        modelos = modelos.filter(ModeloRopa.nombre_modelo.ilike(f"%{q}%"))
        
    modelos = modelos.all()
    total_modelos = ModeloRopa.query.filter_by(estatus='ACTIVO').count()

    return render_template(
        "produccion/modelos/index.html",
        modelos=modelos,
        total_modelos=total_modelos,
        q=q
    )

@modelos_bp.route("/paperera")
@modelos_bp.route("/trash")
@login_required
def trash():
    """Muestra los modelos que han sido desactivados (estatus='INACTIVO')."""
    modelos_inactivos = ModeloRopa.query.filter_by(estatus='INACTIVO').all()
    return render_template("produccion/modelos/trash.html", modelos=modelos_inactivos)

@modelos_bp.route("/registro", methods=["GET", "POST"])
@login_required
def registro_modelo():
    form = ModeloForm()
    
    if request.method == "POST" and form.validate():
        existe = ModeloRopa.query.filter_by(nombre_modelo=form.nombre_modelo.data).first()
        if existe:
            flash("Ya existe un modelo con ese nombre", "error")
            return redirect(url_for('modelos.registro_modelo'))

        imagen_url = "/static/images/default/default-image.png"
        
        # Procesamiento de la imagen
        if form.imagen.data:
            file = form.imagen.data
            filename = secure_filename(f"{uuid.uuid4().hex}_{file.filename}")
            filepath = os.path.join(get_upload_folder(), filename)
            file.save(filepath)
            # Guardar la url parcial estática esperada por el navegador
            imagen_url = f"/static/uploads/modelos/{filename}"

        nuevo_modelo = ModeloRopa(
            nombre_modelo=form.nombre_modelo.data,
            descripcion=form.descripcion.data,
            uuid_categoria=form.uuid_categoria.data,
            imagen_url=imagen_url
        )
        
        db.session.add(nuevo_modelo)
        db.session.commit()
        flash("Modelo creado correctamente", "success")
        return redirect(url_for('modelos.index'))

    return render_template("produccion/modelos/registro_modelo.html", form=form)

@modelos_bp.route("/editar/<uuid_modelo>", methods=["GET", "POST"])
@login_required
def update_modelo(uuid_modelo):
    modelo = ModeloRopa.query.get_or_404(uuid_modelo)

    if request.method == "POST":
        form = ModeloForm(request.form, obj=modelo)
        if form.validate():
            existe = ModeloRopa.query.filter(ModeloRopa.nombre_modelo==form.nombre_modelo.data, ModeloRopa.uuid_modelo!=uuid_modelo).first()
            if existe:
                flash("Ya existe otro modelo con ese nombre", "error")
                return redirect(url_for('modelos.update_modelo', uuid_modelo=uuid_modelo))

            modelo.nombre_modelo = form.nombre_modelo.data
            modelo.descripcion = form.descripcion.data
            modelo.uuid_categoria = form.uuid_categoria.data
            
            # Si envió una imagen nueva, procesar la nueva
            if request.files and 'imagen' in request.files:
                file = request.files['imagen']
                if file.filename != '':
                    filename = secure_filename(f"{uuid.uuid4().hex}_{file.filename}")
                    filepath = os.path.join(get_upload_folder(), filename)
                    file.save(filepath)
                    # Opcionalmente podrías borrar el fichero local antiguo
                    modelo.imagen_url = f"/static/uploads/modelos/{filename}"

            db.session.commit()
            flash("Modelo actualizado correctamente", "success")
            return redirect(url_for('modelos.index'))
    else:
        form = ModeloForm(obj=modelo)

    return render_template("produccion/modelos/update_modelo.html", form=form, modelo=modelo)

@modelos_bp.route("/eliminar/<uuid_modelo>", methods=["POST"])
@login_required
def delete_modelo(uuid_modelo):
    """Soft delete: cambia el estatus a INACTIVO."""
    modelo = ModeloRopa.query.get_or_404(uuid_modelo)
    
    # Si quisieras permitir borrar físicamente si NO tiene dependencias:
    # if not modelo.productos:
    #     db.session.delete(modelo)
    # else:
    
    modelo.estatus = 'INACTIVO'
    db.session.commit()

    flash(f"Modelo '{modelo.nombre_modelo}' movido a inactivos.", "info")
    return redirect(url_for('modelos.index'))

@modelos_bp.route("/restore/<uuid_modelo>", methods=["POST"])
@login_required
def restore(uuid_modelo):
    """Restaura un modelo cambiando su estatus a ACTIVO."""
    modelo = ModeloRopa.query.get_or_404(uuid_modelo)
    modelo.estatus = 'ACTIVO'
    db.session.commit()
    flash(f"Modelo '{modelo.nombre_modelo}' restaurado correctamente.", "success")
    return redirect(url_for('modelos.trash'))

@modelos_bp.route("/ver/<uuid_modelo>")
@login_required
def ver_modelo(uuid_modelo):
    modelo = ModeloRopa.query.get_or_404(uuid_modelo)
    return render_template("produccion/modelos/ver.html", modelo=modelo)
