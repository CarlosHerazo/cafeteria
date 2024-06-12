from django.shortcuts import render
from cafe_app.decorators import custom_login_required
from cafe_app.models import Producto, Categoria, Venta, DetalleVenta, Descuento
from django.db.models import F
from django.contrib.humanize.templatetags.humanize import intcomma
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProductoForm
from django.conf import settings
from django.core.mail import send_mail
import json


def nuevo_producto(request):
    usuario_data = request.session.get('usuario')
    if usuario_data:
        nombre = usuario_data['usuario']
        rol_ = usuario_data['rol']
    
    if request.method == 'POST':
        # Si hay un producto_id en los datos POST, se trata de una actualización
        producto_id = request.POST.get('producto_id')
        if producto_id != "":
            producto = get_object_or_404(Producto, pk=producto_id)
            form = ProductoForm(request.POST, request.FILES, instance=producto)
        else:
            form = ProductoForm(request.POST, request.FILES)
        
        if form.is_valid():
            if not form.cleaned_data['imagen']:
                form.cleaned_data['imagen'] = producto.imagen if producto_id else None
            form.save()
            return redirect('admin_inventarios')
    else:
        form = ProductoForm()

    productos = Producto.objects.all()  # Esto obtiene todos los productos de la base de datos
    return render(request, 'productos/inventarios.html', {"usuario": nombre, "rol": rol_,'form': form,"productos":productos})

def eliminar_producto(request, producto_id):

    if request.method == 'POST':
        producto = get_object_or_404(Producto, pk=producto_id)
        producto.delete()

        return redirect('admin_inventarios')


def buscar_producto(request, producto_id):
 
    # Buscar el producto en la base de datos
    try:
        producto = Producto.objects.get(id=producto_id)
        # Crear un diccionario con los datos del producto
        producto_data = {
            'id': producto.id,
            'nombre': producto.nombre,
            'precio': producto.precio,
            'descripcion': producto.descripcion,
            'imagen': producto.imagen.url,
            'cantidad': producto.cantidad,
            'cafeteria': producto.cafeteria.id,
            'categoria': producto.categoria.id,
        }
        # Devolver la respuesta JSON con los datos del producto
        return JsonResponse(producto_data)
    except Producto.DoesNotExist:
        # Si el producto no existe, devolver un JSON con un mensaje de error
        return JsonResponse({'error': 'El producto no existe'}, status=404)


@custom_login_required
def producto(request):
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
        
        return render(request, "productos/productos.html", {"usuario": nombre, "rol": rol_, "productos": productos, "categorias":categorias})
    else:
        return HttpResponse("No hay sesión")

@custom_login_required  
def inventarios(request):
    print(request.session.items())
    usuario_data = request.session.get('usuario')
    if usuario_data:
        nombre = usuario_data['usuario']
        rol_ = usuario_data['rol']

        productos = Producto.objects.all()  # Esto obtiene todos los productos de la base de datos
        for producto in productos:
            producto.precio_formateado = "${}".format(intcomma(int(producto.precio)))
        return render(request, "productos/inventarios.html", {"usuario": nombre, "rol": rol_,"productos":productos})
    else:
        return HttpResponse("No hay sesión")
    

def filtro(request):
    if request.method == 'GET':
        category_id = request.GET.get('category_id')
        if category_id != "0":
            productos = Producto.objects.filter(categoria_id=category_id)
            for producto in productos:
                producto.precio_formateado = "${}".format(intcomma(int(producto.precio)))
            return render(request, 'productos/productos_filtrados.html', {'productos': productos})
        else:
            # Si no se proporciona una categoría, mostramos todos los productos.
            productos = Producto.objects.all()
            for producto in productos:
                producto.precio_formateado = "${}".format(intcomma(int(producto.precio)))
            return render(request, 'productos/productos_filtrados.html', {'productos': productos})
    else:
        # Si la solicitud no es AJAX o no es de tipo GET, puedes devolver un error o redirigir a otra vista.
        return HttpResponseBadRequest("Bad request")




@custom_login_required
def realizar_pedido(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        cart = data['cart']
        valor_recibido = data['valorRecibido']
        total_pagar = data['totalPagar']
        cliente = data['correoElectronico']
        descuento = data['descuento']
        
        # Guardar la venta en la base de datos
        venta = Venta.objects.create(
            cafeteria_id=1, 
            total=total_pagar,
            nombre_cliente=cliente,
            desc=descuento,
        )
        venta_id = Venta.objects.latest('id')
        # Guardar los detalles de la venta en la base de datos
        for item in cart:
            producto_id = item['id']
            cantidad = item['cantidad']
            producto = Producto.objects.get(id=producto_id)  # Buscar el producto por su ID
            DetalleVenta.objects.create(
                venta=venta,
                producto=producto,
                cantidad=cantidad
            )

            # Restar la cantidad vendida del stock del producto
            Producto.objects.filter(id=producto_id).update(cantidad=F('cantidad') - int(item['cantidad']))
        



        recipient_list=[]
        subject = "Compra sena"
        
        # Asigna el cuerpo del mensaje
        message = f"""Hola,

        Gracias por tu compra en nuestra cafetería. Aquí está el resumen de tu pedido:

        --------------------------------------------------
        Detalle del Pedido:
        --------------------------------------------------
        {cliente},
        
        Productos comprados:
        """
        message += f"""
            ID DE LA COMPRA {venta_id.id}
         """
        # Agregar los productos comprados al mensaje
        for item in cart:
            producto_nombre = item['nombre']  
            cantidad = item['cantidad']
            precio_unitario = item['precio']  
            precio_unitario = float(precio_unitario.replace(',', '.'))
            subtotal = float(cantidad) * precio_unitario
            message += f"----- {producto_nombre}: {cantidad} x ${precio_unitario} = ${subtotal}\n ----- "
        
        message += f"\n valor dado: ${valor_recibido}\n\n"
        # Agregar el total a pagar al mensaje
        message += f"\nTotal a pagar: ${total_pagar}\n\n"

      
        # Mensaje final
        message += """
        ---------------------------------------------------------------------------------------
        Gracias por tu compra. Si tienes alguna pregunta o inquietud, no dudes en contactarnos.
        
        Saludos, El equipo de la Cafetería SENA casa del marques
        ---------------------------------------------------------------------------------------
        """

        email_from = settings.EMAIL_HOST_USER
        recipient_list.append(cliente)
        send_mail(subject, message, email_from, recipient_list, fail_silently=False)


        
        return JsonResponse({'message': 'Pedido realizado exitosamente'})
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)



# actualizar categoria

def buscar_categoria(request, categoria_id):
    if request.method == "GET":
        # Buscar el producto en la base de datos
        try:
            categoria = Categoria.objects.get(id=categoria_id)
            # Crear un diccionario con los datos del producto
            categoria_data = {
                'id': categoria.id,
                'nombre': categoria.nombre,
            
            }
            # Devolver la respuesta JSON con los datos del producto
            return JsonResponse(categoria_data)
        except Producto.DoesNotExist:
            # Si el producto no existe, devolver un JSON con un mensaje de error
            return JsonResponse({'error': 'La categoria no existe'}, status=404)


# actualizar los descuentos

def buscar_descuento(request, descuento_id):
    # Buscar el descuento en la base de datos
    if request.method == "GET":
        try:
            descuento = Descuento.objects.get(id=descuento_id)
            # Crear un diccionario con los datos del descuento
            descuento_data = {
                'id': descuento.id,
                'tipo_descuento': descuento.tipo_descuento,
                'descuento': descuento.desc,
            
            }
            # Devolver la respuesta JSON con los datos del descuento
            return JsonResponse(descuento_data)
        except Producto.DoesNotExist:
            # Si el descuento no existe, devolver un JSON con un mensaje de error
            return JsonResponse({'error': 'El descuento no existe'}, status=404)

def eliminar_categoria(request, categoria_id):
    # Verificar que la solicitud sea POST
    if request.method == 'POST':
        categoria = get_object_or_404(Categoria, pk=categoria_id)
        categoria.delete()
        
        return redirect('admin_configuracion')
    else:
        return redirect('admin_configuracion')

def eliminar_descuento(request, descuento_id):
    # Verificar que la solicitud sea POST
    if request.method == 'POST':
        descuento = get_object_or_404(Descuento, pk=descuento_id)
        descuento.delete()
        
        return redirect('admin_configuracion')
    else:
        return redirect('admin_configuracion')