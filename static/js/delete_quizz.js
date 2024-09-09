function Delete_Quizz() {

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
        
        // Send an AJAX request to the same URL with CSRF token
        $.ajax({
            url: window.location.href,
            method: "POST",
            data: { Delete_Quizz: "True"},
            headers: {
                'X-CSRFToken': getCSRFToken()
            },
            success: function(response) { 

                if ('DATA' in response) {

                    window.location.href = "/dashboard";

                }

            }

        });

    }

}