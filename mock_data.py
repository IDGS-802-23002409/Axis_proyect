import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))

from database.seed.usuarios_roles import run_seed as seed_usuarios_roles
from database.seed.categorias_insumos import run_seed as seed_categorias_insumos
from database.seed.data_proveedores import run_seed as seed_proveedores
from database.seed.data_recetas import run_seed as seed_recetas
from database.seed.productos import run_seed as seed_productos
from database.seed.data_historico_transacciones import run_seed as seed_historico

def main_seed():
    print("=" * 60)
    print("🚀 INICIANDO EJECUCIÓN CENTRALIZADA DE SEEDS DE AXIS 🚀")
    print("=" * 60)

    try:
        print("\n[1/6] Ejecutando: Usuarios y Roles...")
        seed_usuarios_roles()

        print("\n[2/6] Ejecutando: Categorías e Insumos...")
        seed_categorias_insumos()

        print("\n[3/6] Ejecutando: Proveedores...")
        seed_proveedores()

        print("\n[4/6] Ejecutando: Recetas (Explosión de Materiales)...")
        seed_recetas()

        print("\n[5/6] Ejecutando: Productos Terminados...")
        seed_productos()

        print("\n[6/6] Ejecutando: Histórico de Transacciones (2 meses)...")
        seed_historico()

        print("=" * 60)
        print("✅ TODOS LOS SEEDS SE EJECUTARON CORRECTAMENTE ✅")
        print("=" * 60)
    except Exception as e:
        print("=" * 60)
        print(f"❌ OCURRIÓ UN ERROR DURANTE LA EJECUCIÓN DE SEEDS: {e}")
        print("=" * 60)

if __name__ == '__main__':
    main_seed()