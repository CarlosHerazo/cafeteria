from django import forms
from .models import Categoria, Descuento, Empleado, Usuario, Cafeteria
from django.contrib.auth.hashers import make_password

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre']

class DescuentoForm(forms.ModelForm):
    class Meta:
        model = Descuento
        fields = ['tipo_descuento','desc' ] 


class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ['cedula', 'nombre', 'direccion', 'telefono', 'rol', 'cafeteria']  # Campos del modelo Empleado
        labels = {
            'cedula': 'Cédula',
            'nombre': 'Nombre',
            'direccion': 'Dirección',
            'telefono': 'Teléfono',
            'rol': 'Rol',
            'cafeteria': 'Cafetería'
        }
        widgets = {
            'cedula': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'rol': forms.TextInput(attrs={'class': 'form-control'}),
            'cafeteria': forms.Select(attrs={'class': 'form-control'}),
        }

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['correo', 'contrasena', 'usuario', 'empleado']  # Campos del modelo Usuario
        labels = {
            'correo': 'Correo Electrónico',
            'contrasena': 'Contraseña',
            'usuario': 'Nombre de Usuario',
            'empleado': 'Empleado'
        }
        widgets = {
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
            'contrasena': forms.PasswordInput(attrs={'class': 'form-control'}),
            'usuario': forms.TextInput(attrs={'class': 'form-control'}),
            'empleado': forms.Select(attrs={'class': 'form-control'}),
        }



class EmpleadoUsuarioForm(forms.ModelForm):
    # Campos del modelo Empleado
    cedula = forms.CharField(label='Cédula', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    nombre = forms.CharField(label='Nombre', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    direccion = forms.CharField(label='Dirección', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    telefono = forms.CharField(label='Teléfono', max_length=10, widget=forms.TextInput(attrs={'class': 'form-control'}))
    rol = forms.CharField(label='Rol', max_length=90, widget=forms.TextInput(attrs={'class': 'form-control'}))
    cafeteria = forms.ModelChoiceField(queryset=Cafeteria.objects.all(), label='Cafetería', widget=forms.Select(attrs={'class': 'form-control'}))
    
    # Campos del modelo Usuario
    correo = forms.EmailField(label='Correo Electrónico', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    contrasena = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'new-password'}))
    usuario = forms.CharField(label='Nombre de Usuario', max_length=90, widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}))

    class Meta:
        model = Empleado
        fields = ['cedula', 'nombre', 'direccion', 'telefono', 'rol', 'cafeteria']

    def save(self, commit=True):
        if self.instance.pk:
            # Actualización de un empleado existente
            empleado = super().save(commit=False)
            empleado.cedula = self.cleaned_data['cedula']
            empleado.nombre = self.cleaned_data['nombre']
            empleado.direccion = self.cleaned_data['direccion']
            empleado.telefono = self.cleaned_data['telefono']
            empleado.rol = self.cleaned_data['rol']
            empleado.cafeteria = self.cleaned_data['cafeteria']

            if commit:
                empleado.save()
            
            # Actualizar el usuario relacionado
            usuario = empleado.usuario_set.first()
            usuario.correo = self.cleaned_data['correo']
            usuario.usuario = self.cleaned_data['usuario']
            if self.cleaned_data['contrasena']:
                usuario.contrasena = self.cleaned_data['contrasena']  # Actualiza la contraseña solo si hay una nueva
            if commit:
                usuario.save()
        else:
            # Creación de un nuevo empleado y usuario
            empleado = Empleado.objects.create(
                cedula=self.cleaned_data['cedula'],
                nombre=self.cleaned_data['nombre'],
                direccion=self.cleaned_data['direccion'],
                telefono=self.cleaned_data['telefono'],
                rol=self.cleaned_data['rol'],
                cafeteria=self.cleaned_data['cafeteria']
            )
            
            Usuario.objects.create(
                correo=self.cleaned_data['correo'],
                contrasena=make_password(self.cleaned_data['contrasena']),  # Hashear la contraseña
                usuario=self.cleaned_data['usuario'],
                empleado=empleado
            )
        
        return empleado