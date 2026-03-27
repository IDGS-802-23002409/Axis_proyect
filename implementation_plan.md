# Análisis de Protección de Rutas y RBAC

Este documento detalla el estado actual de la seguridad en el proyecto y proporciona una guía para que los desarrolladores limiten rutas y elementos de la interfaz según roles específicos.

## Estado Actual

El proyecto utiliza **Flask-Security-Too** para gestionar la autenticación y autorización. Los componentes clave son:

- **Modelos**: [Usuario](file:///c:/Users/damia/Documents/Axis_proyect/app/models/usuarios.py#19-55) y [Role](file:///c:/Users/damia/Documents/Axis_proyect/app/models/usuarios.py#14-18). **Cada usuario tiene estrictamente un solo rol.**
- **Protección de Rutas**: Se utilizan decoradores en los controladores (blueprints).
- **Lógica de Redirección**: En [app/blueprints/security/routes.py](file:///c:/Users/damia/Documents/Axis_proyect/app/blueprints/security/routes.py), la función [post_login](file:///c:/Users/damia/Documents/Axis_proyect/app/blueprints/security/routes.py#6-24) redirige a los usuarios según su rol único.
- **Registro Automático**: Cualquier usuario nuevo registrado a través de la web recibe automáticamente el rol `cliente`.
- **Flujo de Verificación**: Si un usuario intenta loguearse sin haber verificado su email, el sistema le enviará automáticamente un nuevo correo de confirmación y lo redirigirá a la página de re-envío de instrucciones.

### Roles Disponibles
- `admin`: Acceso total.
- `gerente`: Gestión comercial.
- `produccion`: Acceso al taller.
- `cliente`: Acceso a la tienda.

---

## Guía para el Desarrollador

### 1. Limitar el Acceso a Rutas (Backend)

Para proteger una ruta, se deben importar los decoradores necesarios de `flask_security`:

```python
from flask_security import login_required, roles_required, roles_accepted
```

#### Uso de `@login_required`
Requiere que el usuario esté autenticado.
```python
@bp.route('/mi-ruta')
@login_required
def mi_funcion():
    ...
```

#### Uso de `@roles_required`
Requiere que el usuario tenga **todos** los roles especificados.
```python
@bp.route('/solo-admin')
@roles_required('admin')
def ruta_admin():
    ...
```

#### Uso de `@roles_accepted`
Permite el acceso si el usuario tiene **al menos uno** de los roles indicados.
```python
@bp.route('/taller')
@roles_accepted('admin', 'produccion')
def ruta_taller():
    ...
```

---

## 2. Visibilidad Dinámica en Interfaces (Frontend/Jinja2)

Para que los elementos (links, botones) solo aparezcan para roles específicos, se deben usar los métodos del objeto `current_user` en las plantillas.

### Verificar si un usuario tiene un rol
```html
{% if current_user.has_role('admin') %}
  <a href="{{ url_for('usuarios.index') }}">Panel de Administración</a>
{% endif %}
```

### Ejemplo en [layout.html](file:///c:/Users/damia/Documents/Axis_proyect/app/templates/produccion/layout.html) (Recomendado)
Actualmente, el sidebar en [app/templates/produccion/layout.html](file:///c:/Users/damia/Documents/Axis_proyect/app/templates/produccion/layout.html) tiene elementos estáticos. Deberías cambiarlo a:

```html
<!-- Sidebar -->
<aside ...>
  ...
  {% if current_user.has_role('admin') %}
  <div>
    <p class="...">Administración</p>
    <a href="{{ url_for('usuarios.index') }}" class="...">
      <i data-lucide="users"></i> Usuarios
    </a>
  </div>
  {% endif %}

  {% if current_user.has_role('produccion') %}
  <div>
    <p class="...">Taller</p>
    <!-- Filtros de producción aqui -->
  </div>
  {% endif %}
</aside>
```

### Mostrar Información del Usuario Logueado
Evita usar datos "hardcoded". Usa:
- `{{ current_user.nombre_completo }}`
- `{{ current_user.roles[0].name if current_user.roles else 'Sin Rol' }}` (Aunque solo tengan uno, Flask-Security lo maneja como lista).

---

## Creación de Administrador Inicial

Para crear el primer administrador (ya que el registro web solo crea clientes), he creado un script automatizado para evitar errores de importación.

### Opción A: Usar el script (Recomendado)
Ejecuta esto desde la terminal en la raíz del proyecto:
```bash
python create_admin.py
```
*Si estás usando Docker:* `docker-compose exec flask_app python create_admin.py`

### Opción B: Manual (Flask Shell)
Si prefieres hacerlo manualmente, estos son los comandos corregidos (debes usar `hash_password` para que funcione el login):
```python
flask shell
>>> from app.utils.database_connection import db
>>> from app.models.usuarios import Role
>>> from flask_security.utils import hash_password
>>> ds = app.extensions['security'].datastore
>>> role = Role.query.filter_by(name='admin').first()
>>> ds.create_user(nombre_completo='Admin', email='admin@axis.com', password=hash_password('password123'), roles=[role])
>>> db.session.commit()
```

---

## Verificación Plan

### Pruebas Manuales
1. **Acceso Prohibido**: Intentar acceder a `/usuarios` con un usuario que no sea `admin`. Debe redirigir a `/login` o mostrar un error 403.
2. **Interfaz Condicional**: Iniciar sesión con un usuario de rol `produccion` y verificar que el link de "Usuarios" no aparezca en el menú lateral.
3. **Redirección Post-Login**: Verificar que al loguearse, el usuario sea enviado a la ruta correcta definida en [app/blueprints/security/routes.py](file:///c:/Users/damia/Documents/Axis_proyect/app/blueprints/security/routes.py).
