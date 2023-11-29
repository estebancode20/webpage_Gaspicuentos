from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from .models import Libro, Carrito
from .forms import ContactoForm, CustomUserCreationForm 
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.db.models import Q



def index(request):
    return HttpResponse("estas en el index de ventas")

def home(request):
    categoria_filtrada = request.GET.get('categoria')
    query = request.GET.get('q')

    if categoria_filtrada:
        libros_list = Libro.objects.filter(categoria__nombre=categoria_filtrada)
    else:
        libros_list = Libro.objects.all()

    if query:
        libros_list = libros_list.filter(
            Q(titulo__icontains=query) |
            Q(autor__icontains=query) |
            Q(ISBN__icontains=query)
        )

    # Paginación
    paginator = Paginator(libros_list, 12)  # Muestra 12 libros por página
    page = request.GET.get('page')

    try:
        libros = paginator.page(page)
    except PageNotAnInteger:
        libros = paginator.page(1)
    except EmptyPage:
        libros = paginator.page(paginator.num_pages)

    return render(request, 'home.html', {'libros': libros, 'categoria_filtrada': categoria_filtrada, 'query': query})

def iniciar_sesion(request):
    return render(request,'iniciar_sesion.html')

def crear_cuenta(request):
    return render(request, 'crear_cuenta.html')

"""
def detalle_libro(request):
    libros = Libro.objects.all()
    print(libros)
    return render(request, 'detalle_libro.html')
"""
"""
def detalle_libro(request, libro_id):
    libro = get_object_or_404(Libro, pk=libro_id)
    return render(request, 'detalle_libro.html', {'libro': libro})
"""

def contacto(request):
    data = {
        'form': ContactoForm() 
    }

    if request.method == 'POST':
        formulario = ContactoForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            data["mensaje"]="MENSAJE ENVIADO"
        else:
            data["form"]=formulario

    return render(request,'contacto.html',data)


def registro(request):
    data = {
        'form':CustomUserCreationForm()
    }

    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            user = authenticate(username=formulario.cleaned_data["username"],password=formulario.cleaned_data["password1"])
            login(request,user)
            messages.success(request,"Te has registrado correctamente") 
            return redirect(to="home")
        data["form"]= formulario

    return render(request,'registration/registro.html',data)


def detalle_libro(request, isbn):
    # Obtén el objeto del libro según el ISBN
    libro = get_object_or_404(Libro, ISBN=isbn)

    # Pasa el objeto del libro a la plantilla
    return render(request, 'detalle_libro.html', {'libro': libro})


def agregar_al_carrito(request, isbn):
    libro = get_object_or_404(Libro, ISBN=isbn)
    carrito, created = Carrito.objects.get_or_create(libro=libro, precio_total=libro.precio_venta)

    if not created:
        carrito.cantidad += 1
        carrito.precio_total += libro.precio_venta
        carrito.save()

    return redirect('detalle_libro', isbn=isbn)


def ver_carrito(request):
    carrito = Carrito.objects.all()
    total = sum(item.precio_total for item in carrito)
    return render(request, 'carrito.html', {'carrito': carrito, 'total': total})