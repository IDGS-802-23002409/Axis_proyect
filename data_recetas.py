import sys
import os

# Asegurar imports desde el root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))

from app.app import app
from app.utils.database_connection import db

from app.models.categorias import Categoria
from app.models.insumos import Insumo
from app.models.explosion_materiales import (
    ExplosionMaterialesCabecera,
    ExplosionMaterialesDetalle
)

from app.models.modelos_productos import ProductoTerminado


def run_seed():
    with app.app_context():

        print(">> [INICIO] Creando RECETAS...")

        recetas_data = [
            {
                "nombre": "Playera Negra con Estampado",
                "categoria": "Telas",
                "talla": "XSS",
                "detalles": [
                    {"sku": "TEL-JER-NEG-001", "consumo": 0.65, "ancho": 1.75},
                    {"sku": "RIB-NEG-001", "consumo": 0.08, "ancho": 0.50},
                    {"sku": "HIL-POL-NEG-001", "consumo": 135.00, "ancho": 0.00015},
                    {"sku": "CIN-TAPA-NEG-001", "consumo": 0.65, "ancho": 0.01},
                    {"sku": "EST-LOWKEY-001", "consumo": 1},
                    {"sku": "ETQ-TALLA-001", "consumo": 1},
                    {"sku": "ETQ-MARCA-001", "consumo": 1},
                    {"sku": "ETQ-CUIDADO-001", "consumo": 1}
                ]
            },
            {
                "nombre": "Playera Negra con Estampado",
                "categoria": "Telas",
                "talla": "XS",
                "detalles": [
                    {"sku": "TEL-JER-NEG-001", "consumo": 0.68, "ancho": 1.70},
                    {"sku": "RIB-NEG-001", "consumo": 0.08, "ancho": 0.50},
                    {"sku": "HIL-POL-NEG-001", "consumo": 138.00, "ancho": 0.00015},
                    {"sku": "CIN-TAPA-NEG-001", "consumo": 0.66, "ancho": 0.01},
                    {"sku": "EST-LOWKEY-001", "consumo": 1},
                    {"sku": "ETQ-TALLA-001", "consumo": 1},
                    {"sku": "ETQ-MARCA-001", "consumo": 1},
                    {"sku": "ETQ-CUIDADO-001", "consumo": 1}
                ]
            },
            {
                "nombre": "Playera Negra con Estampado",
                "categoria": "Telas",
                "talla": "S",
                "detalles": [
                    {"sku": "TEL-JER-NEG-001", "consumo": 0.70, "ancho": 1.65},
                    {"sku": "RIB-NEG-001", "consumo": 0.08, "ancho": 0.50},
                    {"sku": "HIL-POL-NEG-001", "consumo": 140.00, "ancho": 0.00015},
                    {"sku": "CIN-TAPA-NEG-001", "consumo": 0.68, "ancho": 0.01},
                    {"sku": "EST-LOWKEY-001", "consumo": 1},
                    {"sku": "ETQ-TALLA-001", "consumo": 1},
                    {"sku": "ETQ-MARCA-001", "consumo": 1},
                    {"sku": "ETQ-CUIDADO-001", "consumo": 1}
                ]
            },
            {
                "nombre": "Playera Negra con Estampado",
                "categoria": "Telas",
                "talla": "M",
                "detalles": [
                    {"sku": "TEL-JER-NEG-001", "consumo": 0.82, "ancho": 1.65},
                    {"sku": "RIB-NEG-001", "consumo": 0.10, "ancho": 0.50},
                    {"sku": "HIL-POL-NEG-001", "consumo": 152.00, "ancho": 0.00015},
                    {"sku": "CIN-TAPA-NEG-001", "consumo": 0.75, "ancho": 0.01},
                    {"sku": "EST-LOWKEY-001", "consumo": 1},
                    {"sku": "ETQ-TALLA-001", "consumo": 1},
                    {"sku": "ETQ-MARCA-001", "consumo": 1},
                    {"sku": "ETQ-CUIDADO-001", "consumo": 1}
                ]
            },
            {
                "nombre": "Playera Negra con Estampado",
                "categoria": "Telas",
                "talla": "L",
                "detalles": [
                    {"sku": "TEL-JER-NEG-001", "consumo": 0.90, "ancho": 1.65},
                    {"sku": "RIB-NEG-001", "consumo": 0.11, "ancho": 0.50},
                    {"sku": "HIL-POL-NEG-001", "consumo": 160.00, "ancho": 0.00015},
                    {"sku": "CIN-TAPA-NEG-001", "consumo": 0.78, "ancho": 0.01},
                    {"sku": "EST-LOWKEY-001", "consumo": 1},
                    {"sku": "ETQ-TALLA-001", "consumo": 1},
                    {"sku": "ETQ-MARCA-001", "consumo": 1},
                    {"sku": "ETQ-CUIDADO-001", "consumo": 1}
                ]
            },
            {
                "nombre": "Playera Negra con Estampado",
                "categoria": "Telas",
                "talla": "XL",
                "detalles": [
                    {"sku": "TEL-JER-NEG-001", "consumo": 0.98, "ancho": 1.65},
                    {"sku": "RIB-NEG-001", "consumo": 0.12, "ancho": 0.50},
                    {"sku": "HIL-POL-NEG-001", "consumo": 168.00, "ancho": 0.00015},
                    {"sku": "CIN-TAPA-NEG-001", "consumo": 0.82, "ancho": 0.01},
                    {"sku": "EST-LOWKEY-001", "consumo": 1},
                    {"sku": "ETQ-TALLA-001", "consumo": 1},
                    {"sku": "ETQ-MARCA-001", "consumo": 1},
                    {"sku": "ETQ-CUIDADO-001", "consumo": 1}
                ]
            },
            {
                "nombre": "Playera Negra con Estampado",
                "categoria": "Telas",
                "talla": "XXL",
                "detalles": [
                    {"sku": "TEL-JER-NEG-001", "consumo": 1.05, "ancho": 1.65},
                    {"sku": "RIB-NEG-001", "consumo": 0.13, "ancho": 0.50},
                    {"sku": "HIL-POL-NEG-001", "consumo": 175.00, "ancho": 0.00015},
                    {"sku": "CIN-TAPA-NEG-001", "consumo": 0.85, "ancho": 0.01},
                    {"sku": "EST-LOWKEY-001", "consumo": 1},
                    {"sku": "ETQ-TALLA-001", "consumo": 1},
                    {"sku": "ETQ-MARCA-001", "consumo": 1},
                    {"sku": "ETQ-CUIDADO-001", "consumo": 1}
                ]
            }
        ]

        # -------------------------
        # CREAR RECETAS
        # -------------------------
        for r in recetas_data:

            categoria = Categoria.query.filter_by(nombre=r["categoria"]).first()
            if not categoria:
                print(f" [ERROR] Categoria '{r['categoria']}' no existe")
                continue

            existe = ExplosionMaterialesCabecera.query.filter_by(
                nombre_receta=r["nombre"],
                talla=r["talla"]
            ).first()

            if existe:
                print(f" [SKIP] Receta ya existe: {r['nombre']} - {r['talla']}")
                continue

            receta = ExplosionMaterialesCabecera(
                nombre_receta=r["nombre"],
                instrucciones_proceso="Proceso estándar de confección",
                uuid_categoria=categoria.uuid_categoria,
                talla=r["talla"],
                uuid_usuario="SYSTEM",
                estatus="ACTIVO"
            )

            db.session.add(receta)
            db.session.flush()

            for d in r["detalles"]:
                insumo = Insumo.query.filter_by(sku=d["sku"]).first()

                if not insumo:
                    print(f"  [ERROR] Insumo no encontrado: {d['sku']}")
                    continue

                db.session.add(
                    ExplosionMaterialesDetalle(
                        uuid_explosion=receta.uuid_explosion,
                        uuid_insumo=insumo.uuid_insumo,
                        consumo_teorico_unitario=d["consumo"],
                        ancho_referencia=d.get("ancho")
                    )
                )

            print(f" [OK] Receta creada: {r['nombre']} ({r['talla']})")

        db.session.commit()

        # -------------------------
        # PRODUCTO TERMINADO (XSS)
        # -------------------------
        print(">> [INICIO] Creando producto terminado XSS...")

        receta_xss = ExplosionMaterialesCabecera.query.filter_by(
            nombre_receta="Playera Negra con Estampado",
            talla="XSS"
        ).first()

        if receta_xss:

            existe_producto = ProductoTerminado.query.filter_by(
                uuid_explosion=receta_xss.uuid_explosion
            ).first()

            if not existe_producto:

                producto = ProductoTerminado(
                    uuid_explosion=receta_xss.uuid_explosion,
                    sku_especifico="PLR-NG-EST-XSS-001",
                    imagen_url=None,
                    precio_venta=199.99,
                    stock_fisico_actual=0,
                    stock_minimo_alerta=10,
                    active=True
                )

                db.session.add(producto)
                db.session.commit()

                print(" [OK] Producto XSS creado correctamente")

            else:
                print(" [SKIP] Producto XSS ya existe")

        else:
            print(" [ERROR] No existe receta XSS")

        print("\n>> [ÉXITO] Recetas + Producto terminado insertados correctamente.")


if __name__ == '__main__':
    run_seed()