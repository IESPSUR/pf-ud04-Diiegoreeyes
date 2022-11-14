from django.conf import settings
from django.db import models
from django.utils import timezone
# Create your models here.
class marca(models.Model):
    nombre = models.CharField(max_length=200, unique='True')

    def __str__(self):
        return self.nombre
class producto(models.Model):
    nombre = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    unidades = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=12, decimal_places=2)
    detalles = models.CharField(max_length=200, blank=True)
    marca = models.ForeignKey(marca, models.PROTECT)

    def __str__(self):
        return '{} {}'.format(self.nombre, self.marca)


class compra(models.Model):
    producto = models.ForeignKey(producto, models.PROTECT)
    unidades = models.PositiveIntegerField()
    importe = models.DecimalField(max_digits=12, decimal_places=2)
    fecha = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    def __str__(self):
        return '{} {}'.format(self.producto, self.unidades)
