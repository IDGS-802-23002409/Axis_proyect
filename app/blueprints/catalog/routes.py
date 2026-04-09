from flask import Blueprint, render_template

catalog_bp = Blueprint('catalog', __name__, template_folder='../../templates/client')

from app.models.explosion_materiales import ExplosionMaterialesCabecera
from app.models.categorias import Categoria

def serialize_receta(e, is_new=False):
    return {
        "id": e.uuid_explosion,
        "name": e.nombre_receta,
        "price": float(e.productos[0].precio_venta) if e.productos else 0.0,
        "image": e.productos[0].imagen_url if e.productos and e.productos[0].imagen_url else "/static/images/default/default-image.png",
        "category": e.categoria.nombre if e.categoria else "Sin Categoria",
        "category_id": e.categoria.uuid_categoria if e.categoria else "all",
        "description": e.instrucciones_proceso or "Confección disponible",
        "sizes": [e.talla],
        "colors": ["Original"],
        "featured": True,
        "new": is_new
    }

def get_serialized_categories():
    base = [{"id": "all", "name": "Todo", "image": "/static/images/default/default-image.png"}]
    for c in Categoria.query.filter_by(estatus_visible=True).all():
        base.append({
            "id": c.uuid_categoria, 
            "name": c.nombre.upper(), 
            "image": c.imagen_url if c.imagen_url else "/static/images/default/default-image.png",
            "description": c.descripcion or "Colección"
        })
    return base

@catalog_bp.route('/')
def index():
    categorias = Categoria.query.filter_by(estatus_visible=True).order_by(Categoria.nombre).all()
    # Traer las últimas 4 recetas como destacadas
    recetas_db = ExplosionMaterialesCabecera.query.filter_by(estatus='ACTIVO').order_by(ExplosionMaterialesCabecera.fecha_creacion.desc()).limit(4).all()
    featured_products = [serialize_receta(e) for e in recetas_db]
    return render_template('index.html', categorias=categorias, featured_products=featured_products)

@catalog_bp.route('/about')
def about():
    return render_template('about.html')

@catalog_bp.route('/catalogo')
@catalog_bp.route('/catalog')
def catalog_view():
    recetas_db = ExplosionMaterialesCabecera.query.filter_by(estatus='ACTIVO').order_by(ExplosionMaterialesCabecera.fecha_creacion.desc()).all()
    products = [serialize_receta(e) for e in recetas_db]
    for p in products:
        p["category"] = p["category_id"] # El js template filtra por data-category={id}
    return render_template('catalogo.html', products=products, categories=get_serialized_categories())

@catalog_bp.route('/nuevo')
def nuevo():
    recetas_db = ExplosionMaterialesCabecera.query.filter_by(estatus='ACTIVO').order_by(ExplosionMaterialesCabecera.fecha_creacion.desc()).limit(8).all()
    products = [serialize_receta(e, is_new=True) for e in recetas_db]
    return render_template('nuevo.html', products=products)

@catalog_bp.route('/producto/<id>')
def producto(id):
    product_db = ExplosionMaterialesCabecera.query.get(id)
    if not product_db:
        return "Producto no encontrado", 404
    
    product = serialize_receta(product_db)
    
    related_db = ExplosionMaterialesCabecera.query.filter_by(uuid_categoria=product_db.uuid_categoria, estatus='ACTIVO').filter(ExplosionMaterialesCabecera.uuid_explosion != id).limit(4).all()
    related = [serialize_receta(e) for e in related_db]
    return render_template('producto.html', product=product, related=related)
