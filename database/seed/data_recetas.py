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
                "categoria": "Playeras",
                "talla": "XSS",
                "detalles": [
                    {"sku": "TEL-JER-NEG-001", "consumo": 0.65, "ancho": 1.75},
                    {"sku": "RIB-NEG-001", "consumo": 0.08, "ancho": 0.50},
                    {"sku": "HIL-POL-NEG-001", "consumo": 135.00, "ancho": 0.00015},
                    {"sku": "CIN-TAPA-NEG-001", "consumo": 0.65, "ancho": 0.01},

                    {"sku": "EST-LOWKEY-001", "cantidad": 1},
                    {"sku": "ETQ-TALLA-XSS-001", "cantidad": 1},
                    {"sku": "ETQ-MARCA-001", "cantidad": 1},
                    {"sku": "ETQ-CUIDADO-001", "cantidad": 1}
                ]
            },

            {
                "nombre": "Playera Negra con Estampado",
                "categoria": "Playeras",
                "talla": "S",
                "detalles": [
                    {"sku": "TEL-JER-NEG-001", "consumo": 0.70, "ancho": 1.65},
                    {"sku": "RIB-NEG-001", "consumo": 0.08, "ancho": 0.50},
                    {"sku": "HIL-POL-NEG-001", "consumo": 140.00, "ancho": 0.00015},
                    {"sku": "CIN-TAPA-NEG-001", "consumo": 0.68, "ancho": 0.01},

                    {"sku": "EST-LOWKEY-001", "cantidad": 1},
                    {"sku": "ETQ-TALLA-S-001", "cantidad": 1},
                    {"sku": "ETQ-MARCA-001", "cantidad": 1},
                    {"sku": "ETQ-CUIDADO-001", "cantidad": 1}
                ]
            },

            {
                "nombre": "Playera Negra con Estampado",
                "categoria": "Playeras",
                "talla": "M",
                "detalles": [
                    {"sku": "TEL-JER-NEG-001", "consumo": 0.82, "ancho": 1.65},
                    {"sku": "RIB-NEG-001", "consumo": 0.10, "ancho": 0.50},
                    {"sku": "HIL-POL-NEG-001", "consumo": 152.00, "ancho": 0.00015},
                    {"sku": "CIN-TAPA-NEG-001", "consumo": 0.75, "ancho": 0.01},

                    {"sku": "EST-LOWKEY-001", "cantidad": 1},
                    {"sku": "ETQ-TALLA-M-001", "cantidad": 1},
                    {"sku": "ETQ-MARCA-001", "cantidad": 1},
                    {"sku": "ETQ-CUIDADO-001", "cantidad": 1}
                ]
            },

            {
                "nombre": "Playera Negra con Estampado",
                "categoria": "Playeras",
                "talla": "L",
                "detalles": [
                    {"sku": "TEL-JER-NEG-001", "consumo": 0.90, "ancho": 1.65},
                    {"sku": "RIB-NEG-001", "consumo": 0.11, "ancho": 0.50},
                    {"sku": "HIL-POL-NEG-001", "consumo": 160.00, "ancho": 0.00015},
                    {"sku": "CIN-TAPA-NEG-001", "consumo": 0.78, "ancho": 0.01},

                    {"sku": "EST-LOWKEY-001", "cantidad": 1},
                    {"sku": "ETQ-TALLA-L-001", "cantidad": 1},
                    {"sku": "ETQ-MARCA-001", "cantidad": 1},
                    {"sku": "ETQ-CUIDADO-001", "cantidad": 1}
                ]
            },

            {
                "nombre": "Playera Negra con Estampado",
                "categoria": "Playeras",
                "talla": "XL",
                "detalles": [
                    {"sku": "TEL-JER-NEG-001", "consumo": 0.98, "ancho": 1.65},
                    {"sku": "RIB-NEG-001", "consumo": 0.12, "ancho": 0.50},
                    {"sku": "HIL-POL-NEG-001", "consumo": 168.00, "ancho": 0.00015},
                    {"sku": "CIN-TAPA-NEG-001", "consumo": 0.82, "ancho": 0.01},

                    {"sku": "EST-LOWKEY-001", "cantidad": 1},
                    {"sku": "ETQ-TALLA-XL-001", "cantidad": 1},
                    {"sku": "ETQ-MARCA-001", "cantidad": 1},
                    {"sku": "ETQ-CUIDADO-001", "cantidad": 1}
                ]
            },

            {
                "nombre": "Playera Negra con Estampado",
                "categoria": "Playeras",
                "talla": "XXL",
                "detalles": [
                    {"sku": "TEL-JER-NEG-001", "consumo": 1.05, "ancho": 1.65},
                    {"sku": "RIB-NEG-001", "consumo": 0.13, "ancho": 0.50},
                    {"sku": "HIL-POL-NEG-001", "consumo": 175.00, "ancho": 0.00015},
                    {"sku": "CIN-TAPA-NEG-001", "consumo": 0.85, "ancho": 0.01},

                    {"sku": "EST-LOWKEY-001", "cantidad": 1},
                    {"sku": "ETQ-TALLA-XXL-001", "cantidad": 1},
                    {"sku": "ETQ-MARCA-001", "cantidad": 1},
                    {"sku": "ETQ-CUIDADO-001", "cantidad": 1}
                ]
            },

            {
                "nombre": "Sudadera Negra con Capucha",
                "categoria": "Playeras",
                "talla": "XSS",
                "detalles": [
                    {"sku": "TEL-FEL-NEG-001", "consumo": 1.40, "ancho": 1.75},
                    {"sku": "RIB-NEG-001", "consumo": 0.20, "ancho": 0.90},
                    {"sku": "HIL-POL-NEG-001", "consumo": 280.00, "ancho": 0.00015},
                    {"sku": "CIN-TAPA-NEG-001", "consumo": 0.30, "ancho": 0.01},
                    {"sku": "ENT-FUS-001", "consumo": 0.05, "ancho": 0.10},

                    {"sku": "CORD-CAP-NEG-001", "cantidad": 1},
                    {"sku": "EST-LOGO-HOODIE-001", "cantidad": 1},
                    {"sku": "OJAL-MET-001", "cantidad": 2},

                    {"sku": "ETQ-TALLA-XSS-001", "cantidad": 1},
                    {"sku": "ETQ-MARCA-001", "cantidad": 1},
                    {"sku": "ETQ-CUIDADO-001", "cantidad": 1}
                ]
            },

            {
                "nombre": "Sudadera Negra con Capucha",
                "categoria": "Sudaderas",
                "talla": "S",
                "detalles": [
                    {"sku": "TEL-FEL-NEG-001", "consumo": 1.55, "ancho": 1.75},
                    {"sku": "RIB-NEG-001", "consumo": 0.22, "ancho": 0.90},
                    {"sku": "HIL-POL-NEG-001", "consumo": 310.00, "ancho": 0.00015},
                    {"sku": "CIN-TAPA-NEG-001", "consumo": 0.35, "ancho": 0.01},
                    {"sku": "ENT-FUS-001", "consumo": 0.05, "ancho": 0.10},

                    {"sku": "CORD-CAP-NEG-001", "cantidad": 1},
                    {"sku": "EST-LOGO-HOODIE-001", "cantidad": 1},
                    {"sku": "OJAL-MET-001", "cantidad": 2},

                    {"sku": "ETQ-TALLA-S-001", "cantidad": 1},
                    {"sku": "ETQ-MARCA-001", "cantidad": 1},
                    {"sku": "ETQ-CUIDADO-001", "cantidad": 1}
                ]
            },

            {
                "nombre": "Sudadera Negra con Capucha",
                "categoria": "Sudaderas",
                "talla": "M",
                "detalles": [
                    {"sku": "TEL-FEL-NEG-001", "consumo": 1.65, "ancho": 1.75},
                    {"sku": "RIB-NEG-001", "consumo": 0.25, "ancho": 0.90},
                    {"sku": "HIL-POL-NEG-001", "consumo": 330.00, "ancho": 0.00015},
                    {"sku": "CIN-TAPA-NEG-001", "consumo": 0.35, "ancho": 0.01},
                    {"sku": "ENT-FUS-001", "consumo": 0.05, "ancho": 0.10},

                    {"sku": "CORD-CAP-NEG-001", "cantidad": 1},
                    {"sku": "EST-LOGO-HOODIE-001", "cantidad": 1},
                    {"sku": "OJAL-MET-001", "cantidad": 2},

                    {"sku": "ETQ-TALLA-M-001", "cantidad": 1},
                    {"sku": "ETQ-MARCA-001", "cantidad": 1},
                    {"sku": "ETQ-CUIDADO-001", "cantidad": 1}
                ]
            },

            {
                "nombre": "Sudadera Negra con Capucha",
                "categoria": "Sudaderas",
                "talla": "L",
                "detalles": [
                    {"sku": "TEL-FEL-NEG-001", "consumo": 1.80, "ancho": 1.75},
                    {"sku": "RIB-NEG-001", "consumo": 0.25, "ancho": 0.90},
                    {"sku": "HIL-POL-NEG-001", "consumo": 355.00, "ancho": 0.00015},
                    {"sku": "CIN-TAPA-NEG-001", "consumo": 0.38, "ancho": 0.01},
                    {"sku": "ENT-FUS-001", "consumo": 0.05, "ancho": 0.10},

                    {"sku": "CORD-CAP-NEG-001", "cantidad": 1},
                    {"sku": "EST-LOGO-HOODIE-001", "cantidad": 1},
                    {"sku": "OJAL-MET-001", "cantidad": 2},

                    {"sku": "ETQ-TALLA-L-001", "cantidad": 1},
                    {"sku": "ETQ-MARCA-001", "cantidad": 1},
                    {"sku": "ETQ-CUIDADO-001", "cantidad": 1}
                ]
            },

            {
                "nombre": "Sudadera Negra con Capucha",
                "categoria": "Sudaderas",
                "talla": "XL",
                "detalles": [
                    {"sku": "TEL-FEL-NEG-001", "consumo": 1.95, "ancho": 1.75},
                    {"sku": "RIB-NEG-001", "consumo": 0.28, "ancho": 0.90},
                    {"sku": "HIL-POL-NEG-001", "consumo": 380.00, "ancho": 0.00015},
                    {"sku": "CIN-TAPA-NEG-001", "consumo": 0.40, "ancho": 0.01},
                    {"sku": "ENT-FUS-001", "consumo": 0.05, "ancho": 0.10},

                    {"sku": "CORD-CAP-NEG-001", "cantidad": 1},
                    {"sku": "EST-LOGO-HOODIE-001", "cantidad": 1},
                    {"sku": "OJAL-MET-001", "cantidad": 2},

                    {"sku": "ETQ-TALLA-XL-001", "cantidad": 1},
                    {"sku": "ETQ-MARCA-001", "cantidad": 1},
                    {"sku": "ETQ-CUIDADO-001", "cantidad": 1}
                ]
            },

            {
                "nombre": "Sudadera Negra con Capucha",
                "categoria": "Sudaderas",
                "talla": "XXL",
                "detalles": [
                    {"sku": "TEL-FEL-NEG-001", "consumo": 2.10, "ancho": 1.75},
                    {"sku": "RIB-NEG-001", "consumo": 0.30, "ancho": 0.90},
                    {"sku": "HIL-POL-NEG-001", "consumo": 410.00, "ancho": 0.00015},
                    {"sku": "CIN-TAPA-NEG-001", "consumo": 0.42, "ancho": 0.01},
                    {"sku": "ENT-FUS-001", "consumo": 0.05, "ancho": 0.10},

                    {"sku": "CORD-CAP-NEG-001", "cantidad": 1},
                    {"sku": "EST-LOGO-HOODIE-001", "cantidad": 1},
                    {"sku": "OJAL-MET-001", "cantidad": 2},

                    {"sku": "ETQ-TALLA-XXL-001", "cantidad": 1},
                    {"sku": "ETQ-MARCA-001", "cantidad": 1},
                    {"sku": "ETQ-CUIDADO-001", "cantidad": 1}
                ]
            },
            {
                "nombre": "Chaqueta Tipo Cazadora/Bomber",
                "categoria": "Chamarras",
                "talla": "XSS",
                "detalles": [
                    {"sku": "TEL-GAB-001", "consumo": 1.30, "ancho": 1.75},
                    {"sku": "FOR-TAF-001", "consumo": 1.20, "ancho": 1.50},
                    {"sku": "RIB-NEG-001", "consumo": 0.25, "ancho": 0.90},
                    {"sku": "HIL-POL-NEG-001", "consumo": 350.00, "ancho": 0.00015},

                    {"sku": "CIE-FRON-001", "cantidad": 1},
                    {"sku": "EST-PERS-001", "cantidad": 1},

                    {"sku": "ETQ-TALLA-XSS-001", "cantidad": 1},
                    {"sku": "ETQ-MARCA-001", "cantidad": 1},
                    {"sku": "ETQ-CUIDADO-001", "cantidad": 1}
                ]
            },

            {
                "nombre": "Chaqueta Tipo Cazadora/Bomber",
                "categoria": "Chamarras",
                "talla": "XS",
                "detalles": [
                    {"sku": "TEL-GAB-001", "consumo": 1.30, "ancho": 1.75},
                    {"sku": "FOR-TAF-001", "consumo": 1.20, "ancho": 1.50},
                    {"sku": "RIB-NEG-001", "consumo": 0.25, "ancho": 0.90},
                    {"sku": "HIL-POL-NEG-001", "consumo": 350.00, "ancho": 0.00015},

                    {"sku": "CIE-FRON-001", "cantidad": 1},
                    {"sku": "EST-PERS-001", "cantidad": 1},

                    {"sku": "ETQ-TALLA-XSS-001", "cantidad": 1},
                    {"sku": "ETQ-MARCA-001", "cantidad": 1},
                    {"sku": "ETQ-CUIDADO-001", "cantidad": 1}
                ]
            },

            {
                "nombre": "Chaqueta Tipo Cazadora/Bomber",
                "categoria": "Chamarras",
                "talla": "S",
                "detalles": [
                    {"sku": "TEL-GAB-001", "consumo": 1.45, "ancho": 1.75},
                    {"sku": "FOR-TAF-001", "consumo": 1.35, "ancho": 1.50},
                    {"sku": "RIB-NEG-001", "consumo": 0.25, "ancho": 0.90},
                    {"sku": "HIL-POL-NEG-001", "consumo": 380.00, "ancho": 0.00015},

                    {"sku": "CIE-FRON-001", "cantidad": 1},
                    {"sku": "EST-PERS-001", "cantidad": 1},

                    {"sku": "ETQ-TALLA-S-001", "cantidad": 1},
                    {"sku": "ETQ-MARCA-001", "cantidad": 1},
                    {"sku": "ETQ-CUIDADO-001", "cantidad": 1}
                ]
            },

            {
                "nombre": "Chaqueta Tipo Cazadora/Bomber",
                "categoria": "Chamarras",
                "talla": "M",
                "detalles": [
                    {"sku": "TEL-GAB-001", "consumo": 1.55, "ancho": 1.75},
                    {"sku": "FOR-TAF-001", "consumo": 1.45, "ancho": 1.50},
                    {"sku": "RIB-NEG-001", "consumo": 0.28, "ancho": 0.90},
                    {"sku": "HIL-POL-NEG-001", "consumo": 410.00, "ancho": 0.00015},

                    {"sku": "CIE-FRON-001", "cantidad": 1},
                    {"sku": "EST-PERS-001", "cantidad": 1},

                    {"sku": "ETQ-TALLA-M-001", "cantidad": 1},
                    {"sku": "ETQ-MARCA-001", "cantidad": 1},
                    {"sku": "ETQ-CUIDADO-001", "cantidad": 1}
                ]
            },

            {
                "nombre": "Chaqueta Tipo Cazadora/Bomber",
                "categoria": "Chamarras",
                "talla": "L",
                "detalles": [
                    {"sku": "TEL-GAB-001", "consumo": 1.70, "ancho": 1.75},
                    {"sku": "FOR-TAF-001", "consumo": 1.60, "ancho": 1.50},
                    {"sku": "RIB-NEG-001", "consumo": 0.28, "ancho": 0.90},
                    {"sku": "HIL-POL-NEG-001", "consumo": 440.00, "ancho": 0.00015},

                    {"sku": "CIE-FRON-001", "cantidad": 1},
                    {"sku": "EST-PERS-001", "cantidad": 1},

                    {"sku": "ETQ-TALLA-L-001", "cantidad": 1},
                    {"sku": "ETQ-MARCA-001", "cantidad": 1},
                    {"sku": "ETQ-CUIDADO-001", "cantidad": 1}
                ]
            },

            {
                "nombre": "Chaqueta Tipo Cazadora/Bomber",
                "categoria": "Chamarras",
                "talla": "XL",
                "detalles": [
                    {"sku": "TEL-GAB-001", "consumo": 1.85, "ancho": 1.75},
                    {"sku": "FOR-TAF-001", "consumo": 1.75, "ancho": 1.50},
                    {"sku": "RIB-NEG-001", "consumo": 0.30, "ancho": 0.90},
                    {"sku": "HIL-POL-NEG-001", "consumo": 480.00, "ancho": 0.00015},

                    {"sku": "CIE-FRON-001", "cantidad": 1},
                    {"sku": "EST-PERS-001", "cantidad": 1},

                    {"sku": "ETQ-TALLA-XL-001", "cantidad": 1},
                    {"sku": "ETQ-MARCA-001", "cantidad": 1},
                    {"sku": "ETQ-CUIDADO-001", "cantidad": 1}
                ]
            },

            {
                "nombre": "Chaqueta Tipo Cazadora/Bomber",
                "categoria": "Chamarras",
                "talla": "XXL",
                "detalles": [
                    {"sku": "TEL-GAB-001", "consumo": 2.00, "ancho": 1.75},
                    {"sku": "FOR-TAF-001", "consumo": 1.90, "ancho": 1.50},
                    {"sku": "RIB-NEG-001", "consumo": 0.32, "ancho": 0.90},
                    {"sku": "HIL-POL-NEG-001", "consumo": 520.00, "ancho": 0.00015},

                    {"sku": "CIE-FRON-001", "cantidad": 1},
                    {"sku": "EST-PERS-001", "cantidad": 1},

                    {"sku": "ETQ-TALLA-XXL-001", "cantidad": 1},
                    {"sku": "ETQ-MARCA-001", "cantidad": 1},
                    {"sku": "ETQ-CUIDADO-001", "cantidad": 1}
                ]
            },

            {
                "nombre": "Pantalón Cargo Negro Hombre",
                "categoria": "Pantalones",
                "talla": "XSS",
                "detalles": [
                    {"sku": "TEL-GAB-NEG-001", "consumo": 1.05, "ancho": 1.75},
                    {"sku": "FOR-VIS-001", "consumo": 0.20, "ancho": 1.50},
                    {"sku": "HIL-POL-NEG-001", "consumo": 240.00, "ancho": 0.00015},

                    {"sku": "CIE-FRON-001", "cantidad": 1},
                    {"sku": "BTN-GOL-001", "cantidad": 1},
                    {"sku": "BRO-PRES-001", "cantidad": 4},

                    {"sku": "ETQ-TALLA-XSS-001", "cantidad": 1},
                    {"sku": "ETQ-MARCA-001", "cantidad": 1},
                    {"sku": "ETQ-CUIDADO-001", "cantidad": 1}
                ]
            },

            {
                "nombre": "Pantalón Cargo Negro Hombre",
                "categoria": "Pantalones",
                "talla": "XS",
                "detalles": [
                    {"sku": "TEL-GAB-NEG-001", "consumo": 1.10, "ancho": 1.75},
                    {"sku": "FOR-VIS-001", "consumo": 0.25, "ancho": 1.50},
                    {"sku": "HIL-POL-NEG-001", "consumo": 255.00, "ancho": 0.00015},

                    {"sku": "CIE-FRON-001", "cantidad": 1},
                    {"sku": "BTN-GOL-001", "cantidad": 1},
                    {"sku": "BRO-PRES-001", "cantidad": 4},

                    {"sku": "ETQ-TALLA-XS-001", "cantidad": 1},
                    {"sku": "ETQ-MARCA-001", "cantidad": 1},
                    {"sku": "ETQ-CUIDADO-001", "cantidad": 1}
                ]
            },

            {
                "nombre": "Pantalón Cargo Negro Hombre",
                "categoria": "Pantalones",
                "talla": "S",
                "detalles": [
                    {"sku": "TEL-GAB-NEG-001", "consumo": 1.15, "ancho": 1.75},
                    {"sku": "FOR-VIS-001", "consumo": 0.25, "ancho": 1.50},
                    {"sku": "HIL-POL-NEG-001", "consumo": 265.00, "ancho": 0.00015},

                    {"sku": "CIE-FRON-001", "cantidad": 1},
                    {"sku": "BTN-GOL-001", "cantidad": 1},
                    {"sku": "BRO-PRES-001", "cantidad": 4},

                    {"sku": "ETQ-TALLA-S-001", "cantidad": 1},
                    {"sku": "ETQ-MARCA-001", "cantidad": 1},
                    {"sku": "ETQ-CUIDADO-001", "cantidad": 1}
                ]
            },

            {
                "nombre": "Pantalón Cargo Negro Hombre",
                "categoria": "Pantalones",
                "talla": "M",
                "detalles": [
                    {"sku": "TEL-GAB-NEG-001", "consumo": 1.25, "ancho": 1.75},
                    {"sku": "FOR-VIS-001", "consumo": 0.30, "ancho": 1.50},
                    {"sku": "HIL-POL-NEG-001", "consumo": 280.00, "ancho": 0.00015},

                    {"sku": "CIE-FRON-001", "cantidad": 1},
                    {"sku": "BTN-GOL-001", "cantidad": 1},
                    {"sku": "BRO-PRES-001", "cantidad": 4},

                    {"sku": "ETQ-TALLA-M-001", "cantidad": 1},
                    {"sku": "ETQ-MARCA-001", "cantidad": 1},
                    {"sku": "ETQ-CUIDADO-001", "cantidad": 1}
                ]
            },

            {
                "nombre": "Pantalón Cargo Negro Hombre",
                "categoria": "Pantalones",
                "talla": "L",
                "detalles": [
                    {"sku": "TEL-GAB-NEG-001", "consumo": 1.35, "ancho": 1.75},
                    {"sku": "FOR-VIS-001", "consumo": 0.30, "ancho": 1.50},
                    {"sku": "HIL-POL-NEG-001", "consumo": 300.00, "ancho": 0.00015},

                    {"sku": "CIE-FRON-001", "cantidad": 1},
                    {"sku": "BTN-GOL-001", "cantidad": 1},
                    {"sku": "BRO-PRES-001", "cantidad": 4},

                    {"sku": "ETQ-TALLA-L-001", "cantidad": 1},
                    {"sku": "ETQ-MARCA-001", "cantidad": 1},
                    {"sku": "ETQ-CUIDADO-001", "cantidad": 1}
                ]
            },

            {
                "nombre": "Pantalón Cargo Negro Hombre",
                "categoria": "Pantalones",
                "talla": "XL",
                "detalles": [
                    {"sku": "TEL-GAB-NEG-001", "consumo": 1.45, "ancho": 1.75},
                    {"sku": "FOR-VIS-001", "consumo": 0.35, "ancho": 1.50},
                    {"sku": "HIL-POL-NEG-001", "consumo": 325.00, "ancho": 0.00015},

                    {"sku": "CIE-FRON-001", "cantidad": 1},
                    {"sku": "BTN-GOL-001", "cantidad": 1},
                    {"sku": "BRO-PRES-001", "cantidad": 4},

                    {"sku": "ETQ-TALLA-XL-001", "cantidad": 1},
                    {"sku": "ETQ-MARCA-001", "cantidad": 1},
                    {"sku": "ETQ-CUIDADO-001", "cantidad": 1}
                ]
            },

            {
                "nombre": "Pantalón Cargo Negro Hombre",
                "categoria": "Pantalones",
                "talla": "XXL",
                "detalles": [
                    {"sku": "TEL-GAB-NEG-001", "consumo": 1.55, "ancho": 1.75},
                    {"sku": "FOR-VIS-001", "consumo": 0.35, "ancho": 1.50},
                    {"sku": "HIL-POL-NEG-001", "consumo": 350.00, "ancho": 0.00015},

                    {"sku": "CIE-FRON-001", "cantidad": 1},
                    {"sku": "BTN-GOL-001", "cantidad": 1},
                    {"sku": "BRO-PRES-001", "cantidad": 4},

                    {"sku": "ETQ-TALLA-XXL-001", "cantidad": 1},
                    {"sku": "ETQ-MARCA-001", "cantidad": 1},
                    {"sku": "ETQ-CUIDADO-001", "cantidad": 1}
                ]
            },
            {
                "nombre": "Jogger Negro Hombre",
                "categoria": "Pantalones",
                "talla": "XSS",
                "detalles": [
                    {"sku": "TEL-FEL-NEG-001", "consumo": 1.05, "ancho": 1.75},
                    {"sku": "RIB-NEG-001", "consumo": 0.20, "ancho": 0.90},
                    {"sku": "HIL-POL-NEG-001", "consumo": 240.00, "ancho": 0.00015},
                    {"sku": "ENT-FUS-001", "consumo": 0.05, "ancho": 0.10},

                    {"sku": "CORD-CAP-NEG-001", "cantidad": 1},
                    {"sku": "OJA-MET-001", "cantidad": 2},

                    {"sku": "ETQ-TALLA-XSS-001", "cantidad": 1},
                    {"sku": "ETQ-MARCA-001", "cantidad": 1},
                    {"sku": "ETQ-CUIDADO-001", "cantidad": 1}
                ]
            },

            {
                "nombre": "Jogger Negro Hombre",
                "categoria": "Pantalones",
                "talla": "XS",
                "detalles": [
                    {"sku": "TEL-FEL-NEG-001", "consumo": 1.10, "ancho": 1.75},
                    {"sku": "RIB-NEG-001", "consumo": 0.20, "ancho": 0.90},
                    {"sku": "HIL-POL-NEG-001", "consumo": 255.00, "ancho": 0.00015},
                    {"sku": "ENT-FUS-001", "consumo": 0.05, "ancho": 0.10},

                    {"sku": "CORD-CAP-NEG-001", "cantidad": 1},
                    {"sku": "OJA-MET-001", "cantidad": 2},

                    {"sku": "ETQ-TALLA-XS-001", "cantidad": 1},
                    {"sku": "ETQ-MARCA-001", "cantidad": 1},
                    {"sku": "ETQ-CUIDADO-001", "cantidad": 1}
                ]
            },

            {
                "nombre": "Jogger Negro Hombre",
                "categoria": "Pantalones",
                "talla": "S",
                "detalles": [
                    {"sku": "TEL-FEL-NEG-001", "consumo": 1.15, "ancho": 1.75},
                    {"sku": "RIB-NEG-001", "consumo": 0.22, "ancho": 0.90},
                    {"sku": "HIL-POL-NEG-001", "consumo": 265.00, "ancho": 0.00015},
                    {"sku": "ENT-FUS-001", "consumo": 0.05, "ancho": 0.10},

                    {"sku": "CORD-CAP-NEG-001", "cantidad": 1},
                    {"sku": "OJA-MET-001", "cantidad": 2},

                    {"sku": "ETQ-TALLA-S-001", "cantidad": 1},
                    {"sku": "ETQ-MARCA-001", "cantidad": 1},
                    {"sku": "ETQ-CUIDADO-001", "cantidad": 1}
                ]
            },

            {
                "nombre": "Jogger Negro Hombre",
                "categoria": "Pantalones",
                "talla": "M",
                "detalles": [
                    {"sku": "TEL-FEL-NEG-001", "consumo": 1.25, "ancho": 1.75},
                    {"sku": "RIB-NEG-001", "consumo": 0.25, "ancho": 0.90},
                    {"sku": "HIL-POL-NEG-001", "consumo": 280.00, "ancho": 0.00015},
                    {"sku": "ENT-FUS-001", "consumo": 0.05, "ancho": 0.10},

                    {"sku": "CORD-CAP-NEG-001", "cantidad": 1},
                    {"sku": "OJA-MET-001", "cantidad": 2},

                    {"sku": "ETQ-TALLA-M-001", "cantidad": 1},
                    {"sku": "ETQ-MARCA-001", "cantidad": 1},
                    {"sku": "ETQ-CUIDADO-001", "cantidad": 1}
                ]
            },

            {
                "nombre": "Jogger Negro Hombre",
                "categoria": "Pantalones",
                "talla": "L",
                "detalles": [
                    {"sku": "TEL-FEL-NEG-001", "consumo": 1.35, "ancho": 1.75},
                    {"sku": "RIB-NEG-001", "consumo": 0.25, "ancho": 0.90},
                    {"sku": "HIL-POL-NEG-001", "consumo": 300.00, "ancho": 0.00015},
                    {"sku": "ENT-FUS-001", "consumo": 0.05, "ancho": 0.10},

                    {"sku": "CORD-CAP-NEG-001", "cantidad": 1},
                    {"sku": "OJA-MET-001", "cantidad": 2},

                    {"sku": "ETQ-TALLA-L-001", "cantidad": 1},
                    {"sku": "ETQ-MARCA-001", "cantidad": 1},
                    {"sku": "ETQ-CUIDADO-001", "cantidad": 1}
                ]
            },

            {
                "nombre": "Jogger Negro Hombre",
                "categoria": "Pantalones",
                "talla": "XL",
                "detalles": [
                    {"sku": "TEL-FEL-NEG-001", "consumo": 1.45, "ancho": 1.75},
                    {"sku": "RIB-NEG-001", "consumo": 0.28, "ancho": 0.90},
                    {"sku": "HIL-POL-NEG-001", "consumo": 325.00, "ancho": 0.00015},
                    {"sku": "ENT-FUS-001", "consumo": 0.05, "ancho": 0.10},

                    {"sku": "CORD-CAP-NEG-001", "cantidad": 1},
                    {"sku": "OJA-MET-001", "cantidad": 2},

                    {"sku": "ETQ-TALLA-XL-001", "cantidad": 1},
                    {"sku": "ETQ-MARCA-001", "cantidad": 1},
                    {"sku": "ETQ-CUIDADO-001", "cantidad": 1}
                ]
            },

            {
                "nombre": "Jogger Negro Hombre",
                "categoria": "Pantalones",
                "talla": "XXL",
                "detalles": [
                    {"sku": "TEL-FEL-NEG-001", "consumo": 1.55, "ancho": 1.75},
                    {"sku": "RIB-NEG-001", "consumo": 0.30, "ancho": 0.90},
                    {"sku": "HIL-POL-NEG-001", "consumo": 350.00, "ancho": 0.00015},
                    {"sku": "ENT-FUS-001", "consumo": 0.05, "ancho": 0.10},

                    {"sku": "CORD-CAP-NEG-001", "cantidad": 1},
                    {"sku": "OJA-MET-001", "cantidad": 2},

                    {"sku": "ETQ-TALLA-XXL-001", "cantidad": 1},
                    {"sku": "ETQ-MARCA-001", "cantidad": 1},
                    {"sku": "ETQ-CUIDADO-001", "cantidad": 1}
                ]
            },
            {
                "nombre": "Chamarra de Mezclilla Azul",
                "categoria": "Chamarras",
                "talla": "XSS",
                "detalles": [
                    {"sku": "TEL-DEN-AZL-001", "consumo": 1.35, "ancho": 1.50},
                    {"sku": "FOR-VIS-001", "consumo": 0.20, "ancho": 1.50},
                    {"sku": "HIL-POL-NEG-001", "consumo": 400.00, "ancho": 0.00015},

                    {"sku": "BTN-GOL-001", "cantidad": 6},
                    {"sku": "REM-MET-001", "cantidad": 4},

                    {"sku": "ETQ-TALLA-XSS-001", "cantidad": 1},
                    {"sku": "ETQ-MARCA-001", "cantidad": 1},
                    {"sku": "ETQ-CUIDADO-001", "cantidad": 1}
                ]
            },

            {
                "nombre": "Chamarra de Mezclilla Azul",
                "categoria": "Chamarras",
                "talla": "XS",
                "detalles": [
                    {"sku": "TEL-DEN-AZL-001", "consumo": 1.40, "ancho": 1.50},
                    {"sku": "FOR-VIS-001", "consumo": 0.20, "ancho": 1.50},
                    {"sku": "HIL-POL-NEG-001", "consumo": 420.00, "ancho": 0.00015},

                    {"sku": "BTN-GOL-001", "cantidad": 6},
                    {"sku": "REM-MET-001", "cantidad": 4},

                    {"sku": "ETQ-TALLA-XS-001", "cantidad": 1},
                    {"sku": "ETQ-MARCA-001", "cantidad": 1},
                    {"sku": "ETQ-CUIDADO-001", "cantidad": 1}
                ]
            },

            {
                "nombre": "Chamarra de Mezclilla Azul",
                "categoria": "Chamarras",
                "talla": "S",
                "detalles": [
                    {"sku": "TEL-DEN-AZL-001", "consumo": 1.50, "ancho": 1.50},
                    {"sku": "FOR-VIS-001", "consumo": 0.25, "ancho": 1.50},
                    {"sku": "HIL-POL-NEG-001", "consumo": 440.00, "ancho": 0.00015},

                    {"sku": "BTN-GOL-001", "cantidad": 6},
                    {"sku": "REM-MET-001", "cantidad": 4},

                    {"sku": "ETQ-TALLA-S-001", "cantidad": 1},
                    {"sku": "ETQ-MARCA-001", "cantidad": 1},
                    {"sku": "ETQ-CUIDADO-001", "cantidad": 1}
                ]
            },

            {
                "nombre": "Chamarra de Mezclilla Azul",
                "categoria": "Chamarras",
                "talla": "M",
                "detalles": [
                    {"sku": "TEL-DEN-AZL-001", "consumo": 1.60, "ancho": 1.50},
                    {"sku": "FOR-VIS-001", "consumo": 0.25, "ancho": 1.50},
                    {"sku": "HIL-POL-NEG-001", "consumo": 465.00, "ancho": 0.00015},

                    {"sku": "BTN-GOL-001", "cantidad": 6},
                    {"sku": "REM-MET-001", "cantidad": 4},

                    {"sku": "ETQ-TALLA-M-001", "cantidad": 1},
                    {"sku": "ETQ-MARCA-001", "cantidad": 1},
                    {"sku": "ETQ-CUIDADO-001", "cantidad": 1}
                ]
            },

            {
                "nombre": "Chamarra de Mezclilla Azul",
                "categoria": "Chamarras",
                "talla": "L",
                "detalles": [
                    {"sku": "TEL-DEN-AZL-001", "consumo": 1.75, "ancho": 1.50},
                    {"sku": "FOR-VIS-001", "consumo": 0.25, "ancho": 1.50},
                    {"sku": "HIL-POL-NEG-001", "consumo": 490.00, "ancho": 0.00015},

                    {"sku": "BTN-GOL-001", "cantidad": 6},
                    {"sku": "REM-MET-001", "cantidad": 4},

                    {"sku": "ETQ-TALLA-L-001", "cantidad": 1},
                    {"sku": "ETQ-MARCA-001", "cantidad": 1},
                    {"sku": "ETQ-CUIDADO-001", "cantidad": 1}
                ]
            },

            {
                "nombre": "Chamarra de Mezclilla Azul",
                "categoria": "Chamarras",
                "talla": "XL",
                "detalles": [
                    {"sku": "TEL-DEN-AZL-001", "consumo": 1.90, "ancho": 1.50},
                    {"sku": "FOR-VIS-001", "consumo": 0.30, "ancho": 1.50},
                    {"sku": "HIL-POL-NEG-001", "consumo": 520.00, "ancho": 0.00015},

                    {"sku": "BTN-GOL-001", "cantidad": 6},
                    {"sku": "REM-MET-001", "cantidad": 4},

                    {"sku": "ETQ-TALLA-XL-001", "cantidad": 1},
                    {"sku": "ETQ-MARCA-001", "cantidad": 1},
                    {"sku": "ETQ-CUIDADO-001", "cantidad": 1}
                ]
            },

            {
                "nombre": "Chamarra de Mezclilla Azul",
                "categoria": "Chamarras",
                "talla": "XXL",
                "detalles": [
                    {"sku": "TEL-DEN-AZL-001", "consumo": 2.05, "ancho": 1.50},
                    {"sku": "FOR-VIS-001", "consumo": 0.30, "ancho": 1.50},
                    {"sku": "HIL-POL-NEG-001", "consumo": 550.00, "ancho": 0.00015},

                    {"sku": "BTN-GOL-001", "cantidad": 6},
                    {"sku": "REM-MET-001", "cantidad": 4},

                    {"sku": "ETQ-TALLA-XXL-001", "cantidad": 1},
                    {"sku": "ETQ-MARCA-001", "cantidad": 1},
                    {"sku": "ETQ-CUIDADO-001", "cantidad": 1}
                ]
            },
           
            {
                "nombre": "Playera Blanca Oversize",
                "categoria": "Playeras",
                "talla": "XSS",
                "detalles": [
                    {"sku": "TEL-JER-BLA-001", "consumo": 0.65, "ancho": 1.75},
                    {"sku": "RIB-BLA-001", "consumo": 0.08, "ancho": 0.50},
                    {"sku": "HIL-POL-BLA-001", "consumo": 135.00, "ancho": 0.00015},
                    {"sku": "CIN-TAPA-BLA-001", "consumo": 0.65, "ancho": 0.01},

                    {"sku": "EST-PERS-001", "cantidad": 1},

                    {"sku": "ETQ-TALLA-XSS-001", "cantidad": 1},
                    {"sku": "ETQ-MARCA-001", "cantidad": 1},
                    {"sku": "ETQ-CUIDADO-001", "cantidad": 1}
                ]
            },

            {
                "nombre": "Playera Blanca Oversize",
                "categoria": "Playeras",
                "talla": "XS",
                "detalles": [
                    {"sku": "TEL-JER-BLA-001", "consumo": 0.70, "ancho": 1.75},
                    {"sku": "RIB-BLA-001", "consumo": 0.08, "ancho": 0.50},
                    {"sku": "HIL-POL-BLA-001", "consumo": 140.00, "ancho": 0.00015},
                    {"sku": "CIN-TAPA-BLA-001", "consumo": 0.68, "ancho": 0.01},

                    {"sku": "EST-PERS-001", "cantidad": 1},

                    {"sku": "ETQ-TALLA-XS-001", "cantidad": 1},
                    {"sku": "ETQ-MARCA-001", "cantidad": 1},
                    {"sku": "ETQ-CUIDADO-001", "cantidad": 1}
                ]
            },

            {
                "nombre": "Playera Blanca Oversize",
                "categoria": "Playeras",
                "talla": "S",
                "detalles": [
                    {"sku": "TEL-JER-BLA-001", "consumo": 0.75, "ancho": 1.75},
                    {"sku": "RIB-BLA-001", "consumo": 0.09, "ancho": 0.50},
                    {"sku": "HIL-POL-BLA-001", "consumo": 145.00, "ancho": 0.00015},
                    {"sku": "CIN-TAPA-BLA-001", "consumo": 0.72, "ancho": 0.01},

                    {"sku": "EST-PERS-001", "cantidad": 1},

                    {"sku": "ETQ-TALLA-S-001", "cantidad": 1},
                    {"sku": "ETQ-MARCA-001", "cantidad": 1},
                    {"sku": "ETQ-CUIDADO-001", "cantidad": 1}
                ]
            },

            {
                "nombre": "Playera Blanca Oversize",
                "categoria": "Playeras",
                "talla": "M",
                "detalles": [
                    {"sku": "TEL-JER-BLA-001", "consumo": 0.82, "ancho": 1.75},
                    {"sku": "RIB-BLA-001", "consumo": 0.10, "ancho": 0.50},
                    {"sku": "HIL-POL-BLA-001", "consumo": 152.00, "ancho": 0.00015},
                    {"sku": "CIN-TAPA-BLA-001", "consumo": 0.75, "ancho": 0.01},

                    {"sku": "EST-PERS-001", "cantidad": 1},

                    {"sku": "ETQ-TALLA-M-001", "cantidad": 1},
                    {"sku": "ETQ-MARCA-001", "cantidad": 1},
                    {"sku": "ETQ-CUIDADO-001", "cantidad": 1}
                ]
            },

            {
                "nombre": "Playera Blanca Oversize",
                "categoria": "Playeras",
                "talla": "L",
                "detalles": [
                    {"sku": "TEL-JER-BLA-001", "consumo": 0.90, "ancho": 1.75},
                    {"sku": "RIB-BLA-001", "consumo": 0.11, "ancho": 0.50},
                    {"sku": "HIL-POL-BLA-001", "consumo": 160.00, "ancho": 0.00015},
                    {"sku": "CIN-TAPA-BLA-001", "consumo": 0.78, "ancho": 0.01},

                    {"sku": "EST-PERS-001", "cantidad": 1},

                    {"sku": "ETQ-TALLA-L-001", "cantidad": 1},
                    {"sku": "ETQ-MARCA-001", "cantidad": 1},
                    {"sku": "ETQ-CUIDADO-001", "cantidad": 1}
                ]
            },

            {
                "nombre": "Playera Blanca Oversize",
                "categoria": "Playeras",
                "talla": "XL",
                "detalles": [
                    {"sku": "TEL-JER-BLA-001", "consumo": 0.98, "ancho": 1.75},
                    {"sku": "RIB-BLA-001", "consumo": 0.12, "ancho": 0.50},
                    {"sku": "HIL-POL-BLA-001", "consumo": 168.00, "ancho": 0.00015},
                    {"sku": "CIN-TAPA-BLA-001", "consumo": 0.82, "ancho": 0.01},

                    {"sku": "EST-PERS-001", "cantidad": 1},

                    {"sku": "ETQ-TALLA-XL-001", "cantidad": 1},
                    {"sku": "ETQ-MARCA-001", "cantidad": 1},
                    {"sku": "ETQ-CUIDADO-001", "cantidad": 1}
                ]
            },

            {
                "nombre": "Playera Blanca Oversize",
                "categoria": "Playeras",
                "talla": "XXL",
                "detalles": [
                    {"sku": "TEL-JER-BLA-001", "consumo": 1.05, "ancho": 1.75},
                    {"sku": "RIB-BLA-001", "consumo": 0.13, "ancho": 0.50},
                    {"sku": "HIL-POL-BLA-001", "consumo": 175.00, "ancho": 0.00015},
                    {"sku": "CIN-TAPA-BLA-001", "consumo": 0.85, "ancho": 0.01},

                    {"sku": "EST-PERS-001", "cantidad": 1},

                    {"sku": "ETQ-TALLA-XXL-001", "cantidad": 1},
                    {"sku": "ETQ-MARCA-001", "cantidad": 1},
                    {"sku": "ETQ-CUIDADO-001", "cantidad": 1}
                ]
            },
            {
                "nombre": 'SUDADERA TIPO "CROP TOP" (AL OMBLIGO) PARA MUJER',
                "categoria": "Sudaderas",
                "talla": "XSS",
                "detalles": [
                    {"sku": "TEL-FEL-BEI-001", "consumo": 0.85, "ancho": 1.75},
                    {"sku": "RIB-BEI-001", "consumo": 0.15, "ancho": 0.90},
                    {"sku": "HIL-POL-BEI-001", "consumo": 220.00, "ancho": 0.00015},
                    {"sku": "CIN-TAPA-BEI-001", "consumo": 0.30, "ancho": 0.01},
                    {"sku": "EST-PERS-001", "consumo": 1},
                    {"sku": "ETQ-TALLA-001", "consumo": 1},
                    {"sku": "ETQ-MARCA-001", "consumo": 1},
                    {"sku": "ETQ-CUIDADO-001", "consumo": 1}
                ]
            },
            {
                "nombre": 'SUDADERA TIPO "CROP TOP" (AL OMBLIGO) PARA MUJER',
                "categoria": "Sudaderas",
                "talla": "XS",
                "detalles": [
                    {"sku": "TEL-FEL-BEI-001", "consumo": 0.90, "ancho": 1.75},
                    {"sku": "RIB-BEI-001", "consumo": 0.15, "ancho": 0.90},
                    {"sku": "HIL-POL-BEI-001", "consumo": 230.00, "ancho": 0.00015},
                    {"sku": "CIN-TAPA-BEI-001", "consumo": 0.32, "ancho": 0.01},
                    {"sku": "EST-PERS-001", "consumo": 1},
                    {"sku": "ETQ-TALLA-001", "consumo": 1},
                    {"sku": "ETQ-MARCA-001", "consumo": 1},
                    {"sku": "ETQ-CUIDADO-001", "consumo": 1}
                ]
            },
            {
                "nombre": 'SUDADERA TIPO "CROP TOP" (AL OMBLIGO) PARA MUJER',
                "categoria": "Sudaderas",
                "talla": "S",
                "detalles": [
                    {"sku": "TEL-FEL-BEI-001", "consumo": 0.95, "ancho": 1.75},
                    {"sku": "RIB-BEI-001", "consumo": 0.18, "ancho": 0.90},
                    {"sku": "HIL-POL-BEI-001", "consumo": 240.00, "ancho": 0.00015},
                    {"sku": "CIN-TAPA-BEI-001", "consumo": 0.35, "ancho": 0.01},
                    {"sku": "EST-PERS-001", "consumo": 1},
                    {"sku": "ETQ-TALLA-001", "consumo": 1},
                    {"sku": "ETQ-MARCA-001", "consumo": 1},
                    {"sku": "ETQ-CUIDADO-001", "consumo": 1}
                ]
            },
            {
                "nombre": 'SUDADERA TIPO "CROP TOP" (AL OMBLIGO) PARA MUJER',
                "categoria": "Sudaderas",
                "talla": "M",
                "detalles": [
                    {"sku": "TEL-FEL-BEI-001", "consumo": 1.05, "ancho": 1.75},
                    {"sku": "RIB-BEI-001", "consumo": 0.20, "ancho": 0.90},
                    {"sku": "HIL-POL-BEI-001", "consumo": 260.00, "ancho": 0.00015},
                    {"sku": "CIN-TAPA-BEI-001", "consumo": 0.35, "ancho": 0.01},
                    {"sku": "EST-PERS-001", "consumo": 1},
                    {"sku": "ETQ-TALLA-001", "consumo": 1},
                    {"sku": "ETQ-MARCA-001", "consumo": 1},
                    {"sku": "ETQ-CUIDADO-001", "consumo": 1}
                ]
            },
            {
                "nombre": 'SUDADERA TIPO "CROP TOP" (AL OMBLIGO) PARA MUJER',
                "categoria": "Sudaderas",
                "talla": "L",
                "detalles": [
                    {"sku": "TEL-FEL-BEI-001", "consumo": 1.15, "ancho": 1.75},
                    {"sku": "RIB-BEI-001", "consumo": 0.20, "ancho": 0.90},
                    {"sku": "HIL-POL-BEI-001", "consumo": 280.00, "ancho": 0.00015},
                    {"sku": "CIN-TAPA-BEI-001", "consumo": 0.38, "ancho": 0.01},
                    {"sku": "EST-PERS-001", "consumo": 1},
                    {"sku": "ETQ-TALLA-001", "consumo": 1},
                    {"sku": "ETQ-MARCA-001", "consumo": 1},
                    {"sku": "ETQ-CUIDADO-001", "consumo": 1}
                ]
            },
            {
                "nombre": 'SUDADERA TIPO "CROP TOP" (AL OMBLIGO) PARA MUJER',
                "categoria": "Sudaderas",
                "talla": "XL",
                "detalles": [
                    {"sku": "TEL-FEL-BEI-001", "consumo": 1.25, "ancho": 1.75},
                    {"sku": "RIB-BEI-001", "consumo": 0.22, "ancho": 0.90},
                    {"sku": "HIL-POL-BEI-001", "consumo": 300.00, "ancho": 0.00015},
                    {"sku": "CIN-TAPA-BEI-001", "consumo": 0.40, "ancho": 0.01},
                    {"sku": "EST-PERS-001", "consumo": 1},
                    {"sku": "ETQ-TALLA-001", "consumo": 1},
                    {"sku": "ETQ-MARCA-001", "consumo": 1},
                    {"sku": "ETQ-CUIDADO-001", "consumo": 1}
                ]
            },
            {
                "nombre": 'SUDADERA TIPO "CROP TOP" (AL OMBLIGO) PARA MUJER',
                "categoria": "Sudaderas",
                "talla": "XXL",
                "detalles": [
                    {"sku": "TEL-FEL-BEI-001", "consumo": 1.35, "ancho": 1.75},
                    {"sku": "RIB-BEI-001", "consumo": 0.25, "ancho": 0.90},
                    {"sku": "HIL-POL-BEI-001", "consumo": 320.00, "ancho": 0.00015},
                    {"sku": "CIN-TAPA-BEI-001", "consumo": 0.42, "ancho": 0.01},
                    {"sku": "EST-PERS-001", "consumo": 1},
                    {"sku": "ETQ-TALLA-001", "consumo": 1},
                    {"sku": "ETQ-MARCA-001", "consumo": 1},
                    {"sku": "ETQ-CUIDADO-001", "consumo": 1}
                ]
            },
            {
                "nombre": "JOGGER PARA MUJER COLOR BEIGE CON TIRA DE COLOR NEGRO",
                "categoria": "Pantalones",
                "talla": "XSS",
                "detalles": [
                    {"sku": "TEL-INT-NEG-001", "consumo": 1.00, "ancho": 1.75},
                    {"sku": "CIN-VIVO-BLA-001", "consumo": 2.10, "ancho": 0.04},
                    {"sku": "ELA-NEG-004CM-001", "consumo": 0.65, "ancho": 0.04},
                    {"sku": "HIL-POL-NEG-001", "consumo": 120.00},
                    {"sku": "HIL-POL-BLA-001", "consumo": 45.00},
                    {"sku": "CIN-TAPA-NEG-001", "consumo": 0.65, "ancho": 0.01},
                    {"sku": "ETQ-TALLA-001", "consumo": 1},
                    {"sku": "ETQ-MARCA-001", "consumo": 1},
                    {"sku": "ETQ-CUIDADO-001", "consumo": 1}
                ]
            },
            {
                "nombre": "JOGGER PARA MUJER COLOR BEIGE CON TIRA DE COLOR NEGRO",
                "categoria": "Pantalones",
                "talla": "XS",
                "detalles": [
                    {"sku": "TEL-INT-NEG-001", "consumo": 1.05, "ancho": 1.75},
                    {"sku": "CIN-VIVO-BLA-001", "consumo": 2.15, "ancho": 0.04},
                    {"sku": "ELA-NEG-004CM-001", "consumo": 0.70, "ancho": 0.04},
                    {"sku": "HIL-POL-NEG-001", "consumo": 125.00},
                    {"sku": "HIL-POL-BLA-001", "consumo": 50.00},
                    {"sku": "CIN-TAPA-NEG-001", "consumo": 0.68, "ancho": 0.01},
                    {"sku": "ETQ-TALLA-001", "consumo": 1},
                    {"sku": "ETQ-MARCA-001", "consumo": 1},
                    {"sku": "ETQ-CUIDADO-001", "consumo": 1}
                ]
            },
            {
                "nombre": "JOGGER PARA MUJER COLOR BEIGE CON TIRA DE COLOR NEGRO",
                "categoria": "Pantalones",
                "talla": "S",
                "detalles": [
                    {"sku": "TEL-INT-NEG-001", "consumo": 1.10, "ancho": 1.75},
                    {"sku": "CIN-VIVO-BLA-001", "consumo": 2.25, "ancho": 0.04},
                    {"sku": "ELA-NEG-004CM-001", "consumo": 0.75, "ancho": 0.04},
                    {"sku": "HIL-POL-NEG-001", "consumo": 130.00},
                    {"sku": "HIL-POL-BLA-001", "consumo": 55.00},
                    {"sku": "CIN-TAPA-NEG-001", "consumo": 0.72, "ancho": 0.01},
                    {"sku": "ETQ-TALLA-001", "consumo": 1},
                    {"sku": "ETQ-MARCA-001", "consumo": 1},
                    {"sku": "ETQ-CUIDADO-001", "consumo": 1}
                ]
            },
            {
                "nombre": "JOGGER PARA MUJER COLOR BEIGE CON TIRA DE COLOR NEGRO",
                "categoria": "Pantalones",
                "talla": "M",
                "detalles": [
                    {"sku": "TEL-INT-NEG-001", "consumo": 1.15, "ancho": 1.75},
                    {"sku": "CIN-VIVO-BLA-001", "consumo": 2.30, "ancho": 0.04},
                    {"sku": "ELA-NEG-004CM-001", "consumo": 0.80, "ancho": 0.04},
                    {"sku": "HIL-POL-NEG-001", "consumo": 135.00},
                    {"sku": "HIL-POL-BLA-001", "consumo": 60.00},
                    {"sku": "CIN-TAPA-NEG-001", "consumo": 0.75, "ancho": 0.01},
                    {"sku": "ETQ-TALLA-001", "consumo": 1},
                    {"sku": "ETQ-MARCA-001", "consumo": 1},
                    {"sku": "ETQ-CUIDADO-001", "consumo": 1}
                ]
            },
            {
                "nombre": "JOGGER PARA MUJER COLOR BEIGE CON TIRA DE COLOR NEGRO",
                "categoria": "Pantalones",
                "talla": "L",
                "detalles": [
                    {"sku": "TEL-INT-NEG-001", "consumo": 1.25, "ancho": 1.75},
                    {"sku": "CIN-VIVO-BLA-001", "consumo": 2.40, "ancho": 0.04},
                    {"sku": "ELA-NEG-004CM-001", "consumo": 0.85, "ancho": 0.04},
                    {"sku": "HIL-POL-NEG-001", "consumo": 145.00},
                    {"sku": "HIL-POL-BLA-001", "consumo": 65.00},
                    {"sku": "CIN-TAPA-NEG-001", "consumo": 0.78, "ancho": 0.01},
                    {"sku": "ETQ-TALLA-001", "consumo": 1},
                    {"sku": "ETQ-MARCA-001", "consumo": 1},
                    {"sku": "ETQ-CUIDADO-001", "consumo": 1}
                ]
            },
            {
                "nombre": "JOGGER PARA MUJER COLOR BEIGE CON TIRA DE COLOR NEGRO",
                "categoria": "Pantalones",
                "talla": "XL",
                "detalles": [
                    {"sku": "TEL-INT-NEG-001", "consumo": 1.35, "ancho": 1.75},
                    {"sku": "CIN-VIVO-BLA-001", "consumo": 2.50, "ancho": 0.04},
                    {"sku": "ELA-NEG-004CM-001", "consumo": 0.90, "ancho": 0.04},
                    {"sku": "HIL-POL-NEG-001", "consumo": 155.00},
                    {"sku": "HIL-POL-BLA-001", "consumo": 70.00},
                    {"sku": "CIN-TAPA-NEG-001", "consumo": 0.82, "ancho": 0.01},
                    {"sku": "ETQ-TALLA-001", "consumo": 1},
                    {"sku": "ETQ-MARCA-001", "consumo": 1},
                    {"sku": "ETQ-CUIDADO-001", "consumo": 1}
                ]
            },
            {
                "nombre": "JOGGER PARA MUJER COLOR BEIGE CON TIRA DE COLOR NEGRO",
                "categoria": "Pantalones",
                "talla": "XXL",
                "detalles": [
                    {"sku": "TEL-INT-NEG-001", "consumo": 1.45, "ancho": 1.75},
                    {"sku": "CIN-VIVO-BLA-001", "consumo": 2.65, "ancho": 0.04},
                    {"sku": "ELA-NEG-004CM-001", "consumo": 1.00, "ancho": 0.04},
                    {"sku": "HIL-POL-NEG-001", "consumo": 165.00},
                    {"sku": "HIL-POL-BLA-001", "consumo": 80.00},
                    {"sku": "CIN-TAPA-NEG-001", "consumo": 0.85, "ancho": 0.01},
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
                        consumo_teorico_unitario=d.get("consumo", 0),
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