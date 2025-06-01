import requests
import google.generativeai as genai
from django.core.files.storage import default_storage
from .models import *
from .manager import *
import tempfile
import re

def OCR(FILE):
    genai.configure(api_key='AIzaSyBZTDDRhL8BQZm2eqx54XwE32e2V5g3etA')

    def fetch_from_cloudinary(cloudinary_url):
        response = requests.get(cloudinary_url)
        if response.status_code == 200:
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(response.content)
                temp_file.seek(0)
                return temp_file.name
        else:
            raise Exception("Failed to fetch file from Cloudinary")

    def upload_to_gemini(path, mime_type=None):
        file = genai.upload_file(path, mime_type=mime_type)
        return file

    def wait_for_files_active(files):
        print("Waiting for file processing...")
        for name in (file.name for file in files):
            file = genai.get_file(name)
            while file.state.name == "PROCESSING":
                file = genai.get_file(name)
            if file.state.name != "ACTIVE":
                raise Exception(f"File {file.name} failed to process")

    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash-thinking-exp-01-21",
        generation_config=generation_config,
        safety_settings=[]
    )

    cloudinary_url = FILE
    local_file_path = fetch_from_cloudinary(cloudinary_url)

    files = [upload_to_gemini(local_file_path, mime_type="application/pdf")]
    wait_for_files_active(files)

    # Add a text prompt along with the file
    response = model.generate_content([
        "Extract all text from the uploaded PDF file.",
        files[0]
    ])

    return response.text

def Conversion(MCQ):
    genai.configure(api_key='AIzaSyCUVg8SJPMHgIY5bCMtUqk5I0tuxNc9o9E')

    # Create the model
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        safety_settings=[]  # See https://ai.google.dev/gemini-api/docs/safety-settings
    )

    chat_session = model.start_chat(
        history=[]
    )

    response_3 = chat_session.send_message(f"""

    ---

    **Prompt:**

    You are a highly capable AI tool specialized in converting Multiple Choice Questions (MCQs) from text or PDF formats into a custom format. Your task is to extract each question, along with its choices and correct answers, and return the data in the following format:

    ```python
    $1/1$ Question 1 $1/1$
    $2/2$ Choice 1 of Question 1 $2/2$
    $3/3$ 0 or 1 $3/3$
    $2/2$ Choice 2 of Question 2 $2/2$  
    $3/3$ 0 or 1 $3/3$
    $2/2$ Choice 3 of Question 3 $2/2$ 
    $3/3$ 0 or 1 $3/3$
    $1/1$ Question 2 $1/1$    
    $2/2$ Choice 1 of Question 2 $2/2$
    $3/3$ 0 or 1 $3/3$
    $2/2$ Choice 2 of Question 2 $2/2$  
    $3/3$ 0 or 1 $3/3$
    $2/2$ Choice 3 of Question 2 $2/2$     
    $3/3$ 0 or 1 $3/3$                                                                       
    ```

    **Instructions:**
                                           
    1. **Extraction:** For every question in the provided text or PDF, extract the question text and all associated choices.
                                           
    2. **Answer Key:** Assign a value of `1` to the correct choice(s) and `0` to the incorrect ones (always refer to the question before answering it choices to be precise).
                                           
    3. **Consistency:** Ensure that every question and its choices are captured without omissions and that every question choice and answer is embeded with  $1/1$ (for questions) , $2/2$ (for choices) or $3/3$ (for answers).
                                           
    4. **Output Format:** Return data in the following way : starting by the question embeded inside a $1/1$ then the choices of the question embeded inside a $2/2$, each choice must be followed by it answer either 0 or 1 embeded in a $3/3$, and the process repeat for the next questions ...
                                           
    5. **Focus:** Do not take into account any variables outside of extracting and formatting the data as specified.

    7. **Order** It is very important that you respect the order of the questions and the choices.
                                           
    6. **Example** : 
            input ->
                    1) La paroi thoracique normale : Cochez l’(es) élément(s) juste(s)
                    A) Elle est formée en arrière par la cyphose thoracique
                    B) Elle est composée latéralement par 10 paires de côtes
                    C) Elle est un tronc de cône à grande base supérieure
                    D) Elle est limitée par le sternum en avant
                    E) Elle présente un orifice cervico-thoracique horizontal
            output ->
                    $1/1$ 1) La paroi thoracique normale : Cochez l’(es) élément(s) juste(s) $1/1$
                    $2/2$ A) Elle est formée en arrière par la cyphose thoracique $2/2$
                    $2/2$ B) Elle est composée latéralement par 10 paires de côtes $2/2$
                    $2/2$ C) Elle est un tronc de cône à grande base supérieure $2/2$
                    $2/2$ D) Elle est limitée par le sternum en avant $2/2$
                    $2/2$ E) Elle présente un orifice cervico-thoracique horizontal $2/2$
                                           
    **Purpose:** The data you provide will be reviewed by professionals for educational purposes. Ensure accuracy and completeness.
                                           

    **Input:**     ''' {MCQ} '''

    ---
        
    """)

    txt_querry = response_3.text

    return txt_querry

def Parser(MCQ):
    data = MCQ.replace('```python', '').replace('```', '').strip()

    # Initialize empty lists
    questions = []
    current_question = None

    # Use regex to match the patterns
    lines = data.splitlines()

    for line in lines:
        try:
            if "$1/1$" in line:  # It's a question
                # Extract the question text
                question = re.search(r'\$1/1\$\s*(.*?)\s*\$1/1\$', line).group(1)
                current_question = [[question]]  # Create a new question array wrapped in an array
                questions.append(current_question)  # Add it to the main list
            elif "$2/2$" in line:  # It's a choice
                # Extract the choice text
                choice = re.search(r'\$2/2\$\s*(.*?)\s*\$2/2\$', line).group(1)
                current_question.append([choice])  # Add the choice to the current question array
            elif "$3/3$" in line:  # It's a 0 or 1 indicator
                # Extract the 0 or 1 value
                value = re.search(r'\$3/3\$\s*(.*?)\s*\$3/3\$', line).group(1)
                current_question[-1].append(int(value))  # Add the 0 or 1 value to the last choice
        except Exception as e:
            print(f"Error encountered: {e}")
            # Return the already parsed questions when an error occurs
            print(questions)
            return questions
   
    print(questions)

    # Output the parsed array
    return questions

def Save_To_DB(MCQ_ARRAY, quizz_id):
    # Convert the string to a Python list
    querry = MCQ_ARRAY

    for data in querry:
        # Add the question to the database
        question = add_question(data[0][0], quizz_id)
        
        # Loop through the choices (elements)
        for elements in data[1:]:
            # Check if the truth value is missing (i.e., length of elements is 1)
            if len(elements) < 2:
                elements.append(0)  # Default truth value to 0 if missing
            
            # Add the choice to the database
            choice = add_choice(str(elements[0]), str(question[0]), quizz_id)
            
            # Set the truth value (1 or 0)
            if elements[1] == 1:
                choice_truth_value = change_choice_truth_value(int(choice[0]), 'true')
            else:
                choice_truth_value = change_choice_truth_value(int(choice[0]), 'false')
