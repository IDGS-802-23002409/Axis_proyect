from flask import render_template, redirect, url_for, flash, request, jsonify
from sqlalchemy.orm import joinedload
from . import proveedores_bp
from .forms import ProveedorForm
from app.models.proveedores import Proveedor
from app.models.usuarios import Usuario
from app.utils.database_connection import db
from flask_security import login_required, roles_accepted, roles_required, current_user
import uuid
import re
from datetime import datetime, timedelta


def _get_chart_data():
    """Genera datos de gráfica para los últimos 6 meses basado en proveedores activos."""
    today = datetime.utcnow()
    labels = []
    data = []
    for i in range(5, -1, -1):
        month = today - timedelta(days=i * 30)
        label = month.strftime("%b %Y")
        count = Proveedor.query.filter(
            Proveedor.fecha_creacion <= month, Proveedor.estatus == True
        ).count()
        labels.append(label)
        data.append(count)
    return labels, data


# --- CONSULTAR (LISTADO PRINCIPAL) ---
@proveedores_bp.route("/")
@login_required
@roles_accepted("admin", "gerente")
def index():
    q = request.args.get("q", "").strip()
    estatus = request.args.get("estatus", "").strip()

    # IMPORTANTE: inicializar query
    query = Proveedor.query

    # filtro por búsqueda
    if q:
        query = query.filter(
            (Proveedor.razon_social.ilike(f"%{q}%")) |
            (Proveedor.rfc.ilike(f"%{q}%"))
        )

    # filtro por estatus
    if estatus:
        if estatus.lower() == "activo":
            query = query.filter(Proveedor.estatus == True)
        elif estatus.lower() == "inactivo":
            query = query.filter(Proveedor.estatus == False)

    # ordenamiento final
    all_proveedores = query.order_by(Proveedor.fecha_creacion.desc()).all()

    form = ProveedorForm()
    chart_labels, chart_data = _get_chart_data()

    return render_template(
        "proveedores_index.html",
        proveedores=all_proveedores,
        form=form,
        chart_labels=chart_labels,
        chart_data=chart_data,
        top_producto={
            "nombre": "Shadow Hoodie",
            "unidades": 42,
            "monto": 12500.50,
            "imagen": None,
        },
        bottom_producto={
            "nombre": "Basic Tee White",
            "stock": 85,
            "imagen": None
        },
        q=q,
        estatus_filtro=estatus,
    )


# --- CREAR Y ACTUALIZAR ---
@proveedores_bp.route("/guardar", methods=["POST"])
@proveedores_bp.route("/editar/<string:uid>", methods=["POST"])
@login_required
@roles_accepted("admin", "gerente")
def guardar(uid=None):
    form = ProveedorForm()

    if form.validate_on_submit():
        if uid:
            proveedor = Proveedor.query.get_or_404(uid)
            msg = "Proveedor actualizado con éxito"
        else:
            proveedor = Proveedor(uuid_proveedor=str(uuid.uuid4()))
            proveedor.usuario_creo_uuid = current_user.uuid_usuario
            db.session.add(proveedor)
            msg = "Proveedor registrado con éxito"

        try:
            proveedor.razon_social = form.razon_social.data.upper()
            proveedor.rfc = form.rfc.data.upper() if form.rfc.data else ""
            proveedor.contacto_nombre = form.contacto_nombre.data

            if form.telefono.data:
                proveedor.telefono = re.sub(r"\D", "", form.telefono.data)

            if uid:
                proveedor.estatus = form.estatus.data

            db.session.commit()
            flash(msg, "success")
            return redirect(url_for("proveedores.index"))

        except Exception as e:
            db.session.rollback()
            flash(f"Error al guardar: {str(e)}", "error")
            return redirect(url_for("proveedores.index"))

    # Si falla la validación, recarga los errores
    all_proveedores = Proveedor.query.order_by(Proveedor.fecha_creacion.desc()).all()
    target_modal = "modal-update" if uid else "modal-registro"
    chart_labels, chart_data = _get_chart_data()
    return render_template(
        "proveedores_index.html",
        proveedores=all_proveedores,
        form=form,
        modal_to_open=target_modal,
        chart_labels=chart_labels,
        chart_data=chart_data,
        top_producto={},
        bottom_producto={},
        edit_uid=uid,
    )


# --- ELIMINAR ---
@proveedores_bp.route("/eliminar/<string:uid>", methods=["POST"])
@login_required
@roles_required("admin")  # Solo el admin puede borrar
def eliminar(uid):
    try:
        proveedor = Proveedor.query.get_or_404(uid)
        proveedor.estatus = False
        db.session.commit()
        flash("Proveedor desactivado correctamente", "success")
    except Exception as e:
        db.session.rollback()
        flash("No se pudo eliminar el proveedor", "error")

    return redirect(url_for("proveedores.index"))


@proveedores_bp.route("/<string:uid>")
@login_required
@roles_accepted("admin", "gerente")
def detalles(uid):
    p = Proveedor.query.get_or_404(uid)

    # --- LOGICA DE REDIRECCIÓN ---
    # Si NO viene el parámetro format=json, significa que el usuario entró desde la URL
    if request.args.get("format") != "json":
        proveedores = (
            Proveedor.query
            .order_by(Proveedor.fecha_creacion.desc())
            .all()
        )
        from .forms import ProveedorForm

        form = ProveedorForm()

        chart_labels, chart_data = _get_chart_data()
        return render_template(
            "proveedores_index.html",
            proveedores=proveedores,
            form=form,
            chart_labels=chart_labels,
            chart_data=chart_data,
            top_producto={},
            bottom_producto={},
        )

    uuid_a_mostrar = p.usuario_creo_uuid if p.usuario_creo_uuid else "SISTEMA"
    return jsonify(
        {
            "uuid": str(p.uuid_proveedor),
            "razon_social": p.razon_social,
            "rfc": p.rfc,
            "contacto_nombre": p.contacto_nombre,
            "telefono": p.telefono,
            
            "estatus": bool(p.estatus),
            "fecha_creacion": (
                p.fecha_creacion.strftime("%d/%m/%Y %H:%M")
                if p.fecha_creacion
                else "---"
            ),
            "fecha_actualizacion": (
                p.fecha_actualizacion.strftime("%d/%m/%Y %H:%M")
                if p.fecha_actualizacion
                else "---"
            ),
            "usuario_creo": uuid_a_mostrar,
        }
    )
