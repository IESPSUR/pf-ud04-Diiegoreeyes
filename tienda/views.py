from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from .forms import ProductoForm, CompraForm


# Create your views here.
def welcome(request):
    return render(request,'tienda/index.html', {})

def listado(request):
    listadoprod = producto.objects.all()
    return render(request,'tienda/listado.html', {'listadoprod':listadoprod})

def compra(request):
    productocompra = producto.objects.all()
    return render(request,'tienda/compra.html', {'productocompra':productocompra})

def formcompra(request, id):
    Producto = get_object_or_404(producto, id=id)
    formulario = CompraForm(request.POST)
    if request.method == 'POST':
        if formulario.is_valid():
            cantidad = formulario.cleaned_data['cantidad']
            if (Producto.unidades > cantidad):
                Producto.unidades = Producto.unidades - cantidad
                Producto.save()
                return redirect('compra')
    return render(request,'tienda/formcompra.html', {'formulario':formulario})

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
