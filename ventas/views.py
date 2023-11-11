from django.shortcuts import render
from django.http import HttpResponse
from .models import Libro



def index(request):
    return HttpResponse("estas en el index de ventas")

def home(request):
    return render(request, 'home.html')

def iniciar_sesion(request):
    return render(request,'iniciar_sesion.html')

def crear_cuenta(request):
    return render(request, 'crear_cuenta.html')


def detalle_libro(request):
    libros = Libro.objects.all()
    print(libros)
    return render(request, 'detalle_libro.html')

"""
def detalle_libro(request, libro_id):
    libro = get_object_or_404(Libro, pk=libro_id)
    return render(request, 'detalle_libro.html', {'libro': libro})
"""
