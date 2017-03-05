AdherantHandler = function(store, resource, options) {

    var config = $.extend({
        resourceUrl: "s5api:adherant_list",
        popupTemplate: "#popup-template",
        detailUrl: "s5api:adherant_detail",
        icon: '/static/s5appadherant/images/adherant-icon.png'
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
            var adherant = this;

            var bindPopup = function(marker) {
                s5map.addPopup(marker, {
                    keepInView: true
                });
                marker.on('click', function(e) {
                    var popup = e.target.getPopup();

                    $.ajax({
                        method: 'GET',
                        url: Urls[config.detailUrl](adherant.id),
                        dataType: 'json',
                        success: function(data) {
                            popup.setContent(HbUtils.render(config.popupTemplate, {
                                adherant: data
                            }));
                            popup.update();
                        }
                    });
                });
            };

            var coords = [
                adherant.adresse.latitude,
                adherant.adresse.longitude
            ];

            s5map.addMarker(coords, {
                icon: L.icon({
                    iconUrl: config.icon,
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