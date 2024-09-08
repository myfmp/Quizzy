import google.generativeai as genai
from .models import *
from django.db.models import IntegerField
from django.db.models.functions import Cast
import re

def MathExpressions(quizz_id):
    Exam = []

    # Collecting questions and choices
    Questions = Question.objects.filter(Quizz_id=quizz_id).annotate(order_as_int=Cast('Order', IntegerField())).order_by('order_as_int')
    for question in Questions:
        tmp = [[question.id, question.Content]]
        Choices = Choice.objects.filter(Question_id=question.id)
        for choice in Choices:
            tmp.append([choice.id, choice.Content])
        Exam.append(tmp)

    genai.configure(api_key='AIzaSyDc1xKtjZc8En8UpsA1s2g6njY5uOdZm1E')

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

    # Process the Exam list in chunks of 20
    chunk_size = 20
    for i in range(0, len(Exam), chunk_size):
        chunk = Exam[i:i + chunk_size]

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
        Don't add // or \\n ... just keep it simple.
        The id's must be integers.
        After processing, return a valid Python array (Use Escaped Quotes inside quotes to not crash the parser) with the same structure as the input, but with mathematical expressions formatted in LaTex syntax.
        Do not include any other variables or text. Only return the modified array with LaTeX formatting applied to mathematical expressions. Failure to adhere to this will cause the code to crash.
        Here is the array to process:
        '''
        {chunk}
        ''' 
        """)

        # Process the response from the AI
        txt_ai = response.text
        cleaned_string = txt_ai.replace('```python', '').replace('```', '').strip()
        print(cleaned_string)

        def parse_complex_string(s):
            # Remove unnecessary characters and clean the string
            s = s.strip()

            # Define a pattern to match each question block
            block_pattern = re.compile(r'\[\[\s*(.*?)\s*\]\]')

            def parse_block(block):
                # Split by '], [' to separate question and choices
                parts = re.split(r'\], \[', block.strip('[]'))

                # Parse the question
                question = parts[0].strip('[]').split(', ', 1)
                question_id = question[0].strip()
                question_text = question[1].strip("'")

                # Parse the choices
                choices = []
                for part in parts[1:]:
                    choice_parts = re.split(r',\s*', part.strip('[]'), 1)
                    choice_id = choice_parts[0].strip()
                    choice_text = choice_parts[1].strip("'")
                    choices.append([choice_id, choice_text])

                return [[question_id, question_text]] + choices

            # Process each block to extract the questions and choices
            result = []
            for match in block_pattern.finditer(s):
                block = match.group(1)
                result.append(parse_block(block))

            return result

        parsed_array = parse_complex_string(cleaned_string)

        for data in parsed_array:
            question = Question.objects.get(id=int(data[0][0]))
            question.Content = data[0][1]
            question.save()
            for elements in data[1:]:
                choice = Choice.objects.get(id=int(elements[0]))
                choice.Content = elements[1]
                choice.save()
