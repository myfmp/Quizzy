function Open_New_Choice_Modal() {

$('.add_question_modal').css('display','none');
$('.add_choice_modal').css('display','block');

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
    $('.add_choice_modal').css('display','none');
    }, 500);    
}
closeBtn.forEach(c => c.addEventListener('click', closeModal))

}