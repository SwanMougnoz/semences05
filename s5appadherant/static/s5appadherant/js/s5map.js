$.fn.s5map = function(options) {
    var config = $.extend({
        jardins: [],
        popupTemplate: "#popup-template",
        detailUrl: "s5api:map_jardin_detail",
        cultureUrl: "s5api:map_culture_list",
        provider: "http://{s}.tile.osm.org/{z}/{x}/{y}.png",
        loadingText: "Loading..."
    }, options);

    return $(this).each(function() {
        var self = this;
        var map, markers = [];

        var bindPopup = function(marker, jardin) {
            marker.bindPopup(config.loadingText);
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
                })

            });
        };

        var addMarker = function(jardin) {
            var coords = [
                jardin.adresse.latitude,
                jardin.adresse.longitude
            ];

            var marker = L.marker(coords).addTo(map);
            bindPopup(marker, jardin);
            markers.push(marker);
        };

        var instanciate = function() {
            map = L.map(self);
            L.tileLayer(config.provider).addTo(map);
        };

        var populate = function() {
            $(config.jardins).each(function(i, jardin) {
                addMarker(jardin)
            });
        };

        var fit = function() {
            var group = new L.featureGroup(markers);
            map.fitBounds(group.getBounds());
        };

        var init = function() {
            instanciate();
            populate();
            fit()
        };

        init();
    });
};