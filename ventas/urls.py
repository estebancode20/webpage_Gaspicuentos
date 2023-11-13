from django.urls import path

from . import views


urlpatterns =[
    path("home/", views.home, name = "home" ),
    path("", views.index ,name="index"),
    path("iniciar_sesion/",views.iniciar_sesion,name="iniciar_sesion"),
    path("crear_cuenta/", views.crear_cuenta,name = "crear_cuenta"),
    path("detalle_libro/",views.detalle_libro,name="detalle_libro"),
    path("contacto/",views.contacto,name="contacto")
]