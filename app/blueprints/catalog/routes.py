from flask import Blueprint, render_template

catalog_bp = Blueprint('catalog', __name__, template_folder='../../templates/client')

from app.models.explosion_materiales import ExplosionMaterialesCabecera
from app.models.modelos_productos import ProductoTerminado
from app.models.categorias import Categoria

def serialize_producto_grouped(lista_productos, is_new=False):
    if not lista_productos: return None
    base = lista_productos[0]
    receta_base = base.explosion
    
    precio = float(base.precio_venta)
    imagen = base.imagen_url if base.imagen_url else "/static/images/default/default-image.png"
    sizes = []
    
    for p in lista_productos:
        sizes.append({
            "name": p.explosion.talla if p.explosion else 'Única',
            "id": p.uuid_explosion
        })
        # Si alguno tiene imagen priorízala
        if p.imagen_url and imagen == "/static/images/default/default-image.png":
            imagen = p.imagen_url

    return {
        "id": base.uuid_producto,
        "name": receta_base.nombre_receta if receta_base else "Producto",
        "price": precio,
        "image": imagen,
        "category": receta_base.categoria.nombre if receta_base and receta_base.categoria else "Sin Categoria",
        "category_id": receta_base.categoria.uuid_categoria if receta_base and receta_base.categoria else "all",
        "description": receta_base.instrucciones_proceso if receta_base else "Confección disponible",
        "sizes": sizes,
        "colors": ["Original"],
        "featured": True,
        "new": is_new
    }

def get_grouped_productos_db(limit=None):
    # Extraemos todos los productos terminados activos
    productos_db = ProductoTerminado.query.filter_by(active=True).all()
    grouped = {}
    
    # Agrupamos por nombre de receta (si tienen)
    for p in productos_db:
        if not p.explosion: continue
        nombre = p.explosion.nombre_receta
        if nombre not in grouped:
            grouped[nombre] = []
        grouped[nombre].append(p)
    
    products = []
    for nombre, lista in grouped.items():
        products.append(serialize_producto_grouped(lista))
        
    if limit:
        return products[:limit]
    return products

def get_serialized_categories():
    base = [{"id": "all", "name": "Todo", "image": "/static/images/default/default-image.png"}]
    for c in Categoria.query.filter_by(estatus_visible=True, tipo="Prenda").order_by(Categoria.nombre).all():
        base.append({
            "id": c.uuid_categoria, 
            "name": c.nombre.upper(), 
            "image": c.imagen_url if c.imagen_url else "/static/images/default/default-image.png",
            "description": c.descripcion or "Colección"
        })
    return base

@catalog_bp.route('/')
def index():
    categorias = Categoria.query.filter_by(estatus_visible=True, tipo="Prenda").order_by(Categoria.nombre).all()
    # Traer las últimas 4 recetas como destacadas
    featured_products = get_grouped_productos_db(limit=4)
    return render_template('index.html', categorias=categorias, featured_products=featured_products)

@catalog_bp.route('/about')
def about():
    return render_template('about.html')

@catalog_bp.route('/catalogo')
@catalog_bp.route('/catalog')
def catalog_view():
    products = get_grouped_productos_db()
    for p in products:
        p["category"] = p["category_id"] # El js template filtra por data-category={id}
    return render_template('catalogo.html', products=products, categories=get_serialized_categories())

@catalog_bp.route('/nuevo')
def nuevo():
    products = get_grouped_productos_db(limit=8)
    for p in products: p["new"] = True
    return render_template('nuevo.html', products=products)

@catalog_bp.route('/producto/<id>')
def producto(id):
    product_db = ProductoTerminado.query.get(id)
    if not product_db or not product_db.explosion:
        return "Producto no encontrado", 404
    
    # Obtener todas las tallas del mismo producto cruzando con receta
    todas_las_tallas = ProductoTerminado.query.join(ExplosionMaterialesCabecera).filter(
        ExplosionMaterialesCabecera.nombre_receta == product_db.explosion.nombre_receta,
        ProductoTerminado.active == True
    ).all()
    
    product = serialize_producto_grouped(todas_las_tallas)
    
    # Productos relacionados de la misma categoría, excluyendo la receta actual
    related_db_raw = ProductoTerminado.query.join(ExplosionMaterialesCabecera).filter(
        ExplosionMaterialesCabecera.uuid_categoria == product_db.explosion.uuid_categoria, 
        ExplosionMaterialesCabecera.nombre_receta != product_db.explosion.nombre_receta,
        ProductoTerminado.active == True
    ).all()
    
    grouped_related = {}
    for p in related_db_raw:
        if p.explosion:
            nombre = p.explosion.nombre_receta
            if nombre not in grouped_related:
                grouped_related[nombre] = []
            grouped_related[nombre].append(p)
        
    related = []
    for count, (nombre, lista) in enumerate(grouped_related.items()):
        if count >= 4: break
        related.append(serialize_producto_grouped(lista))
        
    return render_template('producto.html', product=product, related=related)
