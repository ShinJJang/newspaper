function append_comment(target, data, is_prepend, depth) {
     $.each(data, function(i, comment) {
        var dom_data = "<li class='list-group-item'><div class='depth-" + depth + "'>" +
                        "<h4>" + comment.writer.username +
                        "  <small>" + moment(comment.pub_date).startOf('hour').fromNow() + "</small>" +
                        "  <small><a href='/api/v1/comment/" + comment.id + "/' class='reply'>댓글달기</a></small></h4>" +
                        "<h5>" + comment.content + "</h5></div></li>";

        var next_target;
        if (is_prepend) {
//            next_target = target.prepend(dom_data);
            next_target = $(dom_data).prependTo(target);
        } else {
//            next_target = target.append(dom_data);
            next_target = $(dom_data).appendTo(target);
        }
        if (comment.childs.length > 0) {
            append_comment(next_target, comment.childs, false, depth+1);
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
            move_reply_form();
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

function move_reply_form() {
    $(".reply").on("click", function () {
//        $("#comment-form-wrapper").appendTo($(this).parent().parent().parent().parent());
        if ($("#comment-form input[name='parent-comment']").length > 0) {
            console.log("if");
            $("#comment-form input[name='parent-comment']").val($(this).attr("href"));
        } else {
            console.log("else");
            console.log($("#comment-form"));
            $("#comment-form").append("<input type='hidden' name='parent_comment' value='" + $(this).attr("href") + "'>");
        }
        return false;
    });
}

$("#comment-form").submit(function () {
    var form = $(this).serializeArray();
    var data = {};
    form.forEach(function (item) {
        data[item.name] = item.value;
    });
    data = JSON.stringify(data);
    console.log(data);
    var formURL = $(this).attr("action");
    $.ajax({
        url : formURL,
        contentType: "application/json",
        type: "POST",
        dataType: "json",
        data : data,
        success:function(data, textStatus, jqXHR)
        {
            comment_poll();
            $("#comment-form input[name='content']").val("");
        },
        error: function(jqXHR, textStatus, errorThrown)
        {
            //if fails
        }
    });
    return false;
});
