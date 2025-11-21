from django.urls import path
from . import views
urlpatterns = [
    path ("home/", views.saludo,name="home1"),
    path ("anime/", views.anime,name="principal"),
    path ("bye/", views.despedida,name="bye1",),
    path("plantilla/",views.mundo,name="plantilla"),
]