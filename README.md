## Axis_proyect
ERP para una empresa de ropa llamada "Axis" que tiene como objetivo administrar insumos, monitorizacion de metricas y venta al publico general

## Organizacion del proyecto (file struct)

/proyecto_integrador
│
├── /app
│   ├── /__init__.py          # App Factory: Configuración de Flask
│   ├── /models.py            # Modelos de SQLAlchemy (Tablas MySQL)
│   ├── /auth                 # Blueprint de Autenticación
│   ├── /inventario           # Blueprint de Materias Primas y Producción
│   ├── /ventas               # Blueprint de Punto de Venta (POS)
│   └── /static               # CSS (Tailwind/Bootstrap), JS, Imágenes
│
├── /logs                     # Registro de errores y movimientos [cite: 100]
├── config.py                 # Variables de entorno y llaves secretas
└── run.py                    # Punto de entrada de la aplicación
