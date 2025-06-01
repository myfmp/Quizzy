import google.generativeai as genai
from .models import *
import re

# Function to process the array with AI
def process_with_ai(Exam):
    # Configure the Google Generative AI
    genai.configure(api_key='AIzaSyCLeDS3QDsKfTH5Ri9FSjnFiWC-oBgr7hw')

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

    # Send the array to the AI model
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

    return cleaned_string

