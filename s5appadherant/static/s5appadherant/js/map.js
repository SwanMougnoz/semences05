$(document).ready(function() {
    $.ajax({
        method: 'GET',
        url: Urls['s5api:map_jardin_list'](),
        dataType: 'json',
        success: function(data) {
            $('#adherant-map').s5map({
                jardins: data
            });
        }
    });
});