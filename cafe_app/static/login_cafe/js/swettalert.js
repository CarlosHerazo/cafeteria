document.getElementById("loginForm").addEventListener("submit", function(event) {
    event.preventDefault();  

    // Obtener el valor del token CSRF del documento
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    const formData = new FormData(this);

    // Realiza una petición tipo fetch al endpoint de confirmación de login
    fetch("/confirm_login/", {
        method: "POST",
        body: formData
    })
    .then(response => response.json()) // Convierte la respuesta a formato JSON
    .then(data => {
        // Verifica si hay un mensaje de error y muestra una alerta si es necesario
        if (data.mensaje_error) {
            Swal.fire({
                title: 'Error!',
                text: data.mensaje_error,
                icon: 'error',
                confirmButtonText: 'Ok'
            });
        } else {
            console.log(data)
            rol = data.usuario
            window.location.href = "/inicio/?rol=" + rol;
        }
    })
    .catch(error => {
        console.error("Error:", error);
        Swal.fire({
            title: 'Error!',
            text: 'Hubo un error al procesar la solicitud. Por favor, intenta de nuevo más tarde.',
            icon: 'error',
            confirmButtonText: 'Ok'
        });
    });
});
