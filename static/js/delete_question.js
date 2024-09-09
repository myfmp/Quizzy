function Delete_Question() {

    function getCSRFToken() {
        var csrfToken = null;
        document.cookie.split(';').forEach(function(cookie) {
            var parts = cookie.split('=');
            if (parts[0].trim() == 'csrftoken') {
            csrfToken = parts[1].trim();
            }
        });
        return csrfToken;
    }

    if (confirm("Click 'OK' to continue.")) {
        var urlParams = new URLSearchParams(window.location.search);
        var Question_id  = urlParams.get('question_id');
        var $jquerry_question = ".question_id_"+Question_id;
        $($jquerry_question).css('display','none');
        // Send an AJAX request to the same URL with CSRF token
        $.ajax({
            url: window.location.href,
            method: "POST",
            data: { Question_To_Delete_Id: Question_id},
            headers: {
                'X-CSRFToken': getCSRFToken()
            }
        });
        $("#customMenu").hide();
    }

}