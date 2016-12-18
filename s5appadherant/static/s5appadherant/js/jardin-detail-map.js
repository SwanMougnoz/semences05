$(document).ready(function() {

    var $mapElement = $("#jardin-detail-map");
    var latitude = $mapElement.data('latitude');
    var longitude = $mapElement.data('longitude');

    if (!latitude || !longitude) {
        throw "Impossible d'afficher la position du jardin : latitude ou longitude non fournis";
    }

    var map = L.map('jardin-detail-map').setView([latitude, longitude], 12);
    L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png').addTo(map);
    L.marker([latitude, longitude]).addTo(map);
});