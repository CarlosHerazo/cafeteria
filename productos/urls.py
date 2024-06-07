from django.urls import path
from productos import views
urlpatterns = [
    path('', views.producto, name="admin_productos"), 
    path('filtro/', views.filtro), 
    path('inventarios/', views.nuevo_producto, name="admin_inventarios"),
    path('eliminar/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
    path('buscar_producto/<int:producto_id>/', views.buscar_producto  , name='buscar_producto'),
    path('eliminar_categoria/<int:categoria_id>/', views.eliminar_categoria, name='eliminar_categoria'),
    path('buscar_categoria/<int:categoria_id>/', views.buscar_categoria, name='buscar_categoria'),
    path('buscar_descuento/<int:descuento_id>/', views.buscar_descuento, name='buscar_descuento'),
    path('eliminar_descuento/<int:descuento_id>/', views.eliminar_descuento, name='eliminar_descuento'),
    
]