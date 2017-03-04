$.fn.ajaxPagination = function(resource, options) {

    if (resource === undefined) {
        throw "Pagination impossible, aucunes données fournies";
    }

    var config = $.extend({
        itemTemplate: "#item-template"
    }, options);

    return $(this).each(function() {
        var self = this;
        var $content, $next, $prev, $count;

        var loadComponents = function() {
            $content = $(self).find("[data-pagination-content]");
            $next = $(self).find("[data-pagination-next]");
            $prev = $(self).find("[data-pagination-prev]");
            $count = $(self).find("[data-pagination-count]");
        };

        var bindControl = function($control, url) {
            $control.off('click');

            if (url) {
                $control.prop('disabled', false);
                $control.on('click', fetch(url, update));
            } else {
                $control.prop('disabled', true);
            }
        };

        var bind = function(page) {
            bindControl($next, page.next);
            bindControl($prev, page.previous);
        };

        var update = function(page) {
            $content.html('');
            $(page.results).each(function() {
                var item = HbUtils.render(config.itemTemplate, {
                    data: this
                });
                $content.append(item);
            });
            bind(page);
        };

        var fetch = function(url, callback) {
            if (url) {
                return function() {
                    $.ajax({
                        method: 'GET',
                        url: url,
                        dataType: 'json',
                        success: callback
                    });
                };
            }
        };

        var init = function() {
            loadComponents();
            fetch(resource, function(page) {
                update(page);
                $count.html(page.count);
            })();
        };

        init();
    });
};