$(document).ready(function() {
    var map = L.map('vitrine-map').setView([44.651369, 6.184484], 9);
    L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png').addTo(map);
});