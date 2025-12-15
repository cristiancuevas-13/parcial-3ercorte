# =====================================================================
# URLS.PY - Define las rutas/URLs de la aplicación
# =====================================================================
# Cada path() conecta una URL con una función en views.py
# Formato: path("url/", views.funcion, name="nombre")
#   - "url/" = Lo que aparece en el navegador (ej: localhost/login/)
#   - views.funcion = La función que se ejecuta cuando visitas esa URL
#   - name="nombre" = Nombre para usar en los templates con {% url 'nombre' %}
# =====================================================================

from django.urls import path
from . import views

urlpatterns = [
    # RUTAS ORIGINALES (ya existían)
    path ("home/", views.saludo,name="home1"),
    path ("anime/", views.anime,name="principal"),
    path ("bye/", views.despedida,name="bye1",),
    path("plantilla/",views.mundo,name="plantilla"),
    path("formulario/",views.formulario,name="formulario"),
    path("login/", views.login, name="login"),
    
    # =====================================================================
    # NUEVAS RUTAS AGREGADAS
    # =====================================================================
    
    # LISTA DE USUARIOS: Muestra todos los usuarios en una tabla
    # URL: localhost/usuarios/
    path("usuarios/", views.usuarios, name="usuarios"),
    
    # ELIMINAR USUARIO: Elimina un usuario por su ID
    # URL: localhost/eliminar/5/ (eliminará el usuario con id=5)
    # <int:id> = Captura un número de la URL y lo pasa como parámetro 'id'
    path("eliminar/<int:id>/", views.eliminar_usuario, name="eliminar_usuario"),
    
    # ACTUALIZAR USUARIO: Formulario para editar los datos de un usuario
    # URL: localhost/actualizar/5/ (editará el usuario con id=5)
    path("actualizar/<int:id>/", views.actualizar_usuario, name="actualizar_usuario"),
    
    # CERRAR SESIÓN: Hace logout del usuario
    # URL: localhost/logout/
    path("logout/", views.logout, name="logout"),
    
    # BIENVENIDA: Landing page
    path("", views.welcome, name="welcome"),

    # DASHBOARD
    path("dashboard/", views.dashboard, name="dashboard"),

    # MENÚ CRUD
    path("menu/", views.menu_list, name="menu_list"),
    path("menu/nuevo/", views.crear_producto, name="crear_producto"),
    path("menu/editar/<int:id>/", views.editar_producto, name="editar_producto"),
    path("menu/eliminar/<int:id>/", views.eliminar_producto, name="eliminar_producto"),

    # INVENTARIO CRUD
    path("inventario/", views.inventario_list, name="inventario_list"),
    path("inventario/nuevo/", views.crear_insumo, name="crear_insumo"),
    path("inventario/editar/<int:id>/", views.editar_insumo, name="editar_insumo"),
    path("inventario/eliminar/<int:id>/", views.eliminar_insumo, name="eliminar_insumo"),

    # EMPLEADOS CRUD
    path("empleados/", views.empleados_list, name="empleados_list"),
    path("empleados/nuevo/", views.crear_empleado, name="crear_empleado"),
    path("empleados/editar/<int:id>/", views.editar_empleado, name="editar_empleado"),
    path("empleados/eliminar/<int:id>/", views.eliminar_empleado, name="eliminar_empleado"),
]
# Force Reload