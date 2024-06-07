

// Función para abrir el modal de categoría
const btnCategoria = document.getElementById('abrirModalEmpleado');
btnCategoria.addEventListener('click', function () {
  openModal('empleadoModal');
});

// Seleccionar todos los botones de cerrar para el modal de categoría
const btnCerrarCategoria = document.querySelectorAll('#cerrarModal');
btnCerrarCategoria.forEach(btn => {
  btn.addEventListener('click', function () {
    closeModal('empleadoModal');
  });
});



// Función para abrir un modal dado su ID
function openModal(modalId) {
  document.getElementById(modalId).style.display = 'block';
      // Llenar los campos del formulario con los datos obtenidos
      document.querySelector('input[name="nombre"]').value = "";
      document.querySelector('input[name="categoria_id"]').value = "";
      document.querySelector('h2[id="titulo_modal_categoria"]').textContent = "Nueva Categoria";
      document.querySelector('.btn-actualizar').textContent = "Agregar Categoria"; 
}

// Función para cerrar un modal dado su ID
function closeModal(modalId) {
  document.getElementById(modalId).style.display = 'none';
}

// Cierra el modal si el usuario hace clic fuera de él
window.onclick = function (event) {
  // Obtiene los modales
  const modalCategoria = document.getElementById('categoriaModal');

  // Cierra el modal de categoría si se hace clic fuera
  if (event.target == modalCategoria) {
    closeModal('empleadoModal');
  }

}
