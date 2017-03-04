$(document).ready(function() {
    $.ajax({
        method: 'GET',
        url: Urls['s5api:map_jardin_list'](),
        dataType: 'json',
        success: function(data) {
            $('#vitrine-map').s5map({
                jardins: data
            });
        }
    });
});