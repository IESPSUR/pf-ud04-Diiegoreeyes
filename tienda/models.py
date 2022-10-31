from django.conf import settings
from django.db import models
from django.utils import timezone
# Create your models here.

class producto(models.Model):
    nombre = models.CharField(max_length=200)
    modelo = models.CharField(max_length=200)
    unidades = models.CharField(max_length=200)
    precio = models.CharField(max_length=200)
    detalles = models.TextField()


class marca(models.Model):
    marca = models.TextField()

class compra(models.Model):
    unidades = models.IntegerField
    importe = models.IntegerField
    fecha = models.DateTimeField(default=timezone.now)
