from django.conf import settings
from django.db import models
from django.utils import timezone
# Create your models here.

class producto(models.Model):
    nombre = models.CharField(max_length=200)
    modelo = models.CharField(max_length=200)
    unidades = models.IntegerField()
    precio = models.IntegerField()
    detalles = models.CharField(max_length=200)

class marca(models.Model):
    nombre = models.CharField(max_length=200)

class compra(models.Model):
    unidades = models.CharField(max_length=200)
    importe = models.CharField(max_length=200)
    fecha = models.CharField(max_length=200)
