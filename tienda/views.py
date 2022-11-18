from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import transaction
from datetime import datetime
from django.shortcuts import render,redirect,get_object_or_404
from django.db.models import Sum,Count

from . import forms
from .models import *
from .forms import ProductoForm, CompraForm, MarcaForm,PersonaForm


# Create your views here.

# Vista del index #
def welcome(request):
    return render(request,'tienda/index.html', {})

# Vista Muestra todos los productos para CRUD #
def listado(request):
    listadoprod = producto.objects.all()
    return render(request, 'tienda/listado.html', {'listadoprod':listadoprod})


# Vista Muestra todos los productos para COMPRA #
def listacompra(request):
    productocompra = producto.objects.all()
    return render(request, 'tienda/COMPRA/compra.html', {'productocompra':productocompra})

# Vista CREA USUARIO #
def crearusuario(request):
    if request.method == 'POST':
        # Usa Un Form propio de django de usuario
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect(welcome)
    form = UserCreationForm()
    return render(request,'tienda/COMPRA/crearusuario.html', {'form':form})

# Vista INICIAR SESION #
def iniciar_sesion(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request,user)
                return redirect(welcome)
            else:
                messages.error(request,'Error en el inicio de sesión')
        else:
            messages.error(request,'Fallo en el inicio de sesión')
    form = AuthenticationForm()
    return render(request, 'tienda/COMPRA/iniciar_sesion.html', {'form':form})

# Vista COMPRA PRODUCTO #
@transaction.atomic
@login_required
def formcompra(request, id):

    #Creamos variables necesarias

    Producto = get_object_or_404(producto, id=id)
    formulario = CompraForm(request.POST)
    idprod = Producto.id
    formprod = producto.objects.all()

    total=0

    if request.method == 'POST':

        #Si el formulario es válido
        if formulario.is_valid():
            cantidad = formulario.cleaned_data['cantidad']
            total = Producto.precio * int(cantidad)

            #Si la cantidad de unidades es inferior a Stock
            if (Producto.unidades > cantidad):
                Producto.unidades = Producto.unidades - cantidad
                Producto.save()

                #Guardamos en compra
                Compra = compra(producto=Producto,
                                unidades=cantidad,
                                importe=cantidad*Producto.precio,
                                fecha = datetime.now().date(),
                                user=request.user)

                Compra.save()
            else:
                raise ValidationError('No hay suficientes unidades')
            return redirect('listacompra')
    return render(request, 'tienda/COMPRA/formcompra.html', {'formulario':formulario, 'formprod':formprod, 'idprod':idprod, 'total':total})


# CRUD #
@staff_member_required
def crear(request):
    formulario = ProductoForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('listado')
    return render(request, 'tienda/CRUD/crear.html', {'formulario':formulario})

@staff_member_required
def editar(request, id):
    Producto = producto.objects.get(id=id)
    formulario = ProductoForm(request.POST or None, request.FILES or None, instance=Producto)
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('listado')
    return render(request, 'tienda/CRUD/editar.html', {'formulario':formulario})

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
    return render(request, 'tienda/informes/listado_marca.html', contexto)

def listado_usuario(request):

    username = request.GET.get('user')

    if username:

        formulario = PersonaForm(request.GET)
        compras = compra.objects.all().filter(user=username)
        contexto = {'compras':compras, 'formulario':formulario}

    else:

        formulario = PersonaForm()
        contexto = {'formulario': formulario}

    return render(request, 'tienda/informes/listado_usuario.html', contexto)


def informes(request):
    return render(request, 'tienda/informes/informes.html', {})

def toptenproductos(request):
    unidadesvendidas = compra.objects.values('producto').annotate(total=Sum('importe'),sum_compras=Sum('unidades'),).order_by('-sum_compras')[:10]

    Productos = producto.objects.all()


    return render(request, 'tienda/informes/toptenproductos.html', {'Productos':Productos, 'unidadesvendidas':unidadesvendidas})


def toptenclientes(request):
    comprastotal = compra.objects.values('user').annotate(sum_compras=Sum('importe'))
    Clientes = User.objects.annotate(importe_compras=Sum('compra__importe'),
                                     total_compras=Count('compra')).order_by('-importe_compras')[:3]

    print(Clientes.query)
    return render(request, 'tienda/informes/toptenclientes.html', {'Clientes': Clientes,'comprastotal':comprastotal})
