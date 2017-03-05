$.fn.s5map = function(options) {
    var config = $.extend({
        jardins: [],
        popupTemplate: "#popup-template",
        detailUrl: "s5api:map_jardin_detail",
        cultureUrl: "s5api:map_culture_list",
        provider: "http://{s}.tile.osm.org/{z}/{x}/{y}.png",
        loadingText: "Loading...",
        jardinIcon: '/static/s5appadherant/images/jardin-icon.png'
    }, options);

    return $(this).each(function() {
        var self = this;
        var map, markers;

        var bindPopup = function(marker, jardin) {
            marker.bindPopup(config.loadingText, {
                keepInView: true
            });
            marker.on('click', function(e) {
                var popup = e.target.getPopup();

                $.ajax({
                    method: 'GET',
                    url: Urls[config.detailUrl](jardin.id),
                    dataType: 'json',
                    success: function(data) {
                        popup.setContent(HbUtils.render(config.popupTemplate, {
                            jardin: data
                        }));
                        popup.update();

                        $(popup._contentNode).find('[data-pagination]').ajaxPagination(
                            Urls[config.cultureUrl](jardin.id),
                            {itemTemplate: "#culture-item"}
                        );
                    }
                });
            });
        };

        var addMarker = function(jardin) {
            var coords = [
                jardin.adresse.latitude,
                jardin.adresse.longitude
            ];

            var marker = L.marker(coords, {
                icon: L.icon({
                    iconUrl: config.jardinIcon,
                    iconSize: [38, 38],
                    popupAnchor: [0, -10]
                })
            });

            bindPopup(marker, jardin);
            markers.addLayer(marker);
        };

        var instanciate = function() {
            markers = L.markerClusterGroup();
            map = L.map(self);
            L.tileLayer(config.provider).addTo(map);
        };

        var populate = function() {
            $(config.jardins).each(function() {
                addMarker(this)
            });
            map.addLayer(markers);
        };

        var fit = function() {
            map.fitBounds(markers.getBounds());
        };

        var init = function() {
            instanciate();
            populate();
            fit()
        };

        init();
    });
};