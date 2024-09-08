import google.generativeai as genai
from .models import *
from django.db.models import IntegerField
from django.db.models.functions import Cast
import re

def auto_correct(quizz_id):
    # Configure the Google Generative AI
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

    # Fetch questions and sort them
    Questions = Question.objects.filter(Quizz_id=quizz_id).annotate(order_as_int=Cast('Order', IntegerField())).order_by('order_as_int')

    def parse_complex_string(s):
        # Remove unnecessary characters and clean the string
        s = s.strip()
        
        # Define a pattern to match each question block
        block_pattern = re.compile(r'\[\[\s*(.*?)\s*\]\]')
        
        def parse_block(block):
            # Split by '], [' to separate question and choices
            parts = re.split(r'\], \[', block.strip('[]'))
            question = parts[0].strip('[]').split(', ')
            question_id = question[0].strip().strip("'")
            question_text = question[1].strip().strip("'")
            
            choices = []
            for part in parts[1:]:
                choice_parts = re.split(r',\s*', part.strip('[]'))
                choice_id = choice_parts[0].strip().strip("'")
                choice_text = choice_parts[1].strip().strip("'")
                choice_extra = choice_parts[2].strip().strip("'") if len(choice_parts) > 2 else ''
                choices.append([choice_id, choice_text, choice_extra])
            
            return [[question_id, question_text]] + choices
        
        # Process each block to extract the questions and choices
        result = []
        for match in block_pattern.finditer(s):
            block = match.group(1)
            result.append(parse_block(block))
        
        return result

    def process_batch(batch):
        Exam = []
        for question in batch:
            tmp = []
            tmp.append([question.id, question.Content])
            Choices = Choice.objects.filter(Question_id=question.id)
            for choice in Choices:
                tmp.append([choice.id, choice.Content, 'null'])
            Exam.append(tmp)

        # Send the batch to the model for processing
        response = chat_session.send_message(f""" 
            Task: You are a powerful AI tool designed to complete an array structured in the following format:

            [ 
            [
                ['question_id', 'question'],
                ['id_choice1', 'choice1', ''],
                ['id_choice2', 'choice2', ''],
                ...
            ], 
            [
                ['question_id', 'question'],
                ['id_choice1', 'choice1', ''],
                ['id_choice2', 'choice2', ''],
                ...
            ], 
            ...
            ]

            Objective: Your task is to fill in the empty fields (denoted by '') with true or false.

            Specifically:

            true should be assigned to the correct choice(s) for each question.
            false should be assigned to the incorrect choice(s) for each question.
            You must return the same array given to you but with the truth values filled in the appropriate fields. The output should strictly be the completed python-compatible array. Do not provide any additional information, comments, or explanations.

            Array to process: {Exam}
        """)

        txt_correction = response.text

        # Clean the string by removing '```python' and '```'
        cleaned_string = txt_correction.replace('```python', '').replace('```', '').strip()

        # Parse the corrected string
        corrections = parse_complex_string(cleaned_string)

        # Save the corrections to the database
        for correction in corrections:
            if isinstance(correction, list) and len(correction) > 1:
                for choices in correction[1:]:
                    try:
                        if isinstance(choices, list) and len(choices) >= 3:
                            choice = Choice.objects.get(id=int(choices[0]))
                            choice.Correction = choices[2] == 'true'
                            choice.save()
                    except Choice.DoesNotExist:
                        print(f"Choice with id {choices[0]} does not exist.")
                    except Exception as e:
                        print(f"Error processing choice: {e}")

    # Split the questions into batches of 20
    batch_size = 20
    total_questions = Questions.count()

    for start in range(0, total_questions, batch_size):
        end = min(start + batch_size, total_questions)
        batch = Questions[start:end]
        process_batch(batch)
