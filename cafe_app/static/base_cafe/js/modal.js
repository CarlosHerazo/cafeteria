// Función para abrir el modal
const btn = document.getElementById('abrirModal');
btn.addEventListener('click', function() {
    openModal();
});

// Función para cerrar el modal
const btn2 = document.getElementById('cerrarModal');
btn2.addEventListener('click', closeModal);
function openModal() {
    document.getElementById('miModal').style.display = 'block';
    console.log("abrir");
  }
  
  // Función para cerrar el modal
  function closeModal() {

   
     // Llenar los campos del formulario con los datos obtenidos
     document.querySelector('input[name="producto_id"]').value = "";
     document.querySelector('input[name="nombre"]').value = "";
     document.querySelector('input[name="precio"]').value = "";
     document.querySelector('textarea[name="descripcion"]').value = "";
     // document.querySelector('input[name="imagen"]').value = data.imagen;  // Ajusta según cómo manejes la imagen
     document.querySelector('input[name="cantidad"]').value ="";
     document.querySelector('select[name="cafeteria"]').value = "";
     document.querySelector('select[name="categoria"]').value = "";
     document.querySelector('h2[id="titulo_modal"]').textContent = "Agregar Producto";
     document.querySelector('button[class="btn-actualizar"]').textContent = "Agregar Producto";


      // Mostrar la imagen actual y llenar el campo oculto con la URL
     const imagenActual = document.getElementById('imagen_actual');
     const imagenActualUrl = document.getElementById('imagen_actual_url');
     imagenActual.src = "";
     imagenActualUrl.value = "";
     document.getElementById('miModal').style.display = 'none';
  }
  
  // Cierra el modal si el usuario hace clic fuera de él
  window.onclick = function(event) {
    var modal = document.getElementById('miModal');
    if (event.target == modal) {
      modal.style.display = "none";
    }
  }