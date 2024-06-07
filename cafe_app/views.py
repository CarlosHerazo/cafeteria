from django.shortcuts import render, redirect
from django.contrib.auth import logout

# Create your views here.
def login_cafe(request):
    return render(request, "login/login.html")



def cerrar_sesion(request):
    logout(request)
    return redirect('login')