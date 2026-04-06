from . import recetas_bp
from flask_security import login_required, roles_required, hash_password,roles_accepted,current_user
from .forms import RecetaForm
from flask import render_template, redirect, url_for, flash, request
from sqlalchemy import func
from app.utils.database_connection import db
from app.models.insumos import Insumo
from app.models.modelos_productos import ProductoTerminado
from app.models.explosion_materiales import ExplosionMaterialesDetalle,ExplosionMaterialesCabecera
from app.models.usuarios import Usuario



# ── INDEX CON BÚSQUEDA Y SOLO RECETAS ACTIVAS ──────────────────────────────
@recetas_bp.route('/', methods=['GET'])
@login_required
@roles_accepted('admin', 'gerente', 'produccion')
def index():
    search_query = request.args.get('q', '').strip()  # obtener texto de búsqueda

    # Filtrar solo recetas activas
    query = ExplosionMaterialesCabecera.query.filter_by(estatus='ACTIVO')

    if search_query:
        # Buscar por instrucciones o uuid_explosion
        query = query.filter(
            ExplosionMaterialesCabecera.instrucciones_proceso.ilike(f'%{search_query}%') |
            ExplosionMaterialesCabecera.uuid_explosion.ilike(f'%{search_query}%')
        )

    # Ejecutar la consulta y obtener la lista
    recetas_list = query.all()  # <- asegurarnos de no usar 'recetas' antes

    return render_template(
        'produccion/recetas/index.html', 
        recetas=recetas_list,   # <- aquí pasamos la variable correcta
        search_query=search_query
    )

@recetas_bp.route('/create', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin', 'gerente', 'produccion')
def create():
    insumos_list = Insumo.query.filter_by(estatus='ACTIVO').all()
    form = RecetaForm()

    if form.validate_on_submit():
        # --- Leer insumos desde el formulario ---
        insumos_ids = request.form.getlist('uuid_insumo[]')
        consumos = request.form.getlist('consumo_teorico_unitario[]')
        anchos = request.form.getlist('ancho_referencia[]')

        errores = []
        detalles_validos = []

        # Validar insumos antes de crear la cabecera
        for i, insumo_id in enumerate(insumos_ids):
            insumo_obj = Insumo.query.get(insumo_id)
            if not insumo_obj:
                errores.append(f'El insumo con ID {insumo_id} no existe')
                continue

            unidad = insumo_obj.unidad_medida  # PIEZA o ROLLO según tu modelo

            # Validar consumo según unidad
            try:
                consumo = float(consumos[i])
            except (ValueError, IndexError):
                errores.append(f'El consumo del insumo "{insumo_obj.nombre}" es inválido')
                continue

            if unidad == "PIEZA":
                if consumo <= 0 or not consumo.is_integer():
                    errores.append(f'El consumo del insumo "{insumo_obj.nombre}" debe ser un número entero positivo')
                    continue
                consumo = int(consumo)
            else:  # ROLLO
                if consumo <= 0:
                    errores.append(f'El consumo del insumo "{insumo_obj.nombre}" debe ser mayor a 0')
                    continue

            # Validar ancho solo si es rollo
            try:
                ancho = float(anchos[i]) if anchos[i] else None
                if unidad == "ROLLO" and (ancho is None or ancho <= 0):
                    errores.append(f'El ancho del insumo "{insumo_obj.nombre}" debe ser mayor a 0')
                    continue
            except (ValueError, IndexError):
                errores.append(f'El ancho del insumo "{insumo_obj.nombre}" es inválido')
                continue

            detalles_validos.append({
                "insumo": insumo_obj,
                "consumo": consumo,
                "ancho": ancho
            })

        # Si hubo errores, no se guarda nada y se muestran mensajes
        if errores:
            for e in errores:
                flash(e, 'error')
            return redirect(request.url)

        # --- Crear cabecera de receta ---
        nueva_receta = ExplosionMaterialesCabecera(
            instrucciones_proceso=form.instrucciones_proceso.data.strip(),
            estatus='ACTIVO',
            uuid_usuario=current_user.uuid_usuario
        )
        db.session.add(nueva_receta)
        db.session.flush()  # Genera uuid_explosion sin hacer commit aún

        # --- Crear detalles ---
        for detalle in detalles_validos:
            nuevo_detalle = ExplosionMaterialesDetalle(
                uuid_explosion=nueva_receta.uuid_explosion,
                uuid_insumo=detalle["insumo"].uuid_insumo,
                consumo_teorico_unitario=detalle["consumo"],
                ancho_referencia=detalle["ancho"]
            )
            db.session.add(nuevo_detalle)

        db.session.commit()
        flash('Receta creada con éxito. Ahora puedes crear el producto terminado asociado.', 'success')
        return redirect(url_for('recetas_bp.index'))

    # Mostrar errores del formulario de cabecera si los hubiera
    if form.errors:
        for campo, errores_campo in form.errors.items():
            for e in errores_campo:
                flash(f"{campo}: {e}", 'error')

    return render_template(
        'produccion/recetas/create.html',
        form=form,
        insumos=insumos_list
    )

# ── VIEW ──────────────────────────────
@recetas_bp.route('/ver/<uuid_explosion>')
@login_required
@roles_accepted('admin', 'gerente', 'produccion')
def ver(uuid_explosion):
    # Obtener la receta por UUID
    receta = ExplosionMaterialesCabecera.query.filter_by(uuid_explosion=uuid_explosion).first_or_404()

    # Obtener los insumos asociados
    detalles = ExplosionMaterialesDetalle.query.filter_by(uuid_explosion=uuid_explosion).all()

    # Preparar lista de insumos con sus datos completos
    insumos_info = []
    for detalle in detalles:
        insumos_info.append({
            'nombre': detalle.insumo.nombre,
            'consumo_teorico_unitario': float(detalle.consumo_teorico_unitario),
            'ancho_referencia': float(detalle.ancho_referencia) if detalle.ancho_referencia else None,
            'unidad_medida': detalle.insumo.unidad_medida
        })

    # Obtener info del usuario que creó la receta
    usuario = None
    if receta.uuid_usuario:
        usuario = Usuario.query.filter_by(uuid_usuario=receta.uuid_usuario).first()  # <-- aquí usamos tu modelo Usuario

    return render_template(
        'produccion/recetas/ver.html',
        receta=receta,
        insumos=insumos_info,
        usuario=usuario
    )

# ── ELIMINACIÓN LÓGICA ──────────────────────────────
@recetas_bp.route("/delete/<string:uuid_explosion>", methods=["POST"])
@login_required
@roles_accepted('admin', 'gerente', 'produccion')
def delete(uuid_explosion):
    receta = ExplosionMaterialesCabecera.query.get_or_404(uuid_explosion)

    if receta.estatus == 'INACTIVO':
        flash("La receta ya está inactiva", "warning")
        return redirect(url_for('recetas_bp.index'))

    # Aquí no borramos, solo desactivamos
    receta.estatus = 'INACTIVO'
    db.session.commit()

    flash("Receta desactivada correctamente", "success")
    return redirect(url_for('recetas_bp.index'))


# ── RESTAURAR RECETA ──────────────────────────────
@recetas_bp.route("/restore/<string:uuid_explosion>", methods=["POST"])
@login_required
@roles_accepted('admin', 'gerente', 'produccion')
def restore(uuid_explosion):
    receta = ExplosionMaterialesCabecera.query.get_or_404(uuid_explosion)

    if receta.estatus == 'ACTIVO':
        flash("La receta ya está activa", "warning")
        return redirect(url_for('recetas_bp.index'))

    receta.estatus = 'ACTIVO'
    db.session.commit()

    flash("Receta reactivada correctamente", "success")
    return redirect(url_for('recetas_bp.index'))


# ── TRASH / RECETAS INACTIVAS ──────────────────────────────
@recetas_bp.route("/trash")
@login_required
@roles_accepted('admin', 'gerente', 'produccion')
def trash():
    recetas = ExplosionMaterialesCabecera.query.filter_by(estatus='INACTIVO').all()
    return render_template("produccion/recetas/trash.html", recetas=recetas)