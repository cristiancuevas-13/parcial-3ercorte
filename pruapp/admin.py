from django.contrib import admin

# Register your models here.
from .models import Practica

@admin.register(Practica)
class PracticaAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "password")  # columnas que quieres ver
    search_fields = ("username",)                  # barra de búsqueda
    list_filter = ("username",)
    list_display_links = ("username",)  # Debe ser tupla (con coma) y el campo debe estar en list_display