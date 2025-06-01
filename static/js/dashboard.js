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

const showModal = (openButton, modalContent) => {
    const openBtn = document.getElementsByClassName(openButton);
    const modalContainer = document.getElementById(modalContent);
    
    if (modalContainer) {
        Array.from(openBtn).forEach(btn => {
            btn.addEventListener('click', () => {
                modalContainer.classList.add('show-modal');
            });
        });
    }
};
showModal('open-modal', 'modal-container');

/*=============== CLOSE MODAL ===============*/
const closeBtn = document.querySelectorAll('.close-modal');

function closeModal() {
    const modalContainer = document.getElementById('modal-container');
    modalContainer.classList.remove('show-modal');
}

closeBtn.forEach(c => c.addEventListener('click', closeModal));

const buttons = document.querySelectorAll('.myquiz-button2');

buttons.forEach(button => {
    button.addEventListener('click', function() {
        const url = this.getAttribute('data-url');
        
        // Create a temporary textarea to hold the URL
        const textarea = document.createElement('textarea');
        textarea.value = url;
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
        
    });
});

const buttons2 = document.querySelectorAll('.myquiz-button3');

buttons2.forEach(button => {
    button.addEventListener('click', function() {
        const url = this.getAttribute('data-url');
        
        // Create a temporary textarea to hold the URL
        const textarea = document.createElement('textarea');
        textarea.value = url;
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
        
        // Alert to notify that the URL has been copied

    });
});

$(document).ready(function(){
    $(".open-bank").click(function(){
        $(".bank-manager-container").css('display','block');
        $(".bank-overflow").css('display','block');
    });
});
  

function Close_bank() {
    $(".bank-manager-container").css('display','none');
    $(".bank-overflow").css('display','none');
}
