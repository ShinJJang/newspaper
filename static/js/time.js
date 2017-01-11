$(".time_presentation").each(function (i) {
    var locale_time = moment($(this).text(), moment.ISO_8601).locale('ko').fromNow();
    $(this).html(locale_time);
});
