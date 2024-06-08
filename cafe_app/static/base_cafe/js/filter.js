// Función para asignar controladores de eventos a los botones de "Agregar Producto"
function assignAddToCartHandlers() {
  document.querySelectorAll('.agregar-producto').forEach(button => {
    button.addEventListener('click', function () {
      // Obtiene la información del producto asociado al boton
      const productId = this.getAttribute('data-id');
      const productName = this.getAttribute('data-nombre');
      const productCant = document.getElementById('counter_' + productId).textContent
      const productPrice = this.getAttribute('data-precio');
      const productimage = this.getAttribute('data-imagen');
      const productCanMax = this.getAttribute('data-cantidadMaxima');

      // Crea un objeto con la información del producto
      const product = {
        id: productId,
        nombre: productName,
        imagen: productimage,
        precio: productPrice,
        cantidad: productCant,
        cantidadMaxima: productCanMax
      };



      // Almacena el objeto producto en la sesión del navegador utilizando sessionStorage
      const cart = JSON.parse(sessionStorage.getItem('cart')) || [];
      const productIndex = cart.findIndex(item => item.id === productId);


      // valida si el producto esta en la sesion
      if (productIndex !== -1) {
        // Si el producto está en el carrito, actualizar su cantidad
        cart[productIndex].cantidad = parseInt(cart[productIndex].cantidad) + parseInt(productCant);


        // Actualizar el carrito en la sesión
        sessionStorage.setItem('cart', JSON.stringify(cart));

        // Título del mensaje de confirmación según la cantidad del producto actualizada
        const titleMessage = parseInt(productCant) === 1 ? `Se agregó ${productCant} unidad` : `Se agregaron ${productCant} unidades más`;

        // Mostrar un mensaje de confirmación
        swal("¡Cantidad actualizada!", {
          icon: 'warning',
          title: titleMessage,
          timer: 2500
        });
      } else {
        cart.push(product);
        sessionStorage.setItem('cart', JSON.stringify(cart));

        // Opcional: Puedes mostrar un mensaje de confirmación o realizar otras acciones aquí
        swal("¡Producto agregado!", {
          icon: 'success',
          title: `¡el producto ${productName} se agrego correctamente!`,
          timer: 2500
        })
      }

    });
  });
}



// Llama a la función después de filtrar los productos
$(document).ready(function () {
  $('#filter-button').click(function () {
    var categoryId = $('#category-select').val();
    if (categoryId) {
      $.ajax({
        type: 'GET',
        url: 'http://127.0.0.1:8000/productos/filtro/',
        data: { category_id: categoryId },
        success: function (data) {
          $('#filtered-products').html(data);
          // Después de actualizar los productos filtrados, vuelve a asignar los controladores de eventos
          assignAddToCartHandlers();
        },
        error: function (xhr, status, error) {
          console.error(error);
        }
      });
    }
  });
});
