from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.forms.models import model_to_dict
from cafe_app.models import Usuario, Empleado, Venta, Producto
from django.db.models import Sum, Count
from django.db.models.functions import TruncDay, ExtractWeekDay

# Create your views here.


# inicio de la aplicacion 
def inicio(request):
    usuario_data = request.session.get('usuario')
    if usuario_data:
        usuario = usuario_data['usuario']
        rol_ = usuario_data['rol']

        # Obtener la cantidad de productos
        cantidad_productos = Producto.objects.count()

        # Obtener la cantidad de productos por categoría
        productos_por_categoria = Producto.objects.values('categoria__nombre').annotate(total=Count('id'))
        categorias = [producto['categoria__nombre'] for producto in productos_por_categoria]
        cantidad_productos_por_categoria = [producto['total'] for producto in productos_por_categoria]

        # Obtener las ventas totales por día de la semana
        ventas_por_dia = Venta.objects.annotate(weekday=ExtractWeekDay('fecha')).values('weekday').annotate(total=Sum('total')).order_by('weekday')
        dias_semana = ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado']
        ventas_diarias = [0] * 7  # Inicializar con 0 para cada día

        for venta in ventas_por_dia:
            ventas_diarias[venta['weekday'] - 1] = float(venta['total'])  # weekday 1=Lunes, ..., 7=Domingo

        # Sumar ventas diarias de lunes a sábado
        total_ventas_semana = sum(ventas_diarias[1:7])
        total_ventas_semanales = '{:,.0f}'.format(total_ventas_semana)
        context = {
            'usuario': usuario,
            'rol': rol_,
            'cantidad_productos': cantidad_productos,
            'categorias': categorias,
            'cantidad_productos_por_categoria': cantidad_productos_por_categoria,
            'dias_semana': dias_semana[1:7],  # Lunes a Sábado
            'ventas_diarias': ventas_diarias[1:7],  # Lunes a Sábado
            'total_ventas_semana': total_ventas_semanales,
        }

        return render(request, "views/admin/index.html", context)
    else:
        # Si no hay datos de usuario en la sesión, redirigir o manejar según tu lógica
        return redirect('login')  # Asumiendo que tienes una vista de login



# cofirmacion de las credenciales
def confirm_login(request):
    if request.method == "POST":
        correo = request.POST.get("email")
        pwd_usuario = request.POST.get("pwd_usuario")
        
        try:
            # verificamos si existe el usuario
            usuario_bd = Usuario.objects.get(correo=correo)
            # obtenemos su cedula
            empleado_id = usuario_bd.empleado_id
            # busnamos el empleado asociado a la cedula
            empleado = Empleado.objects.get(cedula=empleado_id)
            # obtenemos el rol
            empleado_rol = empleado.rol
            
        except Usuario.DoesNotExist:
            usuario_bd = None
        if usuario_bd is not None:
            if pwd_usuario == usuario_bd.contrasena:
                # Convertir el objeto Admin a un diccionario
                usuario_data = model_to_dict(usuario_bd)
                # Agregar el campo 'rol' al diccionario
                usuario_data['rol'] = empleado_rol
               
                del usuario_data['contrasena']
                
                request.session['usuario'] = usuario_data
                return JsonResponse({'success': "ok", "usuario":empleado_rol})
            else:
                mensaje_error = "Credenciales incorrectas"
        else:
            mensaje_error = "Usuario no encontrado"

        return JsonResponse({'mensaje_error': mensaje_error})

    return JsonResponse({'error': 'Esta vista solo acepta solicitudes POST.'}, status=405)
