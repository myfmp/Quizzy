function Change_Question_Content(Question_id) {
    
    var $questionbutton = "#question_button_" + Question_id;
    var $save_text = "#question_button_" + Question_id + " .save-text";
    var $loader = "#question_button_" + Question_id + " .custom-loader";

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
   
        var $question_selector = "#question_content_" + Question_id;
        var Question_Content = $($question_selector).val();  

        if (Question_Content && Question_Content.trim() !== "") {

        // Send an AJAX request to the same URL with CSRF token
        $.ajax({
            url: window.location.href,
            method: "POST",
            data: { Update_Question_Content: Question_Content, Question_to_update_Id: Question_id },
            headers: {
              'X-CSRFToken': getCSRFToken()
            }
        });

        $($save_text).css("display", "none");
        $($loader).css("display", "block");

        setTimeout(function() {
            $($questionbutton).slideUp(300); 
            $($loader).css("display", "none");  
            $($save_text).css("display", "block");
        }, 2000);

        }else{
            alert('Please enter a title.')
        }

}
