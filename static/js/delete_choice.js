function Delete_Choice(Choice_id) {

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
        var $jquerry_choice = "#Choice_"+Choice_id;
        $($jquerry_choice).css('display','none');
        // Send an AJAX request to the same URL with CSRF token
        $.ajax({
            url: window.location.href,
            method: "POST",
            data: { Choice_To_Delete_id: Choice_id},
            headers: {
                'X-CSRFToken': getCSRFToken()
            }
        });
    }

}
