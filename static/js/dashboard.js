$(document).ready(() => {

$('#open-sidebar').click(() => {

    // add class active on #sidebar
    $('#sidebar').addClass('active');

    // show sidebar overlay
    $('#sidebar-overlay').removeClass('d-none');

});


$('#sidebar-overlay').click(function () {

    // add class active on #sidebar
    $('#sidebar').removeClass('active');

    // show sidebar overlay
    $(this).addClass('d-none');

});

});

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