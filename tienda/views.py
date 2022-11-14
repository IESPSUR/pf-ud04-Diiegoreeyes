from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render,redirect
from .models import *
from .forms import ProductoForm
# Create your views here.
def welcome(request):
    return render(request,'tienda/index.html', {})

def listado(request):
    listadoprod = producto.objects.all()
    return render(request,'tienda/listado.html', {'listadoprod':listadoprod})

def compra(request):
    listadoprod = producto.objects.all()
    return render(request,'tienda/compra.html', {'listadoprod':listadoprod})

def FormCompra(request, id):
    Producto = producto.objects.get(id=id)
    formulario = ProductoForm(request.POST or None, request.FILES or None, instance=Producto)
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('compra')
    return render(request,'tienda/FormCompra.html', {'formulario':formulario})


@staff_member_required
def crear(request):
    formulario = ProductoForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('listado')
    return render(request,'tienda/crear.html', {'formulario':formulario})

@staff_member_required
def editar(request, id):
    Producto = producto.objects.get(id=id)
    formulario = ProductoForm(request.POST or None, request.FILES or None, instance=Producto)
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('listado')
    return render(request,'tienda/editar.html', {'formulario':formulario})

@staff_member_required
def eliminar(request, id):
    Producto = producto.objects.get(id=id)
    Producto.delete()
    return redirect('listado')
