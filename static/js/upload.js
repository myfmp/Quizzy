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
                    $('.uploader-modal').css('display', 'none');
                    $('.modal_loader').css('display', 'block');
                }
            };
            return xhr;
        },
        success: function (response) {
            $.ajax({
                url: window.location.href,
                method: "POST",
                data: { step2: response.DATA },
                headers: { 'X-CSRFToken': getCSRFToken() },
                success: function (response_2) {
                    if ('DATA' in response_2) {
                        $.ajax({
                            url: window.location.href,
                            method: "POST",
                            data: { step3: response_2.DATA },
                            headers: { 'X-CSRFToken': getCSRFToken() },
                            success: function (response_3) {
                                if ('DATA' in response_3) {
                                    let data = response_3.DATA;

                                    // Function to chunk an array into smaller arrays of given size
                                    function chunkArray(arr, chunkSize) {
                                        let chunks = [];
                                        for (let i = 0; i < arr.length; i += chunkSize) {
                                            chunks.push(arr.slice(i, i + chunkSize));
                                        }
                                        return chunks;
                                    }

                                    let chunkedData = chunkArray(data, 20);

                                    // Function to send each chunk sequentially
                                    function sendChunksSequentially(chunks) {
                                        // Check if there are no chunks left to process
                                        if (chunks.length === 0) {
                                            // All chunks have been sent
                                            var currentUrl = window.location.href;

                                            // Load the new content into the UI
                                            $('#jquery_load').load(currentUrl + ' #Questions_body', function () {
                                                feather.replace();

                                                // Make the divs inside Questions_body sortable
                                                $("#Questions_body").sortable({
                                                    update: function (event, ui) {
                                                        // Update the IDs of each child div
                                                        $("#Questions_body .Question").each(function (index) {
                                                            $(this).attr("id", (index + 1));
                                                        });

                                                        let resultArray = [];
                                                        $('.Question').each(function () {
                                                            let divId = $(this).attr('id');
                                                            let textareaId = $(this).find('textarea').attr('id');
                                                            let number = textareaId.match(/\d+$/)[0];
                                                            resultArray.push([divId, number]);
                                                        });

                                                        // Send the new order
                                                        $.ajax({
                                                            url: window.location.href,
                                                            method: "POST",
                                                            data: { New_Questions_Order: JSON.stringify(resultArray) },
                                                            headers: { 'X-CSRFToken': getCSRFToken() }
                                                        });
                                                    }
                                                });
                                            });

                                            // Hide loader, show modal, and update status
                                            $('.modal_loader').css('display', 'none');
                                            $('.uploader-modal').css('display', 'block');
                                            document.getElementById('status').innerText = 'Upload complete!';
                                            return; // Ensure we exit the function here to prevent further execution
                                        }

                                        // Proceed with sending the next chunk
                                        const currentChunk = chunks.shift(); // Get the first chunk

                                        $.ajax({
                                            url: window.location.href,
                                            method: "POST",
                                            data: { step4: JSON.stringify(currentChunk) },
                                            headers: { 'X-CSRFToken': getCSRFToken() }
                                        }).done(function () {
                                            // Send the next chunk
                                            sendChunksSequentially(chunks);
                                        }).fail(function () {
                                            // Handle the error
                                            $('.modal_loader').css('display', 'none');
                                            $('.uploader-modal').css('display', 'block');
                                            document.getElementById('status').innerText = 'Upload failed!';
                                        });
                                    }

                                    // Start sending chunks
                                    sendChunksSequentially(chunkedData);
                                }
                            }
                        });
                    }
                }
            });
        },
        error: function (xhr, status, error) {
            $('.modal_loader').css('display', 'none');
            $('.uploader-modal').css('display', 'block');
            document.getElementById('status').innerText = 'Upload failed!';
        }
    });
}
