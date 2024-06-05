// Obtener el botón
const checkoutButton = document.getElementById('checkout-button');

// Agregar un evento de escucha al botón
checkoutButton.addEventListener('click', function () {
  realizarPedido();
});

// Función para realizar el pedido
function realizarPedido() {
  const cart = JSON.parse(localStorage.getItem('cart')) || [];
  const valorRecibido = parseFloat(document.getElementById('valor_recibido').value);

  const totalPagarElement = document.getElementById('totalPagar').textContent;
  const descuentoElement = document.getElementById('descuento').textContent;
  const totalPagar = parseFloat(totalPagarElement.replace(/[^\d.-]/g, '')).toFixed(2);
  const descuento = parseFloat(descuentoElement.replace(/[^\d.-]/g, '')).toFixed(2);

  console.log(totalPagar);
  // Definir la variable global con la URL
  const realizarPedidoUrl = "http://127.0.0.1:8000/admin_cafe/realizar_pedido/";


  // Enviar los datos al backend
  // Verificar si el valor recibido es mayor que cero y mayor o igual al total a pagar, ademas si hay productos en el carrito
  let cartData = localStorage.getItem("cart");
  if ((valorRecibido > 0 && valorRecibido >= totalPagar && totalPagar > 0) && (cartData !== null && cartData.length > 0)) {
    // Utilizar SweetAlert para solicitar la dirección de correo electrónico
    Swal.fire({
      title: 'Ingrese su dirección de correo electrónico:',
      input: 'email',
      inputAttributes: {
        autocapitalize: 'off'
      },
      showCancelButton: true,
      confirmButtonText: 'Enviar',
      cancelButtonText: 'Cancelar',
      showLoaderOnConfirm: true,
      preConfirm: (correoElectronico) => {
        // Si el usuario ingresó una dirección de correo electrónico, enviar la solicitud al backend
        if (correoElectronico) {
          return fetch(realizarPedidoUrl, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': getCookie('csrftoken') // Obtener el token CSRF
            },
            body: JSON.stringify({
              cart: cart,
              valorRecibido: valorRecibido,
              totalPagar: totalPagar,
              descuento: descuento,
              correoElectronico: correoElectronico
            })
          })
            .then(response => {
              if (!response.ok) {
                throw new Error(response.statusText);
              }
              return response.json();
            })
            .catch(error => {
              Swal.showValidationMessage(
                `Hubo un error al enviar la solicitud: ${error}`
              );
            });
        } else {
          // Si el usuario no ingresó una dirección de correo electrónico, mostrar un mensaje de error
          return Swal.showValidationMessage('Debe ingresar una dirección de correo electrónico.');
        }
      },
      allowOutsideClick: () => !Swal.isLoading()
    }).then((result) => {
      if (result.isConfirmed) {
        Swal.fire(
          '¡Pedido realizado!',
          'El pedido ha sido realizado exitosamente.',
          'success'
        ).then(() => {
          localStorage.removeItem("cart");
          window.location.reload()
        });

      }
    });
  } else {
    // El valor recibido no es suficiente para realizar el pedido
    Swal.fire(
      'Error',
      'El valor recibido no es suficiente para realizar el pedido.',
      'error'
    );
  }


}

// Obtener el valor del token CSRF
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Buscar el token CSRF
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
