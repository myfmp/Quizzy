function Delete_Question() {

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

    if (confirm("Click 'OK' to continue.")) {
        var urlParams = new URLSearchParams(window.location.search);
        var Question_id  = urlParams.get('question_id');
        var $jquerry_question = ".question_id_" + Question_id;
        
        // Hide the question
        $($jquerry_question).css('display', 'none');

        // Prepare the array to store the new order of visible questions
        let resultArray = [];

        // Re-order the visible questions
        $("#Questions_body .Question:visible").each(function(index) {
            $(this).attr("id", (index + 1));  // Reassign IDs to visible questions only

            // Get the ID of the current question div
            let divId = $(this).attr('id');

            // Find the textarea inside this div and get its ID
            let textareaId = $(this).find('textarea').attr('id');

            // Extract just the number from the textarea ID
            let number = textareaId.match(/\d+$/)[0];

            // Append the div ID and extracted number to the result array
            resultArray.push([divId, number]);
        });

        console.log('test');
        
        console.log(resultArray);

        // Send an AJAX request to handle the deletion and update the order
        $.ajax({
            url: window.location.href,
            method: "POST",
            data: {
                Question_To_Delete_Id: Question_id,  // Send deleted question ID
                New_Questions_Order: JSON.stringify(resultArray)  // Send updated order of questions
            },
            headers: {
                'X-CSRFToken': getCSRFToken()
            }
        });

        // Hide the custom menu
        $("#customMenu").hide();
    }
}
