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

function Create_New_Question() {

    $('.add_question_modal').css('display', 'none');
    $('.modal_loader').css('display', 'block');

    // Show the modal
    const modalContainer = document.getElementById('modal-container');
    modalContainer.classList.add('show-modal');

    var Question_Content = $("#content_for_new_question").val();

    if (Question_Content && Question_Content.trim() !== "") {
   
       // Send an AJAX request to the same URL with CSRF token
       $.ajax({
           url: window.location.href,
           method: "POST",
           data: { New_Question_Content: Question_Content },
           headers: {
             'X-CSRFToken': getCSRFToken()
           },
           success: function(response) {
               if ('DATA' in response) {
                
                    $('#Questions_body').append(`

                        <div class="Question question_id_`+response.DATA[0]+`" id="`+response.DATA[1]+`">

                        <textarea id="question_content_`+response.DATA[0]+`" class="question_content" oninput="DisplaySaveButton('`+response.DATA[0]+`')" type="text">`+response.DATA[2]+`</textarea>

                        <div class="choice_body" id="choice_body_`+response.DATA[0]+`"></div>

                        <button id="question_button_`+response.DATA[0]+`" class="save_buttons" onclick="Change_Question_Content('`+response.DATA[0]+`')"> <div class="save-text" >Save</div> <div class="custom-loader"></div> </button>

                        </div>

                    `);     
                    $('#Questions_body').scrollTop($('#Questions_body')[0].scrollHeight);           
                    const modalContainer = document.getElementById('modal-container')
                        // Hide the loader and show the modal
                        setTimeout(function() {
                            $('.add_question_modal').css('display', 'block');
                            $('.modal_loader').css('display', 'none');
                           $("#content_for_new_question").val('');
                        }, 500);

                        modalContainer.classList.remove('show-modal');
               }
           }
         });
   
    }else{
       alert('Please enter a question.')
    }

}
