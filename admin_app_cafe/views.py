from django.shortcuts import render, redirect
from cafe_app.decorators import custom_login_required
import pandas as pd
from django.contrib.humanize.templatetags.humanize import intcomma
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from xhtml2pdf import pisa
from django.template.loader import get_template 
from io import BytesIO
import json
from django.http import HttpResponse, JsonResponse
from cafe_app.models import Producto, Descuento, Venta, DetalleVenta, Categoria, Empleado, Usuario
from cafe_app.forms import CategoriaForm, DescuentoForm, EmpleadoUsuarioForm
from django.db.models import Sum, Count, F, ExpressionWrapper, DecimalField, Case, When, IntegerField
from django.db.models.functions import ExtractWeekDay
import xlsxwriter
from datetime import datetime
# Create your views here.

@custom_login_required
def index(request):
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

        # Sumar ventas diarias de lunes a sábado
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

@custom_login_required
def carrito(request):
    print(request.session.items())
    usuario_data = request.session.get('usuario')
    if usuario_data:
        nombre = usuario_data['usuario']
        rol_ = usuario_data['rol']
        descuentos = Descuento.objects.all()
        for descuento in descuentos:
            descuento.desc = str(descuento.desc).replace(',', '.')
        return render(request, "views/admin/carrito.html", {"usuario": nombre, "rol": rol_, "descuentos":descuentos})
    else:
        return HttpResponse("No hay sesión")
    

@custom_login_required
def historial(request):
    usuario_data = request.session.get('usuario')
    if usuario_data:
        nombre = usuario_data['usuario']
        rol_ = usuario_data['rol']
        
        # Recuperar los detalles de venta del historial
        detalles_venta = DetalleVenta.objects.all()
        
        # Realizar la multiplicación en la consulta
        detalles_venta = detalles_venta.annotate(total=ExpressionWrapper(F('producto__precio') * F('cantidad'), output_field=DecimalField()))
        
        # Pasar los detalles de venta y otros datos al contexto para el renderizado de la plantilla
        return render(request, "views/admin/historial.html", {
            "usuario": nombre,
            "rol": rol_,
            "detalles_venta": detalles_venta,
        })
    else:
        return HttpResponse("No hay sesión")
    
    
@custom_login_required
def configuracion(request):
    usuario_data = request.session.get('usuario')
    if not usuario_data:
        return HttpResponse("No hay sesión")
    
    nombre = usuario_data['usuario']
    rol_ = usuario_data['rol']
    
    formCategoria = CategoriaForm()  # Mover la definición aquí

    if request.method == 'POST':
        key = request.POST.get('key')
        print(key)
        if key == "categoria":
            categoria_id = request.POST.get('categoria_id')
            if categoria_id:  # Actualización de categoría
                categoria = get_object_or_404(Categoria, pk=categoria_id)
                formCategoria = CategoriaForm(request.POST, request.FILES, instance=categoria)
            else:  # Creación de nueva categoría
                formCategoria = CategoriaForm(request.POST, request.FILES)

            if formCategoria.is_valid():
                formCategoria.save()
                return redirect('admin_configuracion')

        elif key == "descuento":
            descuento_id = request.POST.get('descuento_id')
            print(descuento_id)
            if descuento_id:  # Actualización de categoría
                descuento = get_object_or_404(Descuento, pk=descuento_id)
                formDescuento = DescuentoForm(request.POST, request.FILES, instance=descuento)
            else:  # Creación de nueva categoría
                formDescuento = DescuentoForm(request.POST, request.FILES)
            
            if formDescuento.is_valid():
                formDescuento.save()
                return redirect('admin_configuracion')
    else:
        formDescuento = DescuentoForm()

    categorias = Categoria.objects.all()
    descuentos = Descuento.objects.all()

    return render(request, "views/admin/configuracion.html", {
        "usuario": nombre,
        "rol": rol_,
        "formCategoria": formCategoria,
        "formDescuento": formDescuento,
        "categorias": categorias,
        "descuentos": descuentos,
    })
    
@csrf_exempt
def generar_factura(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        formato = request.GET.get('formato', 'pdf')
        

        if formato == 'pdf':
            return generar_pdf(data)
        elif formato == 'excel':
            return generar_excel(data)
    else:
        return HttpResponse(status=405)

def generar_pdf(data):
    print(data)
    sum_total = 0
    template = get_template('views/admin/factura.html')

    for valor in data:
        id_compra = valor['idCompra'] 
    
    venta = Venta.objects.get(id=id_compra)


    html = template.render({'data': data, 'total_compra':venta.total, 'descuento':venta.desc})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="factura".pdf"'
    
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error al generar PDF', status=500)
    return response

def generar_excel(data):
    # Obtener la fecha desde los datos enviados
    fecha_reporte_str = data['fechaReporte']

    # Convertir la fecha de cadena de texto a objeto datetime
    fecha_reporte_obj = datetime.strptime(fecha_reporte_str, '%Y-%m-%d')

    # Formatear la fecha en el formato deseado
    fecha_reporte = fecha_reporte_obj.strftime('%d-%m-%Y')  # Por ejemplo, '07-06-2024'
    
    if not fecha_reporte:
        return HttpResponse("No se proporcionó una fecha para el reporte", status=400)

    # Convertir la fecha a formato datetime
    fecha_inicio = pd.to_datetime(fecha_reporte)
    fecha_fin = fecha_inicio + pd.DateOffset(days=1)  # Sumamos un día para obtener ventas hasta el final del día

    # Obtener todas las ventas realizadas en esa fecha
    ventas = Venta.objects.filter(fecha__range=[fecha_inicio, fecha_fin])

    # Crear una lista para almacenar los datos de ventas y productos
    datos = []
    
    for venta in ventas:
        detalles = DetalleVenta.objects.filter(venta=venta).select_related('producto')
        for detalle in detalles:
            datos.append({
                'Fecha': venta.fecha.strftime('%Y-%m-%d %H:%M:%S'),  # Formatear la fecha para mejor legibilidad
                'Nombre Cliente': venta.nombre_cliente,
                'Producto': detalle.producto.nombre,
                'Cantidad': detalle.cantidad,
                'Precio Unitario': detalle.producto.precio,
                'Total Venta': venta.total,
                'Cafeteria': venta.cafeteria.nombre,
            })

    # Crear un DataFrame con los datos
    df = pd.DataFrame(datos)

    # Formatear la fecha para usar en el nombre del archivo y la hoja
    fecha_reporte_formateada = fecha_inicio.strftime('%Y-%m-%d')

    # Crear un archivo Excel
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet('Factura')

    # Definir los estilos para las celdas
    bold = workbook.add_format({'bold': True})
    money_format = workbook.add_format({'num_format': '$#,##0.00'})
    
    # Escribir los datos en el archivo Excel
    for i, col in enumerate(df.columns):
        worksheet.write(0, i, col, bold)
        # Ajustar el ancho de las columnas
        worksheet.set_column(i, i, max(len(col), df[col].astype(str).str.len().max()))

    for i, row in df.iterrows():
        for j, value in enumerate(row):
            worksheet.write(i + 1, j, value, money_format if isinstance(value, float) else None)

    workbook.close()
    output.seek(0)

    # Crear la respuesta HTTP con el archivo Excel
    response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="factura_{fecha_reporte_formateada}.xlsx"'
    return response


@custom_login_required   
def empleados(request):
    usuario_data = request.session.get('usuario')
    if usuario_data:
        usuario = usuario_data['usuario']
        rol_ = usuario_data['rol']
        empleado_id = request.POST.get('cedula')
        print(request.POST)
        if request.method == 'POST':
            if empleado_id:
                empleado = get_object_or_404(Empleado, pk=empleado_id)
                form = EmpleadoUsuarioForm(request.POST, instance=empleado)
            else:
                form = EmpleadoUsuarioForm(request.POST)

            if form.is_valid():
                form.save()
                return redirect('admin_inventarios')
        else:
            form = EmpleadoUsuarioForm()
        
        empleados = Empleado.objects.all()  # Obtenemos todos los empleados
        context = {
            "usuarios": Usuario.objects.all(),
            "rol": rol_,
            "form": form,
            "empleados": empleados, # Pasar la lista de empleados al contexto
            "usuario":usuario
        }
        return render(request, "views/admin/empleados.html", context)
    else:
        return redirect('login')


def eliminar_empleado(request, empleado_id):
    # Verificar que la solicitud sea POST
    if request.method == 'POST':
        print(request.POST)
        usuario = get_object_or_404(Usuario, pk=empleado_id)
        usuario.delete()      
        return redirect('admin_empleados')
    else:
        return redirect('admin_empleados')



def buscar_empleado(request, empleado_id):
    # Buscar el descuento en la base de datos
    if request.method == "GET":
        try:
            usuario = Usuario.objects.get(id=empleado_id)
            # Crear un diccionario con los datos del usuario y del empleado asociado
            usuario_data = {
                'id': usuario.id,
                'correo': usuario.correo,
                'contrasena': usuario.contrasena,
                'usuario': usuario.usuario,
                'empleado_nombre': usuario.empleado.nombre,
                'empleado_cedula': usuario.empleado.cedula,
                'empleado_direccion': usuario.empleado.direccion,
                'empleado_telefono': usuario.empleado.telefono,
                'empleado_rol': usuario.empleado.rol,
                'cafeteria_id': usuario.empleado.cafeteria.id,  # ID de la cafetería asociada
                'cafeteria_nombre': usuario.empleado.cafeteria.nombre  # Nombre de la cafetería
            }

            # Devolver la respuesta JSON con los datos del descuento
            return JsonResponse(usuario_data)
        except Producto.DoesNotExist:
            # Si el descuento no existe, devolver un JSON con un mensaje de error
            return JsonResponse({'error': 'El descuento no existe'}, status=404)
        
@custom_login_required
def catalogo(request):
    print(request.session.items())
    usuario_data = request.session.get('usuario')
    if usuario_data:
        # datos usuario
        nombre = usuario_data['usuario']
        rol_ = usuario_data['rol']       
        # Obtener todos los productos
        productos = Producto.objects.all()  # Esto obtiene todos los productos de la base de datos
        for producto in productos:
            producto.precio_formateado = "${}".format(intcomma(int(producto.precio)))
        categorias = Categoria.objects.all()
        
        return render(request, "views/admin/catalogo.html", {"usuario": nombre, "rol": rol_, "productos": productos, "categorias":categorias})
    else:
        return HttpResponse("No hay sesión")