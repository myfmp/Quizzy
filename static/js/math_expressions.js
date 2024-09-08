function Math_Expressions() {
    
    $('.add_question_modal').css('display','none');
    $('.modal_loader').css('display','block');
    
    /*=============== SHOW MODAL ===============*/
    modalContainer = document.getElementById('modal-container')
    modalContainer.classList.add('show-modal')

    // Send an AJAX request to the same URL with CSRF token
    $.ajax({
        url: window.location.href,
        method: "POST",
        data: { IsMath: 'true'},
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