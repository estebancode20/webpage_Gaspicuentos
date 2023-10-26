from django.db import models

# Create your models here.

class Libro(models.Model):
    ISBN = models.CharField(max_length=20, primary_key=True)
    titulo = models.CharField(max_length=255)
    autor = models.CharField(max_length=255, null=True, blank=True)
    editorial = models.CharField(max_length=255, null=True, blank=True)
    categoria_codigo = models.CharField(max_length=36, null=True, blank=True)
    imagen = models.CharField(max_length=255, null=True, blank=True)
    cantidad_disponible = models.IntegerField(null=True, blank=True)