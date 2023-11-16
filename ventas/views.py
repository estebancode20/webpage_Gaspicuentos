from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.http import HttpResponse
from .models import Libro
from .forms import ContactoForm 



def index(request):
    return HttpResponse("estas en el index de ventas")

def home(request):
    categoria_filtrada = request.GET.get('categoria')
    
    if categoria_filtrada:
        libros_list = Libro.objects.filter(categoria__nombre=categoria_filtrada)
    else:
        libros_list = Libro.objects.all()

    # Paginación
    paginator = Paginator(libros_list, 12)  # Muestra 12 libros por página
    page = request.GET.get('page')

    try:
        libros = paginator.page(page)
    except PageNotAnInteger:
        libros = paginator.page(1)
    except EmptyPage:
        libros = paginator.page(paginator.num_pages)

    return render(request, 'home.html', {'libros': libros, 'categoria_filtrada': categoria_filtrada})

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
    print('esta llamando a la vista registro')
    return render(request,'registration/registro.html')