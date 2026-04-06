from flask import Blueprint, render_template

catalog_bp = Blueprint('catalog', __name__, template_folder='../../templates/client')

from app.models.modelos_productos import ModeloRopa
from app.models.categorias import Categoria

def serialize_modelo(m, is_new=False):
    return {
        "id": m.uuid_modelo,
        "name": m.nombre_modelo,
        "price": float(m.productos[0].precio_venta) if m.productos else 0.0,
        "image": m.imagen_url,
        "category": m.categoria.nombre if m.categoria else "Sin Categoria",
        "category_id": m.categoria.uuid_categoria if m.categoria else "all",
        "description": m.descripcion,
        "sizes": [p.talla for p in m.productos],
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
    # Traer los últimos 4 productos como destacados
    modelos_db = ModeloRopa.query.order_by(ModeloRopa.fecha_creacion.desc()).limit(4).all()
    featured_products = [serialize_modelo(m) for m in modelos_db]
    return render_template('index.html', categorias=categorias, featured_products=featured_products)

@catalog_bp.route('/about')
def about():
    return render_template('about.html')

@catalog_bp.route('/catalogo')
@catalog_bp.route('/catalog')
def catalog_view():
    modelos_db = ModeloRopa.query.order_by(ModeloRopa.fecha_creacion.desc()).all()
    products = [serialize_modelo(m) for m in modelos_db]
    for p in products:
        p["category"] = p["category_id"] # El js template filtra por data-category={id}
    return render_template('catalogo.html', products=products, categories=get_serialized_categories())

@catalog_bp.route('/nuevo')
def nuevo():
    new_db = ModeloRopa.query.order_by(ModeloRopa.fecha_creacion.desc()).limit(8).all()
    products = [serialize_modelo(m, is_new=True) for m in new_db]
    return render_template('nuevo.html', products=products)

@catalog_bp.route('/producto/<id>')
def producto(id):
    product_db = ModeloRopa.query.get(id)
    if not product_db:
        return "Producto no encontrado", 404
    
    product = serialize_modelo(product_db)
    
    related_db = ModeloRopa.query.filter_by(uuid_categoria=product_db.uuid_categoria).filter(ModeloRopa.uuid_modelo != id).limit(4).all()
    related = [serialize_modelo(m) for m in related_db]
    return render_template('producto.html', product=product, related=related)
