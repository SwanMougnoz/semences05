$(document).ready(function() {
    var $map = $('#adherant-map');
    var mapStore = {};

    $map.map({
        handlers: [
            JardinHandler(mapStore, 'jardins'),
            AdherantHandler(mapStore, 'adherants', {
                'popupTemplate': '#popup-adherant'
            })
        ]
    });

    $("#map-extend").on('click', function() {
        $map.toggleClass('extended');
    });
});