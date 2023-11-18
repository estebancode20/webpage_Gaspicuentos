import uuid
from django.db import models

class Categoria(models.Model):
    categoria_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=255) 

    def __str__(self):
        return self.nombre

    

class Libro(models.Model):
    ISBN = models.CharField(max_length=20, primary_key=True)
    titulo = models.CharField(max_length=255)
    autor = models.CharField(max_length=255, null=True, blank=True)
    editorial = models.CharField(max_length=255, null=True, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=True, blank=True)
    imagen = models.ImageField(upload_to='imagenes/', verbose_name ="Imagen",null=True)
    cantidad_disponible = models.IntegerField(null=True, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        fila = f"{self.titulo} - Cantidad disponible: {self.cantidad_disponible}"
        return fila
    

opciones_consultas = [
    [0,"consulta"],
    [1,"reclamo"],
    [2,"sugerencia"],
    [3,"felicitaciones"]

]

class Contacto(models.Model):
    nombre = models.CharField(max_length=50)
    correo = models.EmailField()
    tipo_consulta = models.IntegerField(choices=opciones_consultas)
    mensaje = models.TextField()

    def __str__(self):
        fila = f"{self.nombre} + {self.mensaje}"
        return fila 

class Carrito(models.Model):
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    precio_total = models.DecimalField(max_digits=10, decimal_places=2)

    

     
    
