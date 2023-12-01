import uuid
from django.db import models
from django.contrib.auth.models import User


class Categoria(models.Model):
    categoria_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=255) 

    def __str__(self):
        return self.nombre
    


class Autor(models.Model):
    autor_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre


class Editorial(models.Model):
    editorial_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre


class Libro(models.Model):
    ISBN = models.CharField(max_length=20, primary_key=True)
    titulo = models.CharField(max_length=255)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE, null=True, blank=True)
    editorial = models.ForeignKey(Editorial, on_delete=models.CASCADE, null=True, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=True, blank=True)
    imagen = models.ImageField(upload_to='imagenes/', verbose_name ="Imagen",null=True)
    cantidad_disponible = models.IntegerField(null=True, blank=True)
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)

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

# models.py

class Carrito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Cambia 1 por el ID de un usuario existente
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    precio_total = models.DecimalField(max_digits=10, decimal_places=2)
    
# models.py

class Compra(models.Model):
    compra_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_compra = models.DateTimeField(auto_now_add=True)

class DetalleCompra(models.Model):
    detalle_compra_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE)
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    precio_total = models.DecimalField(max_digits=10, decimal_places=2)

     
    
