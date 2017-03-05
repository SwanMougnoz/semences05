JardinHandler = function(store, resource, options) {

    var config = $.extend({
        resourceUrl: "s5api:map_jardin_list",
        popupTemplate: "#popup-template",
        detailUrl: "s5api:map_jardin_detail",
        jardinIcon: '/static/s5appadherant/images/jardin-icon.png',
        cultureUrl: "s5api:map_culture_list"
    }, options);

    var retrieve = function() {
        var deferred = $.Deferred();

        $.ajax({
            method: 'GET',
            url: Urls[config.resourceUrl](),
            dataType: 'json',
            success: function(data) {
                store[resource] = data;
                deferred.resolve();
            }
        });

        return deferred;
    };

    var render = function(s5map) {
        $(store[resource]).each(function() {
            var jardin = this;

            var bindPopup = function(marker) {
                s5map.addPopup(marker, {
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

            var coords = [
                jardin.adresse.latitude,
                jardin.adresse.longitude
            ];

            s5map.addMarker(coords, {
                icon: L.icon({
                    iconUrl: config.jardinIcon,
                    iconSize: [38, 38],
                    popupAnchor: [0, -10]
                })
            }, bindPopup)
        });
    };

    return {
        retrieve: retrieve,
        render: render
    }
};