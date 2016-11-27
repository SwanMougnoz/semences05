$(document).ready(function() {
    var map = L.map('vitrine-map').setView([44.651369, 6.184484], 9);
    L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png').addTo(map);

    // Marker d'exemple
    L.marker([44.899288, 6.645442]).addTo(map);
    L.marker([44.914185, 6.403659]).addTo(map);
    L.marker([44.796908, 6.566301]).addTo(map);
    L.marker([44.561624, 6.081014]).addTo(map);
});