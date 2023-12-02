from django.urls import path

from . import views
from . import views_webpay  


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
    path('webpay', views_webpay.pagar),
    path('webpay_send', views_webpay.pagar_send),
    path('boleta', views_webpay.pagar_boleta),
    path('eliminar_del_carrito/<int:carrito_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('generar_pdf/', views_webpay.generar_pdf, name='generar_pdf'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('libros-mas-vendidos/', views.libros_mas_vendidos, name='libros_mas_vendidos'),

]