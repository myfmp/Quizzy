function Correct() {
    
    $('.add_question_modal').css('display','none');
    $('.modal_loader').css('display','block');
    
    /*=============== SHOW MODAL ===============*/
    modalContainer = document.getElementById('modal-container')
    modalContainer.classList.add('show-modal')

    // Send an AJAX request to the same URL with CSRF token
    $.ajax({
        url: window.location.href,
        method: "POST",
        data: { Auto_Correct: 'Correct'},
        headers: {
            'X-CSRFToken': getCSRFToken()
        },          
        success: function(response) {
            if ('DATA' in response) {

                $.ajax({
                    url: window.location.href,
                    method: "POST",
                    data: { correct2: JSON.stringify(response.DATA)},
                    headers: {
                        'X-CSRFToken': getCSRFToken()
                    },          
                    success: function(response_2) {
                        if ('DATA' in response_2) {
            
                            $.ajax({
                                url: window.location.href,
                                method: "POST",
                                data: { correct3: response_2.DATA},
                                headers: {
                                    'X-CSRFToken': getCSRFToken()
                                },          
                                success: function(response_3) {
                                    if ('DATA' in response_3) {
                        
                                        let data = response_3.DATA;

                                        // Function to chunk an array into smaller arrays of given size
                                        function chunkArray(arr, chunkSize) {
                                            let chunks = [];
                                            for (let i = 0; i < arr.length; i += chunkSize) {
                                                chunks.push(arr.slice(i, chunkSize + i));
                                            }
                                            return chunks;
                                        }
    
                                        let chunkedData = chunkArray(data, 20);
                                        let bigArray = [];
                                        bigArray.push(chunkedData);
    
                                        // Track all AJAX requests
                                        let ajaxRequests = [];
    
                                        // Loop through the big array and send AJAX requests for each chunk
                                        bigArray[0].forEach((chunk) => {
                                            let ajaxRequest = $.ajax({
                                                url: window.location.href,
                                                method: "POST",
                                                data: { correct4: JSON.stringify(chunk) },
                                                headers: { 'X-CSRFToken': getCSRFToken() }
                                            });
                                            ajaxRequests.push(ajaxRequest);
                                        });
    
                                        // Once all chunks have been processed
                                        $.when.apply($, ajaxRequests).done(function () {
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
                            
                                            setTimeout(function() {
                                                $('.add_question_modal').css('display','block');
                                                $('.modal_loader').css('display','none');
                                            }, 500);   
                                            const modalContainer = document.getElementById('modal-container')
                                            modalContainer.classList.remove('show-modal')
                                        });
                        
                                    }
                                }
                            });
            
                        }
                    }
                });

            }
        }
    });

}