from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from .models import Libro, Carrito, Compra, DetalleCompra
from .forms import ContactoForm, CustomUserCreationForm 
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from ventas import models
from django.db.models import Sum
from django.db import connection




def index(request):
    return HttpResponse("estas en el index de ventas")

def home(request):
    categoria_filtrada = request.GET.get('categoria')
    query = request.GET.get('q')

    libros_list = Libro.objects.all()

    if categoria_filtrada:
        libros_list = libros_list.filter(categoria__nombre=categoria_filtrada)

    if query:
        libros_list = libros_list.filter(
            Q(titulo__icontains=query) |
            Q(autor__nombre__icontains=query) |  # Cambiado a buscar en el campo 'nombre' de 'Autor'
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


@login_required
def agregar_al_carrito(request, isbn):
    usuario = request.user
    libro = get_object_or_404(Libro, ISBN=isbn)

    # Busca el carrito existente para el usuario y el libro
    carrito, created = Carrito.objects.get_or_create(usuario=usuario, libro=libro, defaults={'precio_total': libro.precio_venta})

    if not created:
        carrito.cantidad += 1
        carrito.precio_total += libro.precio_venta
        carrito.save()

    # Agrega un mensaje de éxito
    messages.success(request, f'El libro "{libro.titulo}" ha sido agregado al carrito.')

    return redirect('detalle_libro', isbn=isbn)


# views.py

@login_required
def eliminar_del_carrito(request, carrito_id):
    carrito_item = get_object_or_404(Carrito, id=carrito_id)
    carrito_item.delete()
    return redirect('ver_carrito')


# views.py

@login_required
def ver_carrito(request):
    usuario = request.user
    carrito = Carrito.objects.filter(usuario=usuario)
    total = sum(item.precio_total for item in carrito)
    return render(request, 'carrito.html', {'carrito': carrito, 'total': total})





def dashboard(request):
    # Lógica para calcular métricas
    precio_compra_promedio = Libro.objects.aggregate(promedio_compra=Avg('precio_compra'))['promedio_compra']
    precio_venta_promedio = Libro.objects.aggregate(promedio_venta=Avg('precio_venta'))['promedio_venta']

    libros_mas_vendidos = Libro.objects.order_by('-cantidad_disponible')[:5]
    fechas_mas_vendidas = Compra.objects.order_by('-fecha_compra')[:5]

    context = {
        'precio_compra_promedio': precio_compra_promedio,
        'precio_venta_promedio': precio_venta_promedio,
        'libros_mas_vendidos': libros_mas_vendidos,
        'fechas_mas_vendidas': fechas_mas_vendidas,
    }
    return render(request, 'dashboard.html', context)


# views.py
from django.shortcuts import render
from .models import Libro
from django.db import connection

def libros_mas_vendidos(request):
    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT 
                ventas_libro.ISBN, 
                ventas_libro.titulo, 
                SUM(ventas_detallecompra.cantidad) as total_vendido,
                (SELECT SUM(ventas_detallecompra.cantidad * (ventas_libro.precio_venta - ventas_libro.precio_compra))
                 FROM ventas_detallecompra
                 WHERE ventas_detallecompra.libro_id = ventas_libro.ISBN
                 GROUP BY ventas_detallecompra.libro_id
                 ORDER BY SUM(ventas_detallecompra.cantidad) DESC
                 LIMIT 1) as utilidad_acumulada
            FROM ventas_detallecompra
            JOIN ventas_libro ON ventas_detallecompra.libro_id = ventas_libro.ISBN
            GROUP BY ventas_libro.ISBN, ventas_libro.titulo
            ORDER BY total_vendido DESC
            LIMIT 5;
        ''')
        libros_vendidos = cursor.fetchall()

    return render(request, 'libros_mas_vendidos.html', {'libros_vendidos': libros_vendidos})







