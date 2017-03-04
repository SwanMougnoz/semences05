Handlebars.registerHelper('namedlink', function (name, args, content) {
    if (!$.isArray(args)) {
        args = [args]
    }
    var url = Urls[name].apply(this, args);

    return new Handlebars.SafeString(
        '<a href="' + url + '">' + content + '</a>'
    );
});

var renderTemplate = function(selector, context) {
    var source = $(selector).html();
    var template = Handlebars.compile(source);
    return template(context);
};

HbUtils = {
    render: renderTemplate
};