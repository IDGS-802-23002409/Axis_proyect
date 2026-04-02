from flask import Blueprint, render_template

catalog_bp = Blueprint('catalog', __name__, template_folder='../../templates/client')

CATEGORIES = [
  {"id": "all", "name": "Todo"},
  {"id": "hoodies", "name": "Hoodies"},
  {"id": "camisetas", "name": "Camisetas"},
  {"id": "sudaderas", "name": "Sudaderas"},
  {"id": "pantalones", "name": "Pantalones"},
  {"id": "chaquetas", "name": "Chaquetas"},
  {"id": "accesorios", "name": "Accesorios"}
]

PRODUCTS = [
  {
    "id": "1", "name": "AXIS OVERSIZED HOODIE", "price": 89.99, "image": "https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=800&h=1000&fit=crop",
    "category": "hoodies", "description": "Hoodie oversize con estampado graffiti exclusivo. 100% algodón premium.",
    "sizes": ["S", "M", "L", "XL", "XXL"], "colors": ["Negro", "Blanco", "Gris"], "featured": True, "new": True
  },
  {
    "id": "2", "name": "STREET ART TEE", "price": 45.99, "image": "https://images.unsplash.com/photo-1576566588028-4147f3842f27?w=800&h=1000&fit=crop",
    "category": "camisetas", "description": "Camiseta con arte urbano original. Corte relajado.",
    "sizes": ["S", "M", "L", "XL"], "colors": ["Negro", "Blanco"], "featured": True, "new": False
  },
  {
    "id": "3", "name": "CARGO PANTS URBAN", "price": 79.99, "image": "https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?w=800&h=1000&fit=crop",
    "category": "pantalones", "description": "Pantalones cargo con múltiples bolsillos. Estilo militar urbano.",
    "sizes": ["28", "30", "32", "34", "36"], "colors": ["Negro", "Verde Militar", "Beige"], "featured": True, "new": False
  },
  {
    "id": "4", "name": "GRAFFITI BOMBER", "price": 129.99, "image": "https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=800&h=1000&fit=crop",
    "category": "chaquetas", "description": "Bomber jacket con estampado graffiti en la espalda.",
    "sizes": ["S", "M", "L", "XL"], "colors": ["Negro"], "featured": True, "new": True
  },
  {
    "id": "5", "name": "AXIS CAP", "price": 35.99, "image": "https://images.unsplash.com/photo-1588850561407-ed78c282e89b?w=800&h=1000&fit=crop",
    "category": "accesorios", "description": "Gorra snapback con logo AXIS bordado.",
    "sizes": ["Única"], "colors": ["Negro", "Blanco"], "featured": False, "new": False
  },
  {
    "id": "6", "name": "URBAN JOGGERS", "price": 69.99, "image": "https://images.unsplash.com/photo-1552902865-b72c031ac5ea?w=800&h=1000&fit=crop",
    "category": "pantalones", "description": "Joggers de algodón con detalles reflectantes.",
    "sizes": ["S", "M", "L", "XL"], "colors": ["Negro", "Gris"], "featured": False, "new": False
  },
  {
    "id": "7", "name": "REBEL CREWNECK", "price": 75.99, "image": "https://images.unsplash.com/photo-1578587018452-892bacefd3f2?w=800&h=1000&fit=crop",
    "category": "sudaderas", "description": "Sudadera cuello redondo con gráficos abstractos.",
    "sizes": ["S", "M", "L", "XL", "XXL"], "colors": ["Negro", "Blanco", "Morado"], "featured": False, "new": True
  },
  {
    "id": "8", "name": "CHAIN NECKLACE", "price": 49.99, "image": "https://images.unsplash.com/photo-1611652022419-a9419f74343d?w=800&h=1000&fit=crop",
    "category": "accesorios", "description": "Collar de cadena con colgante AXIS.",
    "sizes": ["Única"], "colors": ["Plata", "Negro"], "featured": False, "new": False
  },
  {
    "id": "9", "name": "DISTRESSED DENIM", "price": 99.99, "image": "https://images.unsplash.com/photo-1542272604-787c3835535d?w=800&h=1000&fit=crop",
    "category": "pantalones", "description": "Jeans rotos con parches de arte urbano.",
    "sizes": ["28", "30", "32", "34", "36"], "colors": ["Azul Oscuro", "Negro"], "featured": False, "new": False
  },
  {
    "id": "10", "name": "GRAPHIC LONG SLEEVE", "price": 55.99, "image": "https://images.unsplash.com/photo-1618354691373-d851c5c3a990?w=800&h=1000&fit=crop",
    "category": "camisetas", "description": "Camiseta manga larga con estampado en mangas.",
    "sizes": ["S", "M", "L", "XL"], "colors": ["Negro", "Blanco"], "featured": False, "new": False
  },
  {
    "id": "11", "name": "AXIS BEANIE", "price": 29.99, "image": "https://images.unsplash.com/photo-1576871337622-98d48d1cf531?w=800&h=1000&fit=crop",
    "category": "accesorios", "description": "Gorro de punto con parche AXIS.",
    "sizes": ["Única"], "colors": ["Negro", "Gris", "Morado"], "featured": False, "new": False
  },
  {
    "id": "12", "name": "TECH WINDBREAKER", "price": 119.99, "image": "https://images.unsplash.com/photo-1544022613-e87ca75a784a?w=800&h=1000&fit=crop",
    "category": "chaquetas", "description": "Cortavientos técnico con capucha y detalles reflectantes.",
    "sizes": ["S", "M", "L", "XL"], "colors": ["Negro", "Blanco/Negro"], "featured": False, "new": True
  }
]

@catalog_bp.route('/')
def index():
    return render_template('index.html')

@catalog_bp.route('/about')
def about():
    return render_template('about.html')

@catalog_bp.route('/catalogo')
@catalog_bp.route('/catalog')
def catalog_view():
    return render_template('catalogo.html', products=PRODUCTS, categories=CATEGORIES)

@catalog_bp.route('/nuevo')
def nuevo():
    new_products = [p for p in PRODUCTS if p.get('new')]
    return render_template('nuevo.html', products=new_products)

@catalog_bp.route('/producto/<id>')
def producto(id):
    product = next((p for p in PRODUCTS if p['id'] == id), None)
    if not product:
        return "Producto no encontrado", 404
    
    related = [p for p in PRODUCTS if p['category'] == product['category'] and p['id'] != id][:4]
    return render_template('producto.html', product=product, related=related)
