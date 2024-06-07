from django.urls import path
from recuperacionPass import views
urlpatterns = [
    path('recuperar/', views.recuperar, name="solicitar_recuperacion"),
    path('password_reset_done/', views.mensaje, name='password_reset_done'),
    path('recuperacion/reset/<str:token>/', views.reset_password, name='reset_password'), 
    
]