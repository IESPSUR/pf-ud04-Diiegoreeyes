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
from django.db.models import Sum

from . import forms
from .models import *
from .forms import ProductoForm, CompraForm, MarcaForm,PersonaForm


# Create your views here.

# Vista del index #
def welcome(request):
    return render(request,'tienda/index.html', {})

# Vista Muestra todos los productos para CRUD #
@staff_member_required
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
        # Usamos Un Form propio de django para crear usuario
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
        # Usamos Un Form propio de django para iniciar sesión
        form = AuthenticationForm(request, data=request.POST)
        # Si es válido, recogemos los datos y se lo pasamos a user
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            #Si existe, nos manda al welcome, sino manda un mensaje
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



# INFORMES #
@staff_member_required
def informes(request):
    return render(request, 'tienda/informes/informes.html', {})


# Productos por marca #
def listado_marca(request):
    # Recogemos la marca por el formulario #
    marca = request.GET.get('marca')
    # Si existe el check box del formulario #
    if marca:
        # Recoge Marca del modelo  y filtramos por el valor del input#
        formulario = MarcaForm(request.GET)
        Productos = producto.objects.all().filter(marca=marca)
        # Variable que usaremos #
        contexto = {'Productos':Productos, 'formulario':formulario}
        # Si no existe el check box del formulario no le pasamos el producto #
    else:
        formulario = MarcaForm()
        contexto = {'formulario': formulario}
    return render(request, 'tienda/informes/listado_marca.html', contexto)

# Listado de usuarios #
def listado_usuario(request):

    # Recogemos el usuario por el formulario #

    username = request.GET.get('user')

    # Si existe el check box del formulario #

    if username:
        # Recoge Usuario del modelo y filtramos por el valor del input#

        formulario = PersonaForm(request.GET)
        compras = compra.objects.all().filter(user=username)
        contexto = {'compras':compras, 'formulario':formulario}

    else:
        # Si no existe el check box del formulario no le pasamos el usuario #

        formulario = PersonaForm()
        contexto = {'formulario': formulario}

    return render(request, 'tienda/informes/listado_usuario.html', contexto)

#  TOP 10 PRODUCTOS #
def toptenproductos(request):
    # creamos variable, recogemos el producto del modelo compra y los ordena por la suma de compras #
    unidadesvendidas = compra.objects.values('producto').annotate(total=Sum('importe'),sum_compras=Sum('unidades')).order_by('-sum_compras')[:10]

    Productos = producto.objects.all()


    return render(request, 'tienda/informes/toptenproductos.html', {'Productos':Productos, 'unidadesvendidas':unidadesvendidas})

#  TOP 10 CLIENTES #

def toptenclientes(request):
    # creamos variable, recogemos el usuario del modelo compra y los ordena por la suma de compras #

    comprastotal = compra.objects.values('user').annotate(sum_compras=Sum('importe')).order_by('-sum_compras')[:10]

    Clientes = User.objects.all()

    return render(request, 'tienda/informes/toptenclientes.html', {'Clientes': Clientes,'comprastotal':comprastotal})
