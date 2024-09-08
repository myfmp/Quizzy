// Function to get the CSRF token from the cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function uploadFile() {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];
    const csrftoken = getCookie('csrftoken');

    if (!file) {
        alert('Please select a file.');
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    $.ajax({
        url: window.location.href, // Send the request to the current URL
        type: 'POST',
        data: formData,
        processData: false, // Prevent jQuery from processing the data
        contentType: false, // Prevent jQuery from setting the content-type header
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken); // Add CSRF token to the request
        },
        xhr: function () {
            const xhr = new window.XMLHttpRequest();
            xhr.upload.onprogress = function (e) {
                if (e.lengthComputable) {
                    const percentComplete = (e.loaded / e.total) * 100;
                    $('.uploader-modal').css('display','none');
                    $('.modal_loader').css('display','block');
                }
            };
            return xhr;
        },
        success: function (response) {
            
            var currentUrl = window.location.href;
            // Use the current URL to reload content
            $('#jquery_load').load(currentUrl + ' #Questions_body', function() {

                feather.replace();

                // Make the divs inside parentDiv sortable
                $("#Questions_body").sortable({
                    update: function(event, ui) {
    
                    // Update the IDs of each child div according to their new 
    
                    $("#Questions_body .Question").each(function(index) {
                        $(this).attr("id", (index + 1));
                    });
    
    
                    let resultArray = [];
    
                    $('.Question').each(function() {
                        // Get the ID of the current div
                        let divId = $(this).attr('id');
                        
                        // Find the textarea inside this div and get its ID
                        let textareaId = $(this).find('textarea').attr('id');
                        
                        // Extract just the number from the textarea ID
                        let number = textareaId.match(/\d+$/)[0];
                        
                        // Append the div ID and extracted number to the result array
                        resultArray.push([divId, number]);
                    });
    
                    $.ajax({
                        url: window.location.href,
                        method: "POST",
                        data: { New_Questions_Order : JSON.stringify(resultArray) },
                        headers: {
                            'X-CSRFToken': getCSRFToken()
                        }
                    });
    
                    }
                    });   

            });

            $('.modal_loader').css('display','none');
            $('.uploader-modal').css('display','block');
            document.getElementById('status').innerText = 'Upload complete!';
            // Handle success response (e.g., display a message or update the UI)
        },
        error: function (xhr, status, error) {
            $('.modal_loader').css('display','none');
            $('.uploader-modal').css('display','block');
            document.getElementById('status').innerText = 'Upload failed!';
            // Handle error response (e.g., display an error message)
        }
    });
}
