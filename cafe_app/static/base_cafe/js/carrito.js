document.addEventListener('DOMContentLoaded', function () {
    const cartItems = document.getElementById('cart-items');
    const cartTotal = document.getElementById('cart-total');
    const selectDescuento = document.getElementById('tipo-descuento');

    // Función para obtener el carrito del localStorage
    function getCart() {
        return JSON.parse(localStorage.getItem('cart')) || [];
    }

    // Función para guardar el carrito en el localStorage
    function saveCart(cart) {
        localStorage.setItem('cart', JSON.stringify(cart));
    }

    // Función para actualizar los valores en el HTML
    function actualizarValores(totalSinDescuento, descuento, totalConDescuento) {
        document.getElementById('sinDescuento').textContent = formatNumber(totalSinDescuento.toFixed(2));
        document.getElementById('descuento').textContent = formatNumber(descuento.toFixed(2));
        document.getElementById('totalPagar').textContent = formatNumber(totalConDescuento.toFixed(2));
    }

    // Función para calcular los valores y actualizarlos
    function calcularYActualizarValores() {
        const cart = getCart();
        let totalSinDescuento = cart.reduce((total, producto) => total + parseFloat(producto.cantidad) * parseFloat(producto.precio), 0);
        const descuento = parseFloat(selectDescuento.value); // Obtener el valor del descuento seleccionado
        const descuentoAplicado = totalSinDescuento * descuento;
        const totalConDescuento = totalSinDescuento - descuentoAplicado;
        const cartTotal = document.getElementById('cart-total');
        cartTotal.textContent = `Total: $${formatNumber(totalConDescuento.toFixed(2))}`
        actualizarValores(totalSinDescuento, descuentoAplicado, totalConDescuento);
    }

    // Función para mostrar los productos en el carrito
    function mostrarProductosEnCarrito() {
        const cart = getCart();
        cartItems.innerHTML = ''; // Limpiar la lista de productos antes de volver a agregar

        if (cart.length === 0) {
            const row = document.createElement('tr');
            row.innerHTML = `<td colspan="6">No hay productos en el carrito</td>`;
            cartItems.appendChild(row);
        } else {
            cart.forEach(function (producto) {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td><img src="${producto.imagen}" alt="${producto.nombre}" class="img-pequena"/></td>
                    <td>${producto.nombre}</td>
                    <td>
                        <div class="counter-container">
                            <button class="btn decrement" onclick="decrement(${producto.id})">-</button>
                            <span id="counter_${producto.id}">${parseFloat(producto.cantidad)}</span>
                            <button class="btn increment" onclick="increment(${producto.id}, ${producto.cantidadMaxima})">+</button>
                        </div>
                    </td>
                    <td>$${parseFloat(producto.precio)}</td>
                    <td class="sub" data-id="${producto.id}">$${(parseFloat(producto.cantidad) * parseFloat(producto.precio)).toFixed(2)}</td>
                    <td><button class="eliminar-producto" data-id="${producto.id}">Eliminar</button></td>
                `;
                cartItems.appendChild(row);
            });
        }

        // Calcular y mostrar el total del carrito
        const total = cart.reduce((total, producto) => total + parseFloat(parseFloat(producto.cantidad) * parseFloat(producto.precio)), 0);
        cartTotal.textContent = `Total: $${formatNumber(total.toFixed(2))}`;

        // Calcular y actualizar los valores del descuento y total a pagar
        calcularYActualizarValores();
    }

    // Mostrar los productos en el carrito al cargar la página
    mostrarProductosEnCarrito();

    // Listener para el cambio en la selección de descuento
    selectDescuento.addEventListener('change', calcularYActualizarValores);

    // Agregar evento de clic para eliminar productos del carrito
    cartItems.addEventListener('click', function (event) {
        if (event.target.classList.contains('eliminar-producto')) {
            const productId = event.target.getAttribute('data-id');
            const cart = getCart();
            const index = cart.findIndex(producto => producto.id === productId);
            if (index !== -1) {
                cart.splice(index, 1);
                saveCart(cart);
                mostrarProductosEnCarrito(); // Actualizar la tabla después de eliminar un producto
            }
        }
    });

    // Función para calcular y actualizar el cambio
function calcularCambio() {
    const totalPagarElement = document.getElementById('totalPagar');
    const valorRecibidoElement = document.getElementById('valor_recibido');
    const cambioDarElement = document.getElementById('cambio');

    const totalPagar = parseFloat(totalPagarElement.textContent.replace(/[^\d.]/g, ''));
    const valorRecibido = parseFloat(valorRecibidoElement.value);

    let cambio = valorRecibido - totalPagar;
    cambio = Math.max(0, cambio);

    cambioDarElement.value = formatNumber(cambio.toFixed(2));
}

// Evento para calcular el cambio cuando se modifica el valor recibido
valor_recibido.addEventListener('input', calcularCambio);

// Evento para calcular el cambio cuando se cambia el descuento
document.getElementById('tipo-descuento').addEventListener('change', calcularCambio);
    
function formatNumber(number) {
    return number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

});


