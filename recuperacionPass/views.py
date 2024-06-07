from django.shortcuts import render
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.http import HttpResponse
from cafe_app.models import Usuario
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.utils import timezone
from .forms import PasswordResetRequestForm, PasswordResetForm

# Create your views here.

def recuperar(request):
    form = PasswordResetRequestForm()
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            # Aquí puedes manejar la lógica para enviar el correo electrónico de recuperación
            email = form.cleaned_data['email']
            usuario = Usuario.objects.filter(correo=email).first()
            if usuario:
                token = usuario.generate_password_reset_token()
                # Enviar correo electrónico
                send_mail(
                    'Recuperación de Contraseña',
                    f'Para restablecer su contraseña, haga clic en el siguiente enlace: http://127.0.0.1:8000/recuperacion/reset/{token}/',
                    'from@example.com',
                    [email],
                )
                return redirect('password_reset_done')
            # Envía el correo de recuperación aquí...
            return render(request, 'exito.html')  

    return render(request, "recuperacion.html", {'form': form})

def reset_password(request, token):
    usuario = get_object_or_404(Usuario, password_reset_token=token)
    if timezone.now() > usuario.password_reset_expiry:
        return HttpResponse("Token de restablecimiento ha expirado.")
    
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            nueva_contrasena = form.cleaned_data['new_password']
            usuario.contrasena = make_password(nueva_contrasena)
            usuario.password_reset_token = None
            usuario.password_reset_expiry = None
            usuario.save()
            return redirect('login')
    else:
        form = PasswordResetForm()
    return render(request, 'reset_password.html', {'form': form})


def mensaje(request):
    return render(request, "mensaje.html")