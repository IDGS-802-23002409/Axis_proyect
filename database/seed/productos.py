import sys
import os

# Asegurar imports desde el root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))

from app.app import app
from app.utils.database_connection import db

from app.models.explosion_materiales import ExplosionMaterialesCabecera
from app.models.modelos_productos import ProductoTerminado


def run_seed():
    with app.app_context():

        print(">> [INICIO] Creando PRODUCTOS TERMINADOS...")

        productos_terminados_data = [
            # ───────────────── PLAYERA ─────────────────
            {"sku": "PLR-NG-EST-XS-001", "receta": "Playera Negra con Estampado", "talla": "XS", "precio": 199.99},
            {"sku": "PLR-NG-EST-S-001",  "receta": "Playera Negra con Estampado", "talla": "S",  "precio": 199.99},
            {"sku": "PLR-NG-EST-M-001",  "receta": "Playera Negra con Estampado", "talla": "M",  "precio": 209.99},
            {"sku": "PLR-NG-EST-L-001",  "receta": "Playera Negra con Estampado", "talla": "L",  "precio": 219.99},
            {"sku": "PLR-NG-EST-XL-001", "receta": "Playera Negra con Estampado", "talla": "XL", "precio": 229.99},
            {"sku": "PLR-NG-EST-XXL-001","receta": "Playera Negra con Estampado", "talla": "XXL","precio": 239.99},

            # ───────────────── SUDADERA ─────────────────
            {"sku": "SUD-NG-HOOD-XS-001", "receta": "Sudadera Negra con Capucha", "talla": "XS", "precio": 399.99},
            {"sku": "SUD-NG-HOOD-S-001",  "receta": "Sudadera Negra con Capucha", "talla": "S",  "precio": 409.99},
            {"sku": "SUD-NG-HOOD-M-001",  "receta": "Sudadera Negra con Capucha", "talla": "M",  "precio": 419.99},
            {"sku": "SUD-NG-HOOD-L-001",  "receta": "Sudadera Negra con Capucha", "talla": "L",  "precio": 429.99},
            {"sku": "SUD-NG-HOOD-XL-001", "receta": "Sudadera Negra con Capucha", "talla": "XL", "precio": 439.99},
            {"sku": "SUD-NG-HOOD-XXL-001","receta": "Sudadera Negra con Capucha", "talla": "XXL","precio": 449.99},
            # ───────────────── CHAQUETA BOMBER ─────────────────
            {"sku": "CHA-BOM-XS-001",  "receta": "Chaqueta Tipo Cazadora/Bomber", "talla": "XS",  "precio": 599.99},
            {"sku": "CHA-BOM-S-001",   "receta": "Chaqueta Tipo Cazadora/Bomber", "talla": "S",   "precio": 619.99},
            {"sku": "CHA-BOM-M-001",   "receta": "Chaqueta Tipo Cazadora/Bomber", "talla": "M",   "precio": 639.99},
            {"sku": "CHA-BOM-L-001",   "receta": "Chaqueta Tipo Cazadora/Bomber", "talla": "L",   "precio": 659.99},
            {"sku": "CHA-BOM-XL-001",  "receta": "Chaqueta Tipo Cazadora/Bomber", "talla": "XL",  "precio": 679.99},
            {"sku": "CHA-BOM-XXL-001", "receta": "Chaqueta Tipo Cazadora/Bomber", "talla": "XXL", "precio": 699.99},

            # ───────────────── PANTALÓN CARGO ─────────────────
            {"sku": "CAR-NG-XS-001",   "receta": "Pantalón Cargo Negro Hombre", "talla": "XS",  "precio": 449.99},
            {"sku": "CAR-NG-S-001",    "receta": "Pantalón Cargo Negro Hombre", "talla": "S",   "precio": 459.99},
            {"sku": "CAR-NG-M-001",    "receta": "Pantalón Cargo Negro Hombre", "talla": "M",   "precio": 469.99},
            {"sku": "CAR-NG-L-001",    "receta": "Pantalón Cargo Negro Hombre", "talla": "L",   "precio": 479.99},
            {"sku": "CAR-NG-XL-001",   "receta": "Pantalón Cargo Negro Hombre", "talla": "XL",  "precio": 489.99},
            {"sku": "CAR-NG-XXL-001",  "receta": "Pantalón Cargo Negro Hombre", "talla": "XXL", "precio": 499.99},
                        # ───────────────── JOGGER ─────────────────
            {"sku": "JOG-NG-HOM-XS-001",  "receta": "Jogger Negro Hombre", "talla": "XS",  "precio": 299.99},
            {"sku": "JOG-NG-HOM-S-001",   "receta": "Jogger Negro Hombre", "talla": "S",   "precio": 309.99},
            {"sku": "JOG-NG-HOM-M-001",   "receta": "Jogger Negro Hombre", "talla": "M",   "precio": 319.99},
            {"sku": "JOG-NG-HOM-L-001",   "receta": "Jogger Negro Hombre", "talla": "L",   "precio": 329.99},
            {"sku": "JOG-NG-HOM-XL-001",  "receta": "Jogger Negro Hombre", "talla": "XL",  "precio": 339.99},
            {"sku": "JOG-NG-HOM-XXL-001", "receta": "Jogger Negro Hombre", "talla": "XXL", "precio": 349.99},

            # ───────────────── CHAMARRA MEZCLILLA ─────────────────
            {"sku": "CHM-DEN-AZL-XS-001",  "receta": "Chamarra de Mezclilla Azul", "talla": "XS",  "precio": 499.99},
            {"sku": "CHM-DEN-AZL-S-001",   "receta": "Chamarra de Mezclilla Azul", "talla": "S",   "precio": 509.99},
            {"sku": "CHM-DEN-AZL-M-001",   "receta": "Chamarra de Mezclilla Azul", "talla": "M",   "precio": 519.99},
            {"sku": "CHM-DEN-AZL-L-001",   "receta": "Chamarra de Mezclilla Azul", "talla": "L",   "precio": 529.99},
            {"sku": "CHM-DEN-AZL-XL-001",  "receta": "Chamarra de Mezclilla Azul", "talla": "XL",  "precio": 539.99},
            {"sku": "CHM-DEN-AZL-XXL-001", "receta": "Chamarra de Mezclilla Azul", "talla": "XXL", "precio": 549.99},
            {"sku": "PLR-BLA-OVS-XS-001",  "receta": "Playera Blanca Oversize", "talla": "XS",  "precio": 209.99},

            {"sku": "PLR-BLA-OVS-S-001",   "receta": "Playera Blanca Oversize", "talla": "S",   "precio": 219.99},
            {"sku": "PLR-BLA-OVS-M-001",   "receta": "Playera Blanca Oversize", "talla": "M",   "precio": 229.99},
            {"sku": "PLR-BLA-OVS-L-001",   "receta": "Playera Blanca Oversize", "talla": "L",   "precio": 239.99},
            {"sku": "PLR-BLA-OVS-XL-001",  "receta": "Playera Blanca Oversize", "talla": "XL",  "precio": 249.99},
            {"sku": "PLR-BLA-OVS-XXL-001", "receta": "Playera Blanca Oversize", "talla": "XXL", "precio": 259.99},

            {"sku": "SUD-CRP-MUJ-XS-001",  "receta": 'SUDADERA TIPO "CROP TOP" (AL OMBLIGO) PARA MUJER', "talla": "XS",  "precio": 359.99},
            {"sku": "SUD-CRP-MUJ-S-001",   "receta": 'SUDADERA TIPO "CROP TOP" (AL OMBLIGO) PARA MUJER', "talla": "S",   "precio": 369.99},
            {"sku": "SUD-CRP-MUJ-M-001",   "receta": 'SUDADERA TIPO "CROP TOP" (AL OMBLIGO) PARA MUJER', "talla": "M",   "precio": 379.99},
            {"sku": "SUD-CRP-MUJ-L-001",   "receta": 'SUDADERA TIPO "CROP TOP" (AL OMBLIGO) PARA MUJER', "talla": "L",   "precio": 389.99},
            {"sku": "SUD-CRP-MUJ-XL-001",  "receta": 'SUDADERA TIPO "CROP TOP" (AL OMBLIGO) PARA MUJER', "talla": "XL",  "precio": 399.99},
            {"sku": "SUD-CRP-MUJ-XXL-001", "receta": 'SUDADERA TIPO "CROP TOP" (AL OMBLIGO) PARA MUJER', "talla": "XXL", "precio": 409.99},

            {"sku": "JOG-MUJ-BEI-NG-XSS-001", "receta": "JOGGER PARA MUJER COLOR BEIGE CON TIRA DE COLOR NEGRO", "talla": "XSS", "precio": 299.99},
            {"sku": "JOG-MUJ-BEI-NG-XS-001",  "receta": "JOGGER PARA MUJER COLOR BEIGE CON TIRA DE COLOR NEGRO", "talla": "XS",  "precio": 309.99},
            {"sku": "JOG-MUJ-BEI-NG-S-001",   "receta": "JOGGER PARA MUJER COLOR BEIGE CON TIRA DE COLOR NEGRO", "talla": "S",   "precio": 319.99},
            {"sku": "JOG-MUJ-BEI-NG-M-001",   "receta": "JOGGER PARA MUJER COLOR BEIGE CON TIRA DE COLOR NEGRO", "talla": "M",   "precio": 329.99},
            {"sku": "JOG-MUJ-BEI-NG-L-001",   "receta": "JOGGER PARA MUJER COLOR BEIGE CON TIRA DE COLOR NEGRO", "talla": "L",   "precio": 339.99},
            {"sku": "JOG-MUJ-BEI-NG-XL-001",  "receta": "JOGGER PARA MUJER COLOR BEIGE CON TIRA DE COLOR NEGRO", "talla": "XL",  "precio": 349.99},
            {"sku": "JOG-MUJ-BEI-NG-XXL-001", "receta": "JOGGER PARA MUJER COLOR BEIGE CON TIRA DE COLOR NEGRO", "talla": "XXL", "precio": 359.99},
        ]

        for p in productos_terminados_data:

            print(f">> Procesando producto: {p['sku']}")

            # Buscar receta asociada
            receta = ExplosionMaterialesCabecera.query.filter_by(
                nombre_receta=p["receta"],
                talla=p["talla"]
            ).first()

            if not receta:
                print(f"  [ERROR] No existe receta para {p['receta']} - {p['talla']}")
                continue

            # Evitar duplicados
            existe = ProductoTerminado.query.filter_by(
                sku_especifico=p["sku"]
            ).first()

            if existe:
                print(f"  [SKIP] Producto ya existe: {p['sku']}")
                continue

            producto = ProductoTerminado(
                uuid_explosion=receta.uuid_explosion,
                sku_especifico=p["sku"],
                imagen_url=None,
                precio_venta=p["precio"],
                stock_fisico_actual=0,
                stock_minimo_alerta=10,
                active=True
            )

            db.session.add(producto)

        db.session.commit()

        print(">> [OK] Productos terminados creados correctamente.")


if __name__ == "__main__":
    run_seed()