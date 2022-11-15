from django import forms
from .models import producto, compra

class ProductoForm(forms.ModelForm):
    class Meta:
        model = producto
        fields = '__all__'


class CompraForm(forms.Form):
    cantidad = forms.IntegerField(required=True)
