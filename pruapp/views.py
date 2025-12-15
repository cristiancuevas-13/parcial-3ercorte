# =====================================================================
# IMPORTS - Importar las funciones que necesitamos de Django
# =====================================================================
# render: sirve para mostrar un archivo HTML al usuario
# redirect: sirve para enviar al usuario a otra página
from django.shortcuts import render, redirect, get_object_or_404

# Practica: es el modelo (tabla) donde guardamos los usuarios en la base de datos
from .models import Practica, Producto, Insumo, Empleado

# HttpResponse: sirve para enviar texto simple al navegador
from django.http import HttpResponse

def saludo(request):
    return HttpResponse("Hola mundo")

def despedida(request):
    return HttpResponse("Hasta luego")

def anime(request):
    return render(request, "./1/anime.html")

def mundo(request):
    return render(request, "./plantilla.html")


# =====================================================================
# VISTA DE LOGIN (NUEVA)
# =====================================================================
# PROPÓSITO: Permite al usuario iniciar sesión
# CÓMO FUNCIONA:
#   1. El usuario escribe su usuario y contraseña en el formulario
#   2. Se busca el usuario en la base de datos
#   3. Si existe y la contraseña es correcta, se guarda la sesión
#   4. Si no, se muestra un mensaje de error
# =====================================================================
def login(request):
    # request.method indica cómo llegó el usuario a esta página
    # "POST" significa que envió un formulario
    # "GET" significa que solo está viendo la página
    if request.method == "POST":
        # request.POST.get("nombre") obtiene el valor del campo con name="nombre" del formulario HTML
        usern = request.POST.get("username")  # Obtiene lo que escribió en el campo username
        passw = request.POST.get("password")  # Obtiene lo que escribió en el campo password
        
        # try/except: intenta ejecutar el código, si hay error lo captura
        try:
            # .get() busca UN usuario que tenga ese username en la base de datos
            # Si encuentra más de uno o ninguno, da error
            usuario = Practica.objects.get(username=usern)
            
            # Comparar la contraseña que escribió con la que está guardada
            if usuario.password == passw:
                # ¡Contraseña correcta! Guardar datos en la SESIÓN
                # La sesión es como una "memoria" que recuerda quién está logueado
                # request.session es un diccionario donde guardamos datos
                request.session['usuario_id'] = usuario.id        # Guardar el ID del usuario
                request.session['usuario_nombre'] = usuario.username  # Guardar el nombre
                
                # redirect("nombre") envía al usuario a la URL con ese nombre
                return redirect("dashboard")  # Ir a la página del dashboard (Welcome/Dashboard view)
            else:
                # Contraseña incorrecta - mostrar error
                return render(request, "login.html", {"error": "Contraseña incorrecta"})
                
        except Practica.DoesNotExist:
            # El usuario no existe en la base de datos
            return render(request, "login.html", {"error": "El usuario no existe"})
    
    # Si no es POST (es GET), solo mostrar el formulario vacío
    return render(request, "login.html")


# =====================================================================
# VISTA DE USUARIOS (NUEVA)
# =====================================================================
# PROPÓSITO: Muestra una lista de todos los usuarios registrados
# REQUISITO: El usuario debe estar logueado para ver esta página
# CÓMO FUNCIONA:
#   1. Verifica si hay sesión activa
#   2. Obtiene todos los usuarios de la base de datos
#   3. Envía la lista al template para mostrarla en una tabla
# =====================================================================
def usuarios(request):
    # VERIFICAR SESIÓN: comprobar si el usuario está logueado
    # 'usuario_id' se guardó cuando hizo login, si no existe, no está logueado
    if 'usuario_id' not in request.session:
        return redirect("login")  # No está logueado, enviarlo al login
    
    # .all() obtiene TODOS los registros de la tabla Practica (todos los usuarios)
    lista_usuarios = Practica.objects.all()
    
    # Obtener el nombre del usuario logueado desde la sesión
    usuario_actual = request.session.get('usuario_nombre')
    
    # render() muestra el archivo HTML y le pasa datos
    # Los datos van en un diccionario: {"nombre_variable": valor}
    # En el HTML puedes usar {{ nombre_variable }} para mostrar el valor
    return render(request, "usuarios.html", {
        "usuarios": lista_usuarios,       # Lista de todos los usuarios
        "usuario_actual": usuario_actual  # Nombre del usuario logueado
    })


# =====================================================================
# ELIMINAR USUARIO (NUEVA)
# =====================================================================
# PROPÓSITO: Elimina un usuario de la base de datos
# CÓMO FUNCIONA:
#   1. Recibe el ID del usuario a eliminar desde la URL (ej: /eliminar/5/)
#   2. Busca el usuario con ese ID
#   3. Lo elimina de la base de datos
#   4. Regresa a la lista de usuarios
# =====================================================================
def eliminar_usuario(request, id):
    # 'id' viene de la URL: path("eliminar/<int:id>/", ...)
    # Si la URL es /eliminar/5/, entonces id = 5
    
    # Verificar que esté logueado
    if 'usuario_id' not in request.session:
        return redirect("login")
    
    # get_object_or_404: busca el usuario con ese ID
    # Si no lo encuentra, muestra una página de error 404
    usuario = get_object_or_404(Practica, id=id)
    
    # .delete() elimina el registro de la base de datos
    usuario.delete()
    
    # Volver a la lista de usuarios
    return redirect("usuarios")


# =====================================================================
# CERRAR SESIÓN / LOGOUT (NUEVA)
# =====================================================================
# PROPÓSITO: Cierra la sesión del usuario (lo desloguea)
# CÓMO FUNCIONA:
#   1. Borra todos los datos de la sesión
#   2. El usuario ya no está logueado
#   3. Lo envía al login
# =====================================================================
def logout(request):
    # .flush() elimina TODOS los datos de la sesión
    # Es como "olvidar" quién estaba logueado
    request.session.flush()
    
    # Enviar al usuario al login
    return redirect("welcome")


# =====================================================================
# FORMULARIO DE REGISTRO (MODIFICADA)
# =====================================================================
# PROPÓSITO: Registrar un nuevo usuario
# MODIFICACIÓN: Se agregó el campo imagen_url para guardar URL de imagen
# CÓMO FUNCIONA:
#   1. Usuario llena el formulario con username, password y opcionalmente imagen
#   2. Se verifica que el usuario no exista
#   3. Se verifica que las contraseñas coincidan
#   4. Se crea el nuevo usuario en la base de datos
# =====================================================================
def formulario(request):
    if request.method == "POST":
        # Obtener todos los datos del formulario
        usern = request.POST.get("username")
        passw1 = request.POST.get("password1")
        passw2 = request.POST.get("password2")
        imagen = request.POST.get("imagen_url")  # NUEVO: obtener la URL de imagen

        # .filter() busca usuarios que coincidan con el criterio
        # .exists() devuelve True si encontró al menos uno
        if Practica.objects.filter(username=usern).exists():
            sms = "El nombre de usuario ya existe"
            sms2 = "Segundo mensaje"
            
            info = {
                  'infosms':sms,
                  'infosms2':sms2
            }
            return render(request, "formulario.html", info)
        
        # Verificar que las contraseñas sean iguales
        if passw1 == passw2:
            # .create() crea un nuevo registro en la base de datos
            Practica.objects.create(
                username=usern,
                password=passw2,
                # NUEVO: guardar la URL de imagen (si no escribió nada, guarda None)
                imagen_url=imagen if imagen else None
            )
            return redirect("login")  # Ir al login
            
    return render(request, "formulario.html")


# =====================================================================
# ACTUALIZAR USUARIO (NUEVA)
# =====================================================================
# PROPÓSITO: Modificar los datos de un usuario existente
# CÓMO FUNCIONA:
#   1. Recibe el ID del usuario desde la URL (ej: /actualizar/5/)
#   2. Busca el usuario y muestra sus datos actuales en el formulario
#   3. El usuario modifica los datos que quiera
#   4. Se guardan los cambios en la base de datos
# =====================================================================
def actualizar_usuario(request, id):
    # Verificar que esté logueado
    if 'usuario_id' not in request.session:
        return redirect("login")
    
    # Buscar el usuario por ID
    usuario = get_object_or_404(Practica, id=id)
    
    if request.method == "POST":  # Si envió el formulario con los nuevos datos
        # Obtener los nuevos valores del formulario
        usern = request.POST.get("username")
        passw = request.POST.get("password")
        imagen = request.POST.get("imagen_url")
        
        # Cambiar los valores del usuario
        usuario.username = usern
        usuario.password = passw
        usuario.imagen_url = imagen if imagen else None
        
        # .save() guarda los cambios en la base de datos
        usuario.save()
        
        return redirect("usuarios")  # Volver a la lista
    
    # Si es GET, mostrar el formulario con los datos actuales
    # Enviamos el usuario al template para que muestre sus datos
    return render(request, "actualizar.html", {"usuario": usuario})

# =====================================================================
# VISTA DE BIENVENIDA / LANDING PAGE (NUEVA)
# =====================================================================
# PROPÓSITO: Página principal para usuarios no logueados
def welcome(request):
    return render(request, "welcome.html")

# =====================================================================
# VISTA DASHBOARD (NUEVA)
# =====================================================================
def dashboard(request):
    # VERIFICAR SESIÓN
    if 'usuario_id' not in request.session:
        return redirect("login")
        
    # En un caso real, aquí calcularíamos los ingresos, pedidos, etc.
    return render(request, "dashboard.html")

# =====================================================================
# GESTIÓN DE MENÚ (CRUD)
# =====================================================================

# 1. LISTAR PRODUCTOS
def menu_list(request):
    if 'usuario_id' not in request.session:
        return redirect("login")
    
    productos = Producto.objects.all()
    return render(request, "menu.html", {"productos": productos})

# 2. CREAR PRODUCTO
def crear_producto(request):
    if 'usuario_id' not in request.session:
        return redirect("login")
    
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        
        # Limpiar precio de puntos y comas para guardarlo como entero
        precio_str = request.POST.get("precio").replace('.', '').replace(',', '')
        try:
            precio = int(precio_str)
        except ValueError:
            precio = 0
            
        # Validar tope máximo
        if precio > 1000000:
            precio = 1000000
            
        imagen = request.POST.get("imagen_url")
        stock = request.POST.get("stock") == "on" # Checkbox sends "on" if checked
        
        Producto.objects.create(
            nombre=nombre,
            precio=precio,
            imagen_url=imagen if imagen else "https://via.placeholder.com/150",
            stock=stock
        )
        return redirect("menu_list")
        
    return render(request, "producto_form.html", {"titulo": "Nuevo Producto"})

# 3. EDITAR PRODUCTO
def editar_producto(request, id):
    if 'usuario_id' not in request.session:
        return redirect("login")
        
    producto = get_object_or_404(Producto, id=id)
    
    if request.method == "POST":
        producto.nombre = request.POST.get("nombre")
        
        # Limpiar precio
        precio_str = request.POST.get("precio").replace('.', '').replace(',', '')
        try:
            producto.precio = int(precio_str)
        except ValueError:
            producto.precio = 0
            
        # Validar tope máximo
        if producto.precio > 1000000:
            producto.precio = 1000000
            
        producto.imagen_url = request.POST.get("imagen_url")
        producto.stock = request.POST.get("stock") == "on"
        
        producto.save()
        return redirect("menu_list")
        
    return render(request, "producto_form.html", {"titulo": "Editar Producto", "producto": producto})

# 4. ELIMINAR PRODUCTO
def eliminar_producto(request, id):
    if 'usuario_id' not in request.session:
        return redirect("login")
        
    producto = get_object_or_404(Producto, id=id)
    producto.delete()
    return redirect("menu_list")


# =====================================================================
# GESTIÓN DE INVENTARIO (CRUD)
# =====================================================================

# 1. LISTAR INSUMOS
def inventario_list(request):
    if 'usuario_id' not in request.session:
        return redirect("login")
    
    # Optional Search
    query = request.GET.get("q")
    if query:
        insumos = Insumo.objects.filter(nombre__icontains=query)
    else:
        insumos = Insumo.objects.all()
        
    return render(request, "inventario.html", {"insumos": insumos})

from django.core.exceptions import ValidationError

# 2. CREAR INSUMO
def crear_insumo(request):
    if 'usuario_id' not in request.session:
        return redirect("login")
    
    if request.method == "POST":
        try:
            Insumo.objects.create(
                nombre=request.POST.get("nombre"),
                cantidad=request.POST.get("cantidad"),
                ultima_info=request.POST.get("ultima_info"),
                fecha=request.POST.get("fecha") if request.POST.get("fecha") else None
            )
            return redirect("inventario_list")
        except ValidationError as e:
            return render(request, "insumo_form.html", {
                "titulo": "Nuevo Insumo",
                "error": f"Error de validación: {e}",
                "insumo": request.POST  # Keep user input
            })
        except Exception as e:
             return render(request, "insumo_form.html", {
                "titulo": "Nuevo Insumo",
                "error": f"Error: {e}",
                "insumo": request.POST
            })
        
    return render(request, "insumo_form.html", {"titulo": "Nuevo Insumo"})

# 3. EDITAR INSUMO
def editar_insumo(request, id):
    if 'usuario_id' not in request.session:
        return redirect("login")
        
    insumo = get_object_or_404(Insumo, id=id)
    
    if request.method == "POST":
        try:
            insumo.nombre = request.POST.get("nombre")
            insumo.cantidad = request.POST.get("cantidad")
            insumo.ultima_info = request.POST.get("ultima_info")
            fecha = request.POST.get("fecha")
            insumo.fecha = fecha if fecha else None
            
            insumo.full_clean() # Force validation before save
            insumo.save()
            return redirect("inventario_list")
        except ValidationError as e:
            return render(request, "insumo_form.html", {
                "titulo": "Editar Insumo",
                "error": f"Error de validación: {e}",
                "insumo": request.POST 
            })
        except Exception as e:
            return render(request, "insumo_form.html", {
                "titulo": "Editar Insumo",
                "error": f"Error: {e}",
                "insumo": request.POST
            })
        
    return render(request, "insumo_form.html", {"titulo": "Editar Insumo", "insumo": insumo})

# 4. ELIMINAR INSUMO
def eliminar_insumo(request, id):
    if 'usuario_id' not in request.session:
        return redirect("login")
        
    insumo = get_object_or_404(Insumo, id=id)
    insumo.delete()
    return redirect("inventario_list")


# =====================================================================
# GESTIÓN DE EMPLEADOS (CRUD)
# =====================================================================

# 1. LISTAR EMPLEADOS
def empleados_list(request):
    if 'usuario_id' not in request.session:
        return redirect("login")
    
    query = request.GET.get("q")
    if query:
        empleados = Empleado.objects.filter(nombre__icontains=query)
    else:
        empleados = Empleado.objects.all()
        
    return render(request, "empleados.html", {"empleados": empleados})

# 2. CREAR EMPLEADO
def crear_empleado(request):
    if 'usuario_id' not in request.session:
        return redirect("login")
    
    if request.method == "POST":
        Empleado.objects.create(
            nombre=request.POST.get("nombre"),
            foto_url=request.POST.get("foto_url"),
            rol=request.POST.get("rol"),
            edad=request.POST.get("edad"),
            telefono=request.POST.get("telefono"),
            estado=True # Default to active
        )
        return redirect("empleados_list")
        
    return render(request, "empleado_form.html", {"titulo": "Nuevo Empleado"})

# 3. EDITAR EMPLEADO
def editar_empleado(request, id):
    if 'usuario_id' not in request.session:
        return redirect("login")
        
    empleado = get_object_or_404(Empleado, id=id)
    
    if request.method == "POST":
        empleado.nombre = request.POST.get("nombre")
        empleado.foto_url = request.POST.get("foto_url")
        empleado.rol = request.POST.get("rol")
        empleado.edad = request.POST.get("edad")
        empleado.telefono = request.POST.get("telefono")
        empleado.estado = request.POST.get("estado") == "on"
        
        empleado.save()
        return redirect("empleados_list")
        
    return render(request, "empleado_form.html", {"titulo": "Editar Empleado", "empleado": empleado})

# 4. ELIMINAR EMPLEADO
def eliminar_empleado(request, id):
    if 'usuario_id' not in request.session:
        return redirect("login")
        
    empleado = get_object_or_404(Empleado, id=id)
    empleado.delete()
    return redirect("empleados_list")