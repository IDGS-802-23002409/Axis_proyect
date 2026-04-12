
'''
from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, DecimalField, TextAreaField
from wtforms import validators


class MermaForm(FlaskForm):
    """Formulario para registrar merma de insumos tipo PIEZA en una OP."""

    orden_produccion = SelectField(
        'Orden de producción',
        coerce=str,
        validators=[validators.DataRequired(message='La orden de producción es requerida')]
    )

    insumo = SelectField(
        'Insumo',
        coerce=str,
        validators=[validators.DataRequired(message='El insumo es requerido')]
    )

    cantidad_teorica = IntegerField(
    'Cantidad teórica',
    validators=[
        validators.InputRequired(message='Cantidad teórica requerida'),
        validators.NumberRange(min=1, message='Debe ser al menos 1')
    ]
)

    cantidad_real_consumida = IntegerField(
        'Cantidad real consumida',
        validators=[
            validators.InputRequired(message='Cantidad real requerida'),
            validators.NumberRange(min=0, message='Debe ser mayor o igual que 0')
        ]
    )

    motivo = SelectField(
        'Motivo',
        coerce=str,
        validators=[validators.DataRequired(message='El motivo es requerido')],
        choices=[
            ('',                  'Selecciona un motivo'),
            ('DEFECTO_PROVEEDOR', 'Defecto del proveedor'),
            ('DAÑO_EN_PROCESO',   'Daño en proceso'),
            ('ERROR_OPERARIO',    'Error del operario'),
            ('MUESTRA_PRUEBA',    'Muestra de prueba'),
            ('OTRO',              'Otro'),
        ]
    )

    observaciones = TextAreaField(
        'Observaciones',
        validators=[
            validators.Optional(),
            validators.Length(max=500, message='Máximo 500 caracteres')
        ],
        render_kw={"rows": 4}
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from app.models.produccion import OrdenProduccion
        from app.models.insumos import Insumo

        ordenes = (
            OrdenProduccion.query
            .order_by(OrdenProduccion.fecha_solicitud.desc())
            .all()
        )
        self.orden_produccion.choices = [('', 'Selecciona una orden')] + [
            (
                op.uuid_op,
                f"OP {op.uuid_op[:8]}… · {op.producto.sku_especifico if op.producto else 'N/A'} · {op.estado}"
            )
            for op in ordenes
        ]

        # Solo insumos PIEZA — este form es exclusivo de MermaPiezas
        insumos = (
            Insumo.query
            .filter_by(estatus='ACTIVO', contenido_unidad_medida='PIEZA')
            .order_by(Insumo.nombre)
            .all()
        )
        self.insumo.choices = [('', 'Selecciona un insumo')] + [
            (i.uuid_insumo, f"{i.nombre} ({i.sku})")
            for i in insumos
        ]


class RetazoForm(FlaskForm):
    """
    Formulario para registrar retazos de tela en inventario.

    Si se completa el campo motivo_merma es porque es un defecto que
    afecta la merma calculada de la OP. Si está vacío, es un sobrante normal.
    """

    ejecucion_corte = SelectField(
        'Ejecución de corte',
        coerce=str,
        validators=[validators.DataRequired(message='La ejecución de corte es requerida')]
    )

    rollo_origen = SelectField(
        'Rollo de origen',
        coerce=str,
        validators=[validators.DataRequired(message='El rollo es requerido')]
    )

    metraje = DecimalField(
        'Metraje del retazo (metros)',
        places=4,
        rounding=None,
        validators=[
            validators.InputRequired(message='El metraje es requerido'),
            validators.NumberRange(min=0.0001, message='Debe ser mayor que 0')
        ]
    )

    motivo_merma = TextAreaField(
        'Descripción del motivo',
        validators=[
            validators.Optional(),
            validators.Length(max=500, message='Máximo 500 caracteres')
        ],
        render_kw={"rows": 3}
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from app.models.produccion import EjecucionCorte, OrdenProduccion
        from app.models.inventario import RolloInventario

        # Solo ejecuciones de corte cuya OP no está cancelada
        ejecuciones = (
            EjecucionCorte.query
            .join(OrdenProduccion)
            .order_by(EjecucionCorte.fecha_proceso.desc())
            .all()
        )
        self.ejecucion_corte.choices = [('', 'Selecciona una ejecución')] + [
            (
                ec.uuid_corte,
                f"Corte {ec.uuid_corte[:8]}… · "
                f"OP {ec.uuid_op[:8]}… · "
                f"{ec.fecha_proceso.strftime('%d/%m/%Y') if ec.fecha_proceso else 'N/A'}"
            )
            for ec in ejecuciones
        ]

        # Solo rollos con metraje disponible
        rollos = (
            RolloInventario.query
            .filter(RolloInventario.metraje_continuo_actual > 0)
            .order_by(RolloInventario.fecha_creacion.desc())
            .all()
        )
        self.rollo_origen.choices = [('', 'Selecciona un rollo')] + [
            (
                r.uuid_rollo,
                f"{r.insumo.nombre if r.insumo else 'N/A'} · "
                f"{float(r.metraje_continuo_actual):.2f} m disponibles"
            )
            for r in rollos
        ]



'''