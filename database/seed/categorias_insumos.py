import sys
import os
from datetime import datetime, timezone, timedelta

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))

from app.app import app
from app.utils.database_connection import db
from flask_security.utils import hash_password

from app.models.usuarios import Usuario, Role
from app.models.empleados import Empleado
from app.models.clientes import Cliente
from app.models.insumos import Insumo
from app.models.categorias import Categoria

def run_seed():
    with app.app_context():
        print(">> [INICIO] Creando datos de prueba...")

        # ─────────────────────────────
        # 3. CATEGORÍAS
        # ─────────────────────────────
        categorias_data = [

            # ── Categorías de Insumos ──
            {"nombre": "Telas", "descripcion": "Tipos de telas", "tipo": "Insumo"},
            {"nombre": "Cinta tapacostura", "descripcion": "Cintas de refuerzo", "tipo": "Insumo"},
            {"nombre": "Hilo", "descripcion": "Hilos de costura", "tipo": "Insumo"},
            {"nombre": "Rib de algodon", "descripcion": "Rib elástico para cuello y puños", "tipo": "Insumo"},
            {"nombre": "Etiquetas", "descripcion": "Etiquetas de marca, talla y cuidado", "tipo": "Insumo"},
            {"nombre": "Estampados", "descripcion": "Diseños estampados", "tipo": "Insumo"},
            {"nombre": "Ojalillos", "descripcion": "Ojales metálicos o plásticos", "tipo": "Insumo"},
            {"nombre": "Forro", "descripcion": "Forros textiles", "tipo": "Insumo"},
            {"nombre": "Cierre", "descripcion": "Cierres y cremalleras", "tipo": "Insumo"},
            {"nombre": "Botones", "descripcion": "Botones de prendas", "tipo": "Insumo"},
            {"nombre": "Remaches", "descripcion": "Remaches metálicos", "tipo": "Insumo"},
            {"nombre": "Elastico", "descripcion": "Bandas elásticas", "tipo": "Insumo"},
            {"nombre": "Cuerda", "descripcion": "Cordones y cuerdas textiles", "tipo": "Insumo"},

            # ── Categorías de Prendas ──
            {"nombre": "Playeras", "descripcion": "Playeras y camisetas", "tipo": "Prenda"},
            {"nombre": "Pantalones", "descripcion": "Pantalones y jeans", "tipo": "Prenda"},
            {"nombre": "Vestidos y Faldas", "descripcion": "Vestidos y faldas", "tipo": "Prenda"},
            {"nombre": "Sudaderas", "descripcion": "Sudaderas y hoodies", "tipo": "Prenda"},
            {"nombre": "Chamarras", "descripcion": "Chamarras y abrigos", "tipo": "Prenda"},
            {"nombre": "Shorts", "descripcion": "Shorts y bermudas", "tipo": "Prenda"},
        ]

        categorias_dict = {}

        for c in categorias_data:
            categoria = Categoria.query.filter_by(
                nombre=c["nombre"],
                tipo=c["tipo"]
            ).first()

            if not categoria:
                categoria = Categoria(
                    nombre=c["nombre"],
                    descripcion=c["descripcion"],
                    tipo=c["tipo"]
                )
                db.session.add(categoria)
                db.session.flush()

            categorias_dict[c["nombre"]] = categoria

        db.session.commit()
        print(" [OK] Categorías creadas.")

        # ─────────────────────────────
        # 4. INSUMOS
        # ─────────────────────────────
        insumos_data = [

            # ───────────────── TELAS ─────────────────
            {
                "sku": "TEL-JER-NEG-001",
                "nombre": "Tela Jersey Algodón 100% Negra",
                "categoria": "Telas",
                "unidad_medida": "ROLLO",
                "contenido_cantidad": 50,
                "contenido_unidad_medida": "METRO",
                "stock": 0,
                "stock_min": 50,
                "ancho": 1.50
            },
            {
                "sku": "TEL-FEL-NEG-001",
                "nombre": "Tela Felpa Algodón/Poliéster Negra",
                "categoria": "Telas",
                "unidad_medida": "ROLLO",
                "contenido_cantidad": 50,
                "contenido_unidad_medida": "METRO",
                "stock": 0,
                "stock_min": 30,
                "ancho": 1.75
            },
            {
                "sku": "TEL-INTER-NEG-001",
                "nombre": "Tela Interlock Poliéster Negra",
                "categoria": "Telas",
                "unidad_medida": "ROLLO",
                "contenido_cantidad": 50,
                "contenido_unidad_medida": "METRO",
                "stock": 0,
                "stock_min": 30,
                "ancho": 1.50
            },
            {
                "sku": "TEL-ROJO-POL-001",
                "nombre": "Tela Roja Poliéster/Algodón",
                "categoria": "Telas",
                "unidad_medida": "ROLLO",
                "contenido_cantidad": 50,
                "contenido_unidad_medida": "METRO",
                "stock": 0,
                "stock_min": 20,
                "ancho": 1.50
            },
            {
                "sku": "TEL-GAB-001",
                "nombre": "Tela Exterior (Gabardina/Poliéster)",
                "categoria": "Telas",
                "unidad_medida": "ROLLO",
                "contenido_cantidad": 50,
                "contenido_unidad_medida": "METRO",
                "stock": 0,
                "stock_min": 30,
                "ancho": 1.50
            },

            # ───────────────── RIB ─────────────────
            {
                "sku": "RIB-NEG-001",
                "nombre": "Rib de Algodón Negro (Cuello)",
                "categoria": "Rib de algodon",
                "unidad_medida": "ROLLO",
                "contenido_cantidad": 30,
                "contenido_unidad_medida": "METRO",
                "stock": 0,
                "stock_min": 20,
                "ancho": 1.20
            },
            {
                "sku": "RIB-BEI-001",
                "nombre": "Rib de Algodón Beige",
                "categoria": "Rib de algodon",
                "unidad_medida": "ROLLO",
                "contenido_cantidad": 30,
                "contenido_unidad_medida": "METRO",
                "stock": 0,
                "stock_min": 20,
                "ancho": 1.20
            },
            {
                "sku": "RIB-ROJO-001",
                "nombre": "Rib de Algodón Rojo",
                "categoria": "Rib de algodon",
                "unidad_medida": "ROLLO",
                "contenido_cantidad": 30,
                "contenido_unidad_medida": "METRO",
                "stock": 0,
                "stock_min": 15,
                "ancho": 1.20
            },

            # ───────────────── HILO ─────────────────
            {
                "sku": "HIL-POL-NEG-001",
                "nombre": "Hilo Poliéster 40/2 Negro",
                "categoria": "Hilo",
                "unidad_medida": "ROLLO",
                "contenido_cantidad": 1000,
                "contenido_unidad_medida": "METRO",
                "stock": 0,
                "stock_min": 10,
                "ancho": 0.00015
            },
            {
                "sku": "HIL-POL-BEI-001",
                "nombre": "Hilo Poliéster Beige",
                "categoria": "Hilo",
                "unidad_medida": "ROLLO",
                "contenido_cantidad": 1,
                "contenido_unidad_medida": "METRO",
                "stock": 0,
                "stock_min": 10,
                "ancho": 0.00015
            },
            {
                "sku": "HIL-POL-BLA-001",
                "nombre": "Hilo Poliéster Blanco (Costado)",
                "categoria": "Hilo",
                "unidad_medida": "ROLLO",
                "contenido_cantidad": 1,
                "contenido_unidad_medida": "METRO",
                "stock": 0,
                "stock_min": 10,
                "ancho": 0.00015
            },
            {
                "sku": "HIL-POL-ROJ-001",
                "nombre": "Hilo Poliéster Rojo",
                "categoria": "Hilo",
                "unidad_medida": "ROLLO",
                "contenido_cantidad": 1,
                "contenido_unidad_medida": "METRO",
                "stock": 0,
                "stock_min": 10,
                "ancho": 0.00015
            },

            # ───────────────── CINTAS ─────────────────
            {
                "sku": "CIN-TAPA-NEG-001",
                "nombre": "Cinta Tapacostura Negra",
                "categoria": "Cinta tapacostura",
                "unidad_medida": "ROLLO",
                "contenido_cantidad": 25,
                "contenido_unidad_medida": "METRO",
                "stock": 0,
                "stock_min": 50,
                "ancho": 0.10
            },

            # ───────────────── ELÁSTICO ─────────────────
            {
                "sku": "ELA-4CM-NEG-001",
                "nombre": "Elástico 4cm Negro",
                "categoria": "Elastico",
                "unidad_medida": "ROLLO",
                "contenido_cantidad": 20,
                "contenido_unidad_medida": "METRO",
                "stock": 0,
                "stock_min": 20,
                "ancho": 0.04
            },

            # ───────────────── ESTAMPADOS ─────────────────
            {
                "sku": "EST-LOWKEY-001",
                "nombre": "Estampado Lowkey Street",
                "categoria": "Estampados",
                "unidad_medida": "PIEZA",
                "contenido_cantidad": 1,
                "contenido_unidad_medida": "PIEZA",
                "stock": 0,
                "stock_min": 50
            },
            {
                "sku": "EST-PERS-001",
                "nombre": "Estampado Personalizado",
                "categoria": "Estampados",
                "unidad_medida": "PIEZA",
                "contenido_cantidad": 1,
                "contenido_unidad_medida": "PIEZA",
                "stock": 0,
                "stock_min": 30
            },
            {
                "sku": "EST-LOGO-HOODIE-001",
                "nombre": "Estampado Logo Hoodie",
                "categoria": "Estampados",
                "unidad_medida": "PIEZA",
                "contenido_cantidad": 1,
                "contenido_unidad_medida": "PIEZA",
                "stock": 0,
                "stock_min": 30
            },

            # ───────────────── ETIQUETAS ─────────────────
            {
                "sku": "ETQ-MARCA-001",
                "nombre": "Etiqueta de Marca Bordada",
                "categoria": "Etiquetas",
                "unidad_medida": "PIEZA",
                "contenido_cantidad": 1,
                "contenido_unidad_medida": "PIEZA",
                "stock": 0,
                "stock_min": 100
            },
            {
                "sku": "ETQ-CUIDADO-001",
                "nombre": "Etiqueta de Cuidado/Composición",
                "categoria": "Etiquetas",
                "unidad_medida": "PIEZA",
                "contenido_cantidad": 1,
                "contenido_unidad_medida": "PIEZA",
                "stock": 0,
                "stock_min": 100
            },

            # ───────────────── ETIQUETAS TALLA ─────────────────
            {
                "sku": "ETQ-TALLA-XSS-001",
                "nombre": "Etiqueta Talla XSS",
                "categoria": "Etiquetas",
                "unidad_medida": "PIEZA",
                "contenido_cantidad": 1,
                "contenido_unidad_medida": "PIEZA",
                "stock": 0,
                "stock_min": 100
            },
            {
                "sku": "ETQ-TALLA-XS-001",
                "nombre": "Etiqueta Talla XS",
                "categoria": "Etiquetas",
                "unidad_medida": "PIEZA",
                "contenido_cantidad": 1,
                "contenido_unidad_medida": "PIEZA",
                "stock": 0,
                "stock_min": 100
            },
            {
                "sku": "ETQ-TALLA-S-001",
                "nombre": "Etiqueta Talla S",
                "categoria": "Etiquetas",
                "unidad_medida": "PIEZA",
                "contenido_cantidad": 1,
                "contenido_unidad_medida": "PIEZA",
                "stock": 0,
                "stock_min": 100
            },
            {
                "sku": "ETQ-TALLA-M-001",
                "nombre": "Etiqueta Talla M",
                "categoria": "Etiquetas",
                "unidad_medida": "PIEZA",
                "contenido_cantidad": 1,
                "contenido_unidad_medida": "PIEZA",
                "stock": 0,
                "stock_min": 100
            },
            {
                "sku": "ETQ-TALLA-L-001",
                "nombre": "Etiqueta Talla L",
                "categoria": "Etiquetas",
                "unidad_medida": "PIEZA",
                "contenido_cantidad": 1,
                "contenido_unidad_medida": "PIEZA",
                "stock": 0,
                "stock_min": 100
            },
            {
                "sku": "ETQ-TALLA-XL-001",
                "nombre": "Etiqueta Talla XL",
                "categoria": "Etiquetas",
                "unidad_medida": "PIEZA",
                "contenido_cantidad": 1,
                "contenido_unidad_medida": "PIEZA",
                "stock": 0,
                "stock_min": 100
            },
            {
                "sku": "ETQ-TALLA-XXL-001",
                "nombre": "Etiqueta Talla XXL",
                "categoria": "Etiquetas",
                "unidad_medida": "PIEZA",
                "contenido_cantidad": 1,
                "contenido_unidad_medida": "PIEZA",
                "stock": 0,
                "stock_min": 100
            },

            # ───────────────── HERRAJES ─────────────────
            {
                "sku": "OJAL-MET-001",
                "nombre": "Ojalillos Metálicos",
                "categoria": "Ojalillos",
                "unidad_medida": "PIEZA",
                "contenido_cantidad": 1,
                "contenido_unidad_medida": "PIEZA",
                "stock": 0,
                "stock_min": 100
            },
            {
                "sku": "CORD-CAP-NEG-001",
                "nombre": "Cordón de Algodón Negro",
                "categoria": "Cuerda",
                "unidad_medida": "PIEZA",
                "contenido_cantidad": 30,
                "contenido_unidad_medida": "PIEZA",
                "stock": 0,
                "stock_min": 50
            },
            {
                "sku": "ENT-FUS-001",
                "nombre": "Entretela Fusionable (Refuerzo Ojal)",
                "categoria": "Forro",  # o crea categoría "Entretela" si quieres más limpio
                "unidad_medida": "ROLLO",
                "contenido_cantidad": 50,
                "contenido_unidad_medida": "METRO",
                "stock": 0,
                "stock_min": 20,
                "ancho": 1.00
            },
            {
                "sku": "FOR-TAF-001",
                "nombre": "Forro Interno (Tafeta)",
                "categoria": "Forro",
                "unidad_medida": "ROLLO",
                "contenido_cantidad": 50,
                "contenido_unidad_medida": "METRO",
                "stock": 0,
                "stock_min": 30,
                "ancho": 1.50
            },
            {
                "sku": "CIE-FRON-001",
                "nombre": "Cierre Frontal (Zipper)",
                "categoria": "Cierre",
                "unidad_medida": "PIEZA",
                "contenido_cantidad": 1,
                "contenido_unidad_medida": "PIEZA",
                "stock": 0,
                "stock_min": 50
            },
            {
                "sku": "BTN-GOL-001",
                "nombre": "Broches de Presión (Bolsillos Cargo)",
                "categoria": "Botones",
                "unidad_medida": "PIEZA",
                "contenido_cantidad": 1,
                "contenido_unidad_medida": "PIEZA",
                "stock": 0,
                "stock_min": 100
            },
        ]

        with db.session.no_autoflush:

            existentes = {
                sku for (sku,) in db.session.query(Insumo.sku).all()
            }

            nuevos = []

            for i in insumos_data:

                if i["sku"] in existentes:
                    continue

                categoria_obj = categorias_dict.get(i["categoria"])

                if not categoria_obj:
                    print(f"⚠️ Categoría no encontrada: {i['categoria']}")
                    continue

                nuevos.append(
                    Insumo(
                        sku=i["sku"],
                        nombre=i["nombre"],
                        uuid_categoria=categoria_obj.uuid_categoria,
                        unidad_medida=i["unidad_medida"],
                        contenido_cantidad=i["contenido_cantidad"],
                        contenido_unidad_medida=i["contenido_unidad_medida"],
                        stock_total_acumulado=i["stock"],
                        stock_minimo_alerta=i["stock_min"],
                        ancho=i.get("ancho"),
                        estatus="ACTIVO",
                        usuario_actualizo_uuid=None,
                    )
                )

        db.session.bulk_save_objects(nuevos)
        db.session.commit()
        db.session.close()

        print(" [OK] Insumos creados.")
        print("\n>> [ÉXITO] Seed completo.")


if __name__ == '__main__':
    run_seed()