feather.replace();

function DisplaySaveButton(Question_id) {
    
    var $question_jquerry_content = "#question_content_" + Question_id;
    var $save_button_jquerry_Id = "#question_button_" + Question_id;
    var $saveButton = $($save_button_jquerry_Id);

    $saveButton.stop().slideDown(130); // Slide down animation

}

function DisplaySaveButtonForChoice(Choice_id) {

    var $choice_jquerry_content = "#choice_content_" + Choice_id;
    var $save_button_jquerry_Id = "#choice_button_" + Choice_id;
    var $saveButton = $($save_button_jquerry_Id);

    $saveButton.stop().slideDown(130); // Slide down animation

}

function Uploader() {

    $('.add_question_modal').css('display','none');
    $('.uploader-modal').css('display','block');

    /*=============== SHOW MODAL ===============*/
    modalContainer = document.getElementById('modal-container')
    modalContainer.classList.add('show-modal')

    /*=============== CLOSE MODAL ===============*/
    const closeBtn = document.querySelectorAll('.close-modal')

    function closeModal(){
        const modalContainer = document.getElementById('modal-container')
        modalContainer.classList.remove('show-modal')
        setTimeout(function() {
        $('.add_question_modal').css('display','block');
        $('.uploader-modal').css('display','none');
        }, 500);    
    }
    closeBtn.forEach(c => c.addEventListener('click', closeModal))

}

/*=============== SHOW MODAL ===============*/
const showModal = (openButton, modalContent) =>{
    const openBtn = document.getElementById(openButton),
    modalContainer = document.getElementById(modalContent)
    
    if(openBtn && modalContainer){
        openBtn.addEventListener('click', ()=>{
            modalContainer.classList.add('show-modal')
        })
    }
}
showModal('open-modal','modal-container')

/*=============== CLOSE MODAL ===============*/
const closeBtn = document.querySelectorAll('.close-modal')

function closeModal(){
    const modalContainer = document.getElementById('modal-container')
    modalContainer.classList.remove('show-modal')
}
closeBtn.forEach(c => c.addEventListener('click', closeModal))

//# sourceURL=pen.js

$(document).ready(function() {

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

    var $quizzTitle = $('#quizz_title');
    var $saveButton = $('#title_button');

    $quizzTitle.on('input', function() {
            $saveButton.stop().slideDown(130); // Slide down animation
    });

    // Make the divs inside parentDiv sortable
    $("#Questions_body").sortable({
        update: function(event, ui) {
    
            // Update the IDs of each visible child div according to their new order
            $("#Questions_body .Question:visible").each(function(index) {
                $(this).attr("id", (index + 1));  // Reassign IDs to visible divs only
            });
    
            let resultArray = [];
    
            // Only process visible .Question divs
            $('.Question:visible').each(function() {
                // Get the ID of the current div
                let divId = $(this).attr('id');
    
                // Find the textarea inside this div and get its ID
                let textareaId = $(this).find('textarea').attr('id');
    
                // Extract just the number from the textarea ID
                let number = textareaId.match(/\d+$/)[0];
    
                // Append the div ID and extracted number to the result array
                resultArray.push([divId, number]);
            });
    
            // Send the updated order of visible divs via AJAX
            $.ajax({
                url: window.location.href,
                method: "POST",
                data: { New_Questions_Order: JSON.stringify(resultArray) },
                headers: {
                  'X-CSRFToken': getCSRFToken()
                }
            });
        }
    });

});

$(document).ready(function() {
    // Delegate the contextmenu event to the parent element (e.g., the body)
    $(document).on("contextmenu", ".Question", function(event) {
        event.preventDefault();

        // Get the classes of the div that was right-clicked
        const classList = $(this).attr('class');
        // Split the class list into an array
        const classes = classList.split(/\s+/);
        // Get the second class from the array
        const secondClass = classes[1];
        const match = secondClass.match(/\d+$/);
        id = match[0];

        var urlParams = new URLSearchParams(window.location.search);
        urlParams.set('question_id', id);
        var updatedUrl = `${window.location.origin}${window.location.pathname}?${urlParams.toString()}`;
        history.pushState(null, null, updatedUrl);

        // Hide the custom menu if it's already visible
        $("#customMenu").hide();

        // Position the custom menu at the click position
        $("#customMenu").css({
            top: event.pageY + "px",
            left: event.pageX + "px"
        });

        // Show the custom menu
        $("#customMenu").show();
        return false; // Prevent any further actions
    });

    // Hide the custom menu when clicking outside
    $(document).on("click", function(event) {
        if (!$(event.target).closest("#customMenu").length) {
            $("#customMenu").hide();
        }
    });
});

function Open_Setting() {

    $('.add_question_modal').css('display','none');
    $('.settings-modal').css('display','block');

    /*=============== SHOW MODAL ===============*/
    modalContainer = document.getElementById('modal-container')
    modalContainer.classList.add('show-modal')

    /*=============== CLOSE MODAL ===============*/
    const closeBtn = document.querySelectorAll('.close-modal')

    function closeModal(){
    const modalContainer = document.getElementById('modal-container')
    modalContainer.classList.remove('show-modal')
    setTimeout(function() {
    $('.add_question_modal').css('display','block');
    $('.settings-modal').css('display','none');
    }, 500);    
    }
    closeBtn.forEach(c => c.addEventListener('click', closeModal))

}

$('#quizz_title').attr('contenteditable', 'true');

