function Submit_1() {
    var result = {};

    // Loop through each "choices-blend" div
    $('.choices-container').each(function() {
        var questionID = $(this).attr('id').replace('question_answer_2_', '');  // Extract question ID
            
        // Initialize an array for storing choices if not already initialized
        if (!result[questionID]) {
            result[questionID] = [];
        }

        // Loop through each "choice-blend" within the current "choices-blend"
        $(this).find('.choice').each(function() {
            var choiceID = $(this).find('.choice_answer_2').attr('id').replace('input_to_check_', '');  // Extract choice ID
            var isChecked = $(this).find('.choice_answer_2').is(':checked');
            result[questionID].push([choiceID, isChecked]);  // Add each choice as an array [choiceID, isChecked]
        });
    });

    // Convert the result object to the desired array format
    var finalResult = [];
    for (var questionID in result) {
        if (result.hasOwnProperty(questionID)) {
            finalResult.push([questionID].concat(result[questionID]));
        }
    }

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

    $.ajax({
        url: window.location.href,
        method: "POST",
        data: { User_Answers: JSON.stringify(finalResult) },  // Send the final result as a JSON string
        headers: {
          'X-CSRFToken': getCSRFToken()
        },
        success: function(response) {
            if ('DATA' in response) {

                    // Example two-dimensional array
                    const array = response.DATA;

                    $('.input_to_answer').css("display","none");

                    $('.input_to_answer_2').css("display","none");

                    $(document).ready(function() {
                        // Iterate through the main array
                        array.forEach(subArray => {
                            // Iterate through the second part of each sub-array
                            subArray.slice(1).forEach(([id, status]) => {
                                const element = $(`#choice_wrap_${id}`);
                                const element_2 = $(`#question_answer_${id}`);
                                if (element.length && element_2.length) {
                                    element.addClass(status); // Add the class based on status
                                    element_2.addClass(status);
                                }
                            });
                        });
                    });

                    $('#welcomePage').html('<h2 style="color: #007bff;" >Score :</h3> <h1 class="'+response.APRECIATION+'" >'+response.SCORE+'/'+response.SCORING+'</h1> <button id="startBtn" class="nav-btn">Correction</button>');

                    let divs = $('.nav-div').toArray().map(div => $(div).attr('id'));
                    let currentDivIndex = 0; // Start with the first div in the array
                    
                    // Show the welcome page initially
                    $('#welcomePage').show();
                    $('.nav-div').hide(); // Hide all content divs
                    
                    function showWelcomePage() {
                        $('#welcomePage').show();
                        $('.nav-div').hide();
                        $('#prevBtn').hide();
                        $('#nextBtn').hide();
                        $('#submitBtn').hide();
                    }
                    
                    function showDiv(index) {
                        $('#welcomePage').hide(); // Hide the welcome page
                        $('.nav-div').hide(); // Hide all content divs
                        $('#' + divs[index]).show(); // Show the current div
                    
                        // Hide the Previous button if it's the first div
                        if (index === 0) {
                            $('#prevBtn').hide();
                        } else {
                            $('#prevBtn').show();
                        }
                    
                        // Show Submit button if it's the last div
                        if (index === divs.length - 1) {
                            $('#nextBtn').hide();
                            $('#submitBtn').show();
                        } else {
                            $('#nextBtn').show();
                            $('#submitBtn').hide();
                        }
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
                    
                    $('#format-btn').click(function(){
                        if(isHello){
                            $('.container').hide();
                            $('.buttons').hide();
                            $('.container-blend').show();
                        } else {
                            $('.container-blend').hide();
                            $('.container').show();
                            $('.buttons').show();
                        }
                        isHello = !isHello; // Toggle the state
                    });
                    
                    function resetToInitialState() {
                        currentDivIndex = 0; // Reset to the first div
                        showWelcomePage(); // Show the welcome page
                        $('#format-btn').css('display','none'); // Hide the format button
                    }    

                    $("#submitBtn").text("Score");

                    $("#submitBtn_blend").text("Score");

            }
        }
    }); 
}
