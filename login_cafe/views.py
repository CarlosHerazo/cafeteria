from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.forms.models import model_to_dict
from cafe_app.models import Usuario, Empleado, Venta, Producto
from django.db.models import Sum, Count, Case, When, IntegerField
from django.db.models.functions import ExtractWeekDay
from django.contrib.auth.hashers import check_password
from cafe_app.decorators import custom_login_required
# Create your views here.

@custom_login_required
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

        ventas_por_dia = Venta.objects.annotate(
            weekday=ExtractWeekDay('fecha')
        ).annotate(
            custom_weekday=Case(
                When(weekday=2, then=1),   # Lunes
                When(weekday=3, then=2),   # Martes
                When(weekday=4, then=3),   # Miércoles
                When(weekday=5, then=4),   # Jueves
                When(weekday=6, then=5),   # Viernes
                When(weekday=7, then=6),   # Sábado
                When(weekday=1, then=7),   # Domingo
                output_field=IntegerField()
            )
        ).values('custom_weekday').annotate(
            total=Sum('total')
        ).order_by('custom_weekday')

        # Imprimir las ventas agrupadas por día de la semana
        print(ventas_por_dia)

        # Asignar nombres a los días de la semana en el orden deseado
        dias_semana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']

        # Inicializar una lista con ceros para cada día de la semana
        ventas_diarias = [0] * 7

        # Rellenar la lista con las ventas agrupadas por día
        for venta in ventas_por_dia:
            # Acceder al valor 'custom_weekday' y restar 1 para obtener el índice correcto (0 basado)
            ventas_diarias[venta['custom_weekday'] - 1] = float(venta['total'])  

        total_ventas_semana = sum(ventas_diarias[0:7])
        total_ventas_semanales = '{:,.0f}'.format(total_ventas_semana)
        print("ssd",total_ventas_semana)
        context = {
            'usuario': usuario,
            'rol': rol_,
            'cantidad_productos': cantidad_productos,
            'categorias': categorias,
            'cantidad_productos_por_categoria': cantidad_productos_por_categoria,
            'dias_semana': dias_semana[0:7],  # Lunes a Domingo
            'ventas_diarias': ventas_diarias[0:7],  # Lunes a Domingo
            'total_ventas_semana': total_ventas_semanales,
        }

        return render(request, "views/admin/index.html", context)
    else:
        # Si no hay datos de usuario en la sesión, redirigir 
        return redirect('login')  



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
            if check_password(pwd_usuario, usuario_bd.contrasena):
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
