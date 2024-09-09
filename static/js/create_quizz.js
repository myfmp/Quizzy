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

function Create_New_Quizz() {

 var Title = $("#title_for_new_quizz").val();

 if (Title && Title.trim() !== "") {

    // Send an AJAX request to the same URL with CSRF token
    $.ajax({
        url: window.location.href,
        method: "POST",
        data: { New_Quizz_Title: Title },
        headers: {
          'X-CSRFToken': getCSRFToken()
        },
        success: function(response) {
            if ('URL' in response) {
                window.location.href = "/editor?session="+response.URL;
            }
        }
      });

 }else{
    alert('Please enter a title.')
 }

}