// Asegúrate de que el DOM esté completamente cargado antes de ejecutar el código
document.addEventListener("DOMContentLoaded", function () {

    // Función para abrir el modal y llenar los campos del formulario
    function abrirModal(data) {
        // Abre el modal
        const modal = document.getElementById('miModal');
        modal.style.display = 'block';

        // Llenar los campos del formulario con los datos obtenidos
        document.querySelector('input[name="producto_id"]').value = data.id;
        document.querySelector('input[name="nombre"]').value = data.nombre;
        document.querySelector('input[name="precio"]').value = data.precio;
        document.querySelector('textarea[name="descripcion"]').value = data.descripcion;
        // document.querySelector('input[name="imagen"]').value = data.imagen; 
        document.querySelector('input[name="cantidad"]').value = String(data.cantidad);
        document.querySelector('select[name="cafeteria"]').value = String(data.cafeteria);
        document.querySelector('select[name="categoria"]').value = String(data.categoria);
        document.querySelector('h2[id="titulo_modal"]').textContent = "Actualizar Producto";
        document.querySelector('button[class="btn-actualizar"]').textContent = "Actualizar Producto";

         // Mostrar la imagen actual y llenar el campo oculto con la URL
        const imagenActual = document.getElementById('imagen_actual');
        const imagenActualUrl = document.getElementById('imagen_actual_url');
        imagenActual.src = data.imagen;
        imagenActualUrl.value = data.imagen;
   
        
    }
    // Mostrar previsualización de la imagen


    // Cerrar el modal al hacer clic en el botón "Cancelar"
    document.getElementById('cerrarModal').addEventListener('click', function () {
        const modal = document.getElementById('miModal');
        modal.style.display = 'none';
    });

    // Obtener todos los elementos con la clase 'actualizar_producto'
    var elementos = document.querySelectorAll('.actualizar_producto');

    // Iterar sobre los elementos encontrados
    elementos.forEach(function (elemento) {
        // Agregar un event listener para el evento 'click' a cada elemento
        elemento.addEventListener('click', function () {
            // Obtener el valor del atributo 'data-id' del elemento clickeado
            var id = this.getAttribute('data-id');
            console.log(id);

            // Realizar la solicitud fetch
            fetch("http://127.0.0.1:8000/productos/buscar_producto/" + id, {
                method: 'GET', // Método HTTP
                headers: {
                    'Content-Type': 'application/json', // Tipo de contenido
                },
            })
                .then(function (response) {
                    // Verificar si la respuesta fue exitosa
                    if (!response.ok) {
                        throw new Error('Hubo un problema con la solicitud.');
                    }
                    // Si la respuesta es exitosa, retornar el cuerpo de la respuesta como JSON
                    return response.json();
                })
                .then(function (data) {
                    // Aquí puedes manejar la respuesta del servidor
                    console.log('Respuesta del servidor:', data);
                    // Abrir el modal y llenar los campos del formulario con los datos obtenidos
                    abrirModal(data);
                })
                .catch(function (error) {
                    // Capturar y manejar errores
                    console.error('Error:', error);
                });
        });
    });

   // Manejo del formulario de eliminación para cada formulario presente en la página
const formsEliminar = document.querySelectorAll('.form_eliminar_categoria');

formsEliminar.forEach((form) => {
    form.addEventListener('submit', function (event) {
        event.preventDefault(); // Evita que el formulario se envíe automáticamente

        // Muestra un SweetAlert de confirmación
        Swal.fire({
            title: "¿Estás seguro?",
            text: "Se eliminará la categoria",
            icon: "warning",
            buttons: true,
            dangerMode: true,
        })
        .then((willSubmit) => {
            if (willSubmit) {
                // Si el usuario confirma, envía el formulario
                Swal.fire("Producto eliminado!", {
                    icon: "success",
                }).then(() => {
                    form.submit(); // Envía el formulario después de mostrar el SweetAlert de éxito
                });
            } else {
                // Si el usuario cancela, no hace nada
                return false;
            }
        });
    });
});


});
