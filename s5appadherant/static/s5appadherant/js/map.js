$(document).ready(function() {
    var $map = $('#adherant-map');

    $.ajax({
        method: 'GET',
        url: Urls['s5api:map_jardin_list'](),
        dataType: 'json',
        success: function(data) {
            $map.s5map({
                jardins: data
            });
        }
    });

    $("#map-extend").on('click', function() {
        $map.toggleClass('extended');
    })
});