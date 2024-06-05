from django.shortcuts import render, redirect
import pandas as pd
from django.views.decorators.csrf import csrf_exempt
from xhtml2pdf import pisa
from django.template.loader import get_template 
from io import BytesIO
import json
from django.http import HttpResponse
from cafe_app.models import Producto, Descuento, Venta, DetalleVenta
from django.db.models import Sum, Count, F, ExpressionWrapper, DecimalField
from django.db.models.functions import TruncDay, ExtractWeekDay

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
        ventas_por_dia = Venta.objects.annotate(weekday=ExtractWeekDay('fecha')).values('weekday').annotate(total=Sum('total')).order_by('weekday')
        dias_semana = ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado']
        ventas_diarias = [0] * 7  # Inicializar con 0 para cada día

        for venta in ventas_por_dia:
            ventas_diarias[venta['weekday'] - 1] = float(venta['total'])  # weekday 1=Lunes, ..., 7=Domingo

        # Sumar ventas diarias de lunes a sábado
        total_ventas_semana = sum(ventas_diarias[1:7])
        # Formatear el resultado con puntos de mil
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
    print(request.session.items())
    usuario_data = request.session.get('usuario')
    if usuario_data:
        nombre = usuario_data['usuario']
        rol_ = usuario_data['rol']
        return render(request, "views/admin/configuracion.html", {"usuario": nombre, "rol": rol_})
    else:
        return HttpResponse("No hay sesión")
    
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