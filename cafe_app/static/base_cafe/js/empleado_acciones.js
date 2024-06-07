// Asegúrate de que el DOM esté completamente cargado antes de ejecutar el código
document.addEventListener("DOMContentLoaded", function () {

    // Función para abrir el modal y llenar los campos del formulario
    function abrirModal(data) {
        // Abre el modal
        const modal = document.getElementById('empleadoModal');
        modal.style.display = 'block';
        // Llenar los campos del formulario con los datos obtenidos
        document.querySelector('input[name="cedula"]').value = data.empleado_cedula;
        document.querySelector('input[name="nombre"]').value = data.empleado_nombre;
        document.querySelector('input[name="direccion"]').value = data.empleado_direccion;
        document.querySelector('input[name="telefono"]').value = data.empleado_telefono;
        document.querySelector('input[name="rol"]').value = data.empleado_rol;
        document.querySelector('select[name="cafeteria"]').value = data.cafeteria_id;
        document.querySelector('input[name="correo"]').value = data.correo;
        document.querySelector('input[name="contrasena"]').value = data.contrasena;
        document.querySelector('input[name="usuario"]').value = data.usuario;
        document.querySelector('h2[id="titulo_modal_empleado"]').textContent = "Actualizar Empleado";
        document.querySelector('.actualizarEmpleao').textContent = "Actualizar Empleado";
  
    }




    // Obtener todos los elementos con la clase 'actualizar_categoria'
    var elementos = document.querySelectorAll('.actualizar_empleado');
    console.log(elementos)
    // Iterar sobre los elementos encontrados
    elementos.forEach(function (elemento) {
        // Agregar un event listener para el evento 'click' a cada elemento
        elemento.addEventListener('click', function () {
            // Obtener el valor del atributo 'data-id' del elemento clickeado
            var id = this.getAttribute('data-idEmpleado');
            console.log(id);

            // Realizar la solicitud fetch
            fetch("http://127.0.0.1:8000/admin_cafe/buscarEmpleado/" + id, {
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
const formsEliminar = document.querySelectorAll('.form_eliminar_empleado');

formsEliminar.forEach((form) => {
    form.addEventListener('submit', function (event) {
        event.preventDefault(); // Evita que el formulario se envíe automáticamente

        // Muestra un SweetAlert de confirmación
        Swal.fire({
            title: "¿Estás seguro?",
            text: "Se eliminará un empleado",
            icon: "warning",
            showCancelButton: true,
            confirmButtonColor: "#3085d6",
            cancelButtonColor: "#d33",
            confirmButtonText: "Sí, Elimiar",
            dangerMode: true,
        }).then((result) => {
            if (result.isConfirmed) {
                // Si el usuario confirma, envía el formulario
                Swal.fire("Empleado eliminado!", {
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
