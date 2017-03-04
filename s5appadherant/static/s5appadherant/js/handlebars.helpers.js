Handlebars.registerHelper('namedUrl', function (name, args) {
    if (!$.isArray(args)) {
        args = [args]
    }
    var url = Urls[name].apply(this, args);

    return new Handlebars.SafeString(url);
});

var renderTemplate = function(selector, context) {
    var source = $(selector).html();
    var template = Handlebars.compile(source);
    return template(context);
};

HbUtils = {
    render: renderTemplate
};