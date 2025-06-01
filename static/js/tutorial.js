function Tutorial() {
    $(".navbar").css('pointer-events','none');
    $("#how-to-home-nav").fadeOut(0);
    $("#how-to-correct-nav").fadeOut(0);
    $("#how-to-convert-nav").fadeOut(0);
    $("#how-to-latex-nav").fadeOut(0);
    $("#how-to-preview-nav").fadeOut(0);
    $("#how-to-help-nav").fadeOut(0);
    $("#how-to-settings-nav").fadeOut(0);
    $("#how-to-lovepdf-nav").fadeOut(0);    
    $(".navbar").css('margin-top','8vh'); 
    $(".navbar").css('height','auto');
    $(".navbar").css('z-index','9999');
    $('#how-it-works-question').css('display','block');
    modalContainer = document.getElementById('overlay');
    modalContainer.classList.add('show-modal');
}

function next_1() {
    $('#how-it-works-question').html('<h5 class="tuto_title" >Questions:</h5> <p style="color: black;" id="defza">You can delete questions or add choices to them by right-clicking on them. (If you are using a phone, just maintain the intended question.)</p><button class="next_buttons" onclick="next_2()">Next</button>'); 
}

function next_2() {
    $("#how-to-correct-nav").fadeIn();
    $(".navbar").css('margin-top','15vh'); 
    $("#how-to-add-question-nav").fadeOut(0);
    $("#how-it-works-question").css('top','8vh');
    $('#how-it-works-question').html('<h5 class="tuto_title" >Corrector:</h5> <p style="color: black;" id="defza">After adding questions and choices to your quiz, you can click this button to provide an AI-generated correction for your quiz (which may be inaccurate in some cases).</p><button class="next_buttons" onclick="next_3()">Next</button>'); 
}

function next_3() {
    $("#how-to-convert-nav").fadeIn();
    $(".navbar").css('margin-top','22vh'); 
    $("#how-to-correct-nav").fadeOut(0);
    $("#how-it-works-question").css('top','15vh');
    $('#how-it-works-question').html('<h5 class="tuto_title" >PDF to Quiz:</h5> <p style="color: black;" id="defza">If you have an MCQ in a certain document format, you can convert it to PDF using any free online tool and upload it to Quizzy via this button.</p><button class="next_buttons" onclick="next_4()">Next</button>'); 
}

function next_4() {
    $('#how-it-works-question').html('<h5 class="tuto_title" >PDF to Quiz:</h5> <p style="color: black;" id="defza">After a little while, it will convert your static PDF file into a dynamic quiz you can take online. (Don\'t worry if your PDF isn\'t pretty, is scanned, or the text inside is not selectable using Gemini AI, Quizzy will take care of the job.)</p><button class="next_buttons" onclick="next_5()">Next</button>');
}

function next_5() {
    $("#how-to-latex-nav").fadeIn();
    $(".navbar").css('margin-top','29vh'); 
    $("#how-to-convert-nav").fadeOut(0);
    $("#how-it-works-question").css('top','22vh');
    $('#how-it-works-question').html('<h5 class="tuto_title">LaTex:</h5> <p style="color: black;" id="defza">LaTeX is a language that allows you to display your mathematical expressions beautifully. If your MCQ contains some math and you don\'t know how to write LaTeX, or you\'re just too lazy for that 😂, don\'t be shy and click this button.</p><button class="next_buttons" onclick="next_6()">Next</button>'); 
}

function next_6() {
    $("#how-to-preview-nav").fadeIn();
    $(".navbar").css('margin-top','35vh'); 
    $("#how-to-latex-nav").fadeOut(0);
    $("#how-it-works-question").css('top','31vh');
    $('#how-it-works-question').html('<h5 class="tuto_title">Preview:</h5> <p style="color: black;" id="defza">This button will redirect you to a page where you can actually see how your quiz will look.</p><button class="next_buttons" onclick="next_7()">Next</button>'); 
}

function next_7() {
    $("#how-to-help-nav").fadeIn();
    $(".navbar").css('margin-top','42vh'); 
    $("#how-to-preview-nav").fadeOut(0);
    $("#how-it-works-question").css('top','40vh');
    $('#how-it-works-question').html('<h5 class="tuto_title">Help:</h5> <p style="color: black;" id="defza">I’m sure you know what this is for. In case you don’t, this is the tutorial button 😅.</p><button class="next_buttons" onclick="next_8()">Next</button>'); 
}

function next_8() {
    $("#how-to-lovepdf-nav").fadeIn();
    $(".navbar").css('margin-top','49vh'); 
    $("#how-to-help-nav").fadeOut(0);
    $("#how-it-works-question").css('top','43vh');
    $('#how-it-works-question').html('<h5 class="tuto_title">Split PDF:</h5> <p style="color: black;" id="defza">Separate one page or a whole set for easy conversion into independent PDF files.</p><button class="next_buttons" onclick="next_9()">Next</button>'); 
}

function next_9() {
    $("#how-to-settings-nav").fadeIn();
    $(".navbar").css('margin-top','54vh'); 
    $("#how-to-lovepdf-nav").fadeOut(0);
    $("#how-it-works-question").css('top','46vh');
    $('#how-it-works-question').html('<h5 class="tuto_title">Settings:</h5> <p style="color: black;" id="defza">This is the settings button. You can restrict your quiz by requiring a password to access it, reset your quiz to start from scratch, or simply delete your quiz.</p><button class="next_buttons" onclick="next_10()">Next</button>'); 
}

function next_10() {
    $("#how-to-home-nav").fadeIn(0);
    $("#how-to-add-question-nav").fadeIn(0);
    $("#how-to-correct-nav").fadeIn(0);
    $("#how-to-convert-nav").fadeIn(0);
    $("#how-to-latex-nav").fadeIn(0);
    $("#how-to-preview-nav").fadeIn(0);
    $("#how-to-help-nav").fadeIn(0);
    $("#how-to-settings-nav").fadeIn(0);
    $("#how-to-lovepdf-nav").fadeIn(0);
    $(".navbar").css('margin-top','0px'); 
    $(".navbar").css('height','calc(100vh - 4rem)');
    $(".navbar").css('z-index','0');
    $("#how-it-works-question").css('top','30vh');
    $("#how-it-works-question").css('left','50%');
    $("#how-it-works-question").css('right','50%');
    $("#how-it-works-question").css('transform','translate(-50%, -50%)');
    $('#how-it-works-question').html('<h5 class="tuto_title">Questions:</h5> <p style="color: black;" id="defza">You can modify questions order by swiping them with your mouse or with your finger on mobile phone.</p><button class="next_buttons" onclick="next_11()">Next</button>'); 
}

function next_11() {
    $('#how-it-works-question').html('<h5 class="tuto_title">Choices:</h5> <p style="color: black;" id="defza">You can easily add choices to questions by right-clicking on the ones you wish to modify. This allows you to add new choices, delete existing ones, or assign truth values (true/false) to them for more precise control.</p><button class="next_buttons" onclick="next_12()">Next</button>'); 
}

function next_12() {
    $('#how-it-works-question').html('<h5 class="tuto_title">Saves:</h5> <p style="color: black;" id="defza">After making any modifications, press the (Save) button that will appear to apply your changes.</p><button class="next_buttons" onclick="next_13()">Finish</button>'); 
}

function next_13() {
    $('#overlay').html('<div id="how-it-works-question" style="left: 20vh; top: 5vh; box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.5); display: none; position: absolute; width: 200px; padding: 20px; background-color: white; z-index: 10000; border-radius: 10px; opacity: 1 !important;"><h5 class="tuto_title" >Questions:</h5> <p style="color: black;" id="defza">With this button you can create  new questions.</p><button class="next_buttons" onclick="next_1()">Next</button></div>'); 
    $("#how-it-works-question").fadeOut(0);
    $(".navbar").css('pointer-events','auto');
    modalContainer = document.getElementById('overlay');
    modalContainer.classList.remove('show-modal');
}
