$(document).ready(function() {
    var map = L.map('vitrine-map');
    L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png').addTo(map);

    var markers = [];

    var renderTemplate = function(selector, context) {
        var source = $(selector).html();
        var template = Handlebars.compile(source);
        return template(context);
    };

    Handlebars.registerHelper('s5link', function(name, args, content) {
        if (!$.isArray(args)) {
            args = [args]
        }
        var url = Urls[name].apply(this, args);

        return new Handlebars.SafeString(
            '<a href="'+ url +'">' + content + '</a>'
        );
    });

    var bindPopup = function(marker, jardin) {
        marker.bindPopup("Loading...");
        marker.on('click', function (e) {
            var popup = e.target.getPopup();
            $.ajax({
                method: 'GET',
                url: Urls['s5api:map_jardin_detail'](jardin.id),
                dataType: 'json',
                success: function (data) {
                    popup.setContent(renderTemplate("#popup-template", {
                        jardin: data
                    }));
                    popup.update();
                }
            });
        });
    };

    var addMarker = function(index, jardin) {
        var coords = [
            jardin.adresse.latitude,
            jardin.adresse.longitude
        ];

        var marker = L.marker(coords).addTo(map);
        bindPopup(marker, jardin);
        markers.push(marker);
    };

    $.ajax({
        method: 'GET',
        url: Urls['s5api:map_jardin_list'](),
        dataType: 'json',
        success: function(data) {
            $(data).each(addMarker);
            var group = new L.featureGroup(markers);
            map.fitBounds(group.getBounds());
        }
    });
});