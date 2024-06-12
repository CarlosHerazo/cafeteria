from django.urls import path
from admin_app_cafe import views
from productos.views import realizar_pedido
urlpatterns = [
    path('index/', views.index, name="index"),
    path('catalogoProductos/', views.catalogo, name="catalogoProductosClientes"),
    path('carrito/', views.carrito, name="admin_carrito"),
    path('historial/', views.historial, name="admin_historial"),
    path('empleados/', views.empleados, name="admin_empleados"),
    path('configuracion/', views.configuracion, name="admin_configuracion"),   
    path('realizar_pedido/', realizar_pedido  , name='realizarPedido'),
    path('generarFactura/', views.generar_factura, name='generarFactura'),
    path('eliminarEmpleado/<int:empleado_id>', views.eliminar_empleado, name='eliminar_empleado'),
    path('buscarEmpleado/<int:empleado_id>', views.buscar_empleado, name='buscarEmpleado'),
]