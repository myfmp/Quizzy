function Change_Choice_Content(Choice_id) {
    
    var $choicebutton = "#choice_button_" + Choice_id;
    var $save_text = "#choice_button_" + Choice_id + " .save-text";
    var $loader = "#choice_button_" + Choice_id + " .custom-loader";

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
   
        var $choice_selector = "#choice_content_" + Choice_id;
        var Choice_Content = $($choice_selector).val();  

        if (Choice_Content && Choice_Content.trim() !== "") {

        // Send an AJAX request to the same URL with CSRF token
        $.ajax({
            url: window.location.href,
            method: "POST",
            data: { Updated_Choice_Content: Choice_Content, Choice_to_update_Id: Choice_id },
            headers: {
              'X-CSRFToken': getCSRFToken()
            }
        });

        $($save_text).css("display", "none");
        $($loader).css("display", "block");

        setTimeout(function() {
            $($choicebutton).slideUp(300); 
            $($loader).css("display", "none");  
            $($save_text).css("display", "block");
        }, 2000);

        }else{
            alert('Please enter a title.')
        }

}

