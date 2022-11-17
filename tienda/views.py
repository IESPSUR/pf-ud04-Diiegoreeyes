from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.db import transaction
from datetime import datetime
from django.shortcuts import render,redirect,get_object_or_404

from . import forms
from .models import *
from .forms import ProductoForm, CompraForm


# Create your views here.
def welcome(request):
    return render(request,'tienda/index.html', {})

def listado(request):
    listadoprod = producto.objects.all()
    return render(request,'tienda/listado.html', {'listadoprod':listadoprod})

def listacompra(request):
    productocompra = producto.objects.all()
    return render(request,'tienda/compra.html', {'productocompra':productocompra})


def validationerror(param):
    pass


@transaction.atomic
@login_required
def formcompra(request, id):

    Producto = get_object_or_404(producto, id=id)

    formulario = CompraForm(request.POST)
    idprod = Producto.id

    formprod = producto.objects.all()

    total=0
    if request.method == 'POST':

        if formulario.is_valid():
            cantidad = formulario.cleaned_data['cantidad']
            total = Producto.precio * int(cantidad)
            if (Producto.unidades > cantidad):
                Producto.unidades = Producto.unidades - cantidad
                Producto.save()

                Compra = compra(producto=Producto,
                                unidades=cantidad,
                                importe=cantidad*Producto.precio,
                                fecha = datetime.now().date(),
                                user=request.user)

                Compra.save()
                return redirect('listacompra')
    return render(request,'tienda/formcompra.html', {'formulario':formulario, 'formprod':formprod, 'idprod':idprod,'total':total})

# CRUD #
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
