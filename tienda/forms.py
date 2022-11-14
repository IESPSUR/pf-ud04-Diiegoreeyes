from django import forms
from .models import producto, compra

class ProductoForm(forms.ModelForm):
    class Meta:
        model = producto
        fields = '__all__'

class CompraForm(forms.ModelForm):
    class Meta:
        model = compra
        fields = '__all__'