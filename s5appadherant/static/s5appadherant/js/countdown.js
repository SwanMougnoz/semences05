$.fn.countDown = function(options) {
    var config = $.extend({
        start: 5,
        redirect: null
    }, options);

    return this.each(function() {
        var self = this;
        var remaining = config.start;

        setInterval(function() {
            remaining--;
            $(self).html(remaining);
            if (remaining == 0) {
                clearInterval(this);
                $(self).trigger("countDown:timeout");
                if (config.redirect) {
                    window.location = config.redirect
                }
            }
        }, 1000);
    });
};