# =====================================================================
# MODELS.PY - Define la estructura de la base de datos
# =====================================================================
# Un "modelo" es como una tabla en la base de datos
# Cada campo del modelo es una columna de la tabla
# =====================================================================

from django.db import models

# La clase Practica representa una tabla en la base de datos
# Cada usuario que se registra es una fila en esta tabla
class Practica(models.Model):
    # CharField = Campo de texto
    # max_length = Máximo de caracteres permitidos
    # unique=True = No puede haber dos usuarios con el mismo nombre
    username = models.CharField(max_length=150, unique=True)
    
    # Campo para guardar la contraseña
    password = models.CharField(max_length=128)
    
    # =====================================================================
    # NUEVO CAMPO: imagen_url
    # =====================================================================
    # URLField = Campo para guardar URLs (valida que sea una URL válida)
    # blank=True, null=True = El campo es OPCIONAL
    imagen_url = models.URLField(max_length=500, blank=True, null=True)

    # __str__ define qué se muestra cuando imprimes un objeto Practica
    def __str__(self):
        return self.username

# =====================================================================
# MODELO PRODUCTO (MENU)
# =====================================================================
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    imagen_url = models.URLField(max_length=500, blank=True, null=True)
    precio = models.IntegerField()  # Usamos Entero para precios como $20.000
    stock = models.BooleanField(default=True)  # True = En stock, False = Agotado

    def __str__(self):
        return self.nombre

# =====================================================================
# MODELO INSUMO (INVENTARIO)
# =====================================================================
class Insumo(models.Model):
    nombre = models.CharField(max_length=100) # Ingredientes
    cantidad = models.CharField(max_length=50) # "15 KG", "5 Unidades"
    ultima_info = models.CharField(max_length=100, blank=True, null=True) # "20 KG Hoy"
    fecha = models.DateField(blank=True, null=True) # "27/08/25" (Unidad col in image)

    def __str__(self):
        return self.nombre

# =====================================================================
# MODELO EMPLEADO (RRHH)
# =====================================================================
class Empleado(models.Model):
    nombre = models.CharField(max_length=100)
    foto_url = models.URLField(max_length=500, blank=True, null=True)
    rol = models.CharField(max_length=50) # Cajero, Mesero, Chef
    edad = models.IntegerField()
    telefono = models.CharField(max_length=20)
    estado = models.BooleanField(default=True) # True = Activo

    def __str__(self):
        return self.nombre
