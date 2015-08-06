$(".time_presentation").each(function (i) {
    var locale_time = moment($(this).text()).startOf("hour").fromNow();
    $(this).html(locale_time);
});
