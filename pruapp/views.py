from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def saludo(request):
    return HttpResponse("Hola mundo")

def despedida(request):
    return HttpResponse("Hasta luego")

def anime(request):
    return render(request, "./1/anime.html")
def mundo(request):
    return render(request, "./plantilla.html")

