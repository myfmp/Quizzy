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

function Create_New_Choice() {

    $('.add_choice_modal').css('display', 'none');
    $('.modal_loader').css('display', 'block');

    // Show the modal
    const modalContainer = document.getElementById('modal-container');
    modalContainer.classList.add('show-modal');

    var urlParams = new URLSearchParams(window.location.search);
    var Question_id  = urlParams.get('question_id');

    var New_Choice = $("#content_for_new_choice").val();

    if (New_Choice && New_Choice.trim() !== "") {
   
       // Send an AJAX request to the same URL with CSRF token
       $.ajax({
           url: window.location.href,
           method: "POST",
           data: { New_Choice: New_Choice, Question_Id: Question_id },
           headers: {
             'X-CSRFToken': getCSRFToken()
           },
           success: function(response) {
               if ('DATA' in response) {
                    var choice_body_jquerry = "#choice_body_"+response.DATA[3];
                    console.log(choice_body_jquerry);
                    $(choice_body_jquerry).append(` 
                        <div id="Choice_`+response.DATA[0]+`" class="choice false"> 
                            <textarea id="choice_content_`+response.DATA[0]+`" class="choice_content" oninput="DisplaySaveButtonForChoice('`+response.DATA[0]+`')" >`+response.DATA[1]+`</textarea>
                            <div class="toggle-btn" onclick="Change_Truth_Statement(`+response.DATA[0]+`)">
                            <input id="Choice_input_`+response.DATA[0]+`" type="checkbox" class="cb-value" />
                            <span class="round-btn"></span>
                            </div>
                            <button id="choice_button_`+response.DATA[0]+`" class="save_buttons choice_submit" onclick="Change_Choice_Content('`+response.DATA[0]+`')"> <div class="save-text" >Save</div> <div class="custom-loader"></div> </button>
                            <div class="delete_choice" onclick="Delete_Choice(`+response.DATA[0]+`)"><i data-feather="minus-circle"></i></div>
                        </div>                 
                    `);     
                    feather.replace();
                    $(choice_body_jquerry).scrollTop($(choice_body_jquerry)[0].scrollHeight);   
                    setTimeout(function() {
                        $('.add_question_modal').css('display','block');
                        $('.add_choice_modal').css('display','none');
                    }, 500);            
                    const modalContainer = document.getElementById('modal-container')
                    setTimeout(function() {
                        $('.add_question_modal').css('display', 'block');
                        $('.modal_loader').css('display', 'none');
                        $("#content_for_new_choice").val('');
                    }, 500);

                    modalContainer.classList.remove('show-modal');
               }
           }
         });
   
    }else{
       alert('Please enter a question.')
    }

}   
