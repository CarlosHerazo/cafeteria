// Para el modal de Categorías

// Función para abrir el modal de categoría
const btnCategoria = document.getElementById('abrirModalCategoria');
btnCategoria.addEventListener('click', function () {
  openModal('categoriaModal');
});

// Seleccionar todos los botones de cerrar para el modal de categoría
const btnCerrarCategoria = document.querySelectorAll('#cerrarModal');
btnCerrarCategoria.forEach(btn => {
  btn.addEventListener('click', function () {
    closeModal('categoriaModal');
  });
});

// Para el modal de Descuentos

// Función para abrir el modal de descuento
const btnDescuento = document.getElementById('abrirModalDescuento');
btnDescuento.addEventListener('click', function () {
  openModal('descuentoModal');

});

// Seleccionar todos los botones de cerrar para el modal de descuento
const btnCerrarDescuento = document.querySelectorAll('#cerrarModal');
btnCerrarDescuento.forEach(btn => {
  btn.addEventListener('click', function () {
    closeModal('descuentoModal');
  });
});

// Función para abrir un modal dado su ID
function openModal(modalId) {
  document.getElementById(modalId).style.display = 'block';
  if (modalId == "descuentoModal") {  
    // Cerrar el modal al hacer clic en el botón "Cancelar"
      document.querySelector('input[name="tipo_descuento"]').value = "";
      document.querySelector('input[name="desc"]').value = 0;
      document.querySelector('input[name="descuento_id"]').value = "";
      document.querySelector('h2[id="titulo_modal_descuento"]').textContent = "Nuevo Descuento";
      document.querySelector('.actualizarDescuento').textContent = "Agregar Descuento";
  }else if (modalId == "categoriaModal") {
      // Llenar los campos del formulario con los datos obtenidos
      document.querySelector('input[name="nombre"]').value = "";
      document.querySelector('input[name="categoria_id"]').value = "";
      document.querySelector('h2[id="titulo_modal_categoria"]').textContent = "Nueva Categoria";
      document.querySelector('.btn-actualizar').textContent = "Agregar Categoria";  
  } 
}

// Función para cerrar un modal dado su ID
function closeModal(modalId) {
  document.getElementById(modalId).style.display = 'none';
}

// Cierra el modal si el usuario hace clic fuera de él
window.onclick = function (event) {
  // Obtiene los modales
  const modalCategoria = document.getElementById('categoriaModal');
  const modalDescuento = document.getElementById('descuentoModal');

  // Cierra el modal de categoría si se hace clic fuera
  if (event.target == modalCategoria) {
    closeModal('categoriaModal');
  }

  // Cierra el modal de descuento si se hace clic fuera
  if (event.target == modalDescuento) {
    closeModal('descuentoModal');
  }
}
