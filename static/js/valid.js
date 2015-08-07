function valid_test (data) {
    return /<[a-z][\s\S]*>/i.test(data);
}

$("#signup_form").submit(function () {
    var form = $(this).serializeArray();
    var data = {};
    form.forEach(function (item) {
        data[item.name] = item.value;
    });
    data = JSON.stringify(data);
    if (valid_test(data)) {
        alert("정상적인 값을 입력해주세요");
        return false;
    }
});

$("#thread_form").submit(function () {
    var form = $(this).serializeArray();
    var data = {};
    form.forEach(function (item) {
        data[item.name] = item.value;
    });
    data = JSON.stringify(data);
    if (valid_test(data)) {
        alert("정상적인 값을 입력해주세요");
        return false;
    }
});