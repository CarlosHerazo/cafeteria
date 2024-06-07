document.addEventListener("DOMContentLoaded", function () {
  const form = document.querySelector('#formProducto');
  form.addEventListener('submit', function (event) {
    event.preventDefault(); // Evita que el formulario se envíe automáticamente

    // Muestra un SweetAlert de confirmación
    Swal.fire({
      title: "¿Estás seguro de registrar el producto?",
      text: "Una vez registrado, Podra hacer ventas con el.",
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
      text: "Una vez registrado, se agregara a la lista de categorias.",
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




document.addEventListener("DOMContentLoaded", function () {
  const form = document.querySelector('#formEmpleado');
  form.addEventListener('submit', function (event) {
    event.preventDefault(); // Evita que el formulario se envíe automáticamente

    // Muestra un SweetAlert de confirmación
    // Muestra un SweetAlert de confirmación
    Swal.fire({
      title: "¿Estás seguro de registrar al Empleado?",
      text: "Una vez registrado, podra acceder al sistema",
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: "#3085d6",
      cancelButtonColor: "#d33",
      confirmButtonText: "Sí, registrar",
      cancelButtonText: "Cancelar",
    }).then((result) => {
      if (result.isConfirmed) {
        // Si el usuario confirma, envía el formulario
        Swal.fire("!Empleado registrado!", {
          icon: "success",
        }).then(() => {
          form.submit(); 
        });
      } else {
        // Si el usuario cancela, no hace nada
        return false;
      }
    });
  });
});



document.addEventListener("DOMContentLoaded", function () {
  const form = document.querySelector('#formDescuento');
  form.addEventListener('submit', function (event) {
    event.preventDefault(); // Evita que el formulario se envíe automáticamente

    // Muestra un SweetAlert de confirmación
    // Muestra un SweetAlert de confirmación
    Swal.fire({
      title: "¿Estás seguro de registrar el Descuento?",
      text: "Una vez registrado, se agregara a el menu de opciones de pago",
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: "#3085d6",
      cancelButtonColor: "#d33",
      confirmButtonText: "Sí, registrar",
      cancelButtonText: "Cancelar",
    }).then((result) => {
      if (result.isConfirmed) {
        // Si el usuario confirma, envía el formulario
        Swal.fire("!Descuento registrado!", {
          icon: "success",
        }).then(() => {
          form.submit(); 
        });
      } else {
        // Si el usuario cancela, no hace nada
        return false;
      }
    });
  });
});


