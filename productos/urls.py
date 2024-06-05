from django.urls import path
from productos import views
urlpatterns = [
    path('', views.producto, name="admin_productos"), 
    path('filtro/', views.filtro), 
    path('inventarios/', views.nuevo_producto, name="admin_inventarios"),
    path('eliminar/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
    path('buscar_producto/<int:producto_id>/', views.buscar_producto  , name='buscar_producto'),
    
]