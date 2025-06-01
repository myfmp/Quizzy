
function Restrict_Quizz() {

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

    var Restricted = $("#inpLock").prop('checked');
    
    if (Restricted == true) {

        // Get the input value
        var new_quizz_password = prompt('Enter a password');

        // Check if user canceled the prompt
        if (new_quizz_password === null) {
            // Uncheck the checkbox and notify the user
            $('#inpLock').prop('checked', false);
            return; // Exit the function
        }

        // Send an AJAX request to the same URL with CSRF token
        if (new_quizz_password !== '') {
            
            // Send an AJAX request to the same URL with CSRF token
            $.ajax({
                url: window.location.href,
                method: "POST",
                data: { Quizz_Password: new_quizz_password},
                headers: {
                    'X-CSRFToken': getCSRFToken()
                },
                success: function(response) { 

                    if ('DATA' in response) {

                        $('#inpLock').prop('checked', true);
                        alert('Access locked')

                    }

                }

            });


        }else{

            $('#inpLock').prop('checked', false);
            alert('Please enter a valid password.')

        }

    }else{

        // Send an AJAX request to the same URL with CSRF token
        $.ajax({
            url: window.location.href,
            method: "POST",
            data: { Quizz_Unlocked: 'true'},
            headers: {
                'X-CSRFToken': getCSRFToken()
            },
            success: function(response) { 

                if ('DATA' in response) {

                    $('#inpLock').prop('checked', false);
                    alert('Access unlocked.')

                }

            }

        });

    }

}
