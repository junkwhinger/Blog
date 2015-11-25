$(function() {
    // delete 버튼 누를 때 알림창 띄우기
    $('#delete').on('click', function() {
        if (!confirm('Do you want to delete, really?')) {
            return false;
        };
    });
});
