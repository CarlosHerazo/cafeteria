from django.urls import path
from admin_app_cafe import views
from productos.views import realizar_pedido
urlpatterns = [
    path('index/', views.index, name="index"),
    path('carrito/', views.carrito, name="admin_carrito"),
    path('historial/', views.historial, name="admin_historial"),
    path('configuracion/', views.configuracion, name="admin_configuracion"),   
    path('realizar_pedido/', realizar_pedido  , name='realizarPedido'),
    path('generarFactura/', views.generar_factura, name='generarFactura'),
    
]