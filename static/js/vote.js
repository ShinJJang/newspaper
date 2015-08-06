function vote(node) {
    var thread_id = node.attr("href").split('\/')[2];
    $.ajax({
        url: node.attr("href"),
        dataType: "json",
        success: function(data) {
            $("#vote_count_"+thread_id).html(data.count);
        },
        error: function(data) {
            alert(data.responseJSON.error_message);
        }
    });
}

$("a.vote").on("click", function() {
    vote($(this));
    return false;
});
