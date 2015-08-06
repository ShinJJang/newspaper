function append_comment(target, data, is_prepend, depth) {
     $.each(data, function(i, comment) {
        var dom_data = "<li class='list-group-item'><div class='depth-" + depth + "'>" +
                        "<h4>" + comment.writer.username + "  <small>" + comment.pub_date + "</small></h4>" +
                        "<h5>" + comment.content + "</h5></div></li>";

        if (is_prepend) {
            target = target.prepend(dom_data);
        } else {
            target = target.append(dom_data);
        }
        if (comment.childs.length > 0) {
            append_comment(target, comment.childs, false, ++depth);
        }
     });
}

function wrap_comment_poll() {
    comment_poll();
    setInterval(function () {
        comment_poll();
    }, 5000);
}

function comment_poll() {
    $.ajax({
        url: "/api/v1/comment/?format=json&thread__id=" + thread_id + "&parent_comment__isnull=true",
        success: function (data) {
            $('.comment_wrapper').html("");
            append_comment($('.comment_wrapper'), data.objects, true, 0);
            apply_style_by_depth();
        }, dataType: "json"});
}

$( document ).ready(function() {
    wrap_comment_poll();
});

function apply_style_by_depth() {
    var default_margin = 20;
    var colors = ["#67CEFF", "#41E8CB", "#54FF89", "#6DE841", "#EDFF47"];
    $.each($("div[class*='depth-']"), function (i, item) {
        var depth_num = item.className.split('-')[1];
        $(item).css('margin-left',  default_margin*depth_num + 'px');
        $(item).css('border-left',  "5px solid " +colors[depth_num % 5]);
    });
}

