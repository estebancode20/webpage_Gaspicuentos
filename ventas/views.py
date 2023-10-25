from django.shortcuts import render
from django.http import HttpResponse



def index(request):
    return HttpResponse("estas en el index de ventas")

def home(request):
    return render(request, 'home.html')

def iniciar_sesion(request):
    return render(request,'iniciar_sesion.html')

def crear_cuenta(request):
    return render(request, 'crear_cuenta.html')
