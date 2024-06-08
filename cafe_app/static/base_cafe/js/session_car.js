

// Función para obtener el carrito del localStorage
function getCart() {
    let cart = localStorage.getItem('cart');
    return cart ? JSON.parse(cart) : [];
}

// Función para guardar el carrito en el localStorage
function saveCart(cart) {
    localStorage.setItem('cart', JSON.stringify(cart));
}

// Función para actualizar la vista del carrito
function updateCartView() {
    const cartItems = document.getElementById('cart-items');
    const cartTotal = document.getElementById('cart-total');
    const cart = getCart();
    cartItems.innerHTML = '';

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
    cartTotal.textContent = `Total: $${total.toFixed(2)}`;

    // // Calcular y actualizar los valores del descuento y total a pagar
    // calcularYActualizarValores();
}

// Delegación de eventos para agregar producto
document.addEventListener('click', function (event) {
    if (event.target.classList.contains('agregar-producto')) {
        // Obtiene la información del producto asociado al botón
        const productId = event.target.getAttribute('data-id');
        const productName = event.target.getAttribute('data-nombre');
        const productCant = document.getElementById('counter_' + productId).textContent;
        const productPrice = event.target.getAttribute('data-precio');
        const productImage = event.target.getAttribute('data-imagen');
        const productCanMax = event.target.getAttribute('data-cantidadMaxima');

        // Crea un objeto con la información del producto
        const product = {
            id: productId,
            nombre: productName,
            imagen: productImage,
            precio: productPrice,
            cantidad: productCant,
            cantidadMaxima: productCanMax
        };

        // Almacena el objeto producto en la sesión del navegador utilizando localStorage
        const cart = getCart();
        const productIndex = cart.findIndex(item => item.id === productId);

        // valida si el producto está en la sesión
        if (productIndex !== -1) {
            console.log("cantidad Maxima", productCanMax)
            let comparar = parseInt(cart[productIndex].cantidad) + parseInt(productCant)
            console.log(parseInt(cart[productIndex].cantidad))
            console.log(parseInt(productCant))
            console.log(comparar)
            // Si el producto está en el carrito, actualizar su cantidad
            if (productCanMax >= parseInt(cart[productIndex].cantidad) + parseInt(productCant)) {
                cart[productIndex].cantidad = parseInt(cart[productIndex].cantidad) + parseInt(productCant);

                // Título del mensaje de confirmación según la cantidad del producto actualizada
                const titleMessage = parseInt(productCant) === 1 ? `Se agregó ${productCant} unidad` : `Se agregaron ${productCant} unidades más`;

                // Mostrar un mensaje de confirmación
                Swal.fire({
                    icon: 'warning',
                    title: "¡Cantidad actualizada!",
                    text: titleMessage,
                    timer: 2500
                });
                // Actualizar el carrito en el localStorage
                saveCart(cart);
            } else {
                Swal.fire({
                    icon: 'error',
                    title: "¡Stock Completo en carrito!",
                    text: "No puedes agregar mas de este producto al carrito",
                    timer: 2500
                });
            }


            


        } else {


            cart.push(product);
            saveCart(cart);

            // Opcional: Puedes mostrar un mensaje de confirmación o realizar otras acciones aquí
            Swal.fire({
                icon: 'success',
                title: `¡Producto agregado correctamente!`,
                text: `El producto ${productName} se agregó correctamente.`,
                timer: 2500
            });
        }

        // Actualizar la vista del carrito
        updateCartView();
    }
});

// Evento para escuchar los cambios en el localStorage
window.addEventListener('storage', (event) => {
    if (event.key === 'cart') {
        updateCartView();
    }
});

// Inicializar la vista del carrito al cargar la página
updateCartView();