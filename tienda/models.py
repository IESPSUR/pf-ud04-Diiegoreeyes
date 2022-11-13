from django.conf import settings
from django.db import models
from django.utils import timezone
# Create your models here.
class marca(models.Model):
    nombre = models.CharField(max_length=200, primary_key='true')

class producto(models.Model):
    nombre = models.CharField(max_length=200)
    modelo = models.CharField(max_length=200)
    unidades = models.IntegerField()
    precio = models.IntegerField()
    detalles = models.CharField(max_length=200)
    marca = models.ForeignKey(marca, on_delete=models.CASCADE)

    def __str__(self):
        return '{} {}'.format(self.nombre, self.marca)


class compra(models.Model):
    unidades = models.CharField(max_length=200)
    importe = models.CharField(max_length=200)
    fecha = models.CharField(max_length=200)
