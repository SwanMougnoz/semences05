$(document).ready(function() {
    var $addButton = $("#add-variete-btn");
    var $fields = $("#add-variete-fields");
    var $varieteField = $("#id_variete");

    $addButton.on("click", function() {
        if ($fields.hasClass("hidden")) {
            $fields.removeClass("hidden");
            $addButton.find("i")
                .removeClass("fa-pencil-square-o")
                .addClass("fa-chevron-up");
            $varieteField.prop("disabled", true).val('');
        } else {
            $fields.addClass("hidden");
            $addButton.find("i")
                .removeClass("fa-chevron-up")
                .addClass("fa-pencil-square-o");
            $varieteField.prop("disabled", false);
        }
    });

    $.datetimepicker.setLocale('fr');
    $('.datepicker').datetimepicker({
        format: 'd/m/Y',
        timepicker: false
    });
});