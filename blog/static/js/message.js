$(function() {
    // 2초 후 message 제거하기
    setTimeout(function() {
        $('#message').slideUp()
    }, 2000);

    $('.close').on('click', function() {
        $('#message').slideUp()
    });
});
