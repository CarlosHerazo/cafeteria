from django.db import models
from decimal import Decimal
from django.utils import timezone
import secrets
from datetime import timedelta
# Create your models here.



# Modelo Cafeteria
class Cafeteria(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.TextField()

    def __str__(self) -> str:
        return self.nombre

# Modelo Categorias
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.nombre

# Modelo Productos
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField()
    cantidad = models.IntegerField(null=True)
    imagen = models.ImageField(upload_to='productos_img')
    cafeteria = models.ForeignKey(Cafeteria, on_delete=models.CASCADE)

# Modelo Ventas
class Venta(models.Model):
    cafeteria = models.ForeignKey(Cafeteria, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    nombre_cliente = models.CharField(max_length=90, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    desc = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    
    
class Descuento(models.Model):
    tipo_descuento = models.CharField(max_length=90)
    desc = models.DecimalField(max_digits=10, decimal_places=2)

# Modelo DetalleVenta (para almacenar los productos vendidos en cada venta)
class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()

# Modelo Empleado
class Empleado(models.Model):
    cedula = models.CharField(max_length=100, primary_key=True)
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=10)
    rol = models.CharField(max_length=90)
    cafeteria = models.ForeignKey(Cafeteria, on_delete=models.CASCADE)

# Modelo Usuario
class Usuario(models.Model):
    correo = models.CharField(max_length=90)
    contrasena = models.CharField(max_length=90)
    usuario = models.CharField(max_length=90)
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    password_reset_token = models.CharField(max_length=100, blank=True, null=True)
    password_reset_expiry = models.DateTimeField(blank=True, null=True)

    def generate_password_reset_token(self):
        token = secrets.token_urlsafe(20)  # Genera un token seguro
        self.password_reset_token = token
        self.password_reset_expiry = timezone.now() + timedelta(hours=1)  # Expira en 1 hora
        self.save()
        return token
