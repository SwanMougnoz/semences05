$(document).ready(function() {
    var map = L.map('vitrine-map');
    L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png').addTo(map);

    var markers = [];

    var addMarker = function(index, jardin) {
        var coords = [
            jardin.adresse.latitude,
            jardin.adresse.longitude
        ];
        var marker = L.marker(coords).addTo(map);
        markers.push(marker);
    };

    $.ajax({
        method: 'GET',
        url: Urls['s5api:map_jardin_list'](),
        dataType: 'json',
        success: function(data) {
            $(data).each(addMarker);
            var group = new L.featureGroup(markers);
            map.fitBounds(group.getBounds());
        }
    });
});