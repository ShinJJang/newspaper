function valid_test (data) {
    return /<[a-z][\s\S]*>/i.test(data);
}