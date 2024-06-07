// Asegúrate de que el DOM esté completamente cargado antes de ejecutar el código
document.addEventListener("DOMContentLoaded", function () {

    // Función para abrir el modal y llenar los campos del formulario
    function abrirModal(data) {
        // Abre el modal
        const modal = document.getElementById('descuentoModal');
        modal.style.display = 'block';
        // Llenar los campos del formulario con los datos obtenidos
        document.querySelector('input[name="tipo_descuento"]').value = data.tipo_descuento;
        document.querySelector('input[name="desc"]').value = data.descuento;
        document.querySelector('input[name="descuento_id"]').value = data.id;
        document.querySelector('h2[id="titulo_modal_descuento"]').textContent = "Actualizar Descuento";
        document.querySelector('.actualizarDescuento').textContent = "Actualizar Descuento";
  
    }




    // Obtener todos los elementos con la clase 'actualizar_categoria'
    var elementos = document.querySelectorAll('.actualizar_descuento');
    console.log(elementos)
    // Iterar sobre los elementos encontrados
    elementos.forEach(function (elemento) {
        // Agregar un event listener para el evento 'click' a cada elemento
        elemento.addEventListener('click', function () {
            // Obtener el valor del atributo 'data-id' del elemento clickeado
            var id = this.getAttribute('data-descuentoId');
            console.log(id);

            // Realizar la solicitud fetch
            fetch("http://127.0.0.1:8000/productos/buscar_descuento/" + id, {
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
const formsEliminar = document.querySelectorAll('.form_eliminar_descuento');

formsEliminar.forEach((form) => {
    form.addEventListener('submit', function (event) {
        event.preventDefault(); // Evita que el formulario se envíe automáticamente

        // Muestra un SweetAlert de confirmación
        Swal.fire({
            title: "¿Estás seguro?",
            text: "Se eliminará un descuento",
            icon: "warning",
            showCancelButton: true,
            confirmButtonColor: "#3085d6",
            cancelButtonColor: "#d33",
            confirmButtonText: "Sí, Elimiar",
            dangerMode: true,
        }).then((result) => {
            if (result.isConfirmed) {
                // Si el usuario confirma, envía el formulario
                Swal.fire("Descuento eliminado!", {
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
