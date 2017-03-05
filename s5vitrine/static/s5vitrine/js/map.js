$(document).ready(function() {
    var $map = $('#vitrine-map');
    var mapStore = {};

    $map.map({
        handlers: [
            JardinHandler(mapStore, 'jardins')
        ]
    });
});