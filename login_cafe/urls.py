from django.urls import path
from .views import confirm_login, inicio

urlpatterns = [
    path('inicio/', inicio),
    path('', confirm_login),
    
]