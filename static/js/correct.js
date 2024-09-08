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

            }
        }
    });

}