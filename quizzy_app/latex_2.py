import google.generativeai as genai

def MathExpressions_2(Exam):
    genai.configure(api_key='AIzaSyBkMKT3lb8dXnEYqPFTg7pRh9sV47BKSbA')

    # Create the model
    generation_config = {
        "temperature": 0.9,
        "top_p": 0.9,
        "top_k": 0,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        generation_config=generation_config,
        safety_settings=[]
    )

    chat_session = model.start_chat(history=[])

    response = chat_session.send_message(f"""
    You are a very powerful AI tool. You will be provided with arrays in this format:
    [
        [
            [question_id, 'question'],
            [id_choice1, 'choice1'],
            [id_choice2, 'choice2'],
            ...
        ],
        [
            [question_id, 'question'],
            [id_choice1, 'choice1'],
            [id_choice2, 'choice2'],
            ...
        ],
        ...
    ]
    Your task is to process each array and detect mathematical expressions in the questions and choices. Convert these expressions into MathJax syntax. Ensure that you format each mathematical expression accurately without omitting any.
    For fractions, use the $$ delimiters.
    Ensure that the LaTeX formatting is correct for each mathematical content.
    Also make sure to clean text from // or \\n ...
    The id's must be integers.
    After processing, return a valid Python array (Use Escaped Quotes inside quotes to not crash the parser) with the same structure as the input, but with mathematical expressions formatted in LaTex syntax.
    Do not include any other variables or text. Only return the modified array with LaTeX formatting applied to mathematical expressions. Failure to adhere to this will cause the code to crash.
    Here is the array to process:
    '''
    {Exam}
    ''' 
    """)

    # Process the response from the AI
    txt_ai = response.text

    return txt_ai
