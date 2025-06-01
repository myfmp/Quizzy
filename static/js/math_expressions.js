function Math_Expressions() {
    $('.add_question_modal').css('display', 'none');
    $('.modal_loader').css('display', 'block');

    // Show the modal
    const modalContainer = document.getElementById('modal-container');
    modalContainer.classList.add('show-modal');

    // Initialize an empty array to store AJAX requests
    let ajaxRequests = [];

    // Send an AJAX request to get the initial data
    $.ajax({
        url: window.location.href,
        method: "POST",
        data: { IsMath: 'true' },
        headers: { 'X-CSRFToken': getCSRFToken() },
        success: function(response) {
            if ('DATA' in response) {
                let data = response.DATA;

                // Function to chunk an array into smaller arrays of given size
                function chunkArray(arr, chunkSize) {
                    let chunks = [];
                    for (let i = 0; i < arr.length; i += chunkSize) {
                        chunks.push(arr.slice(i, chunkSize + i));
                    }
                    return chunks;
                }

                // Chunk the data into arrays of 20 items
                let chunkedData = chunkArray(data, 20);

                // Process each chunk and store AJAX requests
                chunkedData.forEach((chunk) => {
                    console.log(JSON.stringify(chunk));
                    let ajaxRequest = $.ajax({
                        url: window.location.href,
                        method: "POST",
                        data: { latex2: JSON.stringify(chunk) },
                        headers: { 'X-CSRFToken': getCSRFToken() }
                    }).then(function(response_2) {
                        console.log(JSON.stringify(response_2.DATA));
                        return $.ajax({
                            url: window.location.href,
                            method: "POST",
                            data: { latex4: JSON.stringify(response_2.DATA) },
                            headers: { 'X-CSRFToken': getCSRFToken() }
                        });
                    });

                    // Push each request to the ajaxRequests array
                    ajaxRequests.push(ajaxRequest);
                });

                // Once all AJAX requests are done, reload content
                $.when.apply($, ajaxRequests).done(function() {
                    let currentUrl = window.location.href;

                    // Reload content using jQuery
                    $('#jquery_load').load(currentUrl + ' #Questions_body', function() {
                        feather.replace();

                        // Make the divs sortable
                        $("#Questions_body").sortable({
                            update: function(event, ui) {
                                // Update the IDs of each child div
                                $("#Questions_body .Question").each(function(index) {
                                    $(this).attr("id", (index + 1));
                                });
                            }
                        });

                        // Hide the loader and show the modal
                        setTimeout(function() {
                            $('.add_question_modal').css('display', 'block');
                            $('.modal_loader').css('display', 'none');
                        }, 500);

                        modalContainer.classList.remove('show-modal');
                    });
                });
            }
        }
    });
}
