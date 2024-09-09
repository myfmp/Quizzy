// Attach the click event handler to the document (or a specific parent element) and delegate to .cb-value
$(document).on('click', '.cb-value', function() {
    var mainParent = $(this).parent('.toggle-btn');
    
    // Toggle the 'active' class based on the presence of the 'active' class
    if ($(mainParent).hasClass('active')) {
        $(mainParent).removeClass('active');
    } else {
        $(mainParent).addClass('active');
    }
});

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

function Change_Truth_Statement(Choice_id){

    var Choice_jquerry_id = '#Choice_'+Choice_id;
    var Choice_input_jquerry_id = '#Choice_input_'+Choice_id;
    var Truth_Value = $(Choice_input_jquerry_id).prop('checked');

        // Send an AJAX request to the same URL with CSRF token
        $.ajax({
            url: window.location.href,
            method: "POST",
            data: { Truth_Value: Truth_Value, Choice_to_update_id: Choice_id },
            headers: {
              'X-CSRFToken': getCSRFToken()
            }
        });
        
        if (Truth_Value===true) {
            $(Choice_jquerry_id).removeClass('false');
            $(Choice_jquerry_id).addClass('true');
        }else{
            $(Choice_jquerry_id).removeClass('true');
            $(Choice_jquerry_id).addClass('false');
        }

}