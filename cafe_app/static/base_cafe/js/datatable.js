
// inventario
$(document).ready(function () {
    var table = $('#inventario').DataTable({
        "columnDefs": [
            { "searchable": false, "targets": [0, 3, 4, 5, 6] } // Desactiva la búsqueda en las columnas 0,3, 4,5,6,7
        ],
        "language": {
            "url": "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Spanish.json",
            "search": "Buscar Producto",
        }
    });
});

$(document).ready(function () {
    var table = $('#historial').DataTable({
        "columnDefs": [
            { "searchable": false, "targets": [0, 1, 2, 4, 5, 6] } // Desactiva la búsqueda en las columnas 0,3, 4,5,6,7
        ],
        "language": {
            "url": "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Spanish.json",
            "search": "Buscar por ID de compra",
        }

    });

    // Capturar el evento de búsqueda en tiempo real
    $('#dt-search-0').on('keyup', function () {
        var searchTerm = $(this).val();
        console.log('Valor de búsqueda:', searchTerm);
        // Aquí puedes hacer lo que necesites con el valor de búsqueda
    });
});


