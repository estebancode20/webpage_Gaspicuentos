from django.urls import path

from . import views


urlpatterns =[
    path("home/", views.home, name = "home" ),
    path("", views.index ,name="index"),
    path("iniciar_sesion/",views.iniciar_sesion,name="iniciar_sesion"),
    path("crear_cuenta/", views.crear_cuenta,name = "crear_cuenta"),
    path("detalle_libro/<str:isbn>/", views.detalle_libro, name='detalle_libro'),
    path("contacto/",views.contacto,name="contacto"),
    path("registro/",views.registro,name="registro"),
    path('agregar_al_carrito/<str:isbn>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('ver_carrito/', views.ver_carrito, name='ver_carrito'),

]