import os
import time
import requests
import google.generativeai as genai
from django.core.files.storage import default_storage
from .models import *
from .manager import *
import uuid
import re
from cloudinary_storage.storage import MediaCloudinaryStorage

def Convert_To_Test(FILE, quizz_id):
    genai.configure(api_key='AIzaSyDc1xKtjZc8En8UpsA1s2g6njY5uOdZm1E')

    def fetch_from_cloudinary(cloudinary_url):
        response = requests.get(cloudinary_url)
        if response.status_code == 200:
            # Create a temporary file
            temp_filename = f"temp_{uuid.uuid4().hex}.pdf"
            with open(temp_filename, 'wb') as f:
                f.write(response.content)
            return temp_filename
        else:
            raise Exception("Failed to fetch file from Cloudinary")

    def upload_to_gemini(path, mime_type=None):
        file = genai.upload_file(path, mime_type=mime_type)
        print(f"Uploaded file '{file.display_name}' as: {file.uri}")
        return file

    def wait_for_files_active(files):
        print("Waiting for file processing...")
        for name in (file.name for file in files):
            file = genai.get_file(name)
            while file.state.name == "PROCESSING":
                print(".", end="", flush=True)
                time.sleep(10)
                file = genai.get_file(name)
            if file.state.name != "ACTIVE":
                raise Exception(f"File {file.name} failed to process")
        print("...all files ready")
        print()

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

    # Fetch the file from Cloudinary
    cloudinary_url = FILE  # Assuming FILE is the Cloudinary URL
    local_file_path = fetch_from_cloudinary(cloudinary_url)

    # Upload file and wait for it to be processed
    files = [upload_to_gemini(local_file_path, mime_type="application/pdf")]
    wait_for_files_active(files)

    chat_session = model.start_chat(
        history=[]
    )

    response_1 = chat_session.send_message(files[0])

    response_2 = chat_session.send_message('Extract all text from file above please.')

    response_3 = chat_session.send_message(f"""

---

**Prompt:**

You are a highly capable AI tool specialized in converting Multiple Choice Questions (MCQs) from text or PDF formats into structured Python arrays. Your task is to extract each question, along with its choices and correct answers, and return the data in the following Python-compatible array format:

```python
[
    [["Question1"], ["choice1", 0 or 1], ["choice2", 0 or 1], ...],
    [["Question2"], ["choice1", 0 or 1], ["choice2", 0 or 1], ...],
    ...
]
```

**Instructions:**
1. **Extraction:** For every question in the provided text or PDF, extract the question text and all associated choices.
2. **Answer Key:** Assign a value of `1` to the correct choice(s) and `0` to the incorrect ones (always refer to the question before answering it choices to be precise).
3. **Consistency:** Ensure that every question and its choices are captured without omissions (Use  Escaped Quotes inside quotes to not crash the parser).
4. **Output Format:** Return the data as a well-structured Python array (compatible with ast literal_eval), ensuring all syntax is correct and compatible.
5. **Focus:** Do not take into account any variables outside of extracting and formatting the data as specified.

**Purpose:** The data you provide will be reviewed by professionals for educational purposes. Ensure accuracy and completeness.
                                           
**Exemple:** [ [ ["Cochez les propositions justes à propos du bassin osseux :"], ["A) Le détroit moyen est limité en avant par la symphyse pubienne",1], ["B) Le détroit supérieur est limité latéralement par la ligne terminale",1], ["C) Le détroit supérieur est limité latéralement par le bord antérieur de l’aileron sacré et la ligne terminale",1], ["D) Le détroit moyen est limité en arrière par le promontoire",0] ], .... ]

**Input:**     ''' {response_2.text} '''

---
    
""")

    txt_querry = response_3.text

    cleaned_string = txt_querry.replace('```python', '').replace('```', '').strip()

    def parse_custom_string(s):
        # Clean up the string
        s = s.strip().replace('\n', ' ')
        
        # Pattern to match the structure of the elements
        pattern = re.compile(
            r'\[\s*\[\s*"(.*?)"\s*\]\s*,\s*((?:\[\s*"(.*?)"\s*,\s*\d+\s*\],?\s*)+)\]'
        )
        
        def parse_inner_list(inner_str):
            items = re.findall(r'\[\s*"(.*?)"\s*,\s*(\d+)\s*\]', inner_str)
            return [[item[0], int(item[1])] for item in items]
        
        result = []
        for match in pattern.finditer(s):
            question = match.group(1)
            options = match.group(2)
            options_list = parse_inner_list(options)
            result.append([[question]] + options_list)
        
        return result

    # Convert the string to a Python list
    querry = parse_custom_string(cleaned_string)

    for data in querry:
        question = add_question(data[0][0], quizz_id)
        for elements in data[1:]:
            choice = add_choice(str(elements[0]), str(question[0]), quizz_id)
            if elements[1] == 1:
                choice_truth_value = change_choice_truth_value(int(choice[0]), 'true')
            else:
                choice_truth_value = change_choice_truth_value(int(choice[0]), 'false')

    # Clean up temporary file
    storage = MediaCloudinaryStorage()
    # Delete the file from Cloudinary
    storage.delete(local_file_path)
