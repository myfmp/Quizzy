function Submit_1() {
    $('#welcomePage').html('<div class="custom-loader-2"></div>');

    var result = [];

    // Loop through each "choices-container" div
    $('.choices-container').each(function() {
        var questionID = $(this).attr('id').replace('question_answer_2_', ''); 
        
        var choices = [];
    
        // Loop through each "choice" within the current "choices-container"
        $(this).find('.choice').each(function() {
            var choiceID = $(this).find('.choice_answer_2').attr('id').replace('input_to_check_', '');
            var isChecked = $(this).find('.choice_answer_2').is(':checked');
            var isTrue = $(this).find('.choice_answer_2').data('answer') === 'True';
            
            choices.push([choiceID, isChecked, isTrue]);
        });
    
        result.push([questionID].concat(choices));
    });
    
    const inputArray = result;
    let resultArray = [];
    let correctQuestions = 0;

    // Loop through the main array
    inputArray.forEach((question) => {
        const choicesStatus = []; 
        let questionCorrect = true;

        // Loop through the choice arrays
        for (let i = 1; i < question.length; i++) {
            const choice = question[i];
            const choiceId = choice[0];
            const isChecked = choice[1];
            const isTrue = choice[2];

            let status;
            if (isTrue && isChecked) {
                status = 'correct';  // Correct option correctly checked
            } else if (isTrue && !isChecked) {
                status = 'corrected';  // Correct option not checked
                questionCorrect = false;
            } else if (!isTrue && isChecked) {
                status = 'negative';  // Incorrect option checked
                questionCorrect = false;
            } else {
                status = 'neutral';  // Incorrect option not checked
            }

            choicesStatus.push([choiceId, status]);
        }

        if (questionCorrect) {
            correctQuestions++;
        }

        resultArray.push(choicesStatus);
    });

    // Calculate total score
    const totalQuestions = inputArray.length;
    const score = totalQuestions > 0 ? (correctQuestions / totalQuestions) : 0;
    let feedback = score > 0.5 ? 'PASS' : 'FAIL';

    // Output the results
    console.log("Result Array:", JSON.stringify(resultArray));
    console.log("Correct Questions:", correctQuestions);
    console.log("Total Questions:", totalQuestions);
    console.log("Score:", score);
    console.log("Feedback:", feedback);

    $('.input_to_answer, .input_to_answer_2').css("display", "none");

    // Apply styles based on the result
    resultArray.forEach(subArray => {
        subArray.forEach(([id, status]) => {
            const element = $(`#choice_wrap_${id}`);
            const element_2 = $(`#question_answer_${id}`);
            
            if (element.length && element_2.length) {
                // Remove any previous status classes
                element.removeClass('correct corrected negative neutral');
                element_2.removeClass('correct corrected negative neutral');
                
                // Add current status class
                element.addClass(status);
                element_2.addClass(status);
            }
        });
    });

    $('#welcomePage').html(`
        <h2 style="color: #007bff;">Score:</h2>
        <h1 class="${feedback}">${(score * 100).toFixed(0)}%</h1>
        <button id="startBtn" class="nav-btn">Correction</button>
    `);

    // Rest of the existing navigation logic remains the same
    // ... (previous code for buttons, div navigation, etc.)

    let divs = $('.nav-div').toArray().map(div => $(div).attr('id'));
    let currentDivIndex = 0; // Start with the first div in the array

    // Show the welcome page initially
    $('#welcomePage').show();
    $('.nav-div').hide(); // Hide all content divs
    
    function showWelcomePage() {
        $('#welcomePage').show();
        $('.nav-div').hide();
        $('#prevBtn, #nextBtn, #submitBtn').hide(); // Hide navigation buttons
    }
    
    function showDiv(index) {
        $('#welcomePage').hide(); // Hide the welcome page
        $('.nav-div').hide(); // Hide all content divs
        $('#' + divs[index]).show(); // Show the current div
    
        $('#prevBtn').toggle(index > 0); // Show/hide Previous button
        $('#nextBtn').toggle(index < divs.length - 1); // Show/hide Next button
        $('#submitBtn').toggle(index === divs.length - 1); // Show/hide Submit button
    }
    
    // Start button click
    $('#startBtn').click(function() {
        showDiv(currentDivIndex); // Start showing the first div
        $('#format-btn').css('display','flex');
    });
    
    // Next button click
    $('#nextBtn').click(function() {
        if (currentDivIndex < divs.length - 1) {
            currentDivIndex++;
            showDiv(currentDivIndex);
        }
    });
    
    // Previous button click
    $('#prevBtn').click(function() {
        if (currentDivIndex > 0) {
            currentDivIndex--;
            showDiv(currentDivIndex);
        }
    });
    
    // Submit button click
    $('#submitBtn').click(function() {
        resetToInitialState(); // Reset everything to the initial state
    });
    
    // Initially show the welcome page
    showWelcomePage();
    
    let isHello = true; // Track state
    
    $('#format-btn').click(function() {
        $('.container, .buttons').toggle(); // Toggle visibility of container and buttons
        $('.container-blend').toggle(); // Toggle visibility of blended container
        isHello = !isHello; // Toggle the state
    });
    
    function resetToInitialState() {
        currentDivIndex = 0; // Reset to the first div
        showWelcomePage(); // Show the welcome page
        $('#format-btn').css('display', 'none'); // Hide the format button
    }    

    $("#submitBtn").text("Score");
    $("#submitBtn_blend").text("Score");
    
}
