from django.urls import path

from . import views


urlpatterns =[
    path("home/", views.home, name = "home" ),
    path("", views.index ,name="index"),
    path("iniciar_sesion/",views.iniciar_sesion,name="iniciar_sesion")


]