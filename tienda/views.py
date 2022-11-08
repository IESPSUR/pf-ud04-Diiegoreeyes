from django.shortcuts import render
from .models import *
# Create your views here.
def welcome(request):
    return render(request,'tienda/index.html', {})

def informe(request):
    listado = producto.objects.all()
    return render(request,'tienda/informe.html/', {'listado': listado} )