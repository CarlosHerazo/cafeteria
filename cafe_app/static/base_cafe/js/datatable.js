
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

// histoiral

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
});

// categoria
$(document).ready(function () {
    var table = $('#categoria').DataTable({
        "columnDefs": [
            { "searchable": false, "targets": [0] } // Desactiva la búsqueda en las columnas 0,3, 4,5,6,7
        ],
        "language": {
            "url": "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Spanish.json",
            "search": "Buscar por categorias",
        }

    });

});


// descuento
$(document).ready(function () {
    var table = $('#descuento').DataTable({
        "columnDefs": [
            { "searchable": false, "targets": [0] } // Desactiva la búsqueda en las columnas 0,3, 4,5,6,7
        ],
        "language": {
            "url": "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Spanish.json",
            "search": "Buscar tipo de descuento",
        }

    });

});

// empleados
$(document).ready(function () {
    var table = $('#empleados').DataTable({
        "columnDefs": [
            { "searchable": false, "targets": [0] } // Desactiva la búsqueda en las columnas 0,3, 4,5,6,7
        ],
        "language": {
            "url": "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Spanish.json",
            "search": "Buscar por cedula",
        }

    });

});





