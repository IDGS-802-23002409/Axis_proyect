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
    modelos = ModeloRopa.query
    
    if q:
        modelos = modelos.filter(ModeloRopa.nombre_modelo.ilike(f"%{q}%"))
        
    modelos = modelos.all()
    total_modelos = ModeloRopa.query.count()

    return render_template(
        "produccion/modelos/index.html",
        modelos=modelos,
        total_modelos=total_modelos,
        q=q
    )

@modelos_bp.route("/registro", methods=["GET", "POST"])
@login_required
def registro_modelo():
    form = ModeloForm()
    
    if request.method == "POST" and form.validate():
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
    modelo = ModeloRopa.query.get_or_404(uuid_modelo)
    
    # Validar si este modelo tiene tallas (productos_terminados) antes de eliminar
    if modelo.productos:
        flash("No se puede eliminar un modelo que tiene productos terminados (tallas) asociados.", "error")
        return redirect(url_for('modelos.index'))

    db.session.delete(modelo)
    db.session.commit()

    flash("Modelo eliminado correctamente", "success")
    return redirect(url_for('modelos.index'))
