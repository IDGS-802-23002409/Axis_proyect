import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))

from app.app import app
from app.utils.database_connection import db
from app.models.proveedores import Proveedor


def run_seed():
    with app.app_context():

        print(">> [INICIO] Seed de proveedores...")

        proveedores_data = [
            {"razon_social": "Textiles del Bajío S.A. de C.V.", "rfc": "TBA901203AB1", "contacto_nombre": "Luis Hernández", "telefono": "4771002001", "usuario_creo_uuid": "SYSTEM", "estatus": True},
            {"razon_social": "Hilos Industriales León", "rfc": "HIL850112CD2", "contacto_nombre": "María Gómez", "telefono": "4771002002", "usuario_creo_uuid": "SYSTEM", "estatus": True},
            {"razon_social": "Distribuidora de Telas El Águila", "rfc": "DTA920415EF3", "contacto_nombre": "Carlos Ramírez", "telefono": "4771002003", "usuario_creo_uuid": "SYSTEM", "estatus": True},
            {"razon_social": "Suministros Textiles del Norte", "rfc": "STN880722GH4", "contacto_nombre": "Ana Torres", "telefono": "4771002004", "usuario_creo_uuid": "SYSTEM", "estatus": True},
            {"razon_social": "Fábrica de Insumos Industriales MX", "rfc": "FII950310IJ5", "contacto_nombre": "José Martínez", "telefono": "4771002005", "usuario_creo_uuid": "SYSTEM", "estatus": True},
            {"razon_social": "Proveedor Textil Central", "rfc": "PTC810620KL6", "contacto_nombre": "Laura Sánchez", "telefono": "4771002006", "usuario_creo_uuid": "SYSTEM", "estatus": True},
            {"razon_social": "El Mundo del Hilo S.A.", "rfc": "EMH930901MN7", "contacto_nombre": "Pedro Vargas", "telefono": "4771002007", "usuario_creo_uuid": "SYSTEM", "estatus": True},
            {"razon_social": "Telas y Confecciones Bajío", "rfc": "TCB870223OP8", "contacto_nombre": "Sofía Delgado", "telefono": "4771002008", "usuario_creo_uuid": "SYSTEM", "estatus": True},
            {"razon_social": "Importadora Textil Nacional", "rfc": "ITN900514QR9", "contacto_nombre": "Ricardo Luna", "telefono": "4771002009", "usuario_creo_uuid": "SYSTEM", "estatus": True},
            {"razon_social": "Innovación Textil Moderna", "rfc": "ITM960830ST0", "contacto_nombre": "Fernanda Cruz", "telefono": "4771002010", "usuario_creo_uuid": "SYSTEM", "estatus": True}
        ]

        insertados = 0
        saltados = 0

        for p in proveedores_data:

            existe = Proveedor.query.filter(
                (Proveedor.rfc == p["rfc"]) |
                (Proveedor.telefono == p["telefono"])
            ).first()

            if existe:
                saltados += 1
                continue

            db.session.add(Proveedor(**p))
            insertados += 1

        db.session.commit()

        print(f">> [OK] Proveedores insertados: {insertados}")
        print(f">> [SKIP] Proveedores existentes: {saltados}")


if __name__ == "__main__":
    run_seed()