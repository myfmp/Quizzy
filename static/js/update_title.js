function Change_Title () {

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

        var Title = $("#quizz_title").text();

        if (Title && Title.trim() !== "") {

        // Send an AJAX request to the same URL with CSRF token
        $.ajax({
            url: window.location.href,
            method: "POST",
            data: { Update_Quizz_Title: Title },
            headers: {
              'X-CSRFToken': getCSRFToken()
            }
        });

        $("#title_button .save-text").css("display", "none");
        $("#title_button .custom-loader").css("display", "block");

        setTimeout(function() {
            $('#title_button').slideUp(300); 
            $("#title_button .custom-loader").css("display", "none");
            $("#title_button .save-text").css("display", "block");
        }, 2000);    

        }else{
            alert('Please enter a title.')
        }

}
