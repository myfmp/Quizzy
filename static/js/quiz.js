feather.replace();

$(document).ready(function() {

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
        $('#settings-btn').css('display','none'); // Hide the settings button
    }    

    });

    function check_the_box(checkbox_id) {
        // Construct the IDs of the checkboxes using the provided checkbox_id
        var id = "#input_to_check_" + checkbox_id;
        var id_2 = "#choice_answer_" + checkbox_id;

        // Set up the change event handler for the first checkbox
        $(id).change(function() {
            // Get the current checked state of the first checkbox
            var isChecked = $(this).prop('checked');

            // Set the second checkbox to match the first checkbox's state
            $(id_2).prop('checked', isChecked);

            // Optionally, log the new state of the second checkbox
            console.log('Checkbox ' + id_2 + ' is now ' + (isChecked ? 'checked' : 'unchecked'));
        });
    }

    function check_the_box_2(checkbox_id) {
        // Construct the IDs of the checkboxes using the provided checkbox_id
        var id_2 = "#input_to_check_" + checkbox_id;
        var id = "#choice_answer_" + checkbox_id;

        // Set up the change event handler for the first checkbox
        $(id).change(function() {
            // Get the current checked state of the first checkbox
            var isChecked = $(this).prop('checked');

            // Set the second checkbox to match the first checkbox's state
            $(id_2).prop('checked', isChecked);

            // Optionally, log the new state of the second checkbox
            console.log('Checkbox ' + id_2 + ' is now ' + (isChecked ? 'checked' : 'unchecked'));
        });
    }

    function resetToInitialState() {
        currentDivIndex = 0; // Reset to the first div
        showWelcomePage(); // Show the welcome page
        $('#format-btn').css('display','none'); // Hide the format button
        $('#settings-btn').css('display','none'); // Hide the settings button
    }   

    function showWelcomePage() {
        $('#welcomePage').show();
        $('.nav-div').hide();
        $('#prevBtn').hide();
        $('#nextBtn').hide();
        $('#submitBtn').hide();
    }

    $(".secondarysubmit").click(function() {
        resetToInitialState();
        $('#format-btn').hide();
        $('.container-blend').hide();
        $('.container').show();
        $('.buttons').show();
    });