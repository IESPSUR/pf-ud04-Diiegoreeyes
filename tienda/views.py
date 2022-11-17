from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from datetime import datetime
from django.shortcuts import render,redirect,get_object_or_404
from django.db.models import Sum,Count

from . import forms
from .models import *
from .forms import ProductoForm, CompraForm, MarcaForm,PersonaForm


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


def listado_marca(request):

    marca = request.GET.get('marca')

    if marca:

        formulario = MarcaForm(request.GET)
        Productos = producto.objects.all().filter(marca=marca)
        contexto = {'Productos':Productos, 'formulario':formulario}

    else:
        formulario = MarcaForm()
        contexto = {'formulario': formulario}
    return render(request, 'tienda/listado_marca.html', contexto)

def listado_usuario(request):

    username = request.GET.get('user')

    if username:

        formulario = PersonaForm(request.GET)
        compras = compra.objects.all().filter(user=request.user)
        contexto = {'compras':compras, 'formulario':formulario}

    else:

        formulario = PersonaForm()
        contexto = {'formulario': formulario}

    return render(request, 'tienda/listado_usuario.html', contexto)

def informes(request):
    return render(request,'tienda/informes.html', {})

def toptenproductos(request):

    Productos = producto.objects.annotate(sum_ventas=Sum('compra__unidades'),
                                          sum_importes=Sum('compra__importe')).order_by('-sum_ventas')[:10]
    return render(request, 'tienda/toptenproductos.html', {'Productos':Productos})


def toptenclientes(request):
    Clientes = User.objects.annotate(importe_compras=Sum('compra__importe'),
                                     total_compras=Count('compra')).order_by('-importe_compras')[:3]
    print(Clientes.query)
    return render(request, 'tienda/toptenclientes.html', {'Clientes': Clientes})