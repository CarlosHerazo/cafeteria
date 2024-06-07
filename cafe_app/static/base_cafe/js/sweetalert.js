document.addEventListener("DOMContentLoaded", function () {
  const form = document.querySelector('#formProducto');
  form.addEventListener('submit', function (event) {
    event.preventDefault(); // Evita que el formulario se envíe automáticamente

    // Muestra un SweetAlert de confirmación
    // Muestra un SweetAlert de confirmación
    Swal.fire({
      title: "¿Estás seguro de registrar el producto?",
      text: "Una vez registrado, no podrás modificar la información.",
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: "#3085d6",
      cancelButtonColor: "#d33",
      confirmButtonText: "Sí, registrar",
      cancelButtonText: "Cancelar",
    }).then((result) => {
      if (result.isConfirmed) {
        // Si el usuario confirma, envía el formulario
        Swal.fire("¡Producto registrado!", {
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



document.addEventListener("DOMContentLoaded", function () {
  const form = document.querySelector('#formCategoria');
  form.addEventListener('submit', function (event) {
    event.preventDefault(); // Evita que el formulario se envíe automáticamente

    // Muestra un SweetAlert de confirmación
    // Muestra un SweetAlert de confirmación
    Swal.fire({
      title: "¿Estás seguro de registrar la categoria?",
      text: "Una vez registrado, no podrás modificar la información.",
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: "#3085d6",
      cancelButtonColor: "#d33",
      confirmButtonText: "Sí, registrar",
      cancelButtonText: "Cancelar",
    }).then((result) => {
      if (result.isConfirmed) {
        // Si el usuario confirma, envía el formulario
        Swal.fire("!Categoria registrado!", {
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


