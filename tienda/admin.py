from django.contrib import admin
from .models import producto,marca,compra

# Register your models here.

admin.site.register(producto)
admin.site.register(marca)
admin.site.register(compra)
