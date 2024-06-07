from django.shortcuts import render, redirect
import pandas as pd
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from xhtml2pdf import pisa
from django.template.loader import get_template 
from io import BytesIO
import json
from django.http import HttpResponse
from cafe_app.models import Producto, Descuento, Venta, DetalleVenta, Categoria, Empleado, Usuario
from cafe_app.forms import CategoriaForm, DescuentoForm, EmpleadoForm, UsuarioForm, EmpleadoUsuarioForm
from django.db.models import Sum, Count, F, ExpressionWrapper, DecimalField, Case, When, IntegerField
from django.db.models.functions import ExtractWeekDay

# Create your views here.
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
    response['Content-Disposition'] = f'attachment; filename="factura.pdf"'
    
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error al generar PDF', status=500)
    return response

def generar_excel(data):
    df = pd.DataFrame(data)
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Factura')
    writer._save()
    output.seek(0)

    response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="factura.xlsx"'
    return response

    
def empleados(request):
    usuario_data = request.session.get('usuario')
    if usuario_data:
        usuario = usuario_data['usuario']
        rol_ = usuario_data['rol']

        # Obtener todos los empleados
        empleados = Empleado.objects.all()

        if request.method == 'POST':
            empleado_id = request.POST.get('empleado_id', "")
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

        context = {
            "usuario": usuario,
            "rol": rol_,
            "form": form,
            "empleados": empleados  # Pasar la lista de empleados al contexto
        }
        return render(request, "views/admin/empleados.html", context)
    else:
        return redirect('login')