from django import forms
from cafe_app.models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'precio', 'descripcion', 'cantidad', 'imagen', 'cafeteria', 'categoria']

