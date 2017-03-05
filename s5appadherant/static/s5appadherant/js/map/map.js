$.fn.map = function(options) {
    var config = $.extend({
        popupLoading: "Chargement...",
        provider: "http://{s}.tile.osm.org/{z}/{x}/{y}.png",
        handlers: []
    }, options);

    return $(this).each(function() {
        var self = this;
        var map, markers;

        self.addMarker = function(coords, options, configureFn) {
            var marker = L.marker(coords, options);
            if (configureFn) {
                configureFn(marker);
            }
            markers.addLayer(marker);
        };

        self.addPopup = function(marker, options, configureFn) {
            var popup = marker.bindPopup(config.popupLoading, options);
            if (configureFn) {
                configureFn(popup);
            }
        };

        var instanciate = function() {
            markers = L.markerClusterGroup();
            map = L.map(self);
            L.tileLayer(config.provider).addTo(map);
        };

        var populate = function() {
            var processedHandlers = [];

            $(config.handlers).each(function(i, handler) {
                var d = $.Deferred();
                processedHandlers.push(d);

                handler.retrieve().then(function() {
                    handler.render(self);
                    d.resolve();
                });
            });

            $.when.apply($, processedHandlers).then(function() {
                map.addLayer(markers);
                render();
            });
        };

        var render = function() {
            map.fitBounds(markers.getBounds());
        };

        var init = function() {
            instanciate();
            populate();
        };

        init();
    });
};